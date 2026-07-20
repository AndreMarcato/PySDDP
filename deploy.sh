#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! command -v git >/dev/null 2>&1; then
  echo "Git não foi encontrado no PATH." >&2
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  echo "Python não foi encontrado no PATH." >&2
  exit 1
fi

if [ $# -ge 1 ]; then
  VERSION="$1"
else
  read -r -p "Digite a nova versão (ex.: 0.0.66): " VERSION
fi

if [ $# -ge 2 ]; then
  MESSAGE="$2"
else
  MESSAGE="Release $VERSION"
fi

if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Versão inválida: $VERSION" >&2
  echo "Use um formato como 0.0.66" >&2
  exit 1
fi

SETUP_FILE="$ROOT_DIR/setup.py"
if [ ! -f "$SETUP_FILE" ]; then
  echo "Arquivo setup.py não encontrado em $ROOT_DIR" >&2
  exit 1
fi

python - <<'PY' "$SETUP_FILE" "$VERSION"
import pathlib
import re
import sys

setup_path = pathlib.Path(sys.argv[1])
version = sys.argv[2]
text = setup_path.read_text(encoding="utf-8")
new_text, count = re.subn(r'(?m)^VERSION\s*=\s*["\'][^"\']+["\']', f'VERSION = "{version}"', text)
if count != 1:
    raise SystemExit("Não foi possível localizar a linha VERSION em setup.py")
setup_path.write_text(new_text, encoding="utf-8")
PY

echo "Versão atualizada para $VERSION em setup.py"

git add -A

git commit -m "$MESSAGE"

BRANCH="$(git branch --show-current)"
if [ -z "$BRANCH" ]; then
  BRANCH="master"
fi

git push origin "$BRANCH"
git tag "$VERSION"
git push origin "$VERSION"

echo ""
echo "Fluxo concluído."
echo "- Commit enviado para o GitHub"
echo "- Tag criada e enviada: $VERSION"
echo "- O CircleCI deve disparar automaticamente após o push da tag"
