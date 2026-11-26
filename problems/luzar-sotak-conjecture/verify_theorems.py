"""Run the standard-library certificate verifiers from any working directory."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = [
    ['theory/verify_two_pole_reduction.py'],
    ['theory/gp_n_2_construction.py'],
    ['alternative/verify_gp2_certificate.py'],
    ['theory/gp7_exact_cover.py', 'theory/gp7_exact_cover_certificate.json'],
    ['literature_review/review_gp_certificates.py'],
]

for command in COMMANDS:
    print('\nChecking ' + command[0], flush=True)
    subprocess.run([sys.executable] + command, cwd=ROOT, check=True)
print('\nAll theorem certificates and construction checks passed.', flush=True)
