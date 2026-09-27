import sqlite3
import hashlib
import time
import threading

# قفل التزامن لمنع اختلاط السلاسل أثناء الكتابة (Thread-Safety)
ledger_lock = threading.Lock()

class VerdixLedger:
    def __init__(self, db_path="verdix_audit.db"):
        # السماح لنفس الاتصال بالعمل عبر خيوط متعددة
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_chain (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    event TEXT,
                    prev_hash TEXT,
                    curr_hash TEXT
                )
            """)

    def record_event(self, event_text):
        # تفعيل القفل: خيط واحد فقط يقرأ البصمة السابقة ويحسب الجديدة في نفس اللحظة
        with ledger_lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT curr_hash FROM audit_chain ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            prev_hash = row[0] if row else "0" * 64

            timestamp = time.time()
            payload = f"{timestamp}{event_text}{prev_hash}".encode()
            curr_hash = hashlib.sha256(payload).hexdigest()

            with self.conn:
                self.conn.execute("""
                    INSERT INTO audit_chain (timestamp, event, prev_hash, curr_hash)
                    VALUES (?, ?, ?, ?)
                """, (timestamp, event_text, prev_hash, curr_hash))

        return curr_hash
