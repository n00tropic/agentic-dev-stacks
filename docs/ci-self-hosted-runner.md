# Self-hosted GitHub Actions runner (macOS)

Follow these repo-specific steps to install a self-hosted runner that handles docs/CI jobs locally on macOS with zsh.

## 1) Prepare a dedicated runner directory

Use a stable path outside the repo worktree to avoid mixing runner artefacts with source code:

```bash
mkdir -p ~/actions-runner/agentic-dev-stacks
cd ~/actions-runner/agentic-dev-stacks
```

## 2) Download the runner binary (pick the right architecture)

- Apple Silicon (arm64):

  ```bash
  curl -fsSLO https://github.com/actions/runner/releases/latest/download/actions-runner-osx-arm64-3.0.0.tar.gz
  tar -xzf actions-runner-osx-arm64-3.0.0.tar.gz
  ```

- Intel (x64): swap `arm64` for `x64` in the URL.

## 3) Generate a repo-scoped token in GitHub UI

- Navigate to **Settings → Actions → Runners → New self-hosted runner → macOS** for this repository.
- Copy the `./config.sh ... --token <TOKEN>` command shown by GitHub (token is short-lived; keep it secret).

## 4) Configure the runner

Run the command from the UI, or adapt this template (replace `<TOKEN>` and labels if desired):

```bash
./config.sh \
  --url https://github.com/n00tropic/agentic-dev-stacks \
  --token <TOKEN> \
  --name mac-runner-1 \
  --work _work \
  --labels self-hosted,mac,local
```

## 5) Run the runner

- Ad hoc (foreground):

  ```bash
  ./run.sh
  ```

  Keep this terminal open while jobs run.

- As a launchd service (background):

  ```bash
  sudo ./svc.sh install
  sudo ./svc.sh start
  ```

  To stop/remove later: `sudo ./svc.sh stop && sudo ./svc.sh uninstall`.

## 6) Verify

- In GitHub: **Settings → Actions → Runners** should show `mac-runner-1` as online.

## 7) Use the runner in workflows

- Jobs that should land on this runner must specify matching labels, e.g.:

```yaml
runs-on: [self-hosted, mac, local]
```

- If you want fallback to GitHub-hosted when the runner is offline, use a matrix or strategy that includes both.

## 8) Security and hygiene

- Run under a non-admin user when possible; keep the runner directory owned by that user.
- Tokens are secrets; if exposed, revoke/rotate via GitHub and re-run `config.sh`.
- Periodically `./svc.sh stop` and delete `~/actions-runner/agentic-dev-stacks/_work` to clean cached workspaces.
- Keep the binary current: re-download on new releases, then re-run `config.sh` with a fresh token.

## 9) Removing the runner cleanly

```bash
cd ~/actions-runner/agentic-dev-stacks
./config.sh remove --token <NEW_TOKEN_FROM_GITHUB>
rm -rf ~/actions-runner/agentic-dev-stacks
```

After removal, delete the runner entry in GitHub UI if it persists.
