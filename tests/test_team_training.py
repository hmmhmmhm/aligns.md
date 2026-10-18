import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/align/scripts'
sys.path.insert(0, str(SCRIPTS))
import export_training_data as base
import export_team_dataset as team
import check_training_adapter as adapter

CRITERION = 'Keep the public API unchanged.'


def example(identifier='example', kind='decision'):
    record = {
        'schema_version': 2, 'id': identifier, 'group_id': 'local-family',
        'recorded_at': '2026-10-18T00:00:00Z', 'scope': 'team:fictional',
        'criteria_version': 'v1', 'source_refs': ['fixture:invented'],
        'origin': 'reconstructed', 'confirmation': 'Invented reviewer confirmed the target.',
        'verification': 'Fictional evidence, not executed code.', 'status': 'candidate',
        'privacy_reviewed': True, 'kind': kind, 'context_reviewed': True,
        'required_context': [CRITERION],
        'training': {
            'prompt': [{'role': 'user', 'content': CRITERION + ' Fix the empty-input bug.'}],
            'chosen': [{'role': 'assistant', 'content': 'Preserve the API and add the missing guard.'}],
            'rejected': [{'role': 'assistant', 'content': 'Replace the API with a new signature.'}],
            'target_confirmed': True, 'pair_confirmed': True, 'same_context': True,
        },
    }
    if kind == 'code':
        patch = '--- a/a.py\n+++ b/a.py\n@@ -1 +1 @@\n-return values[0]\n+return values[0] if values else None\n'
        record['code'] = {'repository': 'fixture:repository', 'base_commit': 'a' * 40,
                          'environment': 'fixture:python', 'patch': patch,
                          'checks': [{'command': ['python', '-m', 'unittest'], 'exit_code': 0,
                                      'checked_at': '2026-10-18T00:01:00Z',
                                      'evidence_path': 'checks/test.txt'}]}
        record['training']['chosen'][0]['content'] = patch
    if kind == 'tool_action':
        record['training'].update(pair_confirmed=False, same_context=False,
            tools=[{'type': 'function', 'function': {'name': 'read_file', 'parameters': {
                'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path']}}}],
            chosen=[{'role': 'assistant', 'tool_calls': [{'id': 'read-1', 'type': 'function',
                'function': {'name': 'read_file', 'arguments': {'path': 'a.py'}}}]}])
        record['training'].pop('rejected')
    record['input_snapshot_sha256'] = base.digest({
        'prompt': record['training']['prompt'], 'tools': record['training'].get('tools', [])})
    return record


def policy():
    return {'schema_version': 2, 'intended_use': 'training_and_evaluation',
            'allowed_reviewers': ['fixture-reviewer'], 'criteria_text': {'team:fictional': CRITERION},
            'withdrawn_ids': [], 'export_plan': {'schema_version': 1,
                'current_criteria': {'team:fictional': 'v1'},
                'include_origins': ['reconstructed'],
                'groups': {'task-a': 'train', 'task-b': 'eval'}}}


