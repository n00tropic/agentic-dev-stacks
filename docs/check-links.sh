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
	case "${os}" in
	Darwin)
		case "${arch}" in
		arm64 | aarch64) echo "aarch64-apple-darwin" ;;
		x86_64) echo "x86_64-apple-darwin" ;;
		*) return 1 ;;
		esac
		;;
	Linux)
		case "${arch}" in
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
	local -a lychee_flags
	lychee_flags=(--no-progress)
	if [[ ${CHECK_EXTERNAL:-0} == "1" ]]; then
		echo "Running lychee with external link checks (http/https)."
		lychee_flags+=(--scheme http --scheme https)
	else
		echo "Running lychee in offline mode (local files and anchors only)."
		lychee_flags+=(--offline)
	fi
	lychee_flags+=(build/site)
	if command -v lychee >/dev/null 2>&1; then
		lychee "${lychee_flags[@]}"
		return
	fi
	target=""
	detect_target_exit=0
	target="$(detect_target)" || detect_target_exit=$?
	if ((detect_target_exit != 0)) || [[ -z ${target-} ]]; then
		echo "Unsupported platform for lychee binary" >&2
		exit 1
	fi
	url="https://github.com/lycheeverse/lychee/releases/latest/download/lychee-${target}.tar.gz"
	tmpdir="$(mktemp -d 2>/dev/null || true)"
	if [[ -z ${tmpdir-} ]]; then
		echo "Failed to create temporary directory for lychee" >&2
		exit 1
	fi
	trap '[[ -n "${tmpdir:-}" ]] && rm -rf "${tmpdir}"' EXIT
	echo "Downloading lychee binary for ${target}..."
	if ! curl -fsSL "${url}" -o "${tmpdir}/lychee.tar.gz"; then
		echo "Failed to download lychee from ${url}" >&2
		exit 1
	fi
	tar -xzf "${tmpdir}/lychee.tar.gz" -C "${tmpdir}"
	bin="${tmpdir}/lychee"
	chmod +x "${bin}"
	"${bin}" "${lychee_flags[@]}"
}

run_lychee
