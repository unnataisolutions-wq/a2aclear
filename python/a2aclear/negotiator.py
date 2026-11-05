"""
a2aclear.negotiator
Autonomous Agent Negotiation Protocol (ANP) Finite-State Machine
"""

import time
import json
from typing import Dict, Any, Optional, Tuple
from .identity import AgentIdentity
from .contract import TaskContract, ContractState

class AutonomousNegotiator:
    """
    Autonomous Negotiation Protocol (ANP) Engine.
    Handles bilateral SLA negotiation, automated counter-offers, and Ed25519 countersigning.
    """
    
    def __init__(self, identity: AgentIdentity, max_budget_paise: int = 1000000):
        self.identity = identity
        self.max_budget_paise = max_budget_paise
        self.active_contracts: Dict[str, TaskContract] = {}

    def propose_contract(
        self,
        task_id: str,
        provider_did: str,
        initial_bid_paise: int,
        currency: str = "INR",
        sla_timeout_seconds: int = 300,
        task_spec: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Agent Originator proposes a task contract to a provider agent.
        """
        spec_str = json.dumps(task_spec or {}, sort_keys=True)
        import hashlib
        spec_hash = hashlib.sha256(spec_str.encode("utf-8")).hexdigest()
        
        contract = TaskContract(
            task_id=task_id,
            originator_did=self.identity.did,
            provider_did=provider_did,
            amount_paise=initial_bid_paise,
            currency=currency,
            sla_timeout_seconds=sla_timeout_seconds,
            task_spec_hash=spec_hash
        )
        
        contract_hash = contract.compute_contract_hash()
        contract.originator_signature = self.identity.sign(contract_hash.encode("utf-8")).hex()
        contract.state = ContractState.PROPOSED
        self.active_contracts[task_id] = contract
        
        return self.identity.sign_envelope(
            payload=contract.to_dict(),
            action="PROPOSE_CONTRACT",
            recipient_did=provider_did
        )

    def evaluate_proposal(
        self,
        envelope: Dict[str, Any],
        minimum_acceptable_paise: int
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Agent Provider evaluates an incoming proposal envelope.
        Returns ("ACCEPT" | "COUNTER" | "REJECT", response_envelope).
        """
        if not AgentIdentity.verify_envelope(envelope):
            raise ValueError("Cryptographic envelope signature verification failed.")
            
        payload = envelope["payload"]
        task_id = payload["task_id"]
        offered_amount = payload["amount_paise"]
        originator_did = envelope["sender_did"]
        
        if offered_amount >= minimum_acceptable_paise:
            # Accept and countersign
            contract = TaskContract(
                task_id=task_id,
                originator_did=originator_did,
                provider_did=self.identity.did,
                amount_paise=offered_amount,
                currency=payload.get("currency", "INR"),
                sla_timeout_seconds=payload.get("sla_timeout_seconds", 300),
                task_spec_hash=payload.get("task_spec_hash", "")
            )
            contract_hash = contract.compute_contract_hash()
            contract.originator_signature = payload.get("originator_signature")
            contract.provider_signature = self.identity.sign(contract_hash.encode("utf-8")).hex()
            contract.state = ContractState.AGREED
            self.active_contracts[task_id] = contract
            
            resp_env = self.identity.sign_envelope(
                payload=contract.to_dict(),
                action="ACCEPT_CONTRACT",
                recipient_did=originator_did
            )
            return "ACCEPT", resp_env
        else:
            # Counter-offer with minimum price
            counter_payload = dict(payload)
            counter_payload["amount_paise"] = minimum_acceptable_paise
            counter_payload["counter_reason"] = "Requested price below compute/inference margin threshold."
            
            resp_env = self.identity.sign_envelope(
                payload=counter_payload,
                action="COUNTER_BID",
                recipient_did=originator_did
            )
            return "COUNTER", resp_env
