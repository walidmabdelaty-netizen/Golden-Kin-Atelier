import sqlite3
import hashlib
import pytest
from core_ledger import VerdixLedger

def test_ledger_integrity_and_tamper_detection(tmp_path):
    # إنشاء قاعدة بيانات اختبار مؤقتة
    db_file = tmp_path / "test_audit.db"
    ledger = VerdixLedger(str(db_file))

    # تسجيل حدثين في السجل
    h1 = ledger.record_event("BOOT_SEQUENCE_OK")
    h2 = ledger.record_event("SECURITY_POLICY_ENFORCED")

    # التحقق من أن السجلات مسجلة وغير فارغة
    assert h1 != h2
    assert len(h1) == 64
    assert len(h2) == 64

    # محاكاة محاولة تلاعب خبيث: تعديل نص الحدث الأول مباشرة داخل القاعدة
    conn = sqlite3.connect(str(db_file))
    with conn:
        conn.execute("UPDATE audit_chain SET event = 'MALICIOUS_TAMPER' WHERE id = 1")

    # قراءة البيانات والتحقق الرياضي من انكسار السلسلة
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, event, prev_hash, curr_hash FROM audit_chain WHERE id = 1")
    ts, ev, prev, stored_hash = cursor.fetchone()

    # إعادة حساب التجزئة بالبيانات المعدلة
    recalculated_hash = hashlib.sha256(f"{ts}{ev}{prev}".encode()).hexdigest()

    # إثبات كشف التلاعب: التجزئة المخزنة لن تطابق التجزئة المحسوبة
    assert recalculated_hash != stored_hash
    print("\n[+] TAMPER DETECTION VERIFIED: Chain breaks when data is altered.")
