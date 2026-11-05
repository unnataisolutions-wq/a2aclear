"""
a2aclear.contract
Formal Task Contract Representation & State Transitions
"""

import time
import json
import hashlib
from enum import Enum
from typing import Dict, Any, Optional

class ContractState(str, Enum):
    PROPOSED = "PROPOSED"
    NEGOTIATING = "NEGOTIATING"
    AGREED = "AGREED"
    ESCROW_LOCKED = "ESCROW_LOCKED"
    SETTLED = "SETTLED"
    DISPUTED = "DISPUTED"
    SLASHED = "SLASHED"

PROTOCOL_INTERCHANGE_BPS = 50  # 50 basis points = 0.50%

class TaskContract:
    """
    Cryptographic Bilateral Task Contract between two AI agents.
    """
    
    def __init__(
        self,
        task_id: str,
        originator_did: str,
        provider_did: str,
        amount_paise: int,
        currency: str = "INR",
        sla_timeout_seconds: int = 300,
        task_spec_hash: str = ""
    ):
        self.task_id = task_id
        self.originator_did = originator_did
        self.provider_did = provider_did
        self.amount_paise = amount_paise
        self.currency = currency
        self.sla_timeout_seconds = sla_timeout_seconds
        self.task_spec_hash = task_spec_hash
        self.created_at = int(time.time())
        self.state = ContractState.PROPOSED
        
        # Settlement allocations
        self.protocol_fee_paise = (self.amount_paise * PROTOCOL_INTERCHANGE_BPS) // 10000
        self.provider_payout_paise = self.amount_paise - self.protocol_fee_paise
        
        self.originator_signature: Optional[str] = None
        self.provider_signature: Optional[str] = None
        self.settlement_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "originator_did": self.originator_did,
            "provider_did": self.provider_did,
            "amount_paise": self.amount_paise,
            "currency": self.currency,
            "protocol_fee_paise": self.protocol_fee_paise,
            "provider_payout_paise": self.provider_payout_paise,
            "sla_timeout_seconds": self.sla_timeout_seconds,
            "task_spec_hash": self.task_spec_hash,
            "created_at": self.created_at,
            "state": self.state.value,
            "originator_signature": self.originator_signature,
            "provider_signature": self.provider_signature,
            "settlement_hash": self.settlement_hash
        }

    def compute_contract_hash(self) -> str:
        data = {
            "task_id": self.task_id,
            "originator_did": self.originator_did,
            "provider_did": self.provider_did,
            "amount_paise": self.amount_paise,
            "currency": self.currency,
            "task_spec_hash": self.task_spec_hash,
            "created_at": self.created_at
        }
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
