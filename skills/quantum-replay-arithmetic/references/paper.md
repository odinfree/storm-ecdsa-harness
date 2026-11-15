# Sources and transfer

[Record-and-replay v1](https://arxiv.org/html/2609.28882v1), sections 4–7: Jump-2 compresses paired decisions; ping-pong changes the update schedule; fused replay combines arithmetic corrections. Windowed interfaces add separate obligations. The paper explicitly retains supported-input correctness limitations despite large random tests.

[Optimized point addition v1](https://arxiv.org/html/2606.02235v1), sections 2–4: in-place multiplication and its inverse support the point-add path; recording Euclidean choices permits delayed coefficient reconstruction and register sharing. Reported distribution-based iteration/width choices are not universal correctness guarantees.

The lane's proposal is to compare these mechanisms within our exact interface and evaluator, not assume their reported totals transfer.
