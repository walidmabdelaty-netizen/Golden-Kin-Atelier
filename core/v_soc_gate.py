import sys
import os
import hashlib
import time
from datetime import datetime, timezone

# --- Link to Project Root ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core_ledger import VerdixLedger 

class VSOC_Engine:
    def __init__(self, db_path):
        # Target DB to project root
        db_full_path = os.path.join(PROJECT_ROOT, db_path)
        self.ledger = VerdixLedger(db_full_path)
        self.sovereign_key = "VERDIX_MASTER_APPROVE_2026"

    def detect_threat(self, threat_data):
        print("\n[!] VERDIX V-SOC: THREAT DETECTED")
        print(f"[*] Analyzing payload: {threat_data}")
        time.sleep(1)
        
        # 90% Automation: Prepare Defense
        threat_hash = hashlib.sha256(threat_data.encode()).hexdigest()
        print(f"[*] Defense Protocol Prepared. Target Hash: {threat_hash[:16]}...")
        print("[*] AUTOMATION PAUSED. WAITING FOR HUMAN SOVEREIGNTY (10%).\n")
        
        return threat_hash

    def execute_sovereign_decision(self, threat_hash, admin_input):
        if admin_input == self.sovereign_key:
            event_log = f"THREAT_BLOCKED_BY_ADMIN_{threat_hash}"
            self.ledger.record_event(event_log)
            print("\n[✓] DECISION APPROVED: Threat blocked and recorded to Immutable Ledger.")
        else:
            event_log = f"THREAT_IGNORED_OR_KEY_FAILED_{threat_hash}"
            self.ledger.record_event(event_log)
            print("\n[X] DECISION REJECTED: No action taken. Logged to Ledger.")

if __name__ == "__main__":
    v_soc = VSOC_Engine("test_audit.db")
    
    active_threat = "UNAUTHORIZED_SQL_INJECTION_ATTEMPT_PORT_443"
    t_hash = v_soc.detect_threat(active_threat)
    
    print(">>> ACTION REQUIRED: Enter Sovereign Key to BLOCK threat, or press Enter to IGNORE:")
    human_decision = input("Admin Key: ")
    
    v_soc.execute_sovereign_decision(t_hash, human_decision)
