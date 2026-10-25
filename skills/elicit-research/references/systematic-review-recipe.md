# Systematic review recipe (operator's template, oct 2026)

Use for a deep question that ordinary search has not settled, or when an independent
literature-backed perspective is needed. Check quota first:

    python3 scripts/elicit.py GET /usage

Request body (save as `review-request.json`; never put a key in it):

    {
      "researchQuestion": "ONE PRECISE QUESTION",
      "searches": [{ "query": "FOCUSED SEARCH STRING", "maxResults": 200 }],
      "abstractScreening": { "generate": true, "depth": "thorough" },
      "fulltextScreening": { "reuseAbstractCriteria": true, "depth": "thorough" },
      "extraction": { "generate": true, "useFigures": false },
      "generateReport": true
    }

Create, then poll the typed detail endpoint (never re-create because it is slow):

    python3 scripts/elicit.py POST /sessions/systematic-reviews --body review-request.json --out review-session.json
    python3 scripts/elicit.py GET /sessions/systematic-reviews/RETURNED_ID --out review-status.json

Read the schema first (`POST /sessions/systematic-reviews --schema`): omitted stages are skipped,
fulltext screening needs abstract screening, and the report needs extraction. The key lives only in
`~/.config/elicit/api-key` (mode 600).
Use a systematic review only for a question that blocks the campaign or needs an outside perspective;
use /search/papers for quick lookups.
