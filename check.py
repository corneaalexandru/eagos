"""Check EAGOS document structure, local links and pinned provenance only."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


VERSION = "5.0.0"
SOURCE_SHA = "bb8136335c5369b9ac9da88d7b91b03dcd1243e8"
ROOT = Path(__file__).resolve().parent
DOCUMENTS = ("readme.md", "eagos.md", "sources.md")


def check():
    errors = []
    documents = {}
    for name in DOCUMENTS:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Missing document: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        documents[name] = text
        if not text.strip():
            errors.append(f"Empty document: {name}")
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if not re.fullmatch(rf"# (?:Sources — )?EAGOS {re.escape(VERSION)}", first_line):
            errors.append(f"Version missing from title: {name}")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(ROOT):
                errors.append(f"Local link leaves distribution: {name}: {target}")
            elif not destination.is_file():
                errors.append(f"Broken local link: {name}: {target}")

    sources = documents.get("sources.md", "")
    base = "https://github.com/corneaalexandru/eagos"
    if f"{base}/commit/{SOURCE_SHA}" not in sources:
        errors.append("Pinned upstream commit is missing from sources.md")
    for name in ("README.md", "00_eagos.md", "04_operating_guide.md",
                 "05_agent_organization.md"):
        if f"{base}/blob/{SOURCE_SHA}/{name}" not in sources:
            errors.append(f"Pinned source link is missing: {name}")
    return errors


if __name__ == "__main__":
    failures = check()
    if failures:
        print("\n".join(failures), file=sys.stderr)
        sys.exit(1)
    print(f"EAGOS {VERSION}: document checks passed; operational controls not assessed.")
