#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

if len(sys.argv) < 2:
    print(json.dumps({"status": "ERROR", "error": "command required"}))
    sys.exit(2)

command = sys.argv[1:]

started = datetime.now(timezone.utc)
t0 = time.monotonic()

result = subprocess.run(
    command,
    capture_output=True,
    text=True
)

finished = datetime.now(timezone.utc)
duration_ms = round((time.monotonic() - t0) * 1000)

execution_id = "RUN-" + started.strftime("%Y%m%dT%H%M%S%fZ")

record = {
    "execution_id": execution_id,
    "provider": "local-terminal",
    "project": "verdix-black-platform",
    "command": command,
    "working_directory": os.getcwd(),
    "started_at": started.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    "finished_at": finished.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    "duration_ms": duration_ms,
    "exit_code": result.returncode,
    "stdout": result.stdout,
    "stderr": result.stderr,
    "status": "PASS" if result.returncode == 0 else "FAIL"
}

execution_dir = Path("evidence/executions")
execution_dir.mkdir(parents=True, exist_ok=True)

artifact = execution_dir / f"{execution_id}.json"
artifact.write_text(json.dumps(record, indent=2) + "\n")

print(json.dumps(record, indent=2))
print(f"artifact={artifact}")

sys.exit(result.returncode)
