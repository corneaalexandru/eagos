#!/usr/bin/env python3
"""Optional EAGOS Discovery / ODS 1.3 helpers: preview/create a portfolio or check recorded integrity.

Python 3.9+, standard library only. No network, research, ranking, or approvals.
Only init --apply writes, exclusively into a new destination.
"""

import argparse
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("eagos_core", PACKAGE / "20_tools/00_eagos.py")
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)
VERSION = "1.3.0"
EXTENSION = "EAGOS-ODS"
SUPPORTED_WORKSPACE_VERSIONS = {"1.0.0", "1.1.0", "1.1.1", "1.2.0", "1.3.0"}
WORKSPACE = "00_opportunity_workspace.md"
MANIFEST = "00_discovery_manifest.json"
TRACKS = {"commercial", "strategic_creative", "internal_tool"}
CRITERIA = {"problem_value", "access_adoption", "value_efficiency", "capability_advantage",
            "delivery_feasibility", "learning_speed", "commitment_fit", "compounding_value"}
KINDS = {"cycle": "CYC", "source": "SRC", "signal": "SIG", "candidate": "OPP", "claim": "CLM",
         "screen": "SCR", "assessment": "ASM", "experiment": "EXP", "decision": "DEC", "handover": "HND"}
REQUIRED = {
    "cycle": "status scope authority started_on query_limit source_limit candidate_limit investigation_limit minutes_limit queries_used sources_used minutes_used investigated_candidates stop_reason result",
    "source": "title kind status location origin published_on inspected_on independence_group finding locator limitations",
    "signal": "source_ids lens observation interpretation",
    "candidate": "cycle_id track status title beneficiary problem situation consequence alternatives mechanism access_route value_model signal_ids critical_unknown next_action validation_slot",
    "claim": "candidate_id claim context status evidence_level supporting_sources opposing_sources decision_context rationale limitations review_on",
    "screen": "candidate_id constraint result scope reason basis",
    "assessment": "candidate_id profile criterion low high claim_ids rationale",
    "experiment": "candidate_id status hypothesis decision_changed inputs_or_participants method measurement success failure inconclusive resources data_and_privacy authority_required stop_condition",
    "decision": "status outcome candidate_ids date approver authorization_evidence target_stage objective scope exclusions resources conditions review_trigger",
    "handover": "candidate_id decision_id status target_stage claim_ids remaining_hypotheses risks success failure first_activity next_gate execution_state receiver accepted_on acceptance_evidence",
}
STATES = {
    "cycle": {"planned", "in-progress", "complete", "paused"},
    "source": {"inspected", "partial", "unavailable"},
    "candidate": {"framed", "screened", "investigating", "compared", "recommended", "selected", "promoted", "parked", "rejected", "merged"},
    "claim": {"unknown", "supported", "disputed", "refuted", "stale"},
    "experiment": {"proposed"},
    "decision": {"proposed", "approved", "rejected", "superseded"},
    "handover": {"draft", "ready_for_review", "transferred", "accepted", "accepted_with_conditions", "rejected", "expired"},
}
LIMITS = ("query", "source", "candidate", "investigation", "minutes")


def unknown(value):
    return value is None or value == [] or (isinstance(value, str) and
        (value.strip().lower() in {"", "unknown", "tbd", "pending"} or bool(core.PLACEHOLDER.search(value))))


def blocks(text):
    """Read exact discovery fences; ignore other code, including nested examples."""
    records, issues, fence, start, body, collecting = [], [], None, 0, [], False
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if match and fence is None:
            fence, start = match.group(1), number
            collecting, body = match.group(2).strip() == "discovery", []
        elif match and fence and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence) and not match.group(2).strip():
            if collecting:
                data, _, errors = core.properties("---\n" + "\n".join(body) + "\n---\n")
                issues.extend((start, "record_syntax", e) for e in errors)
                records.append((start, data))
            fence, collecting = None, False
        elif collecting:
            body.append(line)
    if fence:
        issues.append((start, "fence", "Unclosed code fence"))
    return records, issues


