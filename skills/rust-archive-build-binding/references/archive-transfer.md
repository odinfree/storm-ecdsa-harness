# Exact source archives across hosts

Use these checks when transporting an immutable Git source tree to a different filesystem, particularly macOS to Linux. They supplement the source-to-binary binding workflow; they do not authorize a provider purchase or workload.

- Inspect archive names before extraction. A tree can legitimately contain both `.codex/AGENTS.md` and `.codex/agents.md`; a case-insensitive filesystem cannot represent both. Export and hash the archive on the Mac, then extract on a case-sensitive Linux filesystem. Do not rename or silently discard source entries.
- Extract into a fresh owned directory. Validate relative member paths, reject unsupported entry kinds, and reject members beneath a symlink. Write regular files before symlinks. Apply executable/non-executable Git modes deliberately.
- Validate every link again after the complete link graph exists. A per-creation containment check can become false later: ordered links `a -> b/../safe`, then `b -> .`, can cause the first link to resolve outside the source directory. Treat an unresolvable cycle as a failed extraction.
- Bind each file's bytes and Git mode (`100644` or `100755`), and bind symlink text with mode `120000` without following it. Directory metadata is not a Git tree entry. When you need full tree identity, reconstruct the Git tree from paths, modes and blob bytes, or compare against a separately frozen complete manifest.
- Exercise an altered file, an executable-mode change and a late symlink-chain escape as negative controls. Validate the actual immutable archive on the target filesystem before starting a build. Portable fixtures alone do not establish that an archive's case-sensitive names survived.

A tool that uses a trusted, hash-bound archive may use a narrower extraction contract, but it should not claim general path-escape protection from incomplete checks.
