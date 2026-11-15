# Providers and operation

The configured third-party server is [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server), pinned to 0.8.2 with PDF conversion. Original arXiv sources remain authoritative. The optional local embedding stack is not required for search, full text, LaTeX, citations or watches.

Default installation: `~/.local/share/arxiv-research/arxiv-mcp-0.8.2`; use `bin/python` on macOS/Linux or `Scripts/python.exe` on Windows. Shared host-local library: `~/.local/share/arxiv-library/papers` (or wherever your installation keeps it). Do not synchronize live watch cursors between hosts or run overlapping checks on the same library.

For clients without newly loaded MCP tools, prefer the installed guarded CLI:

```sh
~/.local/bin/arxiv-research list_tools
~/.local/bin/arxiv-research search_papers --json '{"query":"abs:uncomputation","categories":["quant-ph"],"max_results":5}' --out search.json
~/.local/bin/arxiv-research list_watches --out watches.json
```

The CLI serializes its own invocations, spaces them by at least three seconds, and exits nonzero for MCP errors, partial or rate-limited results, and refused version requests. It does not coordinate other native MCP clients or hosts. Keep one request owner across those clients. `--out` retains returned error receipts; a transport exception may occur before there is a result to save.

On a host without the wrapper, the portable raw helper remains available. Its caller must provide equivalent ownership, pacing and result inspection:

```text
<environment-python> <skill>/scripts/arxiv_tool.py list_tools
<environment-python> <skill>/scripts/arxiv_tool.py search_papers --json '{"query":"abs:uncomputation","categories":["quant-ph"],"max_results":5}' --out search.json
<environment-python> <skill>/scripts/arxiv_tool.py list_watches
<environment-python> <skill>/scripts/arxiv_tool.py --calls watches.json --out watch-receipt.json
```

Calls files contain `[{"tool":"watch_topic","arguments":{"topic":"...","categories":["quant-ph"],"max_results":20}}]`. Save responses before interpreting them. `check_alerts` mutates cursors; `list_watches` does not. The server's watch queries cover new publication dates, not every revision of an older paper.

Inspect every topic's status and `has_more`. A successful MCP transport can contain a provider error or partial batch; preserve the receipt and do not report it as zero new papers.

Use `get_paper_outline` / `read_paper_section` for text and `list_paper_latex_sections` / `get_paper_latex_section` for author LaTeX. Read the returned truncation markers and continue until the required construction/proof is covered. Download success is not a complete read. `citation_graph` uses Semantic Scholar and may be incomplete or rate-limited; use Scite or primary references as a documented fallback, without inventing edges.

Scite is a separately connected chat plugin; its connection is not automatically available in remote Codex/Claude CLIs. Discover its tools on the current client. Search with exact DOI/title, check paper identity and editorial notices, inspect actual citation snippets, and record kept/excluded papers with reasons when screening. Use private collections unless the user requests sharing. A dataset with a similar title is not the paper. If full text is unavailable, follow the primary source and label the access gap.

Official sources: [search API](https://info.arxiv.org/help/api/user-manual.html), [RSS/Atom](https://info.arxiv.org/help/rss.html), [email subscriptions](https://info.arxiv.org/help/subscribe.html). Respect API pacing, cache results and bound retries. Email alerts and scheduled agent research are separate services.
