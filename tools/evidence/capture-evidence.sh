set -u                                                                                  ARTIFACT="${1:-}"

if [ -z "$ARTIFACT" ]; then
    echo "ERROR: artifact path is required"     exit 2                                  fi                                          
if [ ! -f "$ARTIFACT" ]; then                   echo "ERROR: artifact not found: $ARTIFACT"                                             exit 3
fi

EXECUTION_ID="$(basename "$ARTIFACT" .json)"
RECORDED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
SHA256="$(sha256sum "$ARTIFACT" | awk '{princhmod +x tools/evidence/capture-evidence.shn
root@localhost:~/verdix-black-platform# cd /root/verdix-black-platform
                                            cat > tools/evidence/capture-evidence.sh <<'EOF'                                        #!/usr/bin/env bash
set -u                                      
ARTIFACT="${1:-}"                           
if [ -z "$ARTIFACT" ]; then
    echo "ERROR: artifact path is required"
    exit 2
fi

if [ ! -f "$ARTIFACT" ]; then
    echo "ERROR: artifact not found: $ARTIFACT"
    exit 3
fi

EXECUTION_ID="$(basename "$ARTIFACT" .json)"                                            RECORDED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"                                          SHA256="$(sha256sum "$ARTIFACT" | awk '{pringit status --shortUS ==="ions/HARD-EXEC-2026=== SCRIPT SYNTAX ===
=== SCRIPT ===                              #!/usr/bin/env bash
set -u                                      
ARTIFACT="${1:-}"                           
if [ -z "$ARTIFACT" ]; then                     echo "ERROR: artifact path is required"
    exit 2                                  fi
                                            if [ ! -f "$ARTIFACT" ]; then
    echo "ERROR: artifact not found: $ARTIFACT"
    exit 3                                  fi
                                            EXECUTION_ID="$(basename "$ARTIFACT" .json)"
RECORDED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
SHA256="$(sha256sum "$ARTIFACT" | awk '{print $1}')"
                                            RECORD_DIR="evidence/records"
RECORD="${RECORD_DIR}/${EXECUTION_ID}.evidence.json"
                                            mkdir -p "$RECORD_DIR"
                                            cat > "$RECORD" <<JSON
{                                             "evidence_id": "${EXECUTION_ID}",
  "execution_id": "${EXECUTION_ID}",          "artifact": "${ARTIFACT}",
  "artifact_sha256": "${SHA256}",             "recorded_at": "${RECORDED_AT}",
  "evidence_status": "CAPTURED",              "verification_status": "UNREVIEWED"
}                                           JSON
                                            echo "=== EVIDENCE CAPTURE ==="
echo "artifact=${ARTIFACT}"                 echo "sha256=${SHA256}"
echo "record=${RECORD}"                     echo "status=CAPTURED"
echo "verification=UNREVIEWED"              === EXECUTION ===
=== EVIDENCE CAPTURE ===                    artifact=evidence/executions/HARD-EXEC-20260908T162953Z.json                            sha256=94a46c0a345a4a2aee160e55e97282ffba2ab20243228145366ea51ec1f3dbee                 record=evidence/records/HARD-EXEC-20260908T162953Z.evidence.json                        status=CAPTURED
verification=UNREVIEWED                     === RECORD ===
{                                             "evidence_id": "HARD-EXEC-20260908T162953Z",                                            "execution_id": "HARD-EXEC-20260908T162953Z",                                           "artifact": "evidence/executions/HARD-EXEC-20260908T162953Z.json",                      "artifact_sha256": "94a46c0a345a4a2aee160e55e97282ffba2ab20243228145366ea51ec1f3dbee",  "recorded_at": "2026-09-08T17:28:12Z",
  "evidence_status": "CAPTURED",              "verification_status": "UNREVIEWED"
}                                           === ORIGINAL HASH ===
94a46c0a345a4a2aee160e55e97282ffba2ab20243228145366ea51ec1f3dbee  evidence/executions/HARD-EXEC-20260908T162953Z.json               === GIT STATUS ===
?? evidence/                                ?? tools/
root@localhost:~/verdix-black-platform#     
c
q
cQ
cd /root/verdix-black-platform
printf '%s\n' '=== EVIDENCE CAPTURE SELF-TEST ==='

echo '[1] Missing argument'
./tools/evidence/capture-evidence.sh
echo "EXIT=$?"

echo
echo '[2] Missing artifact'
./tools/evidence/capture-evidence.sh /tmp/does-not-exist.json
echo "EXIT=$?"

echo
echo '[3] Valid artifact'
./tools/evidence/capture-evidence.sh \
  evidence/executions/HARD-EXEC-20260908T162953Z.json
echo "EXIT=$?"

echo
echo '=== VERIFY ARTIFACT INTEGRITY ==='
sha256sum evidence/executions/HARD-EXEC-20260908T162953Z.json

echo
echo '=== EVIDENCE RECORD ==='
cat evidence/records/HARD-EXEC-20260908T162953Z.evidence.json
root@localhost:~/verdix-black-platform#
Ctrl + C
Ctrl + C
Eda
E
c
Qc
c
c
qQ
exit

q

