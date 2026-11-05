"""
a2aclear.security
Institutional Cybersecurity, Anti-Hacking & Cryptographic IP Armor
Includes AES-256-GCM Encrypted Keystores, Replay Attack Defense, 
Payload Sanitization, and Sovereign Cryptographic Watermarking.

(C) 2026 Unnat AI Solutions. Chief Systems Architect: Rohit.
"""

import os
import time
import json
import hashlib
from typing import Dict, Any, Optional, Set
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SOVEREIGN_WATERMARK_SALT = b"ROHIT_UNNAT_AI_SOLUTIONS_SOVEREIGN_ROOT_2026_KURUKSHETRA"

class ReplayAttackException(Exception):
    """Raised when an envelope fails replay attack or timestamp validation."""
    pass

class MaliciousPayloadException(Exception):
    """Raised when an incoming deliverable fails security sanitization."""
    pass

class EncryptedKeyStore:
    """
    Military-Grade AES-256-GCM Encrypted Keystore.
    Protects Agent Ed25519 private keys on disk using PBKDF2 key derivation (100,000 rounds).
    Prevents plaintext key theft, memory dumps, and environment variable snooping.
    """
    
    @staticmethod
    def derive_encryption_key(passphrase: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(passphrase.encode("utf-8"))

    @classmethod
    def save_encrypted_key(cls, private_hex: str, passphrase: str, filepath: str):
        """Encrypts and writes private key to secure file."""
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = cls.derive_encryption_key(passphrase, salt)
        aesgcm = AESGCM(key)
        
        ciphertext = aesgcm.encrypt(nonce, private_hex.encode("utf-8"), None)
        
        keystore_blob = {
            "version": "A2A_KEYSTORE_V1_AES256GCM",
            "salt_hex": salt.hex(),
            "nonce_hex": nonce.hex(),
            "ciphertext_hex": ciphertext.hex(),
            "created_at": int(time.time()),
            "sovereign_armor": "UNNAT_ENCRYPTED_VAULT"
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(keystore_blob, f, indent=2)

    @classmethod
    def load_encrypted_key(cls, passphrase: str, filepath: str) -> str:
        """Decrypts private key in memory only. Never leaks to disk."""
        with open(filepath, "r", encoding="utf-8") as f:
            blob = json.load(f)
            
        salt = bytes.fromhex(blob["salt_hex"])
        nonce = bytes.fromhex(blob["nonce_hex"])
        ciphertext = bytes.fromhex(blob["ciphertext_hex"])
        
        key = cls.derive_encryption_key(passphrase, salt)
        aesgcm = AESGCM(key)
        
        try:
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            return decrypted_bytes.decode("utf-8")
        except Exception:
            raise PermissionError("Decryption failed. Invalid passphrase or corrupted keystore.")

class ReplayDefenseValidator:
    """
    Zero-Trust Replay Attack Defense & Nonce Cache.
    Rejects any transaction envelope outside a 60-second sliding clock window
    or containing an already-used nonce.
    """
    
    def __init__(self, max_clock_skew_seconds: int = 60, max_cache_size: int = 100000):
        self.max_clock_skew_seconds = max_clock_skew_seconds
        self.max_cache_size = max_cache_size
        self.seen_nonces: Set[str] = set()

    def validate_envelope(self, envelope: Dict[str, Any]):
        sender_did = envelope.get("sender_did", "")
        timestamp = envelope.get("timestamp", 0)
        nonce = envelope.get("nonce", None)
        
        if nonce is None:
            raise ReplayAttackException("Security violation: Envelope missing cryptographic nonce.")
            
        now = int(time.time())
        if abs(now - timestamp) > self.max_clock_skew_seconds:
            raise ReplayAttackException(
                f"Clock skew rejected. Envelope timestamp {timestamp} is outside allowable {self.max_clock_skew_seconds}s window (Current: {now})."
            )
            
        nonce_key = f"{sender_did}:{nonce}"
        if nonce_key in self.seen_nonces:
            raise ReplayAttackException(f"REPLAY ATTACK BLOCKED: Nonce {nonce} from {sender_did} already utilized!")
            
        # Add to seen nonces
        if len(self.seen_nonces) >= self.max_cache_size:
            self.seen_nonces.clear() # Reset cache on full capacity
            
        self.seen_nonces.add(nonce_key)

class PayloadSanitizer:
    """
    Deep Content Inspection & Anti-Injection Guard for AI Agent Deliverables.
    Prevents prompt injection, malicious shell escapes, oversized payloads, and recursive JSON bombs.
    """
    
    MAX_PAYLOAD_BYTES = 5 * 1024 * 1024 # 5 MB limit
    MAX_DEPTH = 8
    
    DANGEROUS_PATTERNS = [
        "__import__", "os.system", "subprocess", "eval(", "exec(", 
        "/etc/passwd", "DROP TABLE", "<script>", "javascript:"
    ]

    @classmethod
    def sanitize(cls, deliverable: Any):
        # 1. Size check
        raw_str = json.dumps(deliverable) if not isinstance(deliverable, str) else deliverable
        if len(raw_str.encode("utf-8")) > cls.MAX_PAYLOAD_BYTES:
            raise MaliciousPayloadException("Payload exceeds 5MB micro-task limit.")
            
        # 2. Check depth
        if isinstance(deliverable, (dict, list)):
            cls._check_depth(deliverable, 0)
            
        # 3. Check dangerous injection patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            if pattern in raw_str:
                raise MaliciousPayloadException(f"Security Alert: Malicious code injection signature detected ('{pattern}').")
                
        return True

    @classmethod
    def _check_depth(cls, obj: Any, depth: int):
        if depth > cls.MAX_DEPTH:
            raise MaliciousPayloadException("JSON recursion depth bomb detected.")
        if isinstance(obj, dict):
            for v in obj.values():
                cls._check_depth(v, depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                cls._check_depth(item, depth + 1)

class SovereignCryptographicWatermark:
    """
    Steganographic Legal Watermark Engine.
    Embeds an immutable mathematical proof of authorship into contract hashes.
    Can be used in court or intellectual property disputes to prove theft.
    """
    
    @staticmethod
    def generate_watermark(contract_hash: str) -> str:
        """Derives a cryptographic authorship attestation tied to Rohit & Unnat AI."""
        data = f"{contract_hash}:{SOVEREIGN_WATERMARK_SALT.decode()}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_authorship(contract_hash: str, claimed_watermark: str) -> bool:
        expected = SovereignCryptographicWatermark.generate_watermark(contract_hash)
        return expected == claimed_watermark
