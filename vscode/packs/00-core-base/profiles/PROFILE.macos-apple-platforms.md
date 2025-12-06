# Profile: macOS – Apple Platforms & Tooling

Slug: `macos-apple-platforms`  
Pack: `00-core-base`

## Intent

macOS and Apple platforms profile, tuned for Swift/Xcode-adjacent workflows.

## Canonical files

- Extensions list: `extensions.macos-apple-platforms.txt`
- Settings override: `settings.macos-apple-platforms.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "macOS – Apple Platforms & Tooling"
  ```

- Merge `settings.macos-apple-platforms.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.macos-apple-platforms.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.macos-apple-platforms.json`

## Workflow tips

- Fill the placeholders: set `swift.path` to the Swift toolchain (`/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swift`) and `lldb.executable` to the LLDB binary before opening Swift packages.
- Formatters: Swift Development Environment + SwiftLint handle Swift; Clang-Format covers C/C++/ObjC. Add repo-specific `.swiftlint.yml` and `.clang-format` files to keep editors and CI identical.
- Remote pairing: Remote SSH/Containers/Repos and Live Share are installed so you can pair on Xcode-adjacent work without sharing the main machine. Disable or uninstall if you need a fully local profile.
- Web/JS bridges: JS Debug Nightly + Playwright cover Catalyst/web targets when SwiftUI integrates with TypeScript frontends.
- MCP guidance: Sonatype server is marked `privacy_sensitive`; never feed unreleased product names or bundle IDs when running outside trusted sandboxes. Context7 is optional—enable only when you need Apple framework docs in the assistant.
