#!/usr/bin/env python3
"""Call the pinned local arXiv MCP over stdio, including from older live sessions."""
import argparse
import asyncio
import json
import os
from pathlib import Path
import sys


def tool_failed(result):
    if result.get('isError'):
        return True
    for part in result.get('content', []):
        if part.get('type') != 'text':
            continue
        try:
            payload = json.loads(part.get('text', ''))
        except (TypeError, ValueError):
            continue
        if isinstance(payload, dict) and (payload.get('error') or payload.get('status') in ['error', 'failed', 'rate_limited']):
            return True
    return False


async def run(args):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    root = Path.home() / '.local/share/arxiv-research'
    envdir = root / 'arxiv-mcp-0.8.2'
    command = envdir / ('Scripts/arxiv-mcp-server.exe' if os.name == 'nt' else 'bin/arxiv-mcp-server')
    if not command.is_file():
        raise RuntimeError(f'Missing pinned server: {command}')
    calls = json.loads(Path(args.calls).read_text(encoding='utf-8')) if args.calls else [{'tool': args.tool, 'arguments': json.loads(args.json)}]
    if not isinstance(calls, list) or not calls:
        raise ValueError('Expected a nonempty array of tool calls')
    params = StdioServerParameters(command=str(command), args=['--storage-path', str(root / 'arxiv-library/papers')])
    results = []
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            for call in calls:
                name = call['tool']
                result = await asyncio.wait_for(session.list_tools() if name == 'list_tools' else session.call_tool(name, call.get('arguments', {})), timeout=args.timeout)
                results.append({'tool': name, 'result': result.model_dump(mode='json')})
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('tool', nargs='?')
    p.add_argument('--json', default='{}')
    p.add_argument('--calls')
    p.add_argument('--out')
    p.add_argument('--timeout', type=int, default=120)
    args = p.parse_args()
    if not args.tool and not args.calls:
        p.error('Provide a tool name or --calls FILE')
    result = asyncio.run(run(args))
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        target = Path(args.out)
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_suffix(target.suffix + '.tmp')
        temp.write_text(data, encoding='utf-8')
        temp.replace(target)
        print(json.dumps({'saved': str(target), 'tools': [x['tool'] for x in result], 'errors': sum(tool_failed(x['result']) for x in result)}))
    else:
        print(data)
    return int(any(tool_failed(x['result']) for x in result))


if __name__ == '__main__':
    sys.exit(main())
