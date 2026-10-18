#!/usr/bin/env python3
"""Validate selected manual team batches and export locally. Never execute code."""

import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath

from export_training_data import digest, prepare, require, timestamp, write_export


def file_bytes(root, name):
    require(isinstance(name, str) and name and "\\" not in name,
            "artifact needs a relative POSIX path")
    parts = PurePosixPath(name)
    require(not parts.is_absolute() and ".." not in parts.parts and name == str(parts),
            "unsafe artifact path")
    path = root
    for part in parts.parts:
        path = path / part
        require(not path.is_symlink(), "symlink artifacts are not supported")
    require(path.is_file(), "missing artifact: " + name)
    return path.read_bytes()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate_policy(policy):
    require(isinstance(policy, dict) and policy.get("schema_version") == 2,
            "team policy must use schema version 2")
    require(policy.get("intended_use") in ("training", "evaluation", "training_and_evaluation"),
            "policy needs intended use")
    reviewers = policy.get("allowed_reviewers")
    require(isinstance(reviewers, list) and reviewers and all(
        isinstance(name, str) and name.strip() for name in reviewers),
        "policy needs authorized reviewer aliases")
    require(isinstance(policy.get("criteria_text"), dict), "policy needs criteria text")
    plan = policy.get("export_plan")
    # Reuse the exporter validation, including allowed splits and origins.
    prepare([], plan)
    for scope in plan["current_criteria"]:
        text = policy["criteria_text"].get(scope)
        require(isinstance(text, str) and text.strip(), "missing criterion snapshot")
    withdrawals = policy.get("withdrawn_ids", [])
    require(isinstance(withdrawals, list) and all(isinstance(v, str) for v in withdrawals),
            "withdrawn_ids must be a list")
    return plan