def init_portfolio(destination, code, name, owner, apply=False, package=PACKAGE):
    if not re.fullmatch(r"[A-Z][A-Z0-9-]{1,19}", code):
        raise ValueError("Code must be 2-20 uppercase letters/digits/hyphens, starting with a letter")
    name, owner = core.validate_text(name, "Name"), core.validate_text(owner, "Owner")
    destination = Path(os.path.abspath(destination))
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError("Destination must not contain symlink components")
    if destination.exists():
        raise ValueError("Destination already exists; initialization never overlays records")
    if not destination.parent.is_dir():
        raise ValueError("Destination parent must already exist")
    starter = package / "11_opportunity_discovery_starter"
    sources = sorted(core.files(starter))
    if not sources or not (starter / WORKSPACE).is_file():
        raise ValueError("Discovery starter is missing")
    values = {"PROJECT_CODE": code, "PROJECT_NAME": name, "PROJECT_OWNER": owner,
              "YYYY-MM-DD": dt.date.today().isoformat()}
    contents, hashes = {}, {}
    for source in sources:
        if source.is_symlink() or not core.inside(source, starter):
            raise ValueError("Invalid starter source")
        relative = source.relative_to(starter).as_posix()
        original = source.read_bytes()
        contents[relative] = core.render(original.decode("utf-8"), values).encode("utf-8")
        hashes[relative] = core.digest(original)
    manifest = {"schema_version": 1, "extension": EXTENSION, "extension_version": VERSION, "framework_version": core.VERSION,
                "source_hashes": hashes, "baseline_hashes": {p: core.digest(v) for p, v in contents.items()},
                "source_paths": {p: "11_opportunity_discovery_starter/" + p for p in contents}}
    contents[MANIFEST] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if apply:
        destination.mkdir(exist_ok=False)
        for relative, data in sorted(contents.items()):
            path = destination / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
    return {"action": "created" if apply else "preview", "destination": str(destination),
            "files": sorted(contents), "authority": "No research, selection, promotion, or project activation granted"}


