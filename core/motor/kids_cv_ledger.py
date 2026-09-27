import json
import os
import hashlib
from datetime import datetime, timezone
from enum import Enum

# ---------------------------------------------------------
# 1. تحديد حالات الدليل (التحقق من الدليل وليس الإنسان)
# ---------------------------------------------------------
class EvidenceState(Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    MISMATCH_HASH = "MISMATCH_HASH"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    REVOKED = "REVOKED"  # للإبطال الإجرائي للدليل نفسه إن لزم الأمر

class KidsCVHashChain:
    """
    محرك السلسلة التراكمية المشفرة للسيرة الذاتية (Kids CV).
    يضيف الأحداث ويربطها رياضياً دون أي تقييم أو تصنيف للبشر.
    """
    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self, storage_path="ledgers/education/kids_cv.json"):
        self.storage_path = storage_path
        self.ledger = self._load_ledger()

    def _load_ledger(self) -> dict:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_ledger(self):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.ledger, f, indent=2, ensure_ascii=False)

    # ---------------------------------------------------------
    # 2. التوحيد (Canonicalization) والتجزئة (Hash)
    # ---------------------------------------------------------
    def _canonicalize_and_hash(self, payload: dict) -> str:
        """توحيد تنسيق البيانات وإنتاج بصمة SHA-256 لا تقبل التلاعب"""
        canonical_string = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        return hashlib.sha256(canonical_string.encode('utf-8')).hexdigest()

    # ---------------------------------------------------------
    # 3. عملية الإضافة (Append Operation)
    # ---------------------------------------------------------
    def append_evidence(self, identity_id: str, evidence_reference: str, issuer: str, content_hash: str) -> dict:
        """
        إضافة دليل تعليمي جديد (Append-Only).
        لا يوجد أي متغيرات تقييمية؛ فقط بيانات الدليل الصامتة.
        """
        if identity_id not in self.ledger:
            self.ledger[identity_id] = []

        history = self.ledger[identity_id]
        
        # تحديد البصمة السابقة لربط السلسلة
        previous_hash = self.GENESIS_HASH
        if len(history) > 0:
            previous_hash = history[-1]["current_event_hash"]

        timestamp = datetime.now(timezone.utc).isoformat()

        # إعداد هيكل البيانات للحدث
        event_payload = {
            "evidence_reference": evidence_reference,
            "issuer": issuer,
            "issued_at": timestamp,
            "content_hash": content_hash,
            "previous_event_hash": previous_hash
        }

        # حساب البصمة الحالية للحدث بأكمله
        current_event_hash = self._canonicalize_and_hash(event_payload)

        event_record = {
            "payload": event_payload,
            "current_event_hash": current_event_hash,
            "verification_state": EvidenceState.VERIFIED.value
        }

        self.ledger[identity_id].append(event_record)
        self._save_ledger()
        return event_record

    # ---------------------------------------------------------
    # 4. التحقق واكتشاف التلاعب (Chain Verification & Tamper Detection)
    # ---------------------------------------------------------
    def verify_chain(self, identity_id: str) -> EvidenceState:
        """
        التحقق من سلامة سلسلة الأدلة بالكامل.
        إذا تم تعديل أي دليل سابق، ستنكسر السلسلة وتُرجع MISMATCH_HASH.
        """
        if identity_id not in self.ledger or not self.ledger[identity_id]:
            return EvidenceState.UNVERIFIED

        history = self.ledger[identity_id]
        expected_previous_hash = self.GENESIS_HASH

        for event in history:
            payload = event["payload"]
            recorded_hash = event["current_event_hash"]

            # 1. التحقق من تطابق البصمة السابقة
            if payload["previous_event_hash"] != expected_previous_hash:
                return EvidenceState.MISMATCH_HASH

            # 2. إعادة حساب البصمة الحالية ومقارنتها بالمسجلة
            recalculated_hash = self._canonicalize_and_hash(payload)
            if recalculated_hash != recorded_hash:
                return EvidenceState.MISMATCH_HASH

            # تحديث البصمة المتوقعة للحدث التالي
            expected_previous_hash = recorded_hash

        return EvidenceState.VERIFIED


# =========================================================
# 5. منطقة الاختبار البشري والدليل (Human Review & Testing)
# =========================================================
if __name__ == "__main__":
    cv = KidsCVHashChain("ledgers/education/test_kids_cv.json")
    child_id = "ID-EDU-2026-001"

    print("\033[1;36m=== 1. إضافة أدلة تعليمية (Append Operation) ===\033[0m")
    
    # الحدث الأول (الحضانة)
    ev1 = cv.append_evidence(
        identity_id=child_id,
        evidence_reference="DOC://MINISTRY_EDU/KG/8899",
        issuer="KG_Academy_01",
        content_hash="a1b2c3d4e5f6..."
    )
    print(f"تم إضافة الدليل الأول. البصمة الحالية: \033[1;33m{ev1['current_event_hash'][:15]}...\033[0m")

    # الحدث الثاني (الابتدائية) - يرتبط بالأول
    ev2 = cv.append_evidence(
        identity_id=child_id,
        evidence_reference="DOC://MINISTRY_EDU/PRI/7766",
        issuer="Primary_School_02",
        content_hash="9f8e7d6c5b4a..."
    )
    print(f"تم إضافة الدليل الثاني. البصمة السابقة: \033[1;32m{ev2['payload']['previous_event_hash'][:15]}...\033[0m")
    print(f"تم إضافة الدليل الثاني. البصمة الحالية: \033[1;33m{ev2['current_event_hash'][:15]}...\033[0m")

    print("\n\033[1;36m=== 2. فحص سلامة السلسلة (Chain Verification) ===\033[0m")
    status = cv.verify_chain(child_id)
    print(f"حالة السلسلة الأصلية: \033[1;32m{status.value}\033[0m")

    print("\n\033[1;31m=== 3. محاكاة اختراق وتلاعب (Tamper Detection) ===\033[0m")
    print("نحاول الآن تغيير جهة الإصدار في الدليل الأول (بأثر رجعي)...")
    
    # محاكاة تعديل خبيث في الملف
    cv.ledger[child_id][0]["payload"]["issuer"] = "FAKE_ACADEMY"
    
    # فحص السلسلة بعد التلاعب
    tampered_status = cv.verify_chain(child_id)
    print(f"حالة السلسلة بعد التلاعب: \033[1;31m{tampered_status.value}\033[0m")
    print("النتيجة: النظام اكتشف التلاعب فوراً ورفض الدليل دون الحكم على الشخص.")
