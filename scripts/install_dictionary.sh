#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${REPO_ROOT}/.venv"
PYTHON_BIN="${VENV_DIR}/bin/python"
DDK_BIN="/Applications/XcodeAdditionalTools/Utilities/DictionaryDevelopmentKit/bin/build_dict.sh"
DDK_BIN_SPACED="/Applications/Additional Tools for Xcode/Utilities/DictionaryDevelopmentKit/bin/build_dict.sh"

echo "[1/6] Checking platform"
if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This installer is for macOS only."
  exit 1
fi

echo "[2/6] Checking DictionaryDevelopmentKit"
if [[ ! -x "${DDK_BIN}" ]]; then
  echo "Missing DictionaryDevelopmentKit build tool: ${DDK_BIN}"
  if [[ -x "${DDK_BIN_SPACED}" ]]; then
    echo "Detected Xcode tools in a path with spaces."
    echo "Rename it so build tools use a space-free path:"
    echo "  sudo mv \"/Applications/Additional Tools for Xcode\" \"/Applications/XcodeAdditionalTools\""
  else
    echo "Install Xcode Additional Tools and try again."
  fi
  exit 1
fi

echo "[3/6] Creating virtual environment (if needed)"
if [[ ! -x "${PYTHON_BIN}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

echo "[4/6] Installing Python dependency: islenska"
"${PYTHON_BIN}" -m pip install --upgrade pip >/dev/null
"${PYTHON_BIN}" -m pip install islenska

echo "[5/6] Building Icelandic dictionary XML"
cd "${REPO_ROOT}"
"${PYTHON_BIN}" scripts/build_dict.py

echo "[6/6] Installing dictionary bundle"
make install

echo "Done. Open Dictionary.app settings and enable 'Íslensk orðabók' if needed."
