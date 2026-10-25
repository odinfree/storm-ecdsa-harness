#!/usr/bin/env python3
"""Small Elicit API client. Credentials never go in command arguments."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import subprocess
import urllib.parse

BASE = 'https://elicit.com/api/v2'
SCHEMA = Path(__file__).resolve().parents[1] / 'references/api-schema.json'
SCHEMA_URL = 'https://docs.elicit.com/openapi.json'
KEY_FILE = Path(os.environ.get('ELICIT_KEY_FILE', '')).expanduser() if os.environ.get('ELICIT_KEY_FILE') \
    else Path.home() / '.config/elicit/api-key'


def load_schema():
    """Read the cached OpenAPI document, downloading Elicit's public copy on first use."""
    if not SCHEMA.exists():
        result = subprocess.run(['curl', '--silent', '--show-error', '--fail', '--max-time', '45', SCHEMA_URL],
                                text=True, capture_output=True, timeout=50)
        if result.returncode:
            raise ValueError(f'Could not download {SCHEMA_URL}; save it to {SCHEMA} by hand.')
        json.loads(result.stdout)
        SCHEMA.write_text(result.stdout)
    return json.loads(SCHEMA.read_text())


def endpoint(method, path):
    parsed = urllib.parse.urlsplit(path)
    if parsed.scheme or parsed.netloc or not path.startswith('/') or parsed.fragment:
        raise ValueError('Use an API-relative path, e.g. /usage, never a URL.')
    schema = load_schema()
    for pattern, operations in schema['paths'].items():
        regex = re.sub(r'\{[^}]+\}', '[^/]+', pattern)
        if re.fullmatch(regex, parsed.path) and method.lower() in operations:
            return operations[method.lower()]
    raise ValueError('Method/path is absent from the saved schema. Check current docs.')


def request(method, path, body=None):
    endpoint(method, path)
    key = os.environ.get('ELICIT_API_KEY', '').strip()
    if not key and KEY_FILE.exists():
        if KEY_FILE.stat().st_mode & 0o077:
            raise ValueError('API key file must have permissions 600.')
        key = KEY_FILE.read_text().strip()
    if not key:
        raise ValueError('Set ELICIT_API_KEY or store the key in ~/.config/elicit/api-key (mode 600).')
    if any(c in key for c in '\r\n"\\'):
        raise ValueError('Invalid characters in API key.')
    command = ['curl', '--silent', '--show-error', '--max-time', '45',
               '--config', '-', '--request', method, BASE + path,
               '--header', 'Accept: application/json',
               '--write-out', '\n%{http_code}']
    if body is not None:
        command += ['--header', 'Content-Type: application/json',
                    '--data-binary', json.dumps(body)]
    # Pass credentials over stdin, not argv. No redirects or automatic retries.
    result = subprocess.run(command, input='header = "Authorization: Bearer ' + key + '"\n',
                            text=True, capture_output=True, timeout=50)
    if result.returncode:
        raise ValueError('Network failure; outcome may be unknown. Reconcile sessions before retrying a creation request.')
    raw, status = result.stdout.rsplit('\n', 1)
    if not 200 <= int(status) < 300:
        raise ValueError(f'HTTP {status}: {raw.replace(key, "[REDACTED]")}\nNo automatic retry performed.')
    return json.loads(raw) if raw else {'status': int(status)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('method', choices=['GET', 'POST', 'PATCH', 'DELETE'])
    parser.add_argument('path', help='API-relative path; quote query strings')
    parser.add_argument('--body', type=Path, help='JSON request file')
    parser.add_argument('--out', type=Path, help='Save complete JSON response')
    parser.add_argument('--schema', action='store_true', help='Show endpoint schema without an API call')
    args = parser.parse_args()
    try:
        result = endpoint(args.method, args.path) if args.schema else request(
            args.method, args.path, json.loads(args.body.read_text()) if args.body else None)
        output = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output)
            print(f'Saved response to {args.out.resolve()}')
        else:
            print(output, end='')
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