def prepare_batches(batch_paths, policy):
    plan = validate_policy(policy)
    records, batches, excluded, seen_batches = [], [], [], set()
    for directory in batch_paths:
        root = Path(directory)
        require(not root.is_symlink() and root.is_dir(), "batch must be a directory")
        submission_bytes = file_bytes(root, "submission.json")
        review_bytes = file_bytes(root, "review.json")
        submission = json.loads(submission_bytes)
        review = json.loads(review_bytes)
        require(isinstance(submission, dict) and submission.get("schema_version") == 2,
                "submission must use schema version 2")
        require(isinstance(review, dict) and review.get("schema_version") == 2,
                "review must use schema version 2")
        batch_id = submission.get("batch_id")
        require(isinstance(batch_id, str) and batch_id and ":" not in batch_id
                and batch_id not in seen_batches, "empty, duplicate or invalid batch ID")
        seen_batches.add(batch_id)
        scope = submission.get("team_scope")
        require(isinstance(scope, str) and scope in plan["current_criteria"],
                "batch scope is not selected")
        require(submission.get("criteria_version") == plan["current_criteria"][scope],
                "stale submission criteria")
        require(submission.get("intended_use") == policy["intended_use"],
                "submission use differs from policy")
        require(submission.get("source_use_confirmed") is True and
                submission.get("privacy_reviewed") is True, "source/privacy review missing")
        for field in ("contributor_alias", "approved_destination"):
            require(isinstance(submission.get(field), str) and submission[field].strip(),
                    "submission needs " + field)
        timestamp(submission.get("prepared_at"))
        timestamp(submission.get("submission_confirmed_at"))
        require(review.get("batch_id") == batch_id and
                review.get("submission_sha256") == sha(submission_bytes),
                "review does not match submitted batch bytes")
        require(review.get("reviewer_alias") in policy["allowed_reviewers"],
                "reviewer is not authorized by selected policy")
        require(review.get("team_criteria_version") == submission["criteria_version"],
                "stale review criteria")
        require(isinstance(review.get("review_ref"), str) and review["review_ref"].strip(),
                "review needs a human approval reference")

        entries = submission.get("files")
        require(isinstance(entries, list) and entries, "submission needs hashed files")
        files, hashes = {}, {}
        for entry in entries:
            require(isinstance(entry, dict), "file entry must be an object")
            name = entry.get("path")
            require(isinstance(name, str) and name not in files and
                    name not in ("submission.json", "review.json"), "invalid file inventory")
            content = file_bytes(root, name)
            require(sha(content) == entry.get("sha256"), "artifact hash mismatch: " + name)
            files[name], hashes[name] = content, sha(content)
        require("records.jsonl" in files, "records.jsonl missing from inventory")
        rows = [json.loads(line) for line in files["records.jsonl"].decode("utf-8").splitlines()
                if line.strip()]
        ids = [r.get("id") if isinstance(r, dict) else None for r in rows]
        require(all(isinstance(i, str) and i and ":" not in i for i in ids)
                and len(set(ids)) == len(ids), "record IDs must be unique within a batch")
        require(submission.get("record_ids") == ids, "record inventory differs from submission")
        decisions = review.get("decisions")
        require(isinstance(decisions, list), "review needs decisions")
        by_id = {}
        for decision in decisions:
            require(isinstance(decision, dict), "decision must be an object")
            identifier = decision.get("record_id")
            require(isinstance(identifier, str) and identifier in ids and identifier not in by_id,
                    "unknown or duplicate review decision")
            require(decision.get("status") in ("approved", "needs_changes", "excluded"),
                    "invalid review status")
            timestamp(decision.get("reviewed_at"))
            require(isinstance(decision.get("reason"), str) and decision["reason"].strip(),
                    "review needs a reason")
            by_id[identifier] = decision
        for original in rows:
            identifier = original["id"]
            output_id = batch_id + ":" + identifier
            decision = by_id.get(identifier)
            if output_id in policy.get("withdrawn_ids", []):
                excluded.append({"id": output_id, "reason": "withdrawn"})
                continue
            if not decision or decision["status"] != "approved":
                excluded.append({"id": output_id, "reason": "team_not_approved"})
                continue
            require(decision.get("record_sha256") == digest(original),
                    "record changed after review: " + output_id)
            require(decision.get("team_target_confirmed") is True,
                    "target not approved by team reviewer")
            require(original.get("schema_version") == 2 and original.get("scope") == scope
                    and original.get("criteria_version") == submission["criteria_version"],
                    "approved record scope/schema/version mismatch")
            require(original.get("status") in ("candidate", "reviewed"),
                    "cannot approve excluded or superseded records")
            training = original.get("training")
            require(isinstance(training, dict), "approved record needs training target")
            if training.get("pair_confirmed") is True:
                require(decision.get("same_context_pair_confirmed") is True and
                        training.get("same_context") is True, "pair needs separate team approval")
            require(policy["criteria_text"][scope] in original.get("required_context", []),
                    "required context must include selected criterion snapshot")
            if original.get("kind") == "code":
                code = original.get("code")
                require(isinstance(code, dict), "code evidence must be an object")
                for check in code.get("checks", []):
                    require(isinstance(check, dict) and check.get("evidence_path") in files,
                            "test evidence is not in hashed submission")
            family = decision.get("shared_task_family_id")
            require(isinstance(family, str) and family in plan["groups"],
                    "review needs a shared task family in the export plan")
            split = plan["groups"][family]
            use = policy["intended_use"]
            require(not (use == "evaluation" and split != "eval") and
                    not (use == "training" and split != "train"), "split exceeds permitted use")
            record = copy.deepcopy(original)
            record.update(id=output_id, group_id=family, status="reviewed")
            records.append(record)
        batches.append({"batch_id": batch_id, "submission_sha256": sha(submission_bytes),
                        "review_sha256": sha(review_bytes), "files": hashes,
                        "reviewer_alias": review["reviewer_alias"],
                        "review_ref": review["review_ref"]})
    output, manifest = prepare(records, plan)
    manifest["team"] = {"policy_sha256": digest(policy), "batches": batches,
                        "verification": "Approval declarations and artifact integrity checked; "
                        "reviewer identity and test execution not independently authenticated."}
    manifest["excluded"].extend(excluded)
    manifest["counts"]["excluded"] = len(manifest["excluded"])
    manifest["quality"] = {
        "approved_unique_records": len(manifest["included"]),
        "task_families": len({r["group_id"] for r in manifest["included"]}),
        "by_kind": {kind: sum(r["kind"] == kind for r in manifest["included"])
                    for kind in ("decision", "code", "tool_action")},
        "by_origin": {origin: sum(r["origin"] == origin for r in manifest["included"])
                      for origin in ("observed", "hypothetical", "reconstructed")},
        "exclusion_reasons": {reason: sum(r["reason"] == reason for r in manifest["excluded"])
                              for reason in sorted({r["reason"] for r in manifest["excluded"]})},
    }
    return output, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", action="append", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--output", type=Path,
                        help="Omit for a read-only validation and count report")
    args = parser.parse_args()
    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"))
        output, manifest = prepare_batches(args.batch, policy)
        if args.output:
            write_export(output, manifest, args.output)
        print(json.dumps({"counts": manifest["counts"], "quality": manifest["quality"]}))
    except (ValueError, OSError, TypeError, KeyError) as error:
        parser.exit(1, "Team export failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
