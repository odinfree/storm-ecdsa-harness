# API operating notes

Source: https://docs.elicit.com/ and https://docs.elicit.com/openapi.json, retrieved 2026-09-11. Base URL: https://elicit.com/api/v2. The adjacent schema snapshot provides exact request/response fields and examples; it may drift.

- Bearer authentication. API access requires Pro or higher. Search result caps: Pro 300, Scale 500, Enterprise 10,000 per request. Default to modest searches, not plan maximums.
- Global rate limit: 100 requests/minute/IP across endpoints. A 429 blocks the IP for five minutes; stop calls for that period rather than rapid retries. The client does not retry automatically.
- Paper corpus is `elicit` or `pubmed`. `searchMode: keyword` is mutually exclusive with `filters` / `trialFilters`; place filter expressions in the keyword query. Preserve parser warnings in the research record.
- Handle 401 as authentication failure, 402 as quota failure, and 403 as an access restriction. Fix 400 payload errors against the schema. After a network error or 5xx on creation, inspect `GET /sessions` to reconcile before any retry; absence from an immediate listing is not proof that submission failed.
- Reports accept `researchQuestion`, optional `title`, `maxSearchPapers` (1–1000), `maxExtractPapers` (1–80), and `isPublic` (default false).
- Systematic reviews support searches, abstract/fulltext screening, extraction, and report generation. Thorough screening retains supporting quotes; fast screening is better suited to triage. Figure extraction costs extra usage. Current schema says `dryRun` is deprecated and can only be false, despite stale property prose suggesting true for estimates. Do not use `dryRun: true` as a cost probe.
- Research Agent endpoints include status, events, messages, artifacts, artifact content/download, and stop. Inspect each operation with `--schema` to see exact cursors, event types, and output fields. A stop is asynchronous; verify the stopped event. Follow-up messages to the research agent are research operations, not messages to other people.
- Library endpoints support source metadata, collections, and parsed full text. Retrieve full text when a source ID is available. `full_text_pending` permits a later retry; `full_text_unavailable` does not imply accessible full text. Saving sources or importing files should serve the requested workflow.
- File attachments require the documented two-step presigned upload. Use returned upload instructions and file IDs. The API client intentionally accepts only documented API-relative endpoints and refuses redirects. Download or upload to provider-issued URLs separately, without the Elicit Authorization header; never forward that key to an artifact storage host.
- Pagination cursors and IDs are opaque. Copy returned values, URL-encode query values, and preserve session IDs across interrupted turns. Keep raw evidence and final synthesis separate.

## Local verification

On 2026-09-11 Python urllib's initial `GET /usage` probe returned Cloudflare 1010. The user's official curl search example subsequently succeeded with HTTP 200 and five papers, confirming working key and search access. The client now uses curl with its normal identity, passes authentication via stdin, and does not follow redirects or retry automatically. Treat future failures according to their actual responses; the earlier urllib failure does not establish an account block.