def check(root, today=None):
    root = Path(os.path.abspath(root))
    path = root / WORKSPACE
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
        raise ValueError("Workspace must be a regular file without symlink components")
    today = today or dt.date.today()
    content = path.read_text(encoding="utf-8")
    header, _, syntax = core.properties(content)
    parsed, parse_issues = blocks(content)
    findings, records, lines = [], {}, {}

    def add(code, message, rid=None, severity="error", line=None):
        findings.append({"severity": severity, "code": code, "record": rid,
                         "line": line or lines.get(rid, 1), "message": message})

    def need(record, keys, code="incomplete"):
        for key in keys.split():
            value = record.get(key)
            if unknown(value) or (isinstance(value, list) and any(unknown(v) for v in value)):
                add(code, "Unresolved " + key, record.get("id"))

    def enum(record, key, values):
        if record.get(key) not in values:
            add("vocabulary", "Invalid " + key, record.get("id"))

    def refs(record, key, kind, multiple=False, nonempty=False):
        value = record.get(key, [] if multiple else "")
        if multiple and (not isinstance(value, list) or any(not isinstance(v, str) for v in value)):
            add("reference_list", key + " must be a scalar string list", record["id"])
            return []
        values = value if multiple else [value]
        if nonempty and not values:
            add("reference", "Empty " + key, record["id"])
        found = []
        for target in values:
            other = records.get(target) if isinstance(target, str) else None
            if not other or other.get("type") != kind:
                add("reference", "Invalid " + key + " reference: " + str(target), record["id"])
            else:
                found.append(other)
        return found

    def number(record, key, positive=False):
        value = str(record.get(key, ""))
        if not re.fullmatch(r"\d+", value) or (positive and int(value) < 1):
            add("number", key + " must be a " + ("positive" if positive else "nonnegative") + " integer", record.get("id"))
            return None
        return int(value)

    def date(record, key, required=False):
        value = record.get(key)
        if unknown(value):
            if required:
                add("date", "Missing " + key, record["id"])
            return None
        try:
            result = dt.date.fromisoformat(str(value))
            if key in {"started_on", "date", "accepted_on"} and result > today:
                add("future_record", key + " cannot claim a future completed event", record["id"])
            return result
        except ValueError:
            add("date", "Invalid ISO date in " + key, record["id"])
            return None

    for issue in syntax:
        add("frontmatter", issue)
    for line, code, message in parse_issues:
        add(code, message, line=line)
    version, extension = header.get("extension_version"), header.get("extension")
    valid_version = isinstance(version, str) and version in SUPPORTED_WORKSPACE_VERSIONS
    valid_extension = extension is None or (isinstance(extension, str) and extension in {"", EXTENSION, "ELAEF-ODS"})
    if header.get("schema_version") != "1" or not valid_version or not valid_extension:
        add("schema", "Expected workspace schema 1 and ODS " + " or ".join(sorted(SUPPORTED_WORKSPACE_VERSIONS)))
    prefix = header.get("portfolio_code", "")
    if not isinstance(prefix, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]{1,19}", prefix):
        add("identity", "Instantiate the portfolio code before checking")
    for key in ("owner", "write_owner"):
        if unknown(header.get(key)):
            add("identity", "Instantiate " + key)
    filters = header.get("required_filters")
    if not isinstance(filters, list) or not filters or any(not isinstance(v, str) or unknown(v) for v in filters):
        add("filters", "Declare a nonempty required_filters list")
        filters = []
    elif len(filters) != len(set(filters)):
        add("filters", "Duplicate required filter")
    for line, record in parsed:
        rid, kind = record.get("id"), record.get("type")
        if not isinstance(rid, str) or not isinstance(kind, str) or kind not in KINDS or not re.fullmatch(re.escape(str(prefix)) + "-" + KINDS.get(kind, "INVALID") + r"-[A-Za-z0-9_-]+", rid):
            add("record_identity", "Invalid record ID/type/prefix", line=line)
            continue
        if rid in records:
            add("duplicate_id", "Duplicate record ID", rid, line=line)
            continue
        records[rid], lines[rid] = record, line
        for key in REQUIRED[kind].split():
            if key not in record:
                add("field", "Missing field " + key, rid)
        if kind in STATES:
            enum(record, "status", STATES[kind])

    candidates = [r for r in records.values() if r["type"] == "candidate"]
    validation_cap = number(header, "validation_limit", True)
    if validation_cap is not None and sum(c.get("validation_slot") == "open" for c in candidates) > validation_cap:
        add("budget", "Open validation work exceeds the portfolio cap across all cycles")
    screens, assessments = {}, set()
    for rid, r in records.items():
        kind = r["type"]
        if kind in {"claim", "screen", "assessment", "experiment", "handover"}:
            refs(r, "candidate_id", "candidate")
        if kind == "source":
            enum(r, "kind", {"public", "internal", "synthetic", "search_lead"})
            date(r, "published_on")
            inspected = date(r, "inspected_on", required=r.get("status") in {"inspected", "partial"})
            if inspected and inspected > today:
                add("future_evidence", "Inspection date is in the future", rid)
            need(r, "title location origin independence_group limitations")
            if r.get("status") in {"inspected", "partial"}:
                need(r, "finding locator")
        elif kind == "signal":
            refs(r, "source_ids", "source", True, True)
            need(r, "lens observation interpretation")
        elif kind == "cycle":
            caps = {k: number(r, k + "_limit", True) for k in LIMITS}
            for key, used in (("query", "queries_used"), ("source", "sources_used"), ("minutes", "minutes_used")):
                count = number(r, used)
                if count is not None and caps[key] is not None and count > caps[key]:
                    add("budget", used + " exceeds the recorded cap", rid)
            investigated = refs(r, "investigated_candidates", "candidate", True)
            ids = [c["id"] for c in investigated]
            if len(ids) != len(set(ids)):
                add("duplicate_reference", "Duplicate investigation entry", rid)
            if any(c.get("cycle_id") != rid for c in investigated):
                add("cycle_membership", "Investigation belongs to another cycle", rid)
            counts = {"candidate": sum(c.get("cycle_id") == rid for c in candidates),
                      "investigation": len(set(ids))}
            for key, count in counts.items():
                if caps[key] is not None and count > caps[key]:
                    add("budget", key + " count exceeds cap", rid)
            if r.get("status") != "planned":
                need(r, "authority scope")
                date(r, "started_on", True)
            if r.get("status") in {"complete", "paused"}:
                need(r, "stop_reason result")
        elif kind == "screen":
            enum(r, "result", {"pass", "fail", "unknown"})
            key = (r.get("candidate_id"), r.get("constraint"))
            if key in screens:
                add("duplicate_screen", "Duplicate current candidate/constraint screening", rid)
            screens[key] = r
            if r.get("constraint") not in filters:
                add("filters", "Screen constraint is not declared in required_filters", rid)
            need(r, "scope reason")
            if r.get("result") != "unknown":
                need(r, "basis")
        elif kind == "claim":
            enum(r, "context", {"market", "operational", "preparation"})
            enum(r, "evidence_level", {"E0", "E1", "E2", "E3", "E4"})
            support = refs(r, "supporting_sources", "source", True)
            oppose = refs(r, "opposing_sources", "source", True)
            need(r, "claim decision_context rationale")
            if r.get("evidence_level") != "E0":
                usable = [s for s in support + oppose if s.get("status") in {"inspected", "partial"} and s.get("kind") != "search_lead"]
                if r.get("context") != "preparation":
                    usable = [s for s in usable if s.get("kind") != "synthetic"]
                if not usable:
                    add("evidence", "Non-E0 claim needs inspected evidence appropriate to its context", rid)
                if r.get("status") == "supported" and not any(s in usable for s in support):
                    add("evidence", "Supported claim has no usable supporting source", rid)
            review = date(r, "review_on")
            if review and review < today:
                add("stale", "Claim review date has passed", rid, "warning")
            if r.get("evidence_level") in {"E3", "E4"}:
                need(r, "limitations")
                add("evidence_review", "Human review must assess source independence and decision-specific sufficiency", rid, "warning")
        elif kind == "assessment":
            enum(r, "profile", TRACKS)
            enum(r, "criterion", CRITERIA)
            owner = records.get(r.get("candidate_id"), {})
            if r.get("profile") != owner.get("track"):
                add("profile", "Assessment must use the candidate's track", rid)
            key = (r.get("candidate_id"), r.get("criterion"))
            if key in assessments:
                add("duplicate_assessment", "Duplicate candidate/criterion assessment", rid)
            assessments.add(key)
            for claim in refs(r, "claim_ids", "claim", True):
                if claim.get("candidate_id") != r.get("candidate_id"):
                    add("claim_scope", "Assessment references another candidate's claim", rid)
            lo, hi = r.get("low"), r.get("high")
            if (lo == "unknown") != (hi == "unknown"):
                add("rating", "Both endpoints must be unknown together", rid)
            elif lo != "unknown":
                if not re.fullmatch(r"[1-5](?:\.\d+)?", str(lo)) or not re.fullmatch(r"[1-5](?:\.\d+)?", str(hi)) or not 1 <= float(lo) <= float(hi) <= 5:
                    add("rating", "Rating must be unknown or a valid 1-5 interval", rid)
            need(r, "rationale")
        elif kind == "decision":
            enum(r, "outcome", {"select", "park", "reject", "defer", "no_new_commitment", "strengthen_existing"})
            selected = refs(r, "candidate_ids", "candidate", True)
            refs_list = r.get("authorization_evidence")
            if not isinstance(refs_list, list) or any(not isinstance(v, str) for v in refs_list):
                add("reference_list", "authorization_evidence must be a string list", rid)
            date(r, "date", required=r.get("status") == "approved")
            expiry = date(r, "expires_on")
            if r.get("status") == "approved":
                need(r, "approver authorization_evidence review_trigger", "authorization")
                if r.get("outcome") == "select":
                    if len(selected) != 1:
                        add("selection", "Selection must identify exactly one candidate", rid)
                    enum(r, "target_stage", {"DEFINE", "DISCOVER", "VALIDATE"})
                    need(r, "objective scope exclusions resources conditions", "authorization")
                    if r.get("target_stage") == "VALIDATE" and any(c.get("validation_slot") not in {"open", "closed"} for c in selected):
                        add("validation_slot", "Approved validation selection needs a tracked open or closed slot", rid)
                if expiry and expiry < today:
                    add("expired_authority", "Approval has expired; do not reuse it", rid)
        elif kind == "handover":
            decisions = refs(r, "decision_id", "decision")
            for claim in refs(r, "claim_ids", "claim", True):
                if claim.get("candidate_id") != r.get("candidate_id"):
                    add("claim_scope", "Handover references another candidate's claim", rid)
            if r.get("status") in {"ready_for_review", "transferred", "accepted", "accepted_with_conditions"}:
                need(r, "target_stage remaining_hypotheses risks success failure first_activity next_gate execution_state", "handover")
                if not decisions or decisions[0].get("status") != "approved" or decisions[0].get("outcome") != "select" or decisions[0].get("candidate_ids") != [r.get("candidate_id")] or decisions[0].get("target_stage") != r.get("target_stage"):
                    add("handover", "Handover needs a matching approved selection and stage", rid)
            if not isinstance(r.get("acceptance_evidence"), list) or any(not isinstance(v, str) for v in r.get("acceptance_evidence", [])):
                add("reference_list", "acceptance_evidence must be a string list", rid)
            if r.get("status") in {"accepted", "accepted_with_conditions"}:
                need(r, "receiver acceptance_evidence", "acceptance")
                date(r, "accepted_on", True)
                if r.get("status") == "accepted_with_conditions":
                    need(r, "conditions permitted_work", "acceptance")

    for c in candidates:
        rid, state = c["id"], c.get("status")
        enum(c, "track", TRACKS)
        enum(c, "validation_slot", {"none", "open", "closed"})
        cycles = refs(c, "cycle_id", "cycle")
        refs(c, "signal_ids", "signal", True)
        need(c, "title next_action")
        if state in {"parked", "rejected"}:
            need(c, "reason reopen_trigger")
        if state == "merged":
            targets = refs(c, "merged_into", "candidate")
            visited, current = {rid}, targets[0] if targets else None
            while current:
                if current["id"] in visited:
                    add("merge_cycle", "Candidate merge cycle", rid)
                    break
                visited.add(current["id"])
                current = records.get(current.get("merged_into"))
        if state in {"screened", "investigating", "compared", "recommended", "selected", "promoted"}:
            need(c, "beneficiary problem situation consequence alternatives mechanism access_route value_model critical_unknown")
            for constraint in filters:
                screen = screens.get((rid, constraint))
                if not screen or screen.get("result") == "fail" or (state in {"selected", "promoted"} and screen.get("result") != "pass"):
                    add("screening", "Required constraint unresolved or failed: " + constraint, rid)
        if state in {"investigating", "compared", "recommended", "selected", "promoted"} and cycles:
            members = cycles[0].get("investigated_candidates")
            if not isinstance(members, list) or rid not in members:
                add("investigation_tracking", "Add candidate to cumulative investigated_candidates", rid)
        if c.get("validation_slot") == "closed":
            need(c, "validation_completion_evidence")
        if state in {"selected", "promoted"} or c.get("validation_slot") == "open":
            decision = refs(c, "selection_decision", "decision")
            d = decision[0] if decision else {}
            if d.get("status") != "approved" or d.get("outcome") != "select" or d.get("candidate_ids") != [rid]:
                add("selection", "Candidate lacks a matching approved selection", rid)
            if d.get("target_stage") == "VALIDATE" and c.get("validation_slot") == "none":
                add("validation_slot", "Selected validation work must occupy a slot until verified closure", rid)
            if c.get("validation_slot") == "open" and d.get("target_stage") != "VALIDATE":
                add("validation_slot", "Open validation slot must reference a VALIDATE selection", rid)
        if state == "promoted":
            handovers = refs(c, "handover_id", "handover")
            h = handovers[0] if handovers else {}
            if h.get("status") not in {"accepted", "accepted_with_conditions"} or h.get("candidate_id") != rid or h.get("decision_id") != c.get("selection_decision"):
                add("promotion", "Promotion requires a matching accepted receiving-project handover", rid)

    active = [r for r in records.values() if r["type"] == "cycle" and r.get("status") == "in-progress"]
    if len(active) > 1:
        add("active_cycles", "Use one active cycle per authoritative workspace")
    errors = sum(f["severity"] == "error" for f in findings)
    return {"extension_version": VERSION, "records": len(records), "errors": errors,
            "warnings": len(findings) - errors, "findings": findings,
            "limits": "Recorded structural integrity only. No source truth, scoring, actual tool-budget enforcement, permission identity, project activation, or receiver acceptance is verified. Prose, search logs, and complete economic/experiment methodology require review."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("init", help="Preview a new portfolio; --apply creates it")
    create.add_argument("destination", type=Path)
    create.add_argument("--code", required=True)
    create.add_argument("--name", required=True)
    create.add_argument("--owner", required=True)
    create.add_argument("--apply", action="store_true")
    validate = commands.add_parser("check", help="Read-only checks on the authoritative workspace")
    validate.add_argument("root", type=Path)
    validate.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_portfolio(args.destination, args.code, args.name, args.owner, args.apply)
        else:
            result = check(args.root)
            if args.format == "text":
                print("ODS: {errors} error(s), {warnings} warning(s), {records} records".format(**result))
                for f in result["findings"]:
                    print("{severity}: line {line}: [{code}] {record}: {message}".format(**f))
                print(result["limits"])
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            return int(bool(result["errors"]))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, RecursionError) as error:
        print("ODS: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
