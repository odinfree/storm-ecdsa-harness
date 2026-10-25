#!/usr/bin/env python3
"""Minimal TypeSafe System One (Jev) client: python3 jev.py REQUEST.json [OUT.json] | python3 jev.py --models
The key is read from $TYPESAFE_API_KEY or ~/.config/typesafe/api-key (mode 600); it is never printed or written."""
import json, os, sys, urllib.request, urllib.error

def key():
    k = os.environ.get('TYPESAFE_API_KEY')
    if not k:
        with open(os.path.expanduser('~/.config/typesafe/api-key')) as f:
            k = f.read().strip()
    return k

def call(method, path, body=None):
    req = urllib.request.Request('https://api.typesafe.ai' + path, method=method,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={'Authorization': 'Bearer ' + key(), 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {'http_error': e.code, 'body': e.read().decode()[:2000]}

if __name__ == '__main__':
    if sys.argv[1] == '--models':
        print(json.dumps(call('GET', '/v1/models'), indent=1))
    else:
        body = json.load(open(sys.argv[1]))
        body.setdefault('model', 'jev-latest')
        out = call('POST', '/v1/systemone', body)
        if len(sys.argv) > 2:
            json.dump(out, open(sys.argv[2], 'w'), indent=1)
        print(json.dumps(out, indent=1))
