#!/usr/bin/env python3
"""Notizbüechli (zmknote): write one row's submission package from a template and machine-read values, and refuse
to write it when anything is missing, stale or unclean.

usage: notizbuechli.py --pkg DIR --width W --template NOTE.tmpl --values values.json --deps deps.json
                       --verified-sha FILE [--board board-latest.tsv] [--max-board-age 1800]
                       [--evidence DIR] [--min-bytes 5120] [--check] [--ready]

  values.json   flat object: placeholder name -> value. Required: TOFFOLI (integer), OPS_SHA256 (64 hex),
                ROW_COMMIT (the submission commit), MODEL (the model credit line). Everything else is yours.
                Fill it from result files by script; a typed number is a number nobody measured.
  NOTE.tmpl     the note with {{NAME}} placeholders. Three are computed here when --board is given:
                {{BAR}} (lowest Toffoli on the board at width <= W), {{BAR_ID}} (its id, 8 chars), {{BOARD_TIME}}.
  deps.json     list of {"submissionId", "rationale", "evidence"}; at most 20 entries.
  --verified-sha  file holding the ops.bin sha256 that an INDEPENDENT rebuild produced (for example the verifier's
                ops.sha256). It must equal OPS_SHA256 and is what gets written to DIR/verified-sha, so the
                submit script's comparison of CLAIM against verified-sha compares two sources, not one.
  --board       Wätterfrosch / Äugli snapshot; the run fails unless TOFFOLI is strictly below the bar, and unless
                the snapshot's .time file is younger than --max-board-age seconds (default 1800). A snapshot with
                no row at this width or below is accepted when it holds at least 100 graded rows.
  --evidence    folder of small text result files copied to DIR/evidence with local paths replaced by <path>.
  --check       write nothing: regenerate and compare with the files in DIR (note, CLAIM, verified-sha).
  --ready       after writing, run the check and write DIR/READY with the UTC time.

Writes DIR/NOTE-<W>.md, deps-<W>.json, CLAIM (toffoli= / sha= / dev=), verified-sha, MODEL.
Exit 1 with "NOTE FAIL: <reason>" on: a missing value, an unfilled placeholder, a local path, an inherited
notice-block marker, a TODO, a note under the minimum size, the commit or ops hash absent from the note text,
more than 20 dependencies, a verified sha that differs, a stale board snapshot, or a bar at or below our own count.
"""
import argparse, datetime, json, os, re, shutil, sys

LOCAL = re.compile(r'/(?:Users|home|root|private/tmp|content)/[^\s\'"`)]*')
MARKERS = ('VERBATIM NOTIC' + 'ES', 'NOTE TO AI AGEN' + 'TS', 'TODO')

def die(m): print('NOTE FAIL:', m); sys.exit(1)

def bar(board, w, max_age):
    best, graded = None, 0
    for line in open(board).read().splitlines()[1:]:
        f = line.split('\t')
        try: q, t = int(float(f[0])), int(float(f[1]))
        except (ValueError, IndexError): continue
        graded += 1
        if q <= w and (best is None or t < best[0]): best = (t, f[4][:8])
    if graded < 100: die(f'board snapshot holds only {graded} graded rows (empty or truncated read?)')
    stamp = board.rsplit('.', 1)[0] + '.time'
    if not os.path.isfile(stamp): die('board snapshot has no .time file: its age is unknown')
    when = open(stamp).read().strip()
    try: age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.strptime(when, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)).total_seconds()
    except ValueError: die('unreadable board time ' + when)
    if age > max_age: die(f'board snapshot is {int(age)} s old (limit {max_age}): refresh it first')
    return (best[0], best[1], when) if best else (None, '-', when)

