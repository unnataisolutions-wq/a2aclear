"""
a2aclear.integrations.langchain
LangChain & LangGraph Integration Adapter for A2AClear Protocol
Allows autonomous LangChain agents to contract, lock escrow, and settle with peer agents.
"""

import json
from typing import Dict, Any, Optional
from ..identity import AgentIdentity
from ..negotiator import AutonomousNegotiator
from ..escrow import MicroEscrowVault

class A2AClearLangChainTool:
    """
    LangChain compatible tool for autonomous financial delegation and micro-escrow settlement.
    """
    
    name: str = "a2aclear_settlement"
    description: str = (
        "Use this tool to autonomously hire, lock micro-escrow, and pay another AI agent "
        "for a specific subtask using the A2AClear sovereign clearinghouse protocol."
    )

    def __init__(self, identity: Optional[AgentIdentity] = None, vault: Optional[MicroEscrowVault] = None):
        self.identity = identity or AgentIdentity.generate()
        self.vault = vault or MicroEscrowVault()
        self.negotiator = AutonomousNegotiator(self.identity)

    def run(self, action: str, **kwargs) -> str:
        """Execute settlement actions from a LangChain agent turn."""
        action = action.upper()
        
        if action == "GET_BALANCE":
            balance = self.vault.get_balance(self.identity.did)
            return json.dumps({
                "agent_did": self.identity.did,
                "balance_inr": f"₹{balance / 100:.2f}",
                "balance_paise": balance
            })
            
        elif action == "HIRE_AND_LOCK_ESCROW":
            task_id = kwargs.get("task_id", f"lc_task_{int(self.identity.did[-8:], 16)}")
            provider_did = kwargs.get("provider_did")
            amount_paise = int(kwargs.get("amount_paise", 5000))
            task_spec = kwargs.get("task_spec", {})
            
            if not provider_did:
                return json.dumps({"error": "provider_did is required to delegate task"})
                
            proposal = self.negotiator.propose_contract(
                task_id=task_id,
                provider_did=provider_did,
                initial_bid_paise=amount_paise,
                currency="INR",
                task_spec=task_spec
            )
            
            contract = self.negotiator.active_contracts[task_id]
            try:
                escrow_record = self.vault.lock_escrow(contract)
                return json.dumps({
                    "status": "ESCROW_LOCKED",
                    "escrow_id": escrow_record["escrow_id"],
                    "task_id": task_id,
                    "locked_amount_inr": f"₹{amount_paise / 100:.2f}",
                    "protocol_fee_inr": f"₹{contract.protocol_fee_paise / 100:.2f} (0.50%)"
                })
            except Exception as e:
                return json.dumps({"error": f"Failed to lock escrow: {str(e)}"})

        elif action == "SETTLE_DELIVERABLE":
            task_id = kwargs.get("task_id")
            deliverable = kwargs.get("deliverable", {})
            contract = self.negotiator.active_contracts.get(task_id)
            if not contract:
                return json.dumps({"error": f"Contract {task_id} not found"})
                
            receipt = self.vault.verify_and_settle(contract, deliverable)
            return json.dumps({
                "status": "SETTLED",
                "settlement_hash": receipt["settlement_hash"],
                "provider_payout_inr": f"₹{receipt['provider_received_paise'] / 100:.2f}",
                "protocol_fee_inr": f"₹{receipt['protocol_fee_paise'] / 100:.2f}"
            })
            
        else:
            return json.dumps({"error": f"Unknown A2AClear action: {action}"})
