#!/usr/bin/env python3
"""Optional, offline EAGOS helpers (maintained module path). Python 3.9+, standard library only.

Only `init --apply` writes files, exclusively into a new directory.
Checks are structural diagnostics, never activation or approval decisions.
"""

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

VERSION = "4.0.0"
LIFECYCLE_STAGES = {"discover", "shape", "incubate", "develop", "launch", "operate", "evolve"}
PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST = "00_eagos_manifest.json"
LEGACY_MANIFEST = "00_elaef_manifest.json"
PLACEHOLDER = re.compile(r"\{\{[^{}\n]+\}\}")
RESERVED = {"README.md", "AGENTS.md", "CHANGELOG.md"}
REUSABLE = {"60_templates", "70_profiles"}
PRIVATE = {"80_private", "10_raw"}
RECORD_ID = re.compile(r"[A-Z][A-Z0-9_-]*-(?:ACT|EVD|DEC|GAT|RSK|HND|CLM|ASM|HYP|OPN|OUT|CHG|CTL|PRJ|ROLE|DLG|RUN|PRC|ATT)-[A-Za-z0-9_-]+")
STATES = {
    "task": {"proposed", "not-started", "ready", "in-progress", "complete", "awaiting-evidence", "awaiting-user", "awaiting-decision", "blocked", "cancelled"},
    "gate": {"not_assessed", "not-assessed", "assessment-ready", "passed", "conditionally-passed", "failed", "deferred", "expired"},
    "decision": {"proposed", "pending", "approved", "rejected", "deferred", "superseded"},
    "handover": {"draft", "ready_for_review", "transferred", "accepted", "accepted_with_conditions", "rejected", "superseded", "expired"},
}
STATES["activity"] = STATES["task"]  # Legacy record type remains valid.
GOVERNANCE_SPEC = importlib.util.spec_from_file_location("eagos_governance", Path(__file__).with_name("03_governance.py"))
governance = importlib.util.module_from_spec(GOVERNANCE_SPEC)
GOVERNANCE_SPEC.loader.exec_module(governance)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inside(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def resolved_string(value):
    return isinstance(value, str) and value.strip().lower() not in {"", "unknown", "tbd", "pending", "not_selected"} and not PLACEHOLDER.search(value)


def resolved_list(value):
    return isinstance(value, list) and bool(value) and all(resolved_string(v) for v in value)


def readable(path, root):
    """Check the unresolved path before reading any checked-project body."""
    path = Path(os.path.abspath(path))
    root = Path(os.path.abspath(root))
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    if any(p.is_symlink() for p in (path, *path.parents)):
        return False
    if any(part.startswith(".") or part in {"__pycache__", "node_modules"} for part in parts):
        return False
    if any(part in PRIVATE for part in parts[:-1]):
        return path.name.startswith("00_") and path.name.endswith("_index.md")
    return True


def files(root):
    """No symlink traversal, hidden trees, private content, or raw source reads."""
    for directory, dirs, names in os.walk(root, followlinks=False):
        current = Path(directory)
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not (current / d).is_symlink() and d not in {"__pycache__", "node_modules"})
        if any(part in PRIVATE for part in current.relative_to(root).parts):
            dirs[:] = []
            names = [n for n in names if n.startswith("00_") and n.endswith("_index.md")]
        for name in sorted(names):
            path = current / name
            if readable(path, root):
                yield path


def scalar(value):
    value = value.strip()
    if not value or value in {"null", "~"}:
        return ""
    if value.startswith('"') or value.startswith("["):
        return json.loads(value)
    if value.startswith("'"):
        if not value.endswith("'") or len(value) < 2:
            raise ValueError("Unclosed quoted scalar")
        return value[1:-1].replace("''", "'")
    return value.split(" #", 1)[0]


