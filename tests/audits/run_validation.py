"""Run repository unit checks and emit named outcomes as reproducible evidence."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class Results(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.outcomes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.outcomes.append({'test': test.id(), 'status': 'passed'})

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.outcomes.append({'test': test.id(), 'status': 'failed'})

    def addError(self, test, error):
        super().addError(test, error)
        self.outcomes.append({'test': test.id(), 'status': 'error'})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.outcomes.append({'test': test.id(), 'status': 'skipped', 'reason': reason})


if __name__ == '__main__':
    results = Results()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        unittest.defaultTestLoader.discover(str(ROOT/'tests'), pattern='test_*.py').run(results)
    sources = list((ROOT/'skills/align/scripts').glob('*.py')) + list((ROOT/'tests').glob('test_*.py'))
    report = {'schema_version': 1, 'scope': 'Local unit tests; not model performance or independent review.',
              'tests_run': results.testsRun, 'failures': len(results.failures),
              'errors': len(results.errors), 'skipped': len(results.skipped),
              'outcomes': results.outcomes,
              'sources': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(sources)}}
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if results.wasSuccessful() else 1)
