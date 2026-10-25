# Oracle receipt

Preserve enough information for a clean machine to replay the claim:

```text
claim:
status:
domain and conventions:
input artifact and hash:
command:
tool and package versions:
seed or deterministic ordering:
output artifact and hash:
coverage, if exhaustive:
independent route and backend:
remaining proof obligation:
```

For an exhaustive finite computation, the receipt must also define the complete search set, its cardinality, shard partition, completed-shard manifest, and skipped/error count. A loop finishing without that accounting does not establish completeness.

For a witness, emit the witness in a simple format and check it with a verifier that does not call the search procedure.
