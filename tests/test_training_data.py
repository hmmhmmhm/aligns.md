import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/align/scripts/export_training_data.py"
SPEC = importlib.util.spec_from_file_location("training_export", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def record(identifier="example-1", group="task-1", prompt="Review this small change."):
    # Invented fixtures only. No personal conversation or repository history.
    return {
        "schema_version": 1, "id": identifier, "group_id": group,
        "recorded_at": "2026-10-18T10:00:00Z", "scope": "project:sample",
        "criteria_version": "v2", "source_refs": ["fixture:decision-1"],
        "origin": "observed", "confirmation": "Fixture user chose the focused review.",
        "verification": "Text reviewed; no code executed.",
        "status": "reviewed", "privacy_reviewed": True,
        "training": {
            "prompt": [{"role": "user", "content": prompt}],
            "chosen": [{"role": "assistant", "content": "I will review the changed behavior."}],
            "rejected": [{"role": "assistant", "content": "I will redesign the entire project."}],
            "target_confirmed": True, "pair_confirmed": True, "same_context": True,
        },
    }


def plan():
    return {"schema_version": 1, "current_criteria": {"project:sample": "v2"},
            "groups": {"task-1": "train", "task-2": "eval"},
            "include_origins": ["observed"]}


class TrainingDataTests(unittest.TestCase):
    def test_exports_only_reviewed_targets_without_private_metadata(self):
        output, manifest = MODULE.prepare([record()], plan())
        self.assertEqual(len(output["sft"]), 1)
        self.assertEqual(len(output["dpo"]), 1)
        self.assertEqual(set(output["sft"][0]), {"messages"})
        self.assertNotIn("fixture:decision", json.dumps(output))
        self.assertEqual(manifest["included"][0]["source_refs"], ["fixture:decision-1"])

    def test_evaluation_family_never_enters_training(self):
        original = record(group="task-2")
        variant = record("variant", "task-2", "Review a related change.")
        output, _ = MODULE.prepare([original, variant], plan())
        self.assertEqual(output["sft"], [])
        self.assertEqual(output["dpo"], [])
        self.assertEqual(len(output["evaluation"]), 2)

    def test_candidates_stale_and_unreviewed_privacy_are_excluded(self):
        for changes, reason in [
            ({"status": "candidate"}, "not_reviewed"),
            ({"status": "superseded"}, "not_reviewed"),
            ({"privacy_reviewed": False}, "privacy_not_reviewed"),
            ({"privacy_reviewed": "true"}, "privacy_not_reviewed"),
            ({"criteria_version": "v1"}, "stale_criteria"),
            ({"scope": "personal:unselected"}, "scope_not_selected"),
        ]:
            with self.subTest(changes=changes):
                candidate = record(); candidate.update(changes)
                output, manifest = MODULE.prepare([candidate], plan())
                self.assertEqual(output["sft"], [])
                self.assertEqual(manifest["excluded"][0]["reason"], reason)

    def test_criterion_confirmation_does_not_confirm_generated_target(self):
        candidate = record(); candidate["training"]["target_confirmed"] = False
        output, manifest = MODULE.prepare([candidate], plan())
        self.assertEqual(output["sft"], [])
        self.assertEqual(manifest["excluded"][0]["reason"], "target_not_confirmed")

    def test_changed_context_cannot_become_a_preference_pair(self):
        candidate = record(); candidate["training"]["same_context"] = False
        output, manifest = MODULE.prepare([candidate], plan())
        self.assertEqual(len(output["sft"]), 1)
        self.assertEqual(output["dpo"], [])
        self.assertIn("dpo_exclusion", manifest["included"][0])

    def test_generated_rejection_without_user_choice_is_not_dpo(self):
        candidate = record(); candidate["training"]["pair_confirmed"] = False
        output, _ = MODULE.prepare([candidate], plan())
        self.assertEqual(output["dpo"], [])

    def test_hypothetical_and_reconstructed_need_explicit_export_inclusion(self):
        for origin in ("hypothetical", "reconstructed"):
            candidate = record(); candidate["origin"] = origin
            output, _ = MODULE.prepare([candidate], plan())
            self.assertEqual(output["sft"], [])
            explicit = plan(); explicit["include_origins"].append(origin)
            output, manifest = MODULE.prepare([candidate], explicit)
            self.assertEqual(len(output["sft"]), 1)
            self.assertEqual(manifest["included"][0]["origin"], origin)

    def test_exact_prompt_leakage_across_families_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "same prompt"):
            MODULE.prepare([record(), record("example-2", "task-2")], plan())

    def test_repeated_example_does_not_inflate_training_count(self):
        output, manifest = MODULE.prepare([record(), record("copy")], plan())
        self.assertEqual(len(output["sft"]), 1)
        self.assertEqual(manifest["excluded"], [{"id": "copy", "reason": "duplicate_example"}])

    def test_missing_split_duplicate_ids_and_missing_evidence_fail(self):
        with self.assertRaisesRegex(ValueError, "split assignment"):
            MODULE.prepare([record(group="unknown")], plan())
        with self.assertRaisesRegex(ValueError, "duplicate record"):
            MODULE.prepare([record(), record()], plan())
        candidate = record(); candidate["confirmation"] = ""
        with self.assertRaisesRegex(ValueError, "confirmation"):
            MODULE.prepare([candidate], plan())

    def test_does_not_silently_flatten_tool_trajectories(self):
        candidate = record()
        candidate["training"]["chosen"][0]["tool_calls"] = [{"name": "test"}]
        with self.assertRaisesRegex(ValueError, "only text"):
            MODULE.prepare([candidate], plan())

    def test_export_preserves_sources_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); data = root / "records.jsonl"; config = root / "plan.json"
            data.write_text(json.dumps(record()) + "\n"); config.write_text(json.dumps(plan()))
            before = data.read_bytes()
            counts = MODULE.export(data, config, root / "export")
            self.assertEqual(counts["sft"], 1)
            self.assertEqual(data.read_bytes(), before)
            with self.assertRaisesRegex(ValueError, "new directory"):
                MODULE.export(data, config, root / "export")

    def test_validation_failure_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); data = root / "records.jsonl"; config = root / "plan.json"
            data.write_text(json.dumps(record(group="unknown")) + "\n")
            config.write_text(json.dumps(plan()))
            with self.assertRaises(ValueError):
                MODULE.export(data, config, root / "export")
            self.assertFalse((root / "export").exists())


if __name__ == "__main__":
    unittest.main()
