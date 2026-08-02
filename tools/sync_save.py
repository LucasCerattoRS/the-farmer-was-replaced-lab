#!/usr/bin/env python3
"""sync_save.py — Linux equivalent of sync_save.ps1 (import TFWR save code
into the curated repo layout). Dry-run by default (reports NEW / CHANGED /
OK / UNMAPPED); pass --apply to copy.

TFWR is a Windows build running under Proton on Linux (no known native
build), so save files live inside a Proton prefix, not under a native
~/.local/share path -- something like
~/.steam/steam/steamapps/compatdata/<APP_ID>/pfx/drive_c/users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves/pygame
but the exact APP_ID isn't known here (not guessing it -- a wrong numeric ID
would just fail silently in a confusing way). This script globs for the
"TheFarmerWasReplaced/.../Saves/pygame" suffix under compatdata/* to find it
automatically; pass --save-dir directly if that doesn't find it (e.g. `find
~/.steam -ipath '*TheFarmerWasReplaced*Saves/pygame' 2>/dev/null` to locate
it yourself first).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_SUFFIX = "AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves/pygame"


def _auto_detect_save_dir() -> Path | None:
    for steam_root in (Path.home() / ".steam/steam", Path.home() / ".local/share/Steam"):
        compatdata = steam_root / "steamapps/compatdata"
        if not compatdata.is_dir():
            continue
        for candidate in compatdata.glob(f"*/pfx/drive_c/users/steamuser/{_SUFFIX}"):
            if candidate.is_dir():
                return candidate
    return None


def md5(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Actually copy files (default: dry-run)")
    parser.add_argument("--save-dir", type=Path, default=None)
    args = parser.parse_args()

    save_dir: Path | None = args.save_dir or _auto_detect_save_dir()
    if save_dir is None or not save_dir.is_dir():
        print(f"Save dir not found{f': {save_dir}' if save_dir else ''}.", file=sys.stderr)
        print("Auto-deteccao falhou (App ID do Proton prefix nao conhecido de antemao).", file=sys.stderr)
        print("Localize com: find ~/.steam -ipath '*TheFarmerWasReplaced*Saves/pygame' 2>/dev/null", file=sys.stderr)
        print("e passe --save-dir <caminho>.", file=sys.stderr)
        return 1

    mapping = json.loads((Path(__file__).parent / "sync_map.json").read_text(encoding="utf-8"))
    skip = set(mapping.get("skip", []))
    files_map = mapping["files"]

    stats = {"new": 0, "changed": 0, "ok": 0, "unmapped": 0}

    for f in sorted(save_dir.iterdir()):
        if not f.is_file() or f.name in skip:
            continue
        dest_rel = files_map.get(f.name)
        if not dest_rel:
            print(f"UNMAPPED  {f.name}")
            stats["unmapped"] += 1
            continue
        dest = REPO / dest_rel
        if not dest.exists():
            print(f"NEW       {f.name} -> {dest_rel}")
            stats["new"] += 1
            if args.apply:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
        elif md5(f) != md5(dest):
            print(f"CHANGED   {f.name} -> {dest_rel}")
            stats["changed"] += 1
            if args.apply:
                shutil.copy2(f, dest)
        else:
            stats["ok"] += 1

    print()
    print(f"OK: {stats['ok']}  NEW: {stats['new']}  CHANGED: {stats['changed']}  UNMAPPED: {stats['unmapped']}")
    if not args.apply and (stats["new"] + stats["changed"]) > 0:
        print("Dry-run only. Re-run with --apply to copy.")
    if stats["unmapped"] > 0:
        print("Add unmapped files to tools/sync_map.json (or to its 'skip' list).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
