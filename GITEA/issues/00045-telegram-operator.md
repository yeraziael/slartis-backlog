---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#45
state: closed
updated_at: 2026-06-24T11:54:48+02:00
is_epic: false
labels:
  - "Systemarchitektur"
publication: sanitized
---

# Telegram: operator

Good — this is where the system stops being “a set of agents” and starts becoming a self-optimizing merge cognition layer.
Below is a Semantic Merge Memory System (SMMS) designed to sit on top of your Rebase + Conflict Resolver architecture.
It learns from conflicts, generalizes patterns, and reduces future merge work by converting repeated conflict classes into deterministic rules.


⸻


1) SYSTEM GOAL
Turn every resolved merge conflict into:
a reusable resolution rule
a semantic fingerprint
a future auto-resolution shortcut
So that:
The same class of conflict is never “reasoned about” twice.


⸻


2) POSITION IN ARCHITECTURE
Slarti (router)
   ↓
Rebase Controller
   ↓
Conflict Analyzer
   ↓
Conflict Resolver Worker
   ↓
Semantic Merge Memory System (THIS LAYER)
   ↓
Rule-enhanced future merges


⸻


3) CORE IDEA
Every merge conflict produces:
(1) Raw artifact
diff
AST mismatch
resolution patch
(2) Semantic fingerprint
what kind of change happened
(3) Resolution strategy
how it was fixed
These are stored as a Merge Experience Record (MER).


⸻


4) MER (MERGE EXPERIENCE RECORD)
{
  "mer_id": "uuid",

  "repo_context": {
    "module": "src/api.py",
    "function_scope": "create_user"
  },

  "conflict_fingerprint": {
    "ast_node_type": "FunctionDef",
    "change_pattern": "parameter_addition_vs_logic_change",
    "overlap_type": "same_function_dual_edit"
  },

  "conflict_class": "SEMANTIC_OVERLAP_FUNCTION_LEVEL",

  "resolution_strategy": {
    "method": "ast_merge_priority_union",
    "rule_applied": "preserve_all_non_conflicting_statements",
    "ordering_rule": "base_then_feature"
  },

  "patch_signature": "hash_of_final_diff",

  "outcome": "success | partial | escalated",

  "tests_status": "passed"
}


⸻


5) SEMANTIC FINGERPRINT ENGINE
This is the core intelligence layer.
5.1 Feature extraction
For each conflict:
AST node type (Function/Class/Import)
edit distance per node
overlap region size
dependency adjacency graph changes
side-effect signature changes


⸻


5.2 Normalized fingerprint
(FUNCTION_DEF, PARAM_CHANGE, LOGIC_DIFF_LOW, SAME_SCOPE)
This becomes the merge “type signature”.


⸻


6) MERGE RULE STORE (GLOBAL MEMORY)
Stored as indexed rules:
{
  "rule_id": "R-001",

  "signature": "FUNCTION_DEF + PARAM_ADD + LOW_LOGIC_OVERLAP",

  "strategy": {
    "type": "AST_MERGE",
    "behavior": "union_parameters + preserve_body_order",
    "conflict_policy": "non-destructive merge"
  },

  "confidence": 0.92,

  "usage_count": 48,

  "last_updated": "timestamp"
}


⸻


7) HOW IT AFFECTS FUTURE MERGES
BEFORE SMMS
Every conflict:
full AST analysis
full reasoning
worker invocation


⸻


AFTER SMMS
Step 1: fingerprint match
if fingerprint in rule_store:
    apply rule مباشرة (no LLM reasoning)
else:
    fallback to resolver worker


⸻


Step 2: rule application bypasses workers
For known patterns:
no LLM inference needed
deterministic patch generation
near-zero token cost for Slarti


⸻


8) LEARNING PIPELINE
8.1 Ingestion trigger
After every successful merge:
if merge_success:
    generate MER
    store in SMMS


⸻


8.2 Deduplication system
Avoid rule explosion:
if similarity(new_mer, existing_rule) > 0.95:
    increment usage_count
else:
    create new rule


⸻


8.3 Rule compression
Periodically:
cluster similar MERs
merge into generalized rules
Example:
12 “parameter addition conflicts”
→ 1 generalized AST merge rule


⸻


9) RULE EXECUTION ENGINE
function resolve_conflict(conflict):

    fingerprint = extract_fingerprint(conflict)

    rule = lookup(fingerprint)

    if rule exists:
        return apply(rule)

    else:
        return fallback_to_resolver_worker()


⸻


10) CONFIDENCE SYSTEM
Each rule has:
confidence score
decay over time
revalidation triggers
confidence -= drift_factor * time
confidence += successful_usage_bonus
If confidence < threshold:
→ revert to worker-based resolution


⸻


11) FAILURE MODES + SAFEGUARDS
11.1 Overgeneralization risk
Problem:
wrong abstraction of conflict type
Fix:
cluster splitting when error rate rises


⸻


11.2 Rule poisoning
Problem:
bad merge encoded as rule
Fix:
