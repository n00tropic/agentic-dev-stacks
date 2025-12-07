# Dist Artefacts

This directory holds build outputs for agent ecosystem bundles.

- `dist/bundles/`: Versioned ZIP bundles per stack/OS (`<bundle-id>-v<version>-<os>.zip`, e.g. `fullstack-js-ts-macos-v0.1.0-macos.zip`).
- `dist/metadata/`: Generated manifests, checksums, and bundle indices (e.g. `<bundle-id>-v<version>-manifest.json`, `checksums-v<version>.txt`, `bundles-index.json`).

The `dist/` tree is a build artefact and should generally be gitignored, except small metadata files if explicitly needed. Bundles themselves are not intended for version control.
