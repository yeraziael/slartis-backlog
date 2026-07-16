---
snapshot_version: gitea-backlog-issue/v1
source: slarti/backlog#211
state: closed
updated_at: 2026-07-14T12:53:51+02:00
is_epic: false
labels:
  []
publication: sanitized
---

# Implement CI-gated branch protection and automatic merging as the standard behavior for all Gitea repositories that have an active CI/CD pipeline.

Gitea instance:
`<internal-gitea-reference>

Scope:

* Inspect all accessible repositories.
* Apply the policy to every repository that has a functional CI/CD pipeline.
* Do not apply automatic merging to repositories without a CI/CD pipeline.
* Make this the default behavior for repositories that gain a CI/CD pipeline in the future.

Primary objective:

Whenever a repository has a functional CI/CD pipeline, its default branch must be protected and eligible pull requests must automatically merge after all required CI and repository conditions succeed.

Use the Gitea REST API and the API schema exposed by the installed Gitea instance as the authoritative source. Do not assume fields or endpoints from another Gitea version.

## 1. Repository discovery and classification

Enumerate all accessible repositories and classify each repository into one of these categories:

1. CI/CD pipeline present and functional.
2. CI/CD configuration present but incomplete, disabled, or not functional.
3. No CI/CD pipeline present.
4. Archived, mirror-only, template, or otherwise unsuitable for automatic modification.

Determine the default branch for each repository through the API. Do not assume that it is always named `main`.

A repository qualifies for this policy only when:

* a CI/CD workflow or equivalent pipeline configuration exists;
* the pipeline runs for pull requests or commits targeting the default branch;
* actual CI status results or check contexts can be identified;
* the pipeline is not obviously disabled, obsolete, or permanently failing due to configuration errors.

Do not invent CI status contexts.

## 2. Existing settings

For every qualifying repository, inspect:

* repository merge settings;
* branch-protection rules affecting the default branch;
* push and force-push permissions;
* branch deletion protection;
* required CI status-check contexts;
* review and approval requirements;
* merge-method configuration;
* automatic source-branch deletion;
* existing auto-merge workflows, bots, hooks, or API integrations.

Consolidate the existing settings with the new standard policy.

Consolidation means:

* preserve useful existing settings;
* preserve stricter protections unless they are obsolete, contradictory, or demonstrably harmful;
* add missing settings required by this policy;
* normalize inconsistent settings across repositories;
* remove duplicated, obsolete, or contradictory automation where justified;
* avoid creating multiple competing auto-merge mechanisms;
* do not weaken an existing protection without documenting the reason;
* do not blindly overwrite repository-specific requirements.

Where repository-specific settings are stricter than the standard policy, retain the stricter setting unless it prevents the repository from functioning correctly.

## 3. Decisions delegated to the agent

For each repository, independently determine:

* which actual CI checks must be mandatory;
* the appropriate merge method;
* whether reviews or approvals are required;
* whether the pull-request branch must be up to date with the default branch;
* whether any repository-specific exception is necessary.

Base these decisions on:

* repository purpose;
* existing CI/CD workflows;
* existing protection settings;
* recent pull-request behavior;
* existing contribution or development documentation;
* the risk of automatic merging for that repository.

Document each decision briefly.

## 4. Standard branch-protection policy

For every qualifying repository, protect its default branch so that:

* direct pushes are prohibited;
* force pushes are prohibited;
* deletion of the protected branch is prohibited;
* required CI checks must succeed before merging;
* pending or failing required checks block merging;
* only actual CI status-check context names are used;
* configured review and approval requirements are enforced;
* rejected reviews block merging where supported and appropriate;
* branch-protection bypass and administrator override are not used by the automation;
* the automation cannot merge draft pull requests.

The exact implementation must follow the installed Gitea version and its exposed API schema.

## 5. Repository merge settings

For every qualifying repository:

* enable the selected merge method;
* set it as the default merge method;
* disable redundant or inappropriate merge methods where justified;
* enable automatic deletion of the source branch after a successful merge;
* retain stricter repository-specific merge restrictions where appropriate.

## 6. Repository-wide automatic merging

Gitea auto-merge may be scheduled per pull request rather than enabled through one permanent repository flag.

Implement a central or reusable mechanism that makes auto-merge the standard behavior for every qualifying repository.

The mechanism must automatically schedule auto-merge for every eligible pull request that:

* targets the protected default branch;
* is not a draft;
* is newly opened, reopened, or converted from draft to ready;
* belongs to a repository classified as having a functional CI/CD pipeline;
* is not explicitly excluded through a documented repository-specific exception.

The automation must:

* schedule auto-merge through the Gitea API;
* use the merge method selected for that repository;
* request deletion of the source branch;
* wait for all required CI checks;
* wait for all required reviews and approvals;
* remain subject to branch protection;
* never use an administrator bypass;
* never merge a pull request with pending or failing requirements;
* behave idempotently if auto-merge is already scheduled;
* handle updated commits and rerun CI without creating duplicate operations;
* avoid logging or exposing API credentials.

Prefer one maintainable shared implementation over copying independent scripts into every repository.

Suitable implementation options include:

* a centrally managed Gitea Actions workflow;
* a reusable workflow invoked by repositories;
* an organization-level trusted automation service;
* an existing Lydia or Slarti automation component;
* another native Gitea mechanism supported by the installed version.

Select the simplest reliable architecture that supports both existing and future repositories.

## 7. Standard behavior for future repositories

Implement a detection and reconciliation mechanism so this policy remains the default over time.

The mechanism must periodically or event-driven:

* discover newly created repositories;
* detect repositories that newly acquire a CI/CD pipeline;
* detect changes to default branches;
* detect drift in branch-protection or merge settings;
* apply or reconcile the standard policy;
* stop applying automatic merge if a pipeline is removed or becomes non-functional;
* preserve documented repository-specific exceptions.

The process must be idempotent.

Do not require a one-time manual command for every future repository.

Maintain a machine-readable policy or configuration defining:

* the standard settings;
* repository eligibility criteria;
* approved exceptions;
* excluded repositories;
* repository-specific overrides;
* last reconciliation result.

## 8. Exceptions

Support explicit exceptions for repositories where automatic merging is unsuitable.

Examples may include:

* production-critical infrastructure;
* repositories requiring mandatory human approval;
* repositories with deployment side effects;
* archived or mirror repositories;
* repositories with unreliable CI;
* repositories containing security-sensitive automation.

Exceptions must be:

* explicit;
* machine-readable;
* documented with a reason;
* narrowly scoped;
* preserved during future reconciliation.

An exception may disable auto-merge while retaining branch protection and mandatory CI.

## 9. Safe execution process

Before making changes:

1. Discover and classify all repositories.
2. Read the current settings through the API.
3. Identify actual CI status contexts.
4. Detect existing automation and possible conflicts.
5. Produce a proposed change plan per repository.
6. Identify repositories that will be skipped or treated as exceptions.

Then apply the changes.

Do not expose or commit API tokens. Use the existing secure secret-management mechanism.

Do not modify archived, mirrored, or unrelated repositories without justification.

Do not remove working existing automation until its replacement has been verified.

## 10. Verification

After applying the policy, read every modified setting back through the API.

For each qualifying repository, verify:

* the correct default branch is protected;
* direct pushes are blocked;
* force pushes are blocked;
* branch deletion is blocked;
* the selected CI contexts are required;
* the selected review policy is active;
* the selected merge method is configured;
* source branches are deleted after successful merge;
* global automation recognizes the repository;
* eligible pull requests are scheduled for auto-merge;
* branch protection remains authoritative.

Where practical, test the behavior with a temporary pull request in at least one representative repository before rolling the policy out to all remaining repositories.

The test must confirm:

* auto-merge is scheduled;
* the pull request does not merge while CI is pending;
* failing CI prevents merging;
* successful CI permits merging;
* required reviews remain enforced;
* the source branch is deleted after merge;
* direct pushes to the protected branch are rejected.

Clean up temporary branches and test pull requests afterward.

## 11. Required output

Provide:

* detected Gitea version;
* API endpoints and fields used;
* list of all repositories inspected;
* classification of every repository;
* detected default branch for every repository;
* detected CI workflows and status contexts;
* previous and resulting settings;
* consolidation decisions;
* selected merge and review policy per repository;
* repositories skipped and the reason;
* exceptions created or preserved;
* description of the global auto-merge mechanism;
* description of the future reconciliation mechanism;
* verification results;
* unsupported or version-specific limitations;
* all files, workflows, services, or configuration records changed.

## Definition of Done

* Every repository with a functional CI/CD pipeline has its default branch protected.
* Direct pushes, force pushes, and deletion of the protected branch are blocked.
* Real CI status checks are required before merging.
* Existing settings have been coherently consolidated with the standard policy.
* Stricter useful protections remain intact.
* Eligible pull requests are automatically scheduled for merge.
* Auto-merge never bypasses CI, reviews, or branch protection.
* Source branches are deleted after successful merging.
* Repositories without functional CI/CD are not automatically merged.
* Newly created repositories automatically receive the policy once a functional CI/CD pipeline exists.
* Configuration drift is detected and reconciled.
* Repository-specific exceptions are supported and documented.
* Final state is verified through API read-back.
* No credentials or secrets are exposed.
