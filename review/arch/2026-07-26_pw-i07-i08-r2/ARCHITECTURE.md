# Architecture

The publication boundary is now fail-closed for every publishable type:

1. The sanitisation gate rejects a symlinked input root, any symlink or special
   entry below it, and missing text/image/archive scanners.
2. ZIPs use Python `ZipFile.testzip()` when Python is available. The fallback
   uses `unzip -t` before content scanning; failure to validate or extract is a
   rejection.
3. The bundle assembler independently rejects paths that escape the input root
   and all non-regular inputs before it copies anything.
4. The existing deterministic inventory and retention validation remain
   unchanged: pass 7 days; fail/prerequisite-error/error 30 days.