def properties(text):
    """Parse only the documented flat scalar / scalar-list frontmatter subset."""
    if not text.startswith("---\n"):
        return {}, text, []
    lines = text.splitlines()
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, text, ["Unclosed frontmatter"]
    data, issues, last = {}, [], None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*):(?:\s+(.*))?", line)
        item = re.fullmatch(r"\s+- (.*)", line)
        try:
            if match:
                key, value = match.group(1), match.group(2) or ""
                if key in data:
                    issues.append("Duplicate property: " + key)
                data[key] = scalar(value)
                if isinstance(data[key], (dict, list)) and (not isinstance(data[key], list) or any(isinstance(v, (dict, list)) for v in data[key])):
                    issues.append("Unsupported nested property: " + key)
                if value in {"|", ">", "|-", ">-"} or value.startswith(("&", "*", "!", "{")):
                    issues.append("Unsupported YAML form: " + key)
                last = key
            elif item and last:
                if data[last] == "":
                    data[last] = []
                if not isinstance(data[last], list):
                    raise ValueError("List item after scalar")
                data[last].append(scalar(item.group(1)))
            else:
                issues.append("Unsupported frontmatter line: " + line.strip())
        except (ValueError, TypeError) as error:
            issues.append(str(error))
    return data, "\n".join(lines[end + 1:]), issues


def prose(text):
    """Remove fenced/inline code before scanning links and headings."""
    result, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not match.group(2).strip():
                fence = None
            result.append("")
        elif fence is None:
            result.append(re.sub(r"(`+).*?\1", "", line))
        else:
            result.append("")
    return "\n".join(result), fence is not None


def slug(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[\[([^]|]+)\|([^]]+)\]\]", r"\2", value)
    return re.sub(r"[^\w\s-]", "", value.lower()).replace(" ", "-")


