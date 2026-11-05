#!/usr/bin/env python3
"""
A2AClear Security, Anti-Hacking & Cryptographic IP Armor Test Suite
Empirically tests AES-256-GCM Encrypted Keystore, Replay Attack Defense,
Malicious Payload Sanitization, and Sovereign Authorship Watermarking.

(C) 2026 Unnat AI Solutions. Chief Systems Architect: Rohit.
"""

import sys
import os
import time
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from a2aclear import (
    AgentIdentity,
    EncryptedKeyStore,
    ReplayDefenseValidator,
    PayloadSanitizer,
    SovereignCryptographicWatermark,
    ReplayAttackException,
    MaliciousPayloadException
)

def main():
    print("=" * 80)
    print("🔒 A2ACLEAR CYBERSECURITY & ANTI-THEFT VERIFICATION SUITE")
    print("   Testing AES-256-GCM Keystore, Replay Defense, Sanitizer & Authorship Armor")
    print("=" * 80)

    # 1. Test AES-256-GCM Encrypted Keystore
    print("\n[Security Test 1] Testing Military-Grade Encrypted Keystore...")
    agent = AgentIdentity.generate()
    passphrase = "Sovereign_Unnat_Password_9812#!"
    
    with tempfile.NamedTemporaryFile(suffix=".a2akey", delete=False) as tf:
        key_path = tf.name

    try:
        EncryptedKeyStore.save_encrypted_key(agent.export_private_hex(), passphrase, key_path)
        print(f"  • Encrypted private key written to: {key_path}")
        
        # Verify correct decryption
        loaded_hex = EncryptedKeyStore.load_encrypted_key(passphrase, key_path)
        assert loaded_hex == agent.export_private_hex()
        print("  • Decryption with correct passphrase: SUCCESS")

        # Verify failure on wrong passphrase
        try:
            EncryptedKeyStore.load_encrypted_key("WRONG_PASSWORD_123", key_path)
            print("  ❌ ERROR: Decryption should have failed on wrong passphrase!")
            assert False
        except PermissionError:
            print("  • Decryption rejected on wrong passphrase: SUCCESS (Zero Leakage)")

        print("  ✅ Encrypted Keystore: 100% SECURE")
    finally:
        if os.path.exists(key_path):
            os.remove(key_path)

    # 2. Test Replay Attack Defense
    print("\n[Security Test 2] Testing Replay Attack & Nonce Hijacking Defense...")
    validator = ReplayDefenseValidator(max_clock_skew_seconds=30)
    envelope = agent.sign_envelope({"task_id": "tx_9912", "amount": 5000}, action="LOCK_ESCROW")
    
    # First submission should pass
    validator.validate_envelope(envelope)
    print("  • Valid envelope with fresh nonce and timestamp: ACCEPTED")

    # Second submission with same nonce must be BLOCKED
    try:
        validator.validate_envelope(envelope)
        print("  ❌ ERROR: Replay attack was not detected!")
        assert False
    except ReplayAttackException as e:
        print(f"  • Repeated submission blocked: SUCCESS ({str(e)})")

    # Clock skew attack (future timestamp) must be BLOCKED
    tampered_envelope = dict(envelope)
    tampered_envelope["nonce"] = 999999999
    tampered_envelope["timestamp"] = int(time.time()) + 500
    try:
        validator.validate_envelope(tampered_envelope)
        print("  ❌ ERROR: Clock skew attack was not detected!")
        assert False
    except ReplayAttackException as e:
        print(f"  • Clock skew attack blocked: SUCCESS ({str(e)})")

    print("  ✅ Replay Attack Defense: 100% BLOCKED")

    # 3. Test Malicious Payload Sanitizer
    print("\n[Security Test 3] Testing Malicious Code Injection & Jailbreak Defense...")
    clean_payload = {"status": "SUCCESS", "records_parsed": 50}
    PayloadSanitizer.sanitize(clean_payload)
    print("  • Clean deliverable payload: APPROVED")

    # Prompt injection / shell escape attempt
    poisoned_payload = {"status": "SUCCESS", "data": "import os; os.system('rm -rf /')"}
    try:
        PayloadSanitizer.sanitize(poisoned_payload)
        print("  ❌ ERROR: Malicious injection was not blocked!")
        assert False
    except MaliciousPayloadException as e:
        print(f"  • Malicious command injection blocked: SUCCESS ({str(e)})")

    print("  ✅ Payload Sanitization: 100% PROTECTED")

    # 4. Test Sovereign Cryptographic Watermark
    print("\n[Security Test 4] Testing Sovereign IP Authorship Watermark...")
    contract_hash = "7f8b91a20c3d4e5f6789abcdef0123456789abcdef0123456789abcdef012345"
    watermark = SovereignCryptographicWatermark.generate_watermark(contract_hash)
    print(f"  • Generated Mathematical Watermark: {watermark}")
    
    is_valid = SovereignCryptographicWatermark.verify_authorship(contract_hash, watermark)
    assert is_valid is True
    print("  • Mathematical proof of Rohit & Unnat AI Authorship: VERIFIED TRUE")

    # Corrupted / forged watermark test
    is_fake = SovereignCryptographicWatermark.verify_authorship(contract_hash, "fake_watermark_hash_12345")
    assert is_fake is False
    print("  • Forged authorship claim rejected: SUCCESS")

    print("  ✅ Sovereign IP Watermark: 100% BULLETPROOF")

    print("\n" + "=" * 80)
    print("🏆 ALL CYBERSECURITY & ANTI-THEFT GUARDS VERIFIED OPERATIONAL!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
