# Updates and maintenance

## GitHub as the source of releases

Maintain the complete plugin under `plugins/framecore-work-creative-studio`. Keep its internal name `framecore-work-creative-studio` stable even though the repository name includes `works`.

Each release must keep the root manifest, compatibility manifest and current documentation version aligned. Preserve the complete starter prompt array, logo and existing tools unless a change was specifically requested. Preserve upstream source bytes and source manifests unless performing an intentional upstream update.

A Git commit does not automatically update the existing hosted ChatGPT plugin. Publish that plugin separately through its authorized update mechanism and verify the returned version and saved source. Never claim synchronization from a commit alone.

## User updates

For a Git-backed marketplace tracking a branch, use:

```sh
codex plugin marketplace upgrade framecore-works-creative-studio
```

A marketplace pinned to `v1.0.0` remains pinned; selecting a later release is an explicit source change. Preserve personal preferences and project records outside the distributed plugin before replacing an installation. Inspect the version after refresh.

Command source: [OpenAI, Package your plugin](https://developers.openai.com/plugins/build/plugins), read 2026-09-28. Exact account permissions and client support must be checked in the user's environment.

## Release procedure

1. Read the current source and preserve unrelated edits.
2. Update current version markers and write an accurate changelog.
3. Run structural validation and only the checks needed for changed behavior.
4. Build ZIPs with `python3 scripts/package_release.py` and inspect their inventories.
5. Confirm repository visibility and distribution terms. Preserve attribution and inspect additions for credentials or private client material.
6. Publish the Git commit and immutable release tag, then the authorized hosted plugin update. If either fails, report each result separately.
7. Verify the saved Git tree and plugin version. Record the actual publication result without rewriting unexecuted tests as passed.

The packaging script creates local files only. It never pushes, tags remotely, creates a repository, invokes providers or updates the hosted plugin.
