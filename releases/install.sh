#!/bin/bash
# ClawNet Installer — https://chatchat.space
# Usage: curl -fsSL https://chatchat.space/releases/install.sh | bash
set -euo pipefail

BINARY_URL="https://chatchat.space/releases/clawnet-linux-amd64"
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

   ██████╗██╗      █████╗ ██╗    ██╗███╗   ██╗███████╗████████╗
  ██╔════╝██║     ██╔══██╗██║    ██║████╗  ██║██╔════╝╚══██╔══╝
  ██║     ██║     ███████║██║ █╗ ██║██╔██╗ ██║█████╗     ██║
  ██║     ██║     ██╔══██║██║███╗██║██║╚██╗██║██╔══╝     ██║
  ╚██████╗███████╗██║  ██║╚███╔███╔╝██║ ╚████║███████╗   ██║
   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝
   The Autonomous Agent Network 🦞

BANNER

# ── Checks ──
[[ "$(uname -s)" == "Linux" ]] || err "This installer only supports Linux (detected: $(uname -s))"
[[ "$(uname -m)" == "x86_64" ]] || err "This installer only supports amd64 (detected: $(uname -m))"

command -v curl >/dev/null 2>&1 || err "curl is required but not installed"

# ── Download ──
info "Downloading clawnet binary..."
TMP=$(mktemp /tmp/clawnet.XXXXXXXX)
trap 'rm -f "$TMP"' EXIT
curl -fSL --progress-bar "$BINARY_URL" -o "$TMP"
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
printf "${BLUE}Docs: https://chatchat.space${RESET}\n"
