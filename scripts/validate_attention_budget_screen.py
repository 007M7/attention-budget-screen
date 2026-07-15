#!/usr/bin/env python3
"""Mechanical validator for Attention Budget Screen v0.1 artifacts."""

import argparse
import json
import sys
from pathlib import Path

SCHEMA_VERSION = "0.1"
MODES = {"full_workflow", "content_quality_only", "attention_only"}
WORKFLOW_DECISIONS = {
    "quick_read_now",
    "read_deep_now",
    "project_relevant_but_not_now",
    "reference_only",
    "defer_or_monitor",
    "do_not_invest_further_now",
    "pending_context",
    "quality_screen_only",
}
TRIAGE_DECISIONS = WORKFLOW_DECISIONS - {"quality_screen_only"}
CONTENT_STATUS = {"evaluated", "indeterminate", "not_run"}
ATTENTION_STATUS = {"evaluated", "indeterminate", "not_run"}
COVERAGE = {"metadata_only", "sampled_content", "full_content", "other"}
ATTENTION_COVERAGE = {"metadata_only", "abstract_and_toc", "sampled_sections", "other"}
RISKS = {"low", "medium", "high", "indeterminate", "not_run"}
RATINGS = {"strong", "mixed", "weak", "unknown", "not_run"}
ORDINAL = {"low", "medium", "high", "unknown"}
CONFIDENCE = {"low", "medium", "high"}
SIGNALS = {
    "concrete_takeaway",
    "source_specificity",
    "author_footprint",
    "cognitive_progress",
}
REQUIRED_TOP_LEVEL = {
    "schema_version",
    "mode",
    "source",
    "workflow_decision",
    "content_quality",
    "attention_gate",
    "uncertainty",
    "not_inferred",
    "recommended_next_gate",
    "writeback_status",
}
FORBIDDEN_KEYS = {
    "ai_generated",
    "truth_score",
    "author_intent",
    "automatic_action",
    "telemetry",
    "upload_source",
    "durable_writeback",
    "install_skill",
    "project_route",
}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def report(status, errors=None, warnings=None):
    return {
        "status": status,
        "schema_version": SCHEMA_VERSION,
        "errors": errors or [],
        "warnings": warnings or [],
    }


def validate_source(source, errors):
    if not isinstance(source, dict):
        errors.append("source must be an object")
        return
    for key in ("title", "path_or_url", "source_type", "sensitivity"):
        if not nonempty(source.get(key)):
            errors.append(f"source.{key} must be a nonempty string")


def validate_content(content, errors):
    if not isinstance(content, dict):
        errors.append("content_quality must be an object")
        return
    status = content.get("status")
    if status not in CONTENT_STATUS:
        errors.append("content_quality.status is invalid")
    if content.get("slop_risk") not in RISKS:
        errors.append("content_quality.slop_risk is invalid")
    if content.get("input_coverage") not in COVERAGE:
        errors.append("content_quality.input_coverage is invalid")
    inspected = content.get("inspected_sections")
    if not isinstance(inspected, list) or not all(nonempty(x) for x in inspected):
        errors.append("content_quality.inspected_sections must be a list of nonempty strings")
    elif content.get("input_coverage") != "metadata_only" and not inspected:
        errors.append("content_quality.inspected_sections must be nonempty unless metadata_only")
    if not nonempty(content.get("basis")):
        errors.append("content_quality.basis must be nonempty")

    signals = content.get("signals")
    if not isinstance(signals, dict):
        errors.append("content_quality.signals must be an object")
        return
    missing = sorted(SIGNALS - set(signals))
    extra = sorted(set(signals) - SIGNALS)
    if missing:
        errors.append("missing content signals: " + ", ".join(missing))
    if extra:
        errors.append("unsupported content signals: " + ", ".join(extra))
    for name in SIGNALS.intersection(signals):
        item = signals[name]
        if not isinstance(item, dict):
            errors.append(f"content_quality.signals.{name} must be an object")
            continue
        if item.get("rating") not in RATINGS:
            errors.append(f"content_quality.signals.{name}.rating is invalid")
        if not nonempty(item.get("evidence")):
            errors.append(f"content_quality.signals.{name}.evidence must be nonempty")
        if item.get("confidence") not in CONFIDENCE:
            errors.append(f"content_quality.signals.{name}.confidence is invalid")
    if status == "not_run":
        if content.get("slop_risk") != "not_run":
            errors.append("content_quality.not_run requires slop_risk=not_run")
        for name in SIGNALS.intersection(signals):
            if signals[name].get("rating") != "not_run":
                errors.append("content_quality.not_run requires all signal ratings=not_run")
    elif content.get("slop_risk") == "not_run":
        errors.append("content_quality evaluated/indeterminate cannot use slop_risk=not_run")


