---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#49
state: closed
updated_at: 2026-06-24T11:54:49+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

For your Ollama-based Worker layer (32GB RAM + 6GB VRAM GTX 980 Ti) you want a model that optimizes for:
strong code synthesis + refactoring
reliable instruction following (low hallucination)
fast inference on limited VRAM
stable long-context behavior under quantization
You are not looking for “best benchmark model”, but for a high-throughput engineering worker model.


⸻


1) Best Overall Choice (balanced default)
Qwen2.5-Coder 7B Instruct (quantized: Q4_K_M or Q5_K_M)
Why it fits your system best:
extremely strong code editing + patch generation
very good instruction adherence (important for deterministic workers)
stable under quantization (important for 980 Ti VRAM limits)
handles:
diffs
refactors
test generation
bug fixing loops
Role in your architecture:
“Primary execution engine for all TYPE A / TYPE B tasks”


⸻


2) Alternative High-Quality Option
DeepSeek-Coder 6.7B Instruct
Strengths:
very strong reasoning over code structure
slightly better at complex debugging than Qwen in some cases
good AST-style transformations
Weakness:
a bit less strict on instruction formatting than Qwen2.5-Coder


⸻


3) Fast / Cheap Worker (optional tier)
Phi-3.5-mini-instruct
Use this if you want:
ultra-fast iterations
simple patching tasks
boilerplate generation
But:
weaker at multi-file reasoning
not ideal for conflict resolution logic


⸻


4) What I would NOT use for your Worker layer
These are common mistakes:
❌ LLaMA 3 8B (general)
good general model
but less deterministic for structured patch workflows
❌ Big models (13B+)
too slow on 980 Ti VRAM constraints
KV-cache pressure breaks iterative loops
❌ “Chat-only tuned” models
too verbose
wastes tokens internally (bad for your loop design)


⸻


5) Recommended Worker Stack (your architecture)
Tiering model (important for your system design):
LEVEL 1 — Fast Executor (simple tasks)
Phi-3.5-mini-instruct
LEVEL 2 — Main Worker (default)
Qwen2.5-Coder 7B Instruct ← PRIMARY
LEVEL 3 — Complex refactor / conflict resolution
DeepSeek-Coder 6.7B Instruct


⸻


6) Suggested Ollama configs
Qwen2.5-Coder (recommended quantization)
q4_K_M → best balance
q5_K_M → better accuracy if VRAM allows
Context window
keep effective context ≤ 8k for stability on 6GB VRAM GPU


⸻


7) How this maps to YOUR system design
In your architecture terms:
Layer
Model
Slarti
(your high-level orchestrator, not LLM-dependent)
Worker (default)
Qwen2.5-Coder 7B
Conflict Resolver
DeepSeek-Coder 6.7B
Fast micro-task worker
Phi-3.5-mini


⸻


8) Key design insight (important)
Your whole system succeeds or fails based on this principle:
Worker model must be deterministic enough to behave like a compiler pass, not a conversational agent.
That is why Qwen2.5-Coder is the center of gravity: it behaves more like a structured transformer for code diffs than a chat model.
