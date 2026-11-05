"""
a2aclear.reputation
Sovereign Reputation Ledger & Collateral Staking Defense System
Maintains mathematical agent reputation, trust scores, and anti-sybil collateral slashing.
"""

import time
import math
from typing import Dict, Any, Optional

class AgentReputationLedger:
    """
    Sovereign Decentralized Reputation & Collateral Staking Engine.
    Computes deterministic reputation metrics based on historical contract execution proofs.
    """
    
    def __init__(self):
        # did -> record
        self.records: Dict[str, Dict[str, Any]] = {}

    def get_or_create(self, did: str) -> Dict[str, Any]:
        if did not in self.records:
            self.records[did] = {
                "did": did,
                "created_at": int(time.time()),
                "total_tasks_attempted": 0,
                "total_tasks_completed": 0,
                "total_volume_settled_paise": 0,
                "sla_breaches": 0,
                "slashed_count": 0,
                "collateral_staked_paise": 0,
                "is_blacklisted": False,
                "reputation_score": 100.0 # Base score for authenticated Ed25519 node
            }
        return self.records[did]

    def stake_collateral(self, did: str, amount_paise: int):
        """Stake bonding collateral to unlock high-tier B2B agent contracts."""
        record = self.get_or_create(did)
        if record["is_blacklisted"]:
            raise PermissionError("Blacklisted agent node cannot stake collateral.")
        record["collateral_staked_paise"] += amount_paise
        self.recompute_score(did)

    def record_settlement(self, did: str, volume_paise: int, latency_ms: float, sla_target_ms: float):
        """Record a successful atomic settlement proof."""
        record = self.get_or_create(did)
        if record["is_blacklisted"]:
            return
            
        record["total_tasks_attempted"] += 1
        record["total_tasks_completed"] += 1
        record["total_volume_settled_paise"] += volume_paise
        
        if latency_ms > sla_target_ms:
            record["sla_breaches"] += 1
            
        self.recompute_score(did)

    def record_slash(self, did: str, reason: str) -> int:
        """Slash 100% of collateral upon malicious behavior or cryptographic forgery."""
        record = self.get_or_create(did)
        record["slashed_count"] += 1
        record["is_blacklisted"] = True
        record["reputation_score"] = 0.0
        slashed_amount = record["collateral_staked_paise"]
        record["collateral_staked_paise"] = 0
        record["slash_reason"] = reason
        return slashed_amount

    def recompute_score(self, did: str) -> float:
        """
        Mathematical Reputation Formula:
        R = 0.50 * CompletionRatio + 0.30 * SLARatio + 0.20 * VolumeLog - SlashedPenalty
        """
        record = self.records[did]
        if record["is_blacklisted"]:
            return 0.0
            
        total = record["total_tasks_attempted"]
        if total == 0:
            return 100.0
            
        completed = record["total_tasks_completed"]
        breaches = record["sla_breaches"]
        
        completion_ratio = (completed / total) * 100.0
        sla_ratio = max(0.0, ((total - breaches) / total) * 100.0)
        
        volume_inr = record["total_volume_settled_paise"] / 100.0
        volume_boost = min(100.0, math.log10(max(1.0, volume_inr)) * 20.0)
        
        score = (0.50 * completion_ratio) + (0.35 * sla_ratio) + (0.15 * volume_boost)
        record["reputation_score"] = round(min(100.0, max(0.0, score)), 2)
        return record["reputation_score"]
