# Architecture

The repository-wide scanner inspects tracked test source as well as production
source. The credential-safe summary test must construct malicious token-shaped
values at runtime, so scanner coverage is retained without embedding patterns
that look like real credentials in Git.