def build(a):
    v = json.load(open(a.values))
    for k in ('TOFFOLI', 'OPS_SHA256', 'ROW_COMMIT', 'MODEL'):
        if not str(v.get(k, '')).strip(): die('missing value ' + k)
    toff = int(v['TOFFOLI']); sha = str(v['OPS_SHA256']); rc = str(v['ROW_COMMIT'])
    if not re.fullmatch(r'[0-9a-f]{64}', sha): die('OPS_SHA256 is not 64 hex digits')
    if not os.path.isfile(a.verified_sha): die('missing verified sha file ' + a.verified_sha)
    vs = open(a.verified_sha).read().split()
    if not vs or vs[0] != sha: die('the independently verified sha differs from OPS_SHA256')
    v.setdefault('WIDTH', a.width); v.setdefault('TOFFOLI_FMT', f'{toff:,}'); v.setdefault('SCORE_FMT', f'{toff * a.width:,}')
    if a.board:
        b, bid, bt = bar(a.board, a.width, a.max_board_age)
        if b is not None and toff >= b: die(f'bar: the board has {b:,} at width <= {a.width} ({bid}); ours is {toff:,}')
        v.update(BAR=(f'{b:,}' if b is not None else 'none'), BAR_ID=bid, BOARD_TIME=bt, MARGIN=(f'{b - toff:,}' if b is not None else 'n/a'))
    t = open(a.template).read()
    for k, x in v.items(): t = t.replace('{{%s}}' % k, str(x))
    left = sorted(set(re.findall(r'\{\{[A-Za-z0-9_]+\}\}', t)))
    if left: die(f'unfilled placeholders {left}')
    if LOCAL.search(t): die('local path in note: ' + LOCAL.search(t).group(0)[:60])
    for m in MARKERS:
        if m in t: die('forbidden text in note: ' + m)
    if rc not in t: die('row commit not in note text')
    if sha not in t: die('ops sha256 not in note text')
    if len(t.encode()) < a.min_bytes: die(f'note is {len(t.encode())} bytes, under {a.min_bytes}')
    d = json.load(open(a.deps))
    if not isinstance(d, list) or len(d) > 20: die('deps must be a list of at most 20 entries')
    for e in d:
        if not all(str(e.get(k, '')).strip() for k in ('submissionId', 'rationale', 'evidence')): die('dependency without submissionId, rationale or evidence')
    ds = json.dumps(d, indent=1, ensure_ascii=False) + '\n'
    if LOCAL.search(ds): die('local path in deps')
    claim = f'toffoli={toff}\nsha={sha}\ndev={rc}\n'
    return t, ds, claim, sha, str(v['MODEL']).strip()

def check(a):
    t, ds, claim, sha, model = build(a); O = a.pkg; W = a.width
    def same(name, want):
        p = os.path.join(O, name)
        if not os.path.isfile(p) or open(p).read() != want: die(name + ' differs from regeneration (or is missing)')
    same(f'NOTE-{W}.md', t); same(f'deps-{W}.json', ds); same('CLAIM', claim); same('verified-sha', sha + '\n')
    print('CHECK OK', W, claim.split('\n')[0], sha[:8])

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pkg', required=True); p.add_argument('--width', type=int, required=True)
    p.add_argument('--template', required=True); p.add_argument('--values', required=True); p.add_argument('--deps', required=True)
    p.add_argument('--verified-sha', required=True); p.add_argument('--max-board-age', type=int, default=1800)
    p.add_argument('--board'); p.add_argument('--evidence'); p.add_argument('--min-bytes', type=int, default=5120)
    p.add_argument('--check', action='store_true'); p.add_argument('--ready', action='store_true')
    a = p.parse_args()
    if a.check: check(a); return
    t, ds, claim, sha, model = build(a); O = a.pkg; W = a.width; os.makedirs(O, exist_ok=True)
    if a.evidence:
        E = os.path.join(O, 'evidence'); os.makedirs(E, exist_ok=True)
        for f in sorted(os.listdir(a.evidence)):
            s = os.path.join(a.evidence, f)
            if not os.path.isfile(s) or os.path.getsize(s) > 3_000_000: continue
            try: x = open(s).read()
            except UnicodeDecodeError: continue
            open(os.path.join(E, f), 'w').write(LOCAL.sub('<path>', x))
    open(os.path.join(O, f'NOTE-{W}.md'), 'w').write(t); open(os.path.join(O, f'deps-{W}.json'), 'w').write(ds)
    open(os.path.join(O, 'CLAIM'), 'w').write(claim); open(os.path.join(O, 'verified-sha'), 'w').write(sha + '\n')
    open(os.path.join(O, 'MODEL'), 'w').write(model + '\n')
    print('NOTE written', W, claim.split('\n')[0])
    if a.ready:
        check(a)
        open(os.path.join(O, 'READY'), 'w').write(datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') + '\n'); print('READY written')

if __name__ == '__main__':
    main()