def anchor_exists(path, anchor):
    text, _ = prose(properties(path.read_text(encoding="utf-8"))[1])
    if anchor.startswith("^"):
        return bool(re.search(r"\^" + re.escape(anchor[1:]) + r"\s*$", text, re.M))
    found, counts = set(), {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        base = slug(heading)
        count = counts.get(base, 0)
        counts[base] = count + 1
        found.add(base if count == 0 else base + "-" + str(count))
        found.add(heading)
    return anchor in found or slug(anchor) in found


def links(text):
    for match in re.finditer(r"!?\[\[([^]\n]+)\]\]", text):
        yield match.group(1).split("|", 1)[0], True
    # Common inline Markdown destinations; complex reference-style links need manual review.
    for match in re.finditer(r"!?\[[^]\n]*\]\((<[^>\n]+>|[^\s)]+)(?:\s+[\"'][^\n]*?[\"'])?\)", text):
        yield match.group(1).strip("<>"), False


def link_issue(root, source, target, wiki, all_files):
    if PLACEHOLDER.search(target):
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None  # No network access; external availability is not tested.
    location, anchor = unquote(parsed.path), unquote(parsed.fragment)
    if not location:
        candidates = [source]
    elif wiki:
        part = Path(location if Path(location).suffix else location + ".md")
        candidates = [p for p in (source.parent / part, root / part) if p.is_file()]
        if not candidates and not location.startswith("."):
            candidates = [p for p in all_files if p.relative_to(root).as_posix().endswith(part.as_posix())]
    else:
        candidates = [source.parent / location]
    body_allowed = any(readable(p, root) for p in candidates)
    candidates = list({p.resolve() for p in candidates})
    if not candidates or not any(p.exists() for p in candidates):
        return "Missing link target: " + target
    if len(candidates) > 1:
        return "Ambiguous Wikilink: " + target
    path = candidates[0]
    if not inside(path, root):
        return "Link leaves the checked project; verify manually: " + target
    if anchor and body_allowed and readable(path, root) and path.suffix == ".md":
        if not anchor_exists(path, anchor):
            return "Missing heading or block: " + target
    return None


def normalized_gate_state(value):
    """Compare legacy/current initial states without changing stored records."""
    return "not_assessed" if value == "not-assessed" else value


def check(root, mode="setup", today=None):
    root = Path(os.path.abspath(root))
    if any(p.is_symlink() for p in (root, *root.parents)):
        raise ValueError("Project root must not contain symlink components")
    if not root.is_dir():
        raise ValueError("Project directory does not exist")
    today = today or dt.date.today()
    findings, records = [], {}
    all_files = list(files(root))

    def add(level, path, code, message):
        findings.append({"severity": level, "path": path.relative_to(root).as_posix(), "code": code, "message": message})

    if not (root / "README.md").is_file() or not readable(root / "README.md", root):
        add("error", root / "README.md", "entrypoint", "Missing or excluded project hub")
    hub, _, _ = properties((root / "README.md").read_text(encoding="utf-8")) if (root / "README.md").is_file() and readable(root / "README.md", root) else ({}, "", [])
    profile = hub.get("conformance_profile", "unknown")
    if mode != "template" and profile not in {"P0", "P1", "P2"}:
        add("error", root / "README.md", "profile", "Declare P0, P1, or P2 in the hub")
    required = ["AGENTS.md"]
    if profile in {"P1", "P2"} or mode == "template":
        required += ["00_control/" + n for n in ("00_project_charter.md", "01_project_state.md", "02_project_activation.md", "03_execution_plan.md", "04_evidence_register.md", "05_decision_log.md", "06_risk_register.md", "07_gate_register.md", "08_change_log.md")]
        required += ["50_handover/01_reference_map.md", "50_handover/02_current_handover.md"]
    for name in required:
        if not (root / name).is_file() or not readable(root / name, root):
            add("warning", root / name, "authority_map", "Baseline record absent; a documented consolidation may be valid")
    seen_names, directories = {}, set()
    for path in all_files:
        relative = path.relative_to(root)
        folded = relative.as_posix().casefold()
        if folded in seen_names:
            add("error", path, "case_collision", "Case-insensitive collision with " + seen_names[folded])
        seen_names[folded] = relative.as_posix()
        directories.update(relative.parents)
        reusable = bool(set(relative.parts) & REUSABLE)
        if path.suffix != ".md":
            continue
        if path.name not in RESERVED and not re.fullmatch(r"(?:\d{2}|\d{4})_[a-z0-9_]+\.md", path.name):
            add("warning", path, "filename", "Numbered Markdown naming differs; document any tool/source exception")
        content = path.read_text(encoding="utf-8")
        data, body, syntax = properties(content)
        for issue in syntax:
            add("error", path, "frontmatter_subset", issue + "; use flat scalar/list properties or a full YAML validator")
        clean, unclosed = prose(body)
        if unclosed:
            add("error", path, "fence", "Unclosed Markdown code fence")
        for target, wiki in links(clean):
            issue = link_issue(root, path, target, wiki, all_files)
            if issue:
                add("warning" if issue.startswith("Link leaves") else "error", path, "link", issue)
        if mode != "template" and not reusable:
            placeholders = sorted(set(PLACEHOLDER.findall(content)))
            if placeholders:
                add("error" if mode == "active" else "warning", path, "placeholder", ", ".join(placeholders))
        if reusable:
            continue
        malformed = False
        for field in ("id", "type", "status"):
            if field in data and not isinstance(data[field], str):
                add("error", path, "record_scalar", field + " must be a string")
                malformed = True
        if malformed:
            continue
        record_id = data.get("id")
        if record_id:
            if record_id in records:
                add("error", path, "duplicate_id", "Duplicate ID: " + str(record_id))
            records[record_id] = (path, data)
        for heading in re.findall(r"^###\s+(.+)$", clean, re.M):
            match = RECORD_ID.match(heading)
            if match:
                inline_id = match.group(0)
                if inline_id in records:
                    add("error", path, "duplicate_id", "Duplicate definition: " + inline_id)
                records[inline_id] = (path, {})
        if mode == "template":
            continue
        kind, state = data.get("type"), data.get("status")
        if "lifecycle_stage" in data:
            stage = data["lifecycle_stage"]
            if not isinstance(stage, str) or stage not in LIFECYCLE_STAGES:
                add("error", path, "lifecycle_stage", "Use a supported descriptive lifecycle stage; stage never grants authority")
        if isinstance(kind, str) and kind in STATES and (not isinstance(state, str) or state not in STATES[kind]):
            add("error", path, "state", "Unknown " + kind + " state: " + str(state))
        for field in ("predecessors", "successors", "outputs", "validation_evidence", "authorization_evidence", "acceptance_evidence", "conditions"):
            if field in data and (not isinstance(data[field], list) or any(not isinstance(v, str) for v in data[field])):
                add("error", path, "list_field", field + " must be a list of strings")
        if isinstance(data.get("outputs"), list):
            for output in data["outputs"]:
                if not isinstance(output, str):
                    continue
                if not resolved_string(output):
                    add("error", path, "output_link", "Output requires a resolved nonblank locator")
                    continue
                locators = list(links(output)) or [(output, False)]
                for target, wiki in locators:
                    issue = link_issue(root, path, target, wiki, all_files)
                    if issue:
                        add("error", path, "output_link", issue)
        if kind in {"activity", "task"} and state == "complete":
            for field in ("outputs", "validation_evidence"):
                if not resolved_list(data.get(field)):
                    add("error", path, "completion", "Complete Task requires " + field + " in tool-checkable records")
        if (kind == "gate" and state in {"passed", "conditionally-passed"}) or (kind == "decision" and state == "approved"):
            for field in ("approver", "authorization_evidence"):
                if not (resolved_list(data.get(field)) if field == "authorization_evidence" else resolved_string(data.get(field))):
                    add("error", path, "approval", "Approved record requires " + field)
        if kind == "gate" and state == "conditionally-passed":
            if not data.get("conditions") or not data.get("conditions_due"):
                add("error", path, "conditions", "Conditional gate requires conditions and conditions_due; review owner/consequence manually")
        if kind == "handover" and state in {"accepted", "accepted_with_conditions"} and not resolved_list(data.get("acceptance_evidence")):
            add("error", path, "acceptance", "Accepted handover requires acceptance_evidence")
        for field in ("review_on", "expires_on", "conditions_due"):
            date_text = str(data.get(field, ""))
            if not date_text or PLACEHOLDER.search(date_text):
                continue
            try:
                date = dt.date.fromisoformat(date_text)
            except ValueError:
                add("warning", path, "date", field + " is not an ISO date; review its trigger manually")
                continue
            if date < today and state not in {"expired", "superseded", "rejected", "cancelled"}:
                add("error" if field in {"expires_on", "conditions_due"} and state in {"passed", "conditionally-passed"} else "warning", path, "stale", field + " has elapsed: " + date_text)
    for directory in sorted(directories):
        if directory != Path(".") and not re.fullmatch(r"(?:\d{2}|\d{4})_[a-z0-9_]+", directory.name):
            add("warning", root / directory, "folder", "Unnumbered folder; document any tool/source exception")
    graph = {}
    for record_id, (path, data) in records.items():
        predecessors = data.get("predecessors", [])
        graph[record_id] = [v for v in predecessors if isinstance(v, str)] if isinstance(predecessors, list) else []
        for field in ("predecessors", "successors"):
            refs = data.get(field, [])
            if not isinstance(refs, list):
                continue
            for reference in refs:
                if not isinstance(reference, str):
                    continue
                if reference not in records:
                    add("error", path, "dependency", "Unknown " + field + " ID: " + str(reference))
                elif field == "predecessors" and data.get("status") in {"ready", "in-progress"}:
                    previous = records[reference][1].get("status")
                    if previous != "complete":
                        add("warning" if previous is None else "error", path, "readiness", "Predecessor is not structurally verified complete: " + reference)
        if data.get("type") in {"activity", "task"} and data.get("status") in {"ready", "in-progress"} and data.get("gate"):
            gate = data["gate"]
            gate_state = records.get(gate, (None, {}))[1].get("status") if isinstance(gate, str) else None
            if gate_state not in {"passed", "conditionally-passed"}:
                add("error", path, "gate_readiness", "Task's required gate is not passed: " + str(gate))
    visiting, visited = set(), set()

    def visit(record_id):
        if record_id in visiting:
            add("error", records[record_id][0], "dependency_cycle", "Predecessor cycle includes " + record_id)
            return
        if record_id in visited or record_id not in records:
            return
        visiting.add(record_id)
        for predecessor in graph[record_id]:
            visit(predecessor)
        visiting.remove(record_id)
        visited.add(record_id)

    for record_id in graph:
        visit(record_id)
    if mode != "template":
        governance.validate_records(records, add, today, PLACEHOLDER)
    activation = hub.get("activation_status", "not_assessed")
    if mode == "active" and activation not in {"passed", "conditionally-passed"}:
        add("error", root / "README.md", "activation", "Hub does not declare passed or conditionally-passed activation")
    if profile in {"P1", "P2"} and mode != "template":
        gate_path = root / "00_control/02_project_activation.md"
        if gate_path.is_file() and not readable(gate_path, root):
            add("error", gate_path, "activation_conflict", "Activation record is excluded from body reads")
        elif gate_path.is_file():
            gate, _, _ = properties(gate_path.read_text(encoding="utf-8"))
            if normalized_gate_state(activation) != normalized_gate_state(gate.get("status")):
                add("error", gate_path, "activation_conflict", "Hub and activation record states differ")
    return {"tool_version": VERSION, "mode": mode, "profile": profile, "checked_files": len(all_files), "errors": sum(f["severity"] == "error" for f in findings), "warnings": sum(f["severity"] == "warning" for f in findings), "findings": findings, "limits": "Structural diagnostics only. No runtime enforcement, budget metering, approval authentication, gate approval, source-truth validation, access audit, full YAML parsing, prose/table semantics, external-link check, or receiver acceptance. Raw/private content is excluded."}


def validate_text(value, label):
    if not value.strip() or any(ord(c) < 32 for c in value) or PLACEHOLDER.search(value):
        raise ValueError(label + " must be nonempty single-line text without placeholders")
    return value


def render(text, values):
    lines, frontmatter = [], False
    for index, line in enumerate(text.splitlines(keepends=True)):
        if line.strip() == "---" and (index == 0 or frontmatter):
            frontmatter = not frontmatter
        for key, value in values.items():
            token = "{{" + key + "}}"
            if token not in line:
                continue
            if frontmatter and re.search(r':\s*".*"\s*$', line):
                prefix, quoted = line.split(":", 1)
                current = json.loads(quoted.strip())
                line = prefix + ": " + json.dumps(current.replace(token, value), ensure_ascii=False) + "\n"
            else:
                escaped = re.sub(r"([\\`*_[\]<>|#])", r"\\\1", value)
                line = line.replace(token, escaped)
        lines.append(line)
    return "".join(lines)


def init_project(destination, code, name, owner, profile, apply=False, package=PACKAGE):
    if not re.fullmatch(r"[A-Z][A-Z0-9-]{1,19}", code):
        raise ValueError("Code must be 2-20 uppercase letters/digits/hyphens, starting with a letter")
    if profile not in {"P0", "P1", "P2"}:
        raise ValueError("Profile must be P0, P1, or P2")
    name, owner = validate_text(name, "Name"), validate_text(owner, "Owner")
    # Reject symlink components before resolution so an alias cannot redirect writes.
    destination = Path(os.path.abspath(destination))
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError("Destination must not contain symlink components")
    if destination.exists():
        raise ValueError("Destination already exists; initialization never overlays an existing project")
    if not destination.parent.is_dir():
        raise ValueError("Destination parent must already exist")
    starter = package / "10_eagos_project_starter"
    if profile == "P0":
        sources = {"README.md": starter / "70_profiles/03_p0_project.md", "AGENTS.md": starter / "AGENTS.md", "01_operating_guide.md": starter / "01_operating_guide.md", ".gitignore": starter / ".gitignore"}
    else:
        sources = {p.relative_to(starter).as_posix(): p for p in files(starter)}
        sources[".gitignore"] = starter / ".gitignore"
    values = {"PROJECT_CODE": code, "PROJECT_NAME": name, "PROJECT_OWNER": owner, "WRITE_OWNER": owner, "P0_P1_OR_P2": profile, "YYYY-MM-DD": dt.date.today().isoformat()}
    content, source_hashes, source_paths = {}, {}, {}
    for relative, source in sorted(sources.items()):
        if source.is_symlink() or not inside(source, starter):
            raise ValueError("Invalid starter source")
        original = source.read_bytes()
        content[relative] = render(original.decode("utf-8"), values).encode("utf-8")
        source_hashes[relative] = digest(original)
        source_paths[relative] = source.relative_to(package).as_posix()
    manifest = {"schema_version": 1, "framework": "EAGOS", "framework_version": VERSION, "source_paths": source_paths, "source_hashes": source_hashes, "baseline_hashes": {p: digest(data) for p, data in content.items()}}
    content[MANIFEST] = (json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    if apply:
        destination.mkdir(exist_ok=False)
        for relative, data in sorted(content.items()):
            path = destination / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
    return {"action": "created" if apply else "preview", "destination": str(destination), "profile": profile, "files": sorted(content), "activation": "not_assessed", "note": "Only supplied identity/profile values are filled. Remaining project facts and approvals require assessment. Interrupted creation may leave an incomplete directory; inspect it before recovery."}


def safe_relative(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("Invalid manifest path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {"..", ".git"} for p in path.parts) or str(path) != value:
        raise ValueError("Manifest path must be a normalized project-relative path: " + value)
    return path


def drift(root, against=None):
    root = root.resolve()
    manifest_path = root / MANIFEST
    if not manifest_path.exists() and not manifest_path.is_symlink():
        manifest_path = root / LEGACY_MANIFEST
    if manifest_path.is_symlink():
        raise ValueError("Manifest must not be a symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported manifest schema")
    baseline = manifest.get("baseline_hashes")
    if not isinstance(baseline, dict) or not baseline:
        raise ValueError("Manifest has no baseline hashes")
    changes = []
    for relative, old_hash in sorted(baseline.items()):
        safe_relative(relative)
        path = root / relative
        if not inside(path, root) or any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError("Manifest target crosses a symlink or project boundary")
        state = "missing" if not path.is_file() else "unchanged" if digest(path.read_bytes()) == old_hash else "locally_modified"
        item = {"path": relative, "local": state}
        if against:
            source = manifest.get("source_paths", {}).get(relative)
            safe_relative(source)
            candidate = against / source
            if not candidate.exists() and source.startswith("10_elaef_project_starter/"):
                candidate = against / source.replace("10_elaef_project_starter/", "10_eagos_project_starter/", 1)
            if not inside(candidate, against) or candidate.is_symlink():
                raise ValueError("Candidate source leaves release boundary")
            item["upstream"] = "removed" if not candidate.is_file() else "unchanged" if digest(candidate.read_bytes()) == manifest.get("source_hashes", {}).get(relative) else "changed"
            item["review"] = "manual_merge" if state == "locally_modified" and item["upstream"] != "unchanged" else "review" if item["upstream"] != "unchanged" else "none"
        changes.append(item)
    additions = sorted(p.relative_to(root).as_posix() for p in files(root) if p.relative_to(root).as_posix() not in baseline and p.name not in {MANIFEST, LEGACY_MANIFEST})
    upstream_additions = []
    if against:
        known = {value.replace("10_elaef_project_starter/", "10_eagos_project_starter/", 1) for value in manifest.get("source_paths", {}).values()}
        upstream_additions = sorted(p.relative_to(against).as_posix() for p in files(against / "10_eagos_project_starter") if p.relative_to(against).as_posix() not in known)
    return {"framework_version": manifest.get("framework_version"), "files": changes, "new_local_files": additions, "new_upstream_candidates": upstream_additions, "note": "Read-only comparison. Local edits are expected; review changes before migration. Nothing is merged, overwritten, approved, or activated."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("init", help="Preview a new project; --apply creates it")
    create.add_argument("destination", type=Path)
    create.add_argument("--code", required=True)
    create.add_argument("--name", required=True)
    create.add_argument("--owner", required=True)
    create.add_argument("--profile", choices=("P0", "P1", "P2"), default="P0")
    create.add_argument("--apply", action="store_true")
    validate = commands.add_parser("check", help="Read-only structural diagnostics")
    validate.add_argument("root", type=Path)
    validate.add_argument("--mode", choices=("template", "setup", "active"), default="setup")
    validate.add_argument("--format", choices=("text", "json"), default="text")
    validate.add_argument("--fail-on-warnings", action="store_true")
    inventory = commands.add_parser("inventory", help="Read-only file map, excluding raw/private content and hidden trees")
    inventory.add_argument("root", type=Path)
    compare = commands.add_parser("drift", help="Compare an initialized project with its baseline and optional release")
    compare.add_argument("root", type=Path)
    compare.add_argument("--against-release", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_project(args.destination, args.code, args.name, args.owner, args.profile, args.apply)
        elif args.command == "check":
            result = check(args.root, args.mode)
            if args.format == "text":
                print("EAGOS {}: {} error(s), {} warning(s), {} files".format(args.mode, result["errors"], result["warnings"], result["checked_files"]))
                for finding in result["findings"]:
                    print("{severity}: {path}: [{code}] {message}".format(**finding))
                print(result["limits"])
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            return int(bool(result["errors"] or (args.fail_on_warnings and result["warnings"])))
        elif args.command == "inventory":
            if not args.root.is_dir():
                raise ValueError("Inventory root does not exist")
            result = {"files": [p.relative_to(args.root).as_posix() for p in files(args.root)], "note": "Paths only; excluded trees are not inventoried. No records are moved or renamed."}
        else:
            result = drift(args.root, args.against_release)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, RecursionError) as error:
        print("EAGOS: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