def validate_attention(attention, errors):
    if not isinstance(attention, dict):
        errors.append("attention_gate must be an object")
        return
    status = attention.get("status")
    if status not in ATTENTION_STATUS:
        errors.append("attention_gate.status is invalid")
    decision = attention.get("triage_decision")
    if decision not in TRIAGE_DECISIONS | {"not_run"}:
        errors.append("attention_gate.triage_decision is invalid")
    for key in ("basis", "fit_target", "uncertainty", "not_inferred", "revisit_trigger", "recommended_next_gate"):
        if not nonempty(attention.get(key)):
            errors.append(f"attention_gate.{key} must be nonempty")
    if attention.get("input_coverage") not in ATTENTION_COVERAGE:
        errors.append("attention_gate.input_coverage is invalid")
    inspected = attention.get("inspected_sections")
    if not isinstance(inspected, list) or not all(nonempty(x) for x in inspected):
        errors.append("attention_gate.inspected_sections must be a list of nonempty strings")
    elif attention.get("input_coverage") != "metadata_only" and not inspected:
        errors.append("attention_gate.inspected_sections must be nonempty unless metadata_only")
    for key in ("expected_deep_read_cost", "expected_decision_impact", "expected_attention_saved"):
        if attention.get(key) not in ORDINAL:
            errors.append(f"attention_gate.{key} is invalid")
    if attention.get("confidence") not in CONFIDENCE:
        errors.append("attention_gate.confidence is invalid")
    if status == "not_run" and decision != "not_run":
        errors.append("attention_gate.not_run requires triage_decision=not_run")
    if status != "not_run" and decision == "not_run":
        errors.append("attention_gate evaluated/indeterminate cannot use triage_decision=not_run")


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return report("invalid", ["root must be a JSON object"])
    forbidden = sorted(FORBIDDEN_KEYS.intersection(data))
    if forbidden:
        errors.append("forbidden top-level keys: " + ", ".join(forbidden))
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append("missing required keys: " + ", ".join(missing))
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("unsupported schema_version: expected 0.1")
    mode = data.get("mode")
    if mode not in MODES:
        errors.append("mode is invalid")
    decision = data.get("workflow_decision")
    if decision not in WORKFLOW_DECISIONS:
        errors.append("workflow_decision is invalid")
    validate_source(data.get("source"), errors)
    validate_content(data.get("content_quality"), errors)
    validate_attention(data.get("attention_gate"), errors)
    for key in ("uncertainty", "not_inferred", "recommended_next_gate"):
        if not nonempty(data.get(key)):
            errors.append(f"{key} must be nonempty")
    if data.get("writeback_status") != "none":
        errors.append("writeback_status must be none")

    content = data.get("content_quality") if isinstance(data.get("content_quality"), dict) else {}
    attention = data.get("attention_gate") if isinstance(data.get("attention_gate"), dict) else {}
    c_status = content.get("status")
    a_status = attention.get("status")
    a_decision = attention.get("triage_decision")
    if mode == "full_workflow":
        if c_status == "not_run" or a_status == "not_run":
            errors.append("full_workflow requires both stages to run or be indeterminate")
        if decision != a_decision:
            errors.append("full_workflow.workflow_decision must equal attention_gate.triage_decision")
    elif mode == "content_quality_only":
        if a_status != "not_run":
            errors.append("content_quality_only requires attention_gate.status=not_run")
        if decision != "quality_screen_only":
            errors.append("content_quality_only.workflow_decision must be quality_screen_only")
    elif mode == "attention_only":
        if c_status != "not_run":
            errors.append("attention_only requires content_quality.status=not_run")
        if decision != a_decision:
            errors.append("attention_only.workflow_decision must equal attention_gate.triage_decision")
    if errors:
        return report("invalid", errors)
    return report("valid")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate Attention Budget Screen v0.1 artifacts")
    parser.add_argument("artifact", help="path to a JSON artifact")
    args = parser.parse_args(argv)
    try:
        with Path(args.artifact).open("r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps(report("usage_or_io_error", [str(exc)]), ensure_ascii=False))
        return 1
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "valid" else 2


if __name__ == "__main__":
    sys.exit(main())
