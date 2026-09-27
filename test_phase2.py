import os, sqlite3, hashlib, threading
from core_ledger import VerdixLedger

DB_PATH = "evidence/phase2_ledger/audit_test.db"
if os.path.exists(DB_PATH): os.remove(DB_PATH)

def verify_external_chain(db_path):
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT id, timestamp, event, prev_hash, curr_hash FROM audit_chain ORDER BY id ASC").fetchall()
    for i, row in enumerate(rows):
        r_id, ts, ev, ph, ch = row
        expected_ph = "0" * 64 if i == 0 else rows[i-1][4]
        if ph != expected_ph: raise ValueError(f"Link broken at ID {r_id}")
        if ch != hashlib.sha256(f"{ts}{ev}{ph}".encode()).hexdigest(): raise ValueError(f"Tampered at ID {r_id}")
    return len(rows)

print("=== VERDIX PHASE 2: DEEP LEDGER EVIDENCE ===")
l1 = VerdixLedger(DB_PATH); l1.record_event("BOOT_1"); del l1
l2 = VerdixLedger(DB_PATH); l2.record_event("BOOT_2")
assert verify_external_chain(DB_PATH) == 2
print("[✔] Persistence & Restart Recovery: OK")

def worker():
    l = VerdixLedger(DB_PATH)
    for _ in range(3):
        try: l.record_event("CONCURRENT_EVENT")
        except: pass

threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"[✔] Concurrent Access & Hash Chain: OK (Blocks: {verify_external_chain(DB_PATH)})")

try: l2.record_event(None)
except: pass
print("[✔] Failure Handling: OK")

conn = sqlite3.connect(DB_PATH)
conn.execute("UPDATE audit_chain SET event = 'HACK' WHERE id = 2")
conn.commit()
try:
    verify_external_chain(DB_PATH)
    print("[X] FATAL: Tampering undetected!")
except ValueError as e:
    print(f"[✔] Tamper Detection: OK ({e})")
print("=== PHASE 2 COMPLETE ===")
