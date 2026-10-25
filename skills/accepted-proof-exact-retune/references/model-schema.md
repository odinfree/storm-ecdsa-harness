# Exact retune model schema

The search input is JSON. All numeric values are integers.

```json
{
  "schema": "accepted-proof-exact-retune-model/v1",
  "accepted_score_centibits": 6764,
  "required_step_centibits": 1,
  "direction": "maximize",
  "max_cases": 1000000,
  "constants": [
    {"name": "n", "value": 262144, "source": "ProximityPrize/SubmissionLower/Model.lean:12"}
  ],
  "parameters": [
    {"name": "errors", "baseline": 80102, "min": 80102, "max": 80112, "step": 1,
     "source": "ProximityPrize/SubmissionLower/Model.lean:44"}
  ],
  "derived": [
    {"name": "agreements", "expr": "n - errors",
     "source": "ProximityPrize/SubmissionLower/Model.lean:45"},
    {"name": "score_cb", "expr": "score_from_exact_certificate",
     "source": "ProximityPrize/SubmissionLower/Protocol.lean:91"}
  ],
  "constraints": [
    {"name": "radius_in_range", "expr": "0 <= errors and errors <= n",
     "source": "ProximityPrize/SubmissionLower/Protocol.lean:73"}
  ],
  "objective": {
    "name": "score_centibits",
    "expr": "score_cb",
    "source": "ProximityPrize/SubmissionLower/Solution.lean:3"
  }
}
```

The sample expression `score_from_exact_certificate` is deliberately not defined. Replace it with the exact integer expression justified by the accepted proof. Never insert a floating-point approximation merely to make the sample executable.

## Expression language

Allowed:

- integer and Boolean literals;
- names defined earlier in the model;
- `+`, `-`, `*`, `//`, `%`, and bounded non-negative `**`;
- comparisons, `and`, `or`, and `not`;
- `abs`, `min`, `max`, and `ceil_div`.

Rejected:

- `/` and floating-point literals;
- attribute access, indexing, comprehensions, lambdas, imports, or arbitrary calls;
- duplicate or forward-referenced names;
- zero divisors and oversized exponentiation;
- source anchors outside the captured import closure.

The baseline parameter assignment must satisfy every constraint. Its objective must equal the snapshot score exactly. That check detects many wrong-variable and wrong-rounding models before enumeration.

