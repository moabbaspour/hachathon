# Changesets

Each Markdown file here is one pending change that will go into the next release. Don't write them by hand; run:

```bash
python3 scripts/release.py add <patch|minor|major> "What changed, for the CHANGELOG"
```

On push to `main`, the Release workflow turns all pending files into one version bump in `.claude-plugin/plugin.json` plus a `CHANGELOG.md` entry, and opens a "chore: version skills" PR. Merging that PR tags and publishes the release.

- `patch`: wording fixes, small behaviour tweaks to an existing skill
- `minor`: a new skill, or a noticeable change to what a skill does
- `major`: removing or renaming a skill
