# Media Ingest Contract

Audiobookshelf is a read-only consumer. Library Curator is the only library
writer: it owns staging, normalization, duplicate detection, quarantine, and
publication. Audiobookshelf must never upload, rename, move, delete, or write
sidecars beside NAS media.

## Library Roots

| Library | Root | Writer |
| --- | --- | --- |
| Audiobooks | `audiobooks/` | Library Curator |
| Podcasts | `podcasts/` | Library Curator or its approved podcast workflow |

Writers publish complete files atomically into exactly one root. Download
caches, temporary files, transcoding workspaces, and quarantine remain outside
the indexed roots.

## Naming And Metadata

| Media | Required path and filename form | Required metadata |
| --- | --- | --- |
| Audiobook | `audiobooks/<Author>/<Series>/<Series> #<NN> - <Title>/` | Author, title, narrator, series and sequence where applicable, language, publication year/date, genre, ISBN/ASIN and publisher where known |
| Audiobook files | `<NN> - <Chapter Title>.<ext>` below the audiobook directory | Embedded title, track number, album/book title, author, narrator and disc where applicable |
| Podcast | `podcasts/<Podcast Title>/<YYYY-MM-DD> - <Episode Title> [podcast-<guid>].<ext>` | Stable feed URL, episode GUID, publication date, podcast title, episode title, author/uploader, description and language where known |

Stable identifiers are identity keys; titles are display values and may change.
Unknown metadata remains explicitly unknown rather than fabricated. Cover art
may be embedded or provided as `cover.<ext>` in the item directory; no sidecar
may contain secrets, viewing data, or unverified personal metadata.

## Validation Before Publication

Before publishing an item, the writer must verify:

1. Its path is under one declared library root and has no temporary suffix.
2. The applicable naming form and required identity/metadata fields parse.
3. Duplicate detection compares content hashes and stable source identity, not
   filenames alone.
4. Source provenance and content hash are written to the Curator audit record,
   not the Audiobookshelf library tree.
5. A library scan is requested only after the completed item is visible through
   the read-only NFS mount.
