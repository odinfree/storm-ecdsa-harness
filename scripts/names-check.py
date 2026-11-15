#!/usr/bin/env python3
"""Namenstag (names-check): check NAMES.md against the tree.

Run from anywhere: python3 scripts/names-check.py
Fails (exit 1) when a skill folder, single-file skill or tool folder has no row in NAMES.md, when a row names
something that does not exist, when a Swiss name is used twice (case-insensitive), when a skill's frontmatter
`name` differs from its folder, or when the title of a SKILL.md or tool README does not start with its Swiss name.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = []

def rows(section):
    text = open(os.path.join(ROOT, 'NAMES.md'), encoding='utf-8').read()
    m = re.search(r'^## %s\n(.*?)(?=^## |\Z)' % re.escape(section), text, re.S | re.M)
    out = []
    for line in (m.group(1) if m else '').splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 3 and not set(cells[0]) <= set('-: ') and cells[0] != 'Swiss name':
            out.append(cells)
    return out

def title(path):
    text = open(path, encoding='utf-8').read()
    if text.startswith('---\n'): text = text[text.index('\n---', 4) + 4:]
    m = re.search(r'^# (.+)$', text, re.M)
    return m.group(1).strip() if m else ''

skills = {c[2].strip('`'): c[0] for c in rows('Skills')}
tools = {c[2].strip('`').replace('tools/', ''): c[0] for c in rows('Tools')}
other = {c[2].strip('`'): c[0] for c in rows('Scripts and notes')}
extra = [c[0] for c in rows('Rows and leads of the November 2026 campaign')]

sdir = os.path.join(ROOT, 'skills')
have = set()
for e in sorted(os.listdir(sdir)):
    p = os.path.join(sdir, e)
    if e.startswith('.'): continue
    if os.path.isdir(p) and os.path.exists(os.path.join(p, 'SKILL.md')): have.add(e)
    elif e.endswith('.md'): have.add(e[:-3])
for s in sorted(have - set(skills)): bad.append(f'skill without a name: {s}')
for s in sorted(set(skills) - have): bad.append(f'named skill does not exist: {s}')
for s in sorted(have & set(skills)):
    p = os.path.join(sdir, s, 'SKILL.md')
    if not os.path.exists(p): p = os.path.join(sdir, s + '.md')
    text = open(p, encoding='utf-8').read()
    m = re.search(r'^name:\s*["\']?([^"\'\n]+)["\']?\s*$', text[:text.index('\n---', 4)], re.M)
    if not m or m.group(1).strip() != s: bad.append(f'frontmatter name differs from folder: {s}')
    if not title(p).startswith(f'{skills[s]} ({s})'): bad.append(f'title of {s} is not "{skills[s]} ({s})": {title(p)!r}')

tdir = os.path.join(ROOT, 'tools')
thave = {e for e in os.listdir(tdir) if os.path.isdir(os.path.join(tdir, e))} if os.path.isdir(tdir) else set()
for t in sorted(thave - set(tools)): bad.append(f'tool without a name: {t}')
for t in sorted(set(tools) - thave): bad.append(f'named tool does not exist: {t}')
for t in sorted(thave & set(tools)):
    r = os.path.join(tdir, t, 'README.md')
    if not os.path.exists(r): bad.append(f'tool without README: {t}')
    elif not title(r).startswith(tools[t]): bad.append(f'README title of {t} does not start with {tools[t]}')
for p in other:
    if not os.path.exists(os.path.join(ROOT, p)): bad.append(f'named path does not exist: {p}')

names = list(skills.values()) + list(tools.values()) + list(other.values()) + extra
seen = {}
for n in names:
    k = n.lower()
    if k in seen: bad.append(f'Swiss name used twice: {n}')
    seen[k] = 1

if bad:
    print('names_check=fail'); [print(' ', b) for b in bad]; sys.exit(1)
print(f'names_check=pass skills={len(skills)} tools={len(tools)} other={len(other)} names={len(names)}')
