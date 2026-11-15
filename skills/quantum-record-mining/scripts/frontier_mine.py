#!/usr/bin/env python3
"""Read-only frontier and record triage. Mentions are leads, never validated rows."""
import argparse
import hashlib
import json
import math
import re
from pathlib import Path


def read_board(path):
    text = Path(path).read_text()
    data = json.loads(text[text.index('{'):])
    rows = []
    for row in data['submissions']:
        m = row.get('officialMetrics') or {}
        # This API is scalar: valid Pareto rows can lose the scalar promotion.
        scored = row.get('status') == 'accepted' or (
            row.get('status') == 'rejected'
            and row.get('rejectionReason') == 'score did not improve current best')
        q, t = m.get('qubits'), m.get('toffoli')
        if (scored and row.get('officialScore') is not None
                and isinstance(q, (int, float)) and isinstance(t, (int, float))
                and math.isfinite(q) and math.isfinite(t) and q > 0 and t > 0):
            rows.append({'q': q, 't': t, 'id': row['id'],
                         'owner': row.get('solverUsername'),
                         'published': row.get('scorePublishedAt'),
                         'scalar_status': row['status']})
    return rows


def ceiling(rows, q):
    valid = [r for r in rows if r['q'] <= q]
    return min(valid, key=lambda r: (r['t'], r['q'], r['id'])) if valid else None


def frontier(rows):
    result, best = [], math.inf
    for row in sorted(rows, key=lambda r: (r['q'], r['t'], r['id'])):
        if row['t'] < best:
            result.append(row)
            best = row['t']
    return result


PAIR = re.compile(r'(?<![\w.])Q?\s*(\d{3,4})\s*[x×*]\s*(\d[\d,]*(?:\.\d+)?)\s*([kKmM]?)(?![\w.])')
NAMED = re.compile(r'\bQ(\d{3,4})\b.{0,35}?\bT\s*(?:=|~|≈|:)?\s*(\d[\d,]*(?:\.\d+)?)\s*([kKmM]?)(?![\w.])')
STATE = re.compile(r'\b(verifier|HOLD|blocked|killed|closed|dead|parked|projected|measured|landed|pending)\b', re.I)


def mentions(paths, rows):
    result = []
    for path in paths:
        for line_no, line in enumerate(Path(path).read_text().splitlines(), 1):
            seen = set()
            for pattern in (PAIR, NAMED):
                for hit in pattern.finditer(line):
                    q = int(hit[1]); t = float(hit[2].replace(',', ''))
                    t *= {'k': 1000, 'm': 1000000, '': 1}[hit[3].lower()]
                    if (q, t) in seen or not 500 <= q <= 5000 or t < 10000:
                        continue
                    seen.add((q, t))
                    front = ceiling(rows, q)
                    result.append({'source': str(path), 'line': line_no,
                                   'q': q, 't_mentioned': t,
                                   'ceiling': front,
                                   'potential_delta_t': front['t']-t if front else None,
                                   'labels_in_line': STATE.findall(line),
                                   'review_required': True,
                                   'text': line.strip()[:1600]})
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('board')
    p.add_argument('--q', type=int, nargs='*', default=[])
    p.add_argument('--notes', nargs='*', default=[])
    p.add_argument('--out', required=True)
    a = p.parse_args()
    rows = read_board(a.board)
    result = {
        'board_sha256': hashlib.sha256(Path(a.board).read_bytes()).hexdigest(),
        'filter': 'accepted OR rejected only for score did not improve current best; official metrics and score required',
        'limitations': 'Snapshot only. Regex mentions require primary receipts and owner check; no automatic admission or exactness claim.',
        'scored_rows': len(rows), 'frontier': frontier(rows),
        'ceilings': {str(q): ceiling(rows, q) for q in a.q},
        'mentions': mentions(a.notes, rows),
    }
    Path(a.out).write_text(json.dumps(result, indent=2)+'\n')
    print(f"{len(rows)} scored rows; {len(result['frontier'])} frontier points; {len(result['mentions'])} unverified mentions")


if __name__ == '__main__':
    main()
