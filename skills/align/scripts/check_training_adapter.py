#!/usr/bin/env python3
"""Inspect selected-target token boundaries using a local tokenizer, without training."""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path


def inspect(rows, tokenizer, maximum):
    results = []
    for index, row in enumerate(rows):
        prompt, target = row["prompt"], row["completion"]
        if not target or len(target) != 1 or target[0].get("role") != "assistant":
            raise ValueError("expected a single selected assistant target")
        options = {"tools": row["tools"]} if row.get("tools") else {}
        prefix = tokenizer.apply_chat_template(prompt, tokenize=False,
                                                add_generation_prompt=True, **options)
        complete = tokenizer.apply_chat_template(prompt + target, tokenize=False,
                                                  add_generation_prompt=False, **options)
        if not complete.startswith(prefix):
            raise ValueError(f"row {index}: chat template changes the prompt at the target boundary")
        before = tokenizer.encode(prefix, add_special_tokens=False)
        tokens = tokenizer.encode(complete, add_special_tokens=False)
        if tokens[:len(before)] != before or len(tokens) <= len(before):
            raise ValueError(f"row {index}: token boundary is not a stable nonempty completion")
        if len(tokens) > maximum:
            raise ValueError(f"row {index}: exceeds token budget; refusing silent truncation")
        labels = [-100] * len(before) + tokens[len(before):]
        if any(v != -100 for v in labels[:len(before)]):
            raise ValueError("prompt labels are not masked")
        results.append({"row": index, "prompt_tokens": len(before),
                        "completion_tokens": len(tokens) - len(before),
                        "total_tokens": len(tokens), "prompt_masked": True})
    if not results:
        raise ValueError("dataset is empty")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--tokenizer", required=True, type=Path,
                        help="Explicit local tokenizer directory; no remote code or downloads")
    parser.add_argument("--max-tokens", required=True, type=int)
    args = parser.parse_args()
    try:
        from transformers import AutoTokenizer
        if args.max_tokens < 1 or not args.tokenizer.is_dir():
            raise ValueError("select a local tokenizer and a positive token budget")
        tokenizer = AutoTokenizer.from_pretrained(str(args.tokenizer), local_files_only=True,
                                                  trust_remote_code=False)
        rows = [json.loads(line) for line in args.dataset.read_text().splitlines() if line.strip()]
        report = inspect(rows, tokenizer, args.max_tokens)
        print(json.dumps({"dataset_sha256": hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
                          "tokenizer_files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                              for p in sorted(args.tokenizer.iterdir()) if p.is_file()},
                          "transformers_version": importlib.metadata.version("transformers"),
                          "max_tokens": args.max_tokens, "rows": report,
                          "limitation": "Tokenizer boundary check only, not trainer collation or learning."},
                         indent=2))
    except (ImportError, ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, "Adapter check failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
