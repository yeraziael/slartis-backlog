# Media Ingest Contract

Jellyfin is a read-only consumer. Library Curator and ytdl-sub are the only
writers covered by this contract. They must write into their staging or target
trees, verify results, and publish through their own approved workflows; they
must never ask Jellyfin to rename, move, delete, or generate sidecars.

## Library Roots

| Library | Root below `/Multimedia/jellyfin` | Writer |
| --- | --- | --- |
| Films | `movies/` | Library Curator |
| Series | `series/` | Library Curator |
| Music | `music/` | Library Curator |
| Music videos | `music-videos/` | Library Curator |
| YouTube archive | `youtube/` | ytdl-sub |

Writers must publish complete files atomically into these roots. Partial files,
temporary directories, download caches, and transcoding workspaces remain
outside every indexed root.

## Naming And Metadata

| Media | Required path and filename form | Required metadata |
| --- | --- | --- |
| Film | `movies/<Title> (<Year>)/<Title> (<Year>) [tmdbid-<id>].<ext>` | Title, production year, TMDb ID where known, language and content rating where known |
| Episode | `series/<Title> (<Year>)/Season <NN>/<Title> - S<NN>E<NN> - <Episode Title>.<ext>` | Series title, year, season, episode, title, language and content rating where known |
| Music | `music/<Album Artist>/<Album> (<Year>)/<Disc-NN>/<Track-NN> - <Title>.<ext>` | Embedded album artist, artist, album, title, disc, track, date/year, genre and MusicBrainz IDs where known |
| Music video | `music-videos/<Artist>/<Title> (<Year>)/<Artist> - <Title>.<ext>` | Embedded artist, title, year/date, genre and MusicBrainz IDs where known |
| YouTube | `youtube/<audience>/<channel-id>/<YYYY-MM-DD> - <title> [youtube-<video-id>].<ext>` | Stable channel ID, stable video ID, publication date, title, uploader/channel name, description and audience manifest |

`<audience>` is a deterministic Keycloak-group set, sorted and joined with
`--`; for example `parents--child-fsk-12`. ytdl-sub must use channel and video
IDs, not mutable handles or titles, as its identity keys. Human-readable title
text is a display value and may change without changing identity.

## Sidecars And Versions

- Curator may provide a sibling `.nfo` only when the source has verified data
  that embedded tags cannot express. The sidecar must contain no viewing data,
  secrets, or unverified age rating.
- ytdl-sub must retain the best available original as canonical media.
- A compatibility rendition is a sibling version, named with the same stable
  identity plus ` - compatibility-<profile>`, and never replaces the original.
- Writers must not create symlinks across library roots or mix films, series,
  music, music videos, and YouTube archives.

## Validation Before Publication

Every writer validates its output before making it visible to Jellyfin:

1. Path is under exactly one declared library root.
2. Filename parses against the relevant form and contains no temporary suffix.
3. Required identity and metadata fields are present; missing ratings remain
   explicitly unknown so Jellyfin authorization can fail closed.
4. Content hash and source/provenance are recorded by the writer, not Jellyfin.
5. The writer publishes a manifest without private titles or personal viewing
   data to its own audit channel.
