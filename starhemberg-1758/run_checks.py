"""Reproduce the partial edition with Python's standard library plus cipherkit."""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
for script in (
    'decode.py', 'verify.py', 'calibrate.py', 'parallel_control.py',
    'parallel_extension.py', 'variant_consistency.py', 'repair_cases.py',
    'joint_candidates.py', 'repair_diagnostic.py',
):
    print(f'Running {script}', flush=True)
    subprocess.run([sys.executable, str(HERE / script)], cwd=HERE, check=True)
subprocess.run([sys.executable, str(HERE / 'edition-2026-09-21/build.py'), '--check'], cwd=HERE, check=True)
print('All checks completed; this does not certify a complete decipherment.')
