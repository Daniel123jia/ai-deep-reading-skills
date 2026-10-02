from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "minimal-v1.6.json"
VALIDATOR = ROOT / "scripts" / "validate_result.py"


def test_example_is_v16_and_valid():
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.6"
    assert data["papers"][0]["paper_lens"]["primary"]
    assert data["papers"][0]["evidence_inventory"]["method_ids"]
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(EXAMPLE), "--strict-warnings"], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
