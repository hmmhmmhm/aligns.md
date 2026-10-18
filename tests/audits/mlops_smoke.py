"""Reproduce the tokenizer/load check using invented batches, no model weights."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tests'))
from test_team_training import batch, example, policy
import check_training_adapter as adapter
import export_team_dataset as team
import export_training_data as base


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tokenizer', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output must be new')
    from transformers import AutoTokenizer
    from datasets import load_dataset
    args.output.mkdir(parents=True)
    paths = []
    for kind in ('decision', 'code', 'tool_action'):
        paths.append(batch(args.output / kind, [example(kind=kind)], name=kind))
    config = policy()
    (args.output/'policy.json').write_text(json.dumps(config, indent=2)+'\n')
    output, manifest = team.prepare_batches(paths, config)
    base.write_export(output, manifest, args.output/'export')
    tokenizer = AutoTokenizer.from_pretrained(str(args.tokenizer), local_files_only=True,
                                              trust_remote_code=False)
    token_rows = adapter.inspect(output['sft-completion'], tokenizer, 4096)
    loaded = {}
    for name in ('sft-completion', 'dpo'):
        dataset = load_dataset('json', data_files=str(args.output/'export'/(name+'.jsonl')), split='train')
        loaded[name] = {'rows': len(dataset), 'columns': dataset.column_names}
    # Exercise the Arrow-loaded rows too: nullable message fields can affect templates.
    from datasets import Dataset
    loaded_tokens = adapter.inspect(list(load_dataset('json',
        data_files=str(args.output/'export/sft-completion.jsonl'), split='train')), tokenizer, 4096)
    report = {'schema_version': 1, 'fixtures': 'Invented reconstructed examples only.',
        'scope': 'Dataset loading and tokenizer boundaries; no trainer, weights, training or team outcomes.',
        'packages': {name: importlib.metadata.version(name) for name in
                     ('transformers', 'datasets', 'tokenizers', 'jinja2')},
        'sources': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [Path(__file__), ROOT/'tests/test_team_training.py',
                      ROOT/'skills/align/scripts/export_training_data.py',
                      ROOT/'skills/align/scripts/export_team_dataset.py',
                      ROOT/'skills/align/scripts/check_training_adapter.py']},
        'tokenizer_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(args.tokenizer.iterdir()) if p.is_file()},
        'loaded': loaded, 'token_rows': token_rows, 'arrow_loaded_token_rows': loaded_tokens}
    (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'loaded': loaded, 'token_rows': token_rows}))


if __name__ == '__main__':
    main()
