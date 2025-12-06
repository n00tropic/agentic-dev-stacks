#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -d build/site ]]; then
	echo "Docs not built. Run ./build-docs.sh first." >&2
	exit 1
fi

detect_target() {
	local os arch
	os="$(uname -s)"
	arch="$(uname -m)"
	case "$os" in
	Darwin)
		case "$arch" in
		arm64 | aarch64) echo "aarch64-apple-darwin" ;;
		x86_64) echo "x86_64-apple-darwin" ;;
		*) return 1 ;;
		esac
		;;
	Linux)
		case "$arch" in
		arm64 | aarch64) echo "aarch64-unknown-linux-gnu" ;;
		x86_64) echo "x86_64-unknown-linux-gnu" ;;
		*) return 1 ;;
		esac
		;;
	*) return 1 ;;
	esac
}

run_lychee() {
	local target url tmpdir bin
	if command -v lychee >/dev/null 2>&1; then
		lychee --scheme http --scheme https --no-progress build/site
		return
	fi
	target="$(detect_target)" || {
		echo "Unsupported platform for lychee binary" >&2
		exit 1
	}
	url="https://github.com/lycheeverse/lychee/releases/latest/download/lychee-${target}.tar.gz"
	tmpdir="$(mktemp -d)"
	trap 'rm -rf "${tmpdir}"' EXIT
	echo "Downloading lychee binary for ${target}..."
	if ! curl -fsSL "${url}" -o "${tmpdir}/lychee.tar.gz"; then
		echo "Failed to download lychee from ${url}" >&2
		exit 1
	fi
	tar -xzf "${tmpdir}/lychee.tar.gz" -C "${tmpdir}"
	bin="${tmpdir}/lychee"
	chmod +x "${bin}"
	"${bin}" --scheme http --scheme https --no-progress build/site
}

run_lychee
