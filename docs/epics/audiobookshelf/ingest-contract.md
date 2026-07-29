# Media Ingest Contract

Audiobookshelf is a read-only consumer. Library Curator is the only writer into Curator-managed library roots: it owns staging, normalization, duplicate detection, quarantine, audit, and publication. Audiobookshelf must never upload, rename, move, delete, or write sidecars beside NAS media.

## Authority And Transition Model

(unchanged)

## Library Roots

(unchanged)

## Naming And Metadata

(unchanged)

## Validation Before Publication

Before publishing an item, the Curator must verify:

1. Its path is under one declared library root and has no temporary suffix.
2. The applicable naming form and required identity/metadata fields parse.
3. Duplicate detection compares content hashes and stable source identity, not filenames alone.
4. Source provenance and content hash are written to the Curator audit record, not the consumer library tree.
5. The complete item is published atomically at item or directory level.
6. A consumer library scan is requested only after the completed item is visible through the read-only mount.

Video-specific validation, including A/V synchronization, subtitle synchronization, track reconstruction, and operator approval of reconstructed media, is explicitly out of scope for this Audiobookshelf contract and belongs in the future Video Curator contract.