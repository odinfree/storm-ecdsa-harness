#!/usr/bin/env python3
"""Groq chat worker: reads the Groq key and base URL from the environment (set them with your secret manager for this
one process), sends a prompt file as one user message, writes the answer to --out. The key never touches argv or logs.

usage:
  <your secret manager> run -- python3 groq.py --model <model> --prompt file.md --out out.md [--system file.md] [--max-tokens N]
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="openai/gpt-oss-120b")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--system", default=None)
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--temperature", type=float, default=0.3)
    ap.add_argument("--reasoning", default=None, help="reasoning_effort for models that support it (low|medium|high)")
    ap.add_argument("--list-models", action="store_true")
    a = ap.parse_args()
    key = os.environ.get("GROQ_API_KEY")
    base = (os.environ.get("GROQ_BASE_URL") or "https://api.groq.com/openai/v1").rstrip("/")
    if not key:
        print("the Groq key is not in the environment (run through your secret manager)", file=sys.stderr); sys.exit(2)
    hdr = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "ecdsafail-worker/1.0 (python-urllib)", "Accept": "application/json"}
    if a.list_models:
        req = urllib.request.Request(base + "/models", headers=hdr)
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        for m in sorted(x["id"] for x in d.get("data", [])):
            print(m)
        return
    msgs = []
    if a.system:
        msgs.append({"role": "system", "content": open(a.system, encoding="utf-8").read()})
    msgs.append({"role": "user", "content": open(a.prompt, encoding="utf-8").read()})
    body = {"model": a.model, "messages": msgs, "max_tokens": a.max_tokens, "temperature": a.temperature}
    if a.reasoning:
        body["reasoning_effort"] = a.reasoning
    data = json.dumps(body).encode()
    t0 = time.time()
    for attempt in range(4):
        try:
            req = urllib.request.Request(base + "/chat/completions", data=data, headers=hdr, method="POST")
            with urllib.request.urlopen(req, timeout=600) as r:
                resp = json.load(r)
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(5 * (attempt + 1)); continue
            print(f"HTTP {e.code}: {msg}", file=sys.stderr); sys.exit(3)
    text = resp["choices"][0]["message"].get("content") or ""
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(text)
    u = resp.get("usage", {})
    print(f"groq[{a.model}] {time.time()-t0:.0f}s in={u.get('prompt_tokens')} out={u.get('completion_tokens')} -> {a.out}")

if __name__ == "__main__":
    main()
