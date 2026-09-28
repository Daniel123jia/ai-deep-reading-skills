from pathlib import Path
import subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
cmd=[sys.executable,str(ROOT/'scripts/validate_result.py'),str(ROOT/'examples/minimal-v1.4.json'),'--strict-warnings']
r=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if r.returncode!=0:
    raise SystemExit(f"smoke test failed\nSTDOUT={r.stdout}\nSTDERR={r.stderr}")
print('SMOKE TEST PASSED')
