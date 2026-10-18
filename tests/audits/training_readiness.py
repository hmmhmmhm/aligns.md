"""Describe exporter behavior with invented fixtures; never collect or train."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/align/scripts/export_training_data.py"
SPEC = importlib.util.spec_from_file_location("exporter", SCRIPT)
EXPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORTER)


def record(identifier="fixture-1"):
    # The observed flag exercises that export path. All content here is fictional.
    return {
        "schema_version": 1, "id": identifier, "group_id": "fixture-task",
        "recorded_at": "2026-10-18T00:00:00Z", "scope": "team:fixture",
        "criteria_version": "v1", "source_refs": ["fixture:only"],
        "origin": "observed", "confirmation": "Invented reviewer accepted this target.",
        "verification": "No code was executed in this fictional example.",
        "status": "reviewed", "privacy_reviewed": True,
        "training": {
            "prompt": [{"role": "user", "content": "Implement the fixture change."}],
            "chosen": [{"role": "assistant", "content": "Make the focused change."}],
            "rejected": [{"role": "assistant", "content": "Rewrite the whole application."}],
            "target_confirmed": True, "pair_confirmed": True, "same_context": True,
        },
    }


PLAN = {
    "schema_version": 1, "current_criteria": {"team:fixture": "v1"},
    "groups": {"fixture-task": "train", "fixture-eval": "eval"},
    "include_origins": ["observed"],
}


def run():
    cases = []

    def probe(name, records, inspect=None):
        try:
            output, manifest = EXPORTER.prepare(records, PLAN)
            cases.append({"case": name, "outcome": "exported",
                          "counts": manifest["counts"],
                          "observation": inspect(output) if inspect else None})
        except ValueError as error:
            cases.append({"case": name, "outcome": "rejected", "reason": str(error)})

    probe("text_format", [record()], lambda out: {
        "sft_fields": sorted(out["sft"][0]), "dpo_fields": sorted(out["dpo"][0])})

    context = record()
    context["context"] = "fixture-critical-constraint: preserve the public API"
    probe("context_only_in_evidence", [context], lambda out: {
        "constraint_present_in_trainer_rows": "fixture-critical-constraint" in json.dumps(out)})

    history = record()
    history["training"]["prompt"] = [
        {"role": "user", "content": "Implement the fixture change."},
        {"role": "assistant", "content": "fixture-bad-earlier-turn: rewrite everything."},
        {"role": "user", "content": "Keep the change focused."},
    ]
    probe("bad_assistant_history", [history], lambda out: {
        "bad_turn_present_in_sft": any("fixture-bad-earlier-turn" in m["content"]
                                       for m in out["sft"][0]["messages"]),
        "explicit_target_mask_present": any("mask" in k for k in out["sft"][0]),
    })

    inverse = record("fixture-2")
    inverse["training"]["chosen"], inverse["training"]["rejected"] = (
        inverse["training"]["rejected"], inverse["training"]["chosen"])
    probe("opposite_preferences_same_context", [record(), inverse])

    unchecked = record()
    unchecked.update(verification="Not run; code correctness unknown.",
                     recorded_at="not-a-timestamp")
    probe("unverified_code_and_invalid_timestamp", [unchecked])

    probe("no_submission_or_team_review_file", [record()])

    tools = record()
    tools["training"]["chosen"][0]["tool_calls"] = [{"function": {"name": "test"}}]
    probe("tool_call_target", [tools])

    overlap = record("fixture-eval-1")
    overlap["group_id"] = "fixture-eval"
    probe("exact_prompt_across_splits", [record(), overlap])
    paraphrase = copy.deepcopy(overlap)
    paraphrase["training"]["prompt"][0]["content"] = "Please implement the fixture change."
    probe("related_prompt_different_family", [record(), paraphrase])

    candidate = record()
    candidate["status"] = "candidate"
    probe("unreviewed_candidate", [candidate])

    return {
        "schema_version": 1,
        "purpose": "Offline contract audit, not a training or performance benchmark.",
        "fixtures": "Entirely invented; observed flags exercise exporter branches only.",
        "exporter_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cases": cases,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
