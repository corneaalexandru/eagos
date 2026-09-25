"""Check EAGOS document metadata, local links and pinned provenance only."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from eagos import GovernanceError
from eagos.conventions import markdown_body, validate_identifier

VERSION = "5.1.0"
SOURCE_SHA = "bb8136335c5369b9ac9da88d7b91b03dcd1243e8"
ROOT = Path(__file__).resolve().parent
DOCUMENTS = ("readme.md", "eagos.md", "sources.md", "examples/project.md")


def check():
    errors, documents = [], {}
    for name in DOCUMENTS:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Missing document: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        documents[name] = text
        try:
            body = markdown_body(text)
        except GovernanceError as error:
            errors.append(f"Invalid frontmatter: {name}: {error}")
            continue
        header = re.match(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
        if not header:
            errors.append(f"Missing frontmatter: {name}")
            continue
        fields = dict(re.findall(r"^([a-z_]+):[ \t]*(.*)$", header[1], re.M))
        fields = {key: value.strip().strip('"').strip("'") for key, value in fields.items()}
        for key in ("title", "type", "status", "updated"):
            if not fields.get(key):
                errors.append(f"Missing {key} metadata: {name}")
        if fields.get("framework") != "EAGOS" or fields.get("framework_version") != VERSION:
            errors.append(f"Framework version mismatch: {name}")
        first_line = body.strip().splitlines()[0] if body.strip() else ""
        if name.startswith("examples/"):
            try:
                validate_identifier(fields.get("id"))
            except GovernanceError as error:
                errors.append(f"Invalid example identity: {name}: {error}")
            if not first_line.startswith("# "):
                errors.append(f"Missing example title: {name}")
        elif not re.fullmatch(rf"# (?:Sources — )?EAGOS {re.escape(VERSION)}", first_line):
            errors.append(f"Version missing from title: {name}")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", body):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.is_file():
                errors.append(f"Invalid local link: {name}: {target}")

    sources = documents.get("sources.md", "")
    base = "https://github.com/corneaalexandru/eagos"
    if f"{base}/commit/{SOURCE_SHA}" not in sources:
        errors.append("Pinned upstream commit is missing from sources.md")
    for name in ("README.md", "00_eagos.md", "04_operating_guide.md", "05_agent_organization.md"):
        if f"{base}/blob/{SOURCE_SHA}/{name}" not in sources:
            errors.append(f"Pinned source link is missing: {name}")
    return errors


if __name__ == "__main__":
    failures = check()
    if failures:
        print("\n".join(failures), file=sys.stderr)
        sys.exit(1)
    print(f"EAGOS {VERSION}: document checks passed; operational controls not assessed.")
