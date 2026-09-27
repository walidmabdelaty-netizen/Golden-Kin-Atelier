import re
import json
import base64
import time
from typing import Dict, Any, Tuple

# الثوابت المعيارية للمواصفة v1.1
SCHEMA_VERSION = "v1.1"
PROTOCOL_VERSION = "v1.0"
ALLOWED_PACKET_TYPES = {"CONTRACT", "AUDIT_RECORD", "EVIDENCE", "KEY_MATERIAL"}
ALLOWED_CLASSIFICATIONS = {"INTERNAL", "RESTRICTED"}
ALLOWED_CRYPTO_SUITES = {"VSS-AES256GCM-MLKEM768-ED25519-v1"}
ALLOWED_KEM_ALGS = {"ML-KEM-768"}
ALLOWED_SIG_ALGS = {"Ed25519", "ML-DSA-65"}

# سياسة التوقيت: أقصى انحراف مستقبلي 60 ثانية، وأقصى عمر للحزمة 3600 ثانية
MAX_CLOCK_SKEW_SEC = 60
MAX_PACKET_AGE_SEC = 3600

UUID_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")

def canonical_bytes(data: Dict[str, Any]) -> bytes:
    """تحويل حتمي منضبط للبايتات لمنع اختلاف التجزئة عبر المنصات"""
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('utf-8')

def is_valid_base64(data: Any, expected_length: int = None) -> bool:
    if not isinstance(data, str):
        return False
    try:
        decoded = base64.b64decode(data, validate=True)
        if expected_length is not None and len(decoded) != expected_length:
            return False
        return True
    except Exception:
        return False

def validate_verdix_packet_v1(packet: Dict[str, Any], current_time: int = None) -> Tuple[bool, str]:
    if not isinstance(packet, dict):
        return False, "Packet must be a dictionary"

    required_sections = {"header", "kem_envelope", "payload", "proof"}
    if set(packet.keys()) != required_sections:
        return False, f"Packet root keys mismatch. Expected exactly: {required_sections}"

    now = int(time.time()) if current_time is None else current_time

    # 1. تدقيق الـ Header
    h = packet.get("header", {})
    if not isinstance(h, dict):
        return False, "Header must be a dictionary"

    if h.get("schema_version") != SCHEMA_VERSION:
        return False, f"Unsupported schema_version: {h.get('schema_version')}"
    if h.get("protocol_version") != PROTOCOL_VERSION:
        return False, f"Unsupported protocol_version: {h.get('protocol_version')}"
    if not UUID_REGEX.match(str(h.get("packet_id", ""))):
        return False, "packet_id must be a valid UUIDv4"
    if h.get("packet_type") not in ALLOWED_PACKET_TYPES:
        return False, f"Invalid packet_type: {h.get('packet_type')}"

    created_at = h.get("created_at")
    # استبعاد نوع bool صراحة لأن bool فرع من int في Python
    if type(created_at) is not int:
        return False, "created_at must be an integer Unix timestamp"
    if created_at > now + MAX_CLOCK_SKEW_SEC:
        return False, "created_at is too far in the future (clock skew violation)"
    if created_at < now - MAX_PACKET_AGE_SEC:
        return False, "created_at is expired (exceeds MAX_PACKET_AGE_SEC)"

    if h.get("classification") not in ALLOWED_CLASSIFICATIONS:
        return False, f"Invalid classification: {h.get('classification')}"
    if h.get("crypto_suite") not in ALLOWED_CRYPTO_SUITES:
        return False, f"Unsupported crypto_suite: {h.get('crypto_suite')}"
    if not isinstance(h.get("issuer_id"), str) or not h.get("issuer_id"):
        return False, "issuer_id must be a non-empty string"

    # 2. تدقيق الـ KEM Envelope
    k = packet.get("kem_envelope", {})
    if not isinstance(k, dict):
        return False, "kem_envelope must be a dictionary"
    if k.get("algorithm") not in ALLOWED_KEM_ALGS:
        return False, f"Unsupported KEM algorithm: {k.get('algorithm')}"
    if not isinstance(k.get("key_id"), str) or not k.get("key_id"):
        return False, "key_id in kem_envelope must be a non-empty string"
    if not is_valid_base64(k.get("encapsulated_key"), expected_length=1088):
        return False, "encapsulated_key must be Base64-encoded bytes of length 1088"

    # 3. تدقيق الـ Payload
    p = packet.get("payload", {})
    if not isinstance(p, dict):
        return False, "payload must be a dictionary"
    if not is_valid_base64(p.get("nonce"), expected_length=12):
        return False, "nonce must be Base64-encoded bytes of length 12"
    if not is_valid_base64(p.get("auth_tag"), expected_length=16):
        return False, "auth_tag must be Base64-encoded bytes of length 16"
    if not is_valid_base64(p.get("ciphertext")):
        return False, "ciphertext must be valid Base64-encoded bytes"

    # 4. تدقيق الـ Proof
    pr = packet.get("proof", {})
    if not isinstance(pr, dict):
        return False, "proof must be a dictionary"
    if pr.get("signature_algorithm") not in ALLOWED_SIG_ALGS:
        return False, f"Unsupported signature_algorithm: {pr.get('signature_algorithm')}"
    if not isinstance(pr.get("signing_key_id"), str) or not pr.get("signing_key_id"):
        return False, "signing_key_id must be a non-empty string"
    if not is_valid_base64(pr.get("signature")):
        return False, "signature must be valid Base64-encoded bytes"

    return True, "SCHEMA_V1_VALIDATED"