def batch(root, records=None, name='batch-a'):
    records = records if records is not None else [example()]
    root.mkdir(parents=True)
    (root / 'records.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
    (root / 'checks').mkdir()
    (root / 'checks/test.txt').write_text('Invented passing test receipt; not an execution result.\n')
    submission = {'schema_version': 2, 'batch_id': name, 'contributor_alias': 'fixture-author',
        'team_scope': 'team:fictional', 'criteria_version': 'v1',
        'prepared_at': '2026-10-18T00:00:00Z', 'submission_confirmed_at': '2026-10-18T00:02:00Z',
        'intended_use': 'training_and_evaluation', 'record_ids': [r['id'] for r in records],
        'source_use_confirmed': True, 'privacy_reviewed': True,
        'approved_destination': 'fixture:private-intake', 'files': [
            {'path': path, 'sha256': team.sha((root / path).read_bytes())}
            for path in ['records.jsonl', 'checks/test.txt']]}
    (root / 'submission.json').write_text(json.dumps(submission))
    review = {'schema_version': 2, 'batch_id': name, 'reviewer_alias': 'fixture-reviewer',
        'team_criteria_version': 'v1', 'review_ref': 'fixture:explicit-approval',
        'submission_sha256': team.sha((root / 'submission.json').read_bytes()),
        'decisions': [{'record_id': r['id'], 'record_sha256': base.digest(r), 'status': 'approved',
            'reason': 'Invented approved example.', 'reviewed_at': '2026-10-18T00:03:00Z',
            'team_target_confirmed': True, 'same_context_pair_confirmed': r['kind'] != 'tool_action',
            'shared_task_family_id': 'task-a'} for r in records]}
    (root / 'review.json').write_text(json.dumps(review))
    return root


def edit(root, filename, change):
    path = root / filename
    data = json.loads(path.read_text()); change(data); path.write_text(json.dumps(data))


class TeamTrainingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.batch = batch(self.root / 'batch')

    def run_batch(self, selected=None):
        return team.prepare_batches([self.batch], selected or policy())

    def test_approved_batch_exports_completion_and_provenance(self):
        output, manifest = self.run_batch()
        self.assertEqual(len(output['sft-completion']), 1)
        self.assertEqual(len(output['dpo']), 1)
        self.assertEqual(manifest['included'][0]['id'], 'batch-a:example')
        self.assertEqual(manifest['quality']['by_origin']['reconstructed'], 1)
        self.assertNotIn('fixture-reviewer', json.dumps(output))

    def test_changed_file_is_rejected(self):
        (self.batch / 'checks/test.txt').write_text('Modified after approval')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.run_batch()

    def test_changed_submission_is_rejected(self):
        edit(self.batch, 'submission.json', lambda d: d.update(contributor_alias='other'))
        with self.assertRaisesRegex(ValueError, 'submitted batch bytes'):
            self.run_batch()

    def test_unlisted_reviewer_is_rejected(self):
        edit(self.batch, 'review.json', lambda d: d.update(reviewer_alias='unapproved'))
        with self.assertRaisesRegex(ValueError, 'not authorized'):
            self.run_batch()

    def test_missing_or_stale_record_approval_is_rejected(self):
        edit(self.batch, 'review.json', lambda d: d['decisions'][0].update(record_sha256='wrong'))
        with self.assertRaisesRegex(ValueError, 'changed after review'):
            self.run_batch()

    def test_pending_review_is_excluded(self):
        edit(self.batch, 'review.json', lambda d: d['decisions'][0].update(status='needs_changes'))
        output, manifest = self.run_batch()
        self.assertEqual(output['sft-completion'], [])
        self.assertEqual(manifest['excluded'][0]['reason'], 'team_not_approved')

    def test_withdrawn_record_is_excluded(self):
        selected = policy(); selected['withdrawn_ids'] = ['batch-a:example']
        output, manifest = self.run_batch(selected)
        self.assertEqual(output['dpo'], [])
        self.assertEqual(manifest['excluded'][0]['reason'], 'withdrawn')

    def test_pair_requires_separate_approval(self):
        edit(self.batch, 'review.json', lambda d: d['decisions'][0].update(same_context_pair_confirmed=False))
        with self.assertRaisesRegex(ValueError, 'separate team approval'):
            self.run_batch()

    def test_context_cannot_be_metadata_only(self):
        record = example(); record['required_context'].append('Critical missing constraint')
        self.batch = batch(self.root / 'bad-context', [record])
        with self.assertRaisesRegex(ValueError, 'missing from training input'):
            self.run_batch()

    def test_changed_prompt_needs_new_context_review(self):
        record = example(); record['training']['prompt'][0]['content'] += ' New facts.'
        self.batch = batch(self.root / 'changed-context', [record])
        with self.assertRaisesRegex(ValueError, 'snapshot changed'):
            self.run_batch()

    def test_required_criterion_snapshot_is_enforced(self):
        selected = policy(); selected['criteria_text']['team:fictional'] = 'Different rule.'
        with self.assertRaisesRegex(ValueError, 'criterion snapshot'):
            self.run_batch(selected)

    def test_previous_bad_assistant_is_context_not_completion(self):
        record = example()
        record['training']['prompt'] += [{'role': 'assistant', 'content': 'Wrong earlier answer'},
                                        {'role': 'user', 'content': 'Please correct it.'}]
        record['input_snapshot_sha256'] = base.digest({'prompt': record['training']['prompt'], 'tools': []})
        self.batch = batch(self.root / 'history', [record])
        output, _ = self.run_batch()
        self.assertNotIn('Wrong earlier answer', json.dumps(output['sft-completion'][0]['completion']))
        self.assertIn('Wrong earlier answer', json.dumps(output['sft-completion'][0]['prompt']))

    def test_contradictory_pairs_are_rejected_across_batches(self):
        inverse = example()
        inverse['training']['chosen'], inverse['training']['rejected'] = (
            inverse['training']['rejected'], inverse['training']['chosen'])
        other = batch(self.root / 'other', [inverse], name='batch-b')
        with self.assertRaisesRegex(ValueError, 'preference cycle'):
            team.prepare_batches([self.batch, other], policy())

    def test_code_evidence_exports_without_claiming_execution(self):
        self.batch = batch(self.root / 'code', [example(kind='code')])
        _, manifest = self.run_batch()
        self.assertEqual(manifest['quality']['by_kind']['code'], 1)
        self.assertIn('not independently authenticated', manifest['team']['verification'])

    def test_failed_code_check_is_rejected(self):
        record = example(kind='code'); record['code']['checks'][0]['exit_code'] = 1
        self.batch = batch(self.root / 'code', [record])
        with self.assertRaisesRegex(ValueError, 'did not pass'):
            self.run_batch()

    def test_unhashed_code_evidence_is_rejected(self):
        record = example(kind='code'); record['code']['checks'][0]['evidence_path'] = 'unknown.txt'
        self.batch = batch(self.root / 'code', [record])
        with self.assertRaisesRegex(ValueError, 'hashed submission'):
            self.run_batch()

    def test_tool_action_preserves_schema_and_argument_objects(self):
        self.batch = batch(self.root / 'tool', [example(kind='tool_action')])
        output, _ = self.run_batch()
        self.assertEqual(output['sft'], [])
        row = output['sft-completion'][0]
        self.assertEqual(row['completion'][0]['tool_calls'][0]['function']['arguments'], {'path': 'a.py'})
        self.assertEqual(row['tools'][0]['function']['name'], 'read_file')

    def test_missing_tool_result_is_rejected(self):
        record = example(kind='tool_action')
        record['training']['prompt'] += record['training']['chosen']
        record['training']['prompt'].append({'role': 'user', 'content': 'Continue.'})
        record['input_snapshot_sha256'] = base.digest({'prompt': record['training']['prompt'],
                                                      'tools': record['training']['tools']})
        self.batch = batch(self.root / 'tool', [record])
        with self.assertRaisesRegex(ValueError, 'missing tool responses'):
            self.run_batch()

    def test_train_eval_exact_overlap_is_rejected(self):
        other = batch(self.root / 'other', name='batch-b')
        edit(other, 'review.json', lambda d: d['decisions'][0].update(shared_task_family_id='task-b'))
        with self.assertRaisesRegex(ValueError, 'same prompt'):
            team.prepare_batches([self.batch, other], policy())

    def test_invalid_timestamp_is_rejected(self):
        edit(self.batch, 'review.json', lambda d: d['decisions'][0].update(reviewed_at='today'))
        with self.assertRaisesRegex(ValueError, 'invalid timestamp'):
            self.run_batch()

    def test_artifact_paths_reject_traversal_and_symlinks(self):
        for name in ['../secret', '/tmp/secret', 'checks/../records.jsonl']:
            with self.assertRaises(ValueError):
                team.file_bytes(self.batch, name)
        (self.batch / 'linked').symlink_to(self.batch / 'records.jsonl')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            team.file_bytes(self.batch, 'linked')

    def test_cli_validates_without_writing_and_export_refuses_overwrite(self):
        config = self.root / 'policy.json'; config.write_text(json.dumps(policy()))
        command = [sys.executable, str(SCRIPTS / 'export_team_dataset.py'), '--batch', str(self.batch),
                   '--policy', str(config)]
        checked = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(json.loads(checked.stdout)['counts']['sft-completion'], 1)
        destination = self.root / 'export'
        exported = subprocess.run(command + ['--output', str(destination)], capture_output=True, text=True)
        self.assertEqual(exported.returncode, 0, exported.stderr)
        manifest = json.loads((destination / 'manifest.json').read_text())
        self.assertEqual(manifest['files']['sft-completion.jsonl'],
                         team.sha((destination / 'sft-completion.jsonl').read_bytes()))
        repeated = subprocess.run(command + ['--output', str(destination)], capture_output=True, text=True)
        self.assertNotEqual(repeated.returncode, 0)

    def test_failed_validation_creates_no_export(self):
        output = self.root / 'export'
        config = self.root / 'policy.json'; config.write_text(json.dumps(policy()))
        (self.batch / 'checks/test.txt').write_text('Tampered')
        result = subprocess.run([sys.executable, str(SCRIPTS / 'export_team_dataset.py'),
            '--batch', str(self.batch), '--policy', str(config), '--output', str(output)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
