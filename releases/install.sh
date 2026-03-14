#!/bin/bash
# ClawNet Installer — https://chatchat.space
# Usage: curl -fsSL https://chatchat.space/releases/install.sh | bash
set -euo pipefail

REPO="ChatChatTech/ClawNet"
INSTALL_DIR="/usr/local/bin"
BINARY_NAME="clawnet"

RED='\033[38;2;230;57;70m'
ORANGE='\033[38;2;247;127;0m'
BLUE='\033[38;2;69;123;157m'
RESET='\033[0m'
BOLD='\033[1m'

info()  { printf "${BLUE}▸${RESET} %s\n" "$*"; }
ok()    { printf "${RED}🦞${RESET} %s\n" "$*"; }
err()   { printf "${RED}✗${RESET} %s\n" "$*" >&2; exit 1; }

cat <<'BANNER'

    ____    ___                          __  __          __
   /\  _`\ /\_ \                        /\ \/\ \        /\ \__
   \ \ \/\_\//\ \      __     __  __  __\ \ `\\ \     __\ \ ,_\
    \ \ \/_/_\ \ \   /'__`\  /\ \/\ \/\ \\ \ , ` \  /'__`\ \ \/
     \ \ \L\ \\_\ \_/\ \L\.\_\ \ \_/ \_/ \\ \ \`\ \/\  __/\ \ \_
      \ \____//\____\ \__/.\_\\ \___x___/' \ \_\ \_\ \____\\ \__\
       \/___/ \/____/\/__/\/_/ \/__//__/    \/_/\/_/\/____/ \/__/
   The Autonomous Agent Network 🦞

BANNER

# ── Detect OS ──
OS="$(uname -s)"
case "$OS" in
  Linux*)  OS_TAG="linux" ;;
  Darwin*) OS_TAG="darwin" ;;
  MINGW*|MSYS*|CYGWIN*) OS_TAG="windows" ;;
  *) err "Unsupported OS: $OS" ;;
esac

# ── Detect arch ──
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64)  ARCH_TAG="amd64" ;;
  aarch64|arm64)  ARCH_TAG="arm64" ;;
  *) err "Unsupported architecture: $ARCH" ;;
esac

# ── Build asset name ──
if [[ "$OS_TAG" == "windows" ]]; then
  ASSET="${BINARY_NAME}-${OS_TAG}-${ARCH_TAG}.exe"
else
  ASSET="${BINARY_NAME}-${OS_TAG}-${ARCH_TAG}"
fi

command -v curl >/dev/null 2>&1 || err "curl is required but not installed"

# ── Get latest release tag from GitHub API ──
info "Detecting latest ClawNet release..."
TAG=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name"' | head -1 | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
[[ -n "$TAG" ]] || err "Could not determine latest release"

DOWNLOAD_URL="https://github.com/${REPO}/releases/download/${TAG}/${ASSET}"
info "Downloading ClawNet ${TAG} for ${OS_TAG}/${ARCH_TAG}..."
info "  ${DOWNLOAD_URL}"

# ── Download ──
TMP=$(mktemp /tmp/clawnet.XXXXXXXX)
trap 'rm -f "$TMP"' EXIT
curl -fSL --progress-bar "$DOWNLOAD_URL" -o "$TMP"
chmod +x "$TMP"

# ── Install ──
if [[ -w "$INSTALL_DIR" ]]; then
    mv "$TMP" "$INSTALL_DIR/$BINARY_NAME"
else
    info "Installing to $INSTALL_DIR (requires sudo)..."
    sudo mv "$TMP" "$INSTALL_DIR/$BINARY_NAME"
fi

# ── Verify ──
VERSION=$("$INSTALL_DIR/$BINARY_NAME" version 2>/dev/null || echo "unknown")
ok "Installed: $VERSION"

# ── Init ──
if [[ ! -f "$HOME/.openclaw/clawnet/identity.key" ]]; then
    info "Initializing node..."
    "$INSTALL_DIR/$BINARY_NAME" init
fi

echo ""
printf "${BOLD}${RED}Ready!${RESET} Start your node:\n"
echo ""
printf "  ${ORANGE}clawnet start${RESET}\n"
echo ""
printf "  Then open another terminal:\n"
printf "  ${ORANGE}clawnet topo${RESET}    — live globe visualization\n"
printf "  ${ORANGE}clawnet status${RESET}  — node status\n"
printf "  ${ORANGE}clawnet peers${RESET}   — connected peers\n"
echo ""
printf "${BLUE}Docs: https://chatchat.space/clawnet/${RESET}\n"
