#!/usr/bin/env python3
"""Export reviewed text decision examples. No collection, network or training."""

import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def messages(value, target=False):
    require(isinstance(value, list) and value, "messages must be a nonempty list")
    for message in value:
        require(isinstance(message, dict) and set(message) == {"role", "content"},
                "only text role/content messages are supported")
        require(message["role"] in ("system", "user", "assistant"),
                "unsupported role; tool trajectories need a separate adapter")
        require(isinstance(message["content"], str) and message["content"].strip(),
                "empty or nontext message content")
    if target:
        require(len(value) == 1 and value[0]["role"] == "assistant",
                "a target must contain one assistant message")
    else:
        require(value[-1]["role"] == "user", "a text prompt must end with the user")
    return value


def prepare(records, plan):
    require(isinstance(plan, dict) and plan.get("schema_version") == 1,
            "unsupported export plan")
    current = plan.get("current_criteria")
    groups = plan.get("groups")
    origins = plan.get("include_origins", ["observed"])
    require(isinstance(current, dict) and current and all(
        isinstance(k, str) and k and isinstance(v, str) and v
        for k, v in current.items()), "current_criteria must map scopes to versions")
    require(isinstance(groups, dict) and all(
        isinstance(k, str) and k and v in ("train", "eval") for k, v in groups.items()),
        "groups must map task families to train or eval")
    require(isinstance(origins, list) and origins and all(
        v in ("observed", "hypothetical", "reconstructed") for v in origins),
        "invalid include_origins")
    output = {"sft": [], "dpo": [], "evaluation": []}
    manifest = {"schema_version": 1, "plan": plan, "included": [], "excluded": []}
    seen_ids, prompt_splits, seen_examples = set(), {}, set()

    for record in records:
        require(isinstance(record, dict) and record.get("schema_version") == 1,
                "unsupported record schema")
        identifier = record.get("id")
        require(isinstance(identifier, str) and identifier, "record needs an id")
        require(identifier not in seen_ids, "duplicate record id: " + identifier)
        seen_ids.add(identifier)
        training = record.get("training") or {}
        require(isinstance(training, dict), "training must be an object or null")
        scope = record.get("scope")
        require(isinstance(scope, str) and scope, "record needs a scope")
        reason = None
        if record.get("status") != "reviewed":
            reason = "not_reviewed"
        elif record.get("privacy_reviewed") is not True:
            reason = "privacy_not_reviewed"
        elif scope not in current:
            reason = "scope_not_selected"
        elif record.get("criteria_version") != current[scope]:
            reason = "stale_criteria"
        elif record.get("origin") not in origins:
            reason = "origin_not_selected"
        elif training.get("target_confirmed") is not True:
            reason = "target_not_confirmed"
        if reason:
            manifest["excluded"].append({"id": identifier, "reason": reason})
            continue

        for field in ("recorded_at", "confirmation", "verification"):
            require(isinstance(record.get(field), str) and record[field].strip(),
                    identifier + " needs " + field + " evidence or explicit limits")
        source_refs = record.get("source_refs")
        require(isinstance(source_refs, list) and source_refs and all(
            isinstance(v, str) and v.strip() for v in source_refs),
            identifier + " needs source references")
        group = record.get("group_id")
        require(isinstance(group, str) and group in groups,
                identifier + " has no task-family split assignment")
        split = groups[group]
        prompt = messages(training.get("prompt"))
        chosen = messages(training.get("chosen"), target=True)
        fingerprint = hashlib.sha256(json.dumps(
            prompt, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        require(fingerprint not in prompt_splits or prompt_splits[fingerprint] == split,
                "same prompt appears in train and evaluation")
        prompt_splits[fingerprint] = split
        example_key = json.dumps([prompt, chosen], sort_keys=True, ensure_ascii=False)
        if example_key in seen_examples:
            manifest["excluded"].append({"id": identifier, "reason": "duplicate_example"})
            continue
        seen_examples.add(example_key)
        entry = {key: record[key] for key in (
            "id", "group_id", "scope", "criteria_version", "origin", "source_refs",
            "recorded_at", "confirmation", "verification")}
        entry.update(split=split, rows={})
        if split == "eval":
            entry["rows"]["evaluation"] = len(output["evaluation"])
            output["evaluation"].append({"id": identifier, "prompt": prompt,
                                          "expected_response": chosen})
        else:
            entry["rows"]["sft"] = len(output["sft"])
            output["sft"].append({"messages": prompt + chosen})
            if training.get("pair_confirmed") is True and training.get("same_context") is True:
                rejected = messages(training.get("rejected"), target=True)
                require(chosen != rejected, "chosen and rejected must differ")
                entry["rows"]["dpo"] = len(output["dpo"])
                output["dpo"].append({"prompt": prompt, "chosen": chosen, "rejected": rejected})
            else:
                entry["dpo_exclusion"] = "no_confirmed_same_context_pair"
        manifest["included"].append(entry)
    manifest["counts"] = {key: len(value) for key, value in output.items()}
    manifest["counts"]["excluded"] = len(manifest["excluded"])
    return output, manifest


def export(records_path, plan_path, destination):
    destination = Path(destination)
    require(not destination.exists() and not destination.is_symlink(),
            "output must be a new directory")
    records = [json.loads(line) for line in Path(records_path).read_text(encoding="utf-8").splitlines()
               if line.strip()]
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    output, manifest = prepare(records, plan)
    # Validate everything before creating any output. Never modify source records.
    destination.mkdir(mode=0o700)
    for name, rows in output.items():
        path = destination / (name + ".jsonl")
        with path.open("x", encoding="utf-8") as stream:
            path.chmod(0o600)
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    path = destination / "manifest.json"
    with path.open("x", encoding="utf-8") as stream:
        path.chmod(0o600)
        json.dump(manifest, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return manifest["counts"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(export(args.records, args.plan, args.output)))
    except (ValueError, OSError) as error:
        parser.exit(1, "Export failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
