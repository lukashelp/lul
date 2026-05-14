#!/usr/bin/env python3
"""Sort files in a directory into subfolders by file type."""

import argparse
import shutil
import sys
from pathlib import Path

CATEGORIES = {
    "Images":     {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff", ".heic", ".raw"},
    "Videos":     {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg"},
    "Audio":      {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus"},
    "Documents":  {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp", ".txt", ".rtf", ".md"},
    "Archives":   {".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z", ".dmg", ".iso"},
    "Code":       {".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".sh", ".bash",
                   ".c", ".cpp", ".h", ".java", ".rs", ".go", ".rb", ".php", ".swift", ".kt"},
    "Executables":{".exe", ".msi", ".deb", ".rpm", ".appimage", ".apk", ".ipa"},
    "Fonts":      {".ttf", ".otf", ".woff", ".woff2"},
}

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
DIM    = "\033[2m"
RED    = "\033[91m"


def categorize(suffix: str) -> str:
    s = suffix.lower()
    for cat, exts in CATEGORIES.items():
        if s in exts:
            return cat
    return "Misc"


def unique_dest(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    i = 1
    while True:
        candidate = dest.parent / f"{stem} ({i}){suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def sort_directory(target: Path, dry_run: bool) -> None:
    files = [f for f in target.iterdir() if f.is_file()]

    if not files:
        print(f"{YELLOW}Keine Dateien in {target} gefunden.{RESET}")
        return

    moves: list[tuple[Path, Path]] = []
    for f in sorted(files):
        cat = categorize(f.suffix)
        dest = unique_dest(target / cat / f.name)
        moves.append((f, dest))

    # Preview
    print(f"\n{BOLD}{CYAN}{'VORSCHAU' if dry_run else 'SORTIERUNG'}{RESET}  "
          f"{DIM}({len(moves)} Datei(en) in {target}){RESET}\n")

    current_cat = None
    for src, dst in moves:
        cat = dst.parent.name
        if cat != current_cat:
            print(f"  {BOLD}{cat}/{RESET}")
            current_cat = cat
        arrow = f"{DIM}→{RESET}" if dry_run else f"{GREEN}→{RESET}"
        renamed = f"  {DIM}(→ {dst.name}){RESET}" if dst.name != src.name else ""
        print(f"    {src.name}{renamed}  {arrow}  {dst.parent.name}/")

    if dry_run:
        print(f"\n{YELLOW}Dry-run — nichts wurde verschoben.{RESET}")
        print(f"Zum Ausführen: {BOLD}python filesort.py --run{RESET}\n")
        return

    # Execute
    errors = 0
    for src, dst in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(src), str(dst))
        except Exception as e:
            print(f"{RED}  Fehler: {src.name}: {e}{RESET}")
            errors += 1

    ok = len(moves) - errors
    print(f"\n{GREEN}{BOLD}Fertig:{RESET} {ok} Datei(en) verschoben"
          + (f", {RED}{errors} Fehler{RESET}" if errors else "") + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="filesort",
        description="Sortiert Dateien eines Ordners nach Dateityp in Unterordner.",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(Path.home() / "Downloads"),
        help="Zu sortierender Ordner (Standard: ~/Downloads)",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Dateien wirklich verschieben (ohne diesen Flag: nur Vorschau)",
    )

    args = parser.parse_args()
    target = Path(args.directory).expanduser().resolve()

    if not target.is_dir():
        print(f"{RED}Fehler: '{target}' ist kein Verzeichnis.{RESET}")
        sys.exit(1)

    sort_directory(target, dry_run=not args.run)


if __name__ == "__main__":
    main()
