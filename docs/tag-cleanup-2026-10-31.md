# Release tag cleanup (2026-10-31)

The owner approved deleting old release tags on 2026-10-31 ("tagi możesz posprzątać"). This reverses the 2026-10-29 audit recommendation to keep every tag. The repository had 199 tags `v1.0.0` to `v1.161.1`, almost all with a GitHub Release.

## What stays

14 tags (13 with a GitHub Release):

- `v1.156.0` to `v1.161.1` (11 releases): the current release, the baseline that `scripts/release.py` and `scripts/check_version_bump.py` read (they only need the latest tag), recent tag pins in Claude Code installs, and 1.156.0, the version the hosted ChatGPT Work plugin carries.
- `v1.33.0`, `v1.111.1` and `v1.126.0`: linked from `docs/sound-test-1.33.0.md`, `docs/reviews/audit-closure-2026-10-20.md` and `docs/audit-repairs-and-handover-2026-10-24.md`.

No Toolbox or Open Assets file pins a Studio tag; both companions have no tags of their own.

## What goes

The other 185 tags are listed with their commit and date in [tag-cleanup-2026-10-31.txt](tag-cleanup-2026-10-31.txt). They were deleted on 2026-10-31 with `git push origin --delete` from the owner's Mac after the owner's typed approval (cloud agent sessions get HTTP 403 for tag and release deletion). GitHub removed 184 of their releases with the tags; the remaining draft (1.0.0) was deleted by hand. Readback: 14 tags, 13 published releases (`v1.33.0` is a tag without a release), no drafts. Release notes stay in `CHANGELOG.md` and `plugins/framecore-work-creative-studio/docs/release-history.md`; the `release_url` fields in older `verification/*.json` records are history and now point to deleted releases.

## Restoring a tag

Every listed commit is on `main`, so a tag can be recreated from the list, for example:

```bash
git tag v1.150.0 <commit from the list> && git push origin refs/tags/v1.150.0
```

A recreated tag has no GitHub Release; rebuild its assets with `scripts/package_release.py` at that commit if they are needed.
