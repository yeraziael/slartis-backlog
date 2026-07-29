# Media Ingest Contract

Audiobookshelf is a read-only consumer. Library Curator is the only writer into
Curator-managed library roots: it owns staging, normalization, duplicate
detection, quarantine, audit, and publication. Audiobookshelf must never upload,
rename, move, delete, or write sidecars beside NAS media.

## Authority And Transition Model

The contract is defined per root rather than per application.

| Root or interface | Current writer | Current consumers | Status |
| --- | --- | --- | --- |
| `audiobooks/` | Library Curator | Audiobookshelf and, prospectively, Jellyfin | Curator-managed shared root |
| `podcasts/` | Library Curator | Audiobookshelf and, prospectively, Jellyfin | Curator-managed shared root |
| CWAUTO import folder | Library Curator | CWAUTO import process | Transitional hand-off interface |
| CWAUTO library | CWAUTO | CWAUTO | Legacy application-owned root |

Acquisition tools such as yt-dlp and podcast downloaders write only to declared
Curator input or staging folders outside indexed library roots. They never
publish directly into `audiobooks/`, `podcasts/`, the CWAUTO library, or any
other consumer-indexed root.

CWAUTO currently has one application-owned library and remains read-write on
that library. Until Library Curator supports e-book preparation, no Curator
e-book publication path is active. Once e-book preparation is implemented, the
first migration phase is for the Curator to place prepared e-books into the
CWAUTO import folder; CWAUTO remains responsible for importing and writing its
own library. Moving the CWAUTO library itself under Curator publication authority
is a later, explicit migration and is not implied by this contract.

The prospective end state is that Jellyfin, Audiobookshelf, and CWAUTO consume
applicable Curator-managed shared roots read-only. CWAUTO's current read-write
rights apply only to its isolated legacy library and must not grant write access
to Curator-managed roots.

## Library Roots

| Library | Root | Writer |
| --- | --- | --- |
| Audiobooks | `audiobooks/` | Library Curator |
| Podcasts | `podcasts/` | Library Curator |

The Curator assembles and validates a complete item outside the indexed root and
publishes the item atomically at directory or item level. Download caches,
temporary files, transcoding workspaces, input folders, and quarantine remain
outside indexed roots.

## Naming And Metadata

| Media | Required path and filename form | Required metadata |
| --- | --- | --- |
| Series audiobook | `audiobooks/<Author>/<Series>/<Series> #<NN> - <Title>/` | Author, title, narrator, series, sequence, language, publication year/date, genre, ISBN/ASIN and publisher where known |
| Standalone audiobook | `audiobooks/<Author>/<Title>/` | Author, title, narrator, language, publication year/date, genre, ISBN/ASIN and publisher where known |
| Audiobook files | `<NN> - <Chapter Title>.<ext>` below the audiobook directory | Embedded title, track number, album/book title, author, narrator and disc where applicable |
| Podcast | `podcasts/<Podcast Title>/<YYYY-MM-DD> - <Episode Title> [podcast-<safe-id>].<ext>` | Stable feed URL, original episode GUID, publication date, podcast title, episode title, author/uploader, description and language where known |

`<safe-id>` is a deterministic filesystem-safe representation derived from the
original episode GUID. The original GUID remains the identity value in metadata
and the Curator audit record.

Stable identifiers are identity keys; titles are display values and may change.
Unknown metadata remains explicitly unknown rather than fabricated. Cover art
may be embedded or provided as `cover.<ext>` in the item directory; no sidecar
may contain secrets, viewing data, or unverified personal metadata.

## Validation Before Publication

Before publishing an item, the Curator must verify:

1. Its path is under one declared library root and has no temporary suffix.
2. The applicable naming form and required identity/metadata fields parse.
3. Duplicate detection compares content hashes and stable source identity, not
   filenames alone.
4. Source provenance and content hash are written to the Curator audit record,
   not the consumer library tree.
5. The complete item is published atomically at item or directory level.
6. A consumer library scan is requested only after the completed item is visible
   through the read-only mount.
