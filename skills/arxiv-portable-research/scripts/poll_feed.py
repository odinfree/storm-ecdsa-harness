#!/usr/bin/env python3
"""Fetch a bounded official Atom feed; persist deduplicated intake before cursors."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

FEED = 'https://rss.arxiv.org/atom/quant-ph+cs.DS+cs.CC+cs.AR+cs.CR'


def atomic(path, obj):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


def parse(data):
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(data)
    if root.tag != '{http://www.w3.org/2005/Atom}feed':
        raise ValueError('Expected an Atom feed; cursor unchanged')
    records = []
    for item in root.findall('a:entry', ns):
        get = lambda tag: ' '.join((item.findtext('a:' + tag, '', ns) or '').split())
        record = {k: get(k) for k in ['id', 'title', 'published', 'updated', 'summary']}
        record['categories'] = [c.get('term') for c in item.findall('a:category', ns)]
        record['links'] = [c.get('href') for c in item.findall('a:link', ns)]
        if not record['id'] or not record['title']:
            raise ValueError('Malformed entry; cursor unchanged')
        record['key'] = hashlib.sha256((record['id'] + '\n' + record['updated']).encode()).hexdigest()
        records.append(record)
    return records


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--library', type=Path, default=Path.home()/'.local/share/arxiv-research/arxiv-library')
    args = p.parse_args()
    root = args.library
    root.mkdir(parents=True, exist_ok=True)
    lock = root / '.feed-poll.lock'
    try:
        lock.mkdir()
    except FileExistsError:
        raise SystemExit('Another feed poll holds the lock. Reconcile its process before recovery.')
    try:
        (lock/'owner.json').write_text(json.dumps({'pid':__import__('os').getpid(),'started':dt.datetime.now(dt.timezone.utc).isoformat()}))
        statepath = root/'feed-state.json'
        state = json.loads(statepath.read_text()) if statepath.exists() else {'seen': []}
        headers = {'User-Agent': 'PortableResearchFeed/1.0 (personal research; cached daily intake)'}
        for key, header in [('etag','If-None-Match'),('last_modified','If-Modified-Since')]:
            if state.get(key): headers[header] = state[key]
        try:
            with urllib.request.urlopen(urllib.request.Request(FEED, headers=headers), timeout=30) as r:
                data = r.read(8*1024*1024+1)
                if len(data)>8*1024*1024: raise ValueError('Feed exceeds 8MiB; cursor unchanged')
                records = parse(data)
                response_headers = dict(r.headers)
        except urllib.error.HTTPError as e:
            if e.code==304:
                print(json.dumps({'status':'not_modified','new':0})); return
            raise
        seen = set(state['seen'])
        new = []
        for item in records:
            if item['key'] not in seen:
                new.append(item); seen.add(item['key'])
        now = dt.datetime.now(dt.timezone.utc)
        intake = root/'intake'; intake.mkdir(exist_ok=True)
        out = intake/(now.strftime('%Y%m%dT%H%M%S.%fZ')+'-feed.json')
        atomic(out, {'fetched_at':now.isoformat(),'feed':FEED,'total':len(records),'new':new})
        atomic(statepath, {'seen':sorted(seen),'etag':response_headers.get('ETag'),'last_modified':response_headers.get('Last-Modified'),'checked_at':now.isoformat(),'last_intake':str(out)})
        print(json.dumps({'status':'fetched','total':len(records),'new':len(new),'saved':str(out)}))
    finally:
        (lock/'owner.json').unlink(missing_ok=True)
        lock.rmdir()


if __name__=='__main__':
    main()
