#!/usr/bin/env python3
"""Türhüeter (claim-gate): refuse a submit while another lane holds an open CLAIM on the account.

usage: claim-gate.py ACCOUNT_NAME [MAILBOX_FILE]
  ACCOUNT_NAME   the account you are about to submit from, as other lanes write it in the mailbox
  MAILBOX_FILE   the shared append-only text file; default: environment variable CLAIM_MAILBOX
environment:
  CLAIM_SELF     your own tag (default "me"); posts by this tag, or by "<tag>-<anything>", never block you
  CLAIM_ACCOUNTS optional: every account name the team uses, space-separated. A closing post that names another
                 of these accounts and not yours does not close a claim on yours.
  CLAIM_TAIL     how many trailing lines to read (default 200)
exit: 0 and "free" when no open claim is found; 1 and one "BLOCKED by <tag>: <text>" line per open claim;
      2 when the mailbox cannot be read (a gate that cannot read refuses).

Mailbox format: a post starts with "[tag] ..." or "tag: ..." (a tag is letters, digits, dot, dash, underscore);
lines without such a prefix continue the previous post. An open claim is a post by another tag that contains the word CLAIM and names the account (or
says "second account", or "either ... account"), with no later post from the same tag that says submitted,
released, yielded or graded ("not submitted" does not close a claim). Conservative on purpose: when in doubt
it refuses.
"""
import os, re, sys

def open_claims(lines, account, me, accounts=()):
    posts, cur = [], None
    for l in lines:
        m = re.match(r'^\[([^\]]+)\]', l) or re.match(r'^([A-Za-z0-9_.-]+): ', l)
        if m:
            cur = {'tag': m.group(1).strip(), 'text': l}; posts.append(cur)
        elif cur is not None:
            cur['text'] += ' ' + l
    held = {}
    others = [a.lower() for a in accounts if a.lower() != account.lower()]
    for p in posts:
        tag, t = p['tag'], p['text']; tl = t.lower()
        if tag == me or tag.startswith(me + '-'): continue
        closes = (re.search(r'\bsubmitted\b', tl) and 'not submitted' not in tl) or 'released' in tl or 'yielded' in tl or 'graded' in tl
        # a closing post about ANOTHER account leaves a claim on this one open
        if closes and not (account.lower() not in tl and any(o in tl for o in others)):
            held.pop(tag, None)
        if re.search(r'\bCLAIM\b', t) and (account.lower() in tl or 'second account' in tl or ('either' in tl and 'account' in tl)):
            held[tag] = t[:300]
    return held

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    account = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('CLAIM_MAILBOX', '')
    me = os.environ.get('CLAIM_SELF', 'me')
    try:
        lines = open(path, errors='replace').read().split('\n')[-int(os.environ.get('CLAIM_TAIL', '200')):]
    except Exception as e:
        print(f'BLOCKED: cannot read mailbox {path!r}: {e}'); sys.exit(2)
    held = open_claims(lines, account, me, os.environ.get('CLAIM_ACCOUNTS', '').split())
    if held:
        for tag, t in held.items(): print(f'BLOCKED by {tag}: {t}')
        sys.exit(1)
    print('free'); sys.exit(0)

if __name__ == '__main__':
    main()
