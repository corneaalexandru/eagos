"""Shared record names. Hosts enforce filesystem boundaries."""

import re
from pathlib import PurePosixPath

from . import GovernanceError

CONTRACT_VERSION = 1
PATHS = {
    "policy": "00_governance/policy.md",
    "decisions": "00_governance/decisions",
    "initiatives": "10_initiatives",
    "tasks": "20_tasks",
    "evidence": "30_evidence",
    "outputs": "40_outputs",
    "inputs": "20_tasks/inputs",
}


def validate_identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", value):
        raise GovernanceError("Use a lowercase identifier with underscores, at most 64 characters")
    return value


def validate_evidence_path(relative):
    if not isinstance(relative, str) or "\\" in relative or any(part in ("", ".", "..") for part in relative.split("/")):
        raise GovernanceError("Evidence requires a relative Markdown path")
    path = PurePosixPath(relative)
    if path.is_absolute() or path.suffix != ".md" or not path.is_relative_to(PATHS["evidence"]):
        raise GovernanceError("Evidence must be Markdown under " + PATHS["evidence"] + "/")
    if any(not re.fullmatch(r"[a-z0-9][a-z0-9_]*", part) for part in path.parts[:-1]) or not re.fullmatch(r"[a-z0-9][a-z0-9_]*\.md", path.name):
        raise GovernanceError("Use lowercase evidence paths with underscores")
    return path.as_posix()


def validate_evidence_text(text):
    """Require content beyond a title; this does not certify a claim's truth."""
    if not isinstance(text, str) or not any(
        re.search(r"[\w]", line) and not re.match(r"^\s*#{1,6}(?:\s|$)", line)
        for line in text.splitlines()
    ):
        raise GovernanceError("Evidence must contain substantive text beyond headings")
    return text
