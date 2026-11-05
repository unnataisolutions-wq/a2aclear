"""
a2aclear.identity
Cryptographic Agent Identity & Sovereign DID Management (Ed25519)
"""

import os
import time
import json
import base64
import hashlib
from typing import Dict, Any, Tuple
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class AgentIdentity:
    """
    Sovereign Cryptographic Identity for an Autonomous AI Agent.
    Generates and manages Ed25519 asymmetric keypairs and A2AClear DIDs.
    Format: did:a2a:<64-character-hex-encoded-public-key>
    """
    
    def __init__(self, private_key: ed25519.Ed25519PrivateKey = None):
        if private_key is None:
            self._private_key = ed25519.Ed25519PrivateKey.generate()
        else:
            self._private_key = private_key
            
        self._public_key = self._private_key.public_key()
        pub_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        self.pubkey_hex = pub_bytes.hex()
        self.did = f"did:a2a:{self.pubkey_hex}"

    @classmethod
    def generate(cls) -> "AgentIdentity":
        """Generate a new ephemeral or persistent Agent Identity."""
        return cls()

    @classmethod
    def from_seed(cls, seed: bytes) -> "AgentIdentity":
        """Derive an Agent Identity deterministically from a 32-byte seed."""
        if len(seed) < 32:
            seed = hashlib.sha256(seed).digest()
        else:
            seed = seed[:32]
        priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
        return cls(priv)

    @classmethod
    def from_private_hex(cls, hex_str: str) -> "AgentIdentity":
        """Load Agent Identity from private key hex string."""
        raw_bytes = bytes.fromhex(hex_str.strip())
        priv = ed25519.Ed25519PrivateKey.from_private_bytes(raw_bytes)
        return cls(priv)

    def export_private_hex(self) -> str:
        """Export private key as hex string."""
        raw_bytes = self._private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        return raw_bytes.hex()

    def sign(self, data: bytes) -> bytes:
        """Sign arbitrary byte payload using Ed25519."""
        return self._private_key.sign(data)

    def sign_envelope(self, payload: Dict[str, Any], action: str, recipient_did: str = "*") -> Dict[str, Any]:
        """
        Create a cryptographically signed A2AClear Envelope.
        """
        envelope = {
            "a2a_version": "1.0.0",
            "sender_did": self.did,
            "recipient_did": recipient_did,
            "timestamp": int(time.time()),
            "nonce": int.from_bytes(os.urandom(8), "big"),
            "action": action,
            "payload": payload
        }
        canonical_str = json.dumps(envelope, sort_keys=True, separators=(",", ":"))
        signature_bytes = self.sign(canonical_str.encode("utf-8"))
        envelope["signature"] = signature_bytes.hex()
        return envelope

    @staticmethod
    def verify_envelope(envelope: Dict[str, Any]) -> bool:
        """
        Verify the Ed25519 signature of an incoming A2AClear envelope.
        """
        try:
            env_copy = dict(envelope)
            signature_hex = env_copy.pop("signature", None)
            if not signature_hex:
                return False
            
            sender_did = env_copy.get("sender_did", "")
            if not sender_did.startswith("did:a2a:"):
                return False
            
            pubkey_hex = sender_did.replace("did:a2a:", "").strip()
            pub_bytes = bytes.fromhex(pubkey_hex)
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
            
            canonical_str = json.dumps(env_copy, sort_keys=True, separators=(",", ":"))
            pub_key.verify(bytes.fromhex(signature_hex), canonical_str.encode("utf-8"))
            return True
        except Exception:
            return False
