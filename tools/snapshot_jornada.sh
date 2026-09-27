#!/bin/sh
# Copia os scripts do save novo (pygame2) pra jornada/codigo/. O git guarda a evolução.
S=$(find ~/.local/share/Steam/steamapps/compatdata/*/pfx -type d -path '*TheFarmerWasReplaced/Saves/pygame2' 2>/dev/null | head -1)
[ -n "$S" ] || { echo "save pygame2 não encontrado" >&2; exit 1; }
cd "$(dirname "$0")/../jornada/codigo" || exit 1
rm -f ./*.py
find "$S" -maxdepth 1 -name '*.py' ! -name '__builtins__.py' -exec cp {} . \;
cp "$S/save.json" ../save.json
ls
