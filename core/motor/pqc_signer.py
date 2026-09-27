import secrets
import hashlib
import json

class LamportPQCSigner:
    """
    محرك توقيع رقمي مقاوم للحوسبة الكمومية (Hash-Based PQC Signature)
    يعتمد على متانة دوال التجزئة ذات الاتجاه الواحد لمقاومة خوارزميات الكسر الكمي.
    """
    def __init__(self):
        # 1. توليد المفتاح الخاص (256 زوجاً من البايتات العشوائية لتغطية 256 بت)
        self.private_key = [
            (secrets.token_bytes(32), secrets.token_bytes(32))
            for _ in range(256)
        ]
        # 2. اشتقاق المفتاح العام عبر تجزئة كل رقم سري
        self.public_key = [
            (hashlib.sha256(pair[0]).hexdigest(), hashlib.sha256(pair[1]).hexdigest())
            for pair in self.private_key
        ]

    def get_public_key(self) -> list:
        """تصدير المفتاح العام لمشاركته مع منصات التحقق"""
        return self.public_key

    def sign_hash(self, document_sha256: str) -> list:
        """
        توقيع البصمة الرقمية للوثيقة عبر كشف العناصر المقابلة لقيم البتات
        """
        # تحويل بصمة المستند إلى سلسلة من البتات (256 بت)
        binary_string = bin(int(document_sha256, 16))[2:].zfill(256)
        signature = []

        for i, bit in enumerate(binary_string):
            if bit == '0':
                signature.append(self.private_key[i][0].hex())
            else:
                signature.append(self.private_key[i][1].hex())

        return signature

    @staticmethod
    def verify_signature(document_sha256: str, signature: list, public_key: list) -> bool:
        """
        التحقق من التوقيع بمقارنة تجزئة التوقيع مع المفتاح العام المعلن
        """
        if len(signature) != 256 or len(public_key) != 256:
            return False

        binary_string = bin(int(document_sha256, 16))[2:].zfill(256)

        for i, bit in enumerate(binary_string):
            revealed_secret = bytes.fromhex(signature[i])
            hashed_secret = hashlib.sha256(revealed_secret).hexdigest()

            # مطابقة التجزئة مع المفتاح العام المقابل لقيمة البت
            expected_public_hash = public_key[i][0] if bit == '0' else public_key[i][1]
            if hashed_secret != expected_public_hash:
                return False

        return True


if __name__ == "__main__":
    print("\033[1;36m=== 1. توليد زوج مفاتيح مقاوم للكم (PQC KeyGen) ===\033[0m")
    signer = LamportPQCSigner()
    pub_key = signer.get_public_key()
    print("تم توليد المفتاح العام المكون من 256 نقطة تحقق بنجاح.")

    # محاكاة بصمة وثيقة صادرة من النواة
    evidence_hash = hashlib.sha256("DOC://MINISTRY_EDU/KG/8899".encode('utf-8')).hexdigest()
    print(f"بصمة الوثيقة المراد توقيعها: \033[1;33m{evidence_hash}\033[0m")

    print("\n\033[1;36m=== 2. توقيع الدليل تشفيرياً (PQC Signing) ===\033[0m")
    pqc_sig = signer.sign_hash(evidence_hash)
    print(f"تم إنشاء التوقيع المقاوم للكم (حجمه 256 قطعة سرية مكشوفة).")

    print("\n\033[1;36m=== 3. فحص صحة التوقيع عبر المفتاح العام ===\033[0m")
    is_valid = LamportPQCSigner.verify_signature(evidence_hash, pqc_sig, pub_key)
    print(f"حالة التحقق الرياضي: \033[1;32m{is_valid} (VERIFIED_PQC)\033[0m")

    print("\n\033[1;31m=== 4. محاكاة محاولة تلاعب بالوثيقة الموقع عليها ===\033[0m")
    fake_hash = hashlib.sha256("DOC://MINISTRY_EDU/KG/FAKE".encode('utf-8')).hexdigest()
    tampered_check = LamportPQCSigner.verify_signature(fake_hash, pqc_sig, pub_key)
    print(f"حالة التحقق بعد التلاعب: \033[1;31m{tampered_check} (REJECTED_TAMPERED)\033[0m")
