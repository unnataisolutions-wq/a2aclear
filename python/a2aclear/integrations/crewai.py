"""
a2aclear.integrations.crewai
CrewAI Multi-Agent Swarm Financial Settlement Adapter
Enables autonomous financial settlements between members of a CrewAI swarm.
"""

import json
from typing import Dict, Any, List, Optional
from ..identity import AgentIdentity
from ..contract import TaskContract
from ..escrow import MicroEscrowVault

class A2ACrewSettlementHandler:
    """
    Financial manager for CrewAI swarms.
    Assigns Ed25519 identities to each crew agent and manages inter-agent micropayments.
    """
    
    def __init__(self, crew_name: str = "UnnatEnterpriseSwarm"):
        self.crew_name = crew_name
        self.vault = MicroEscrowVault()
        self.agent_identities: Dict[str, AgentIdentity] = {}

    def register_crew_agent(self, agent_role: str, initial_deposit_paise: int = 10000) -> AgentIdentity:
        """Assign an Ed25519 identity to a crew agent and fund its balance."""
        identity = AgentIdentity.generate()
        self.agent_identities[agent_role] = identity
        if initial_deposit_paise > 0:
            self.vault.deposit(identity.did, initial_deposit_paise)
        return identity

    def settle_crew_step(
        self,
        from_role: str,
        to_role: str,
        task_name: str,
        step_cost_paise: int,
        task_output: Any
    ) -> Dict[str, Any]:
        """
        Executes an atomic micro-settlement when one crew agent hands off work to another.
        """
        buyer = self.agent_identities.get(from_role) or self.register_crew_agent(from_role)
        seller = self.agent_identities.get(to_role) or self.register_crew_agent(to_role, initial_deposit_paise=0)

        contract = TaskContract(
            task_id=f"crew_{from_role}_{to_role}_{task_name}",
            originator_did=buyer.did,
            provider_did=seller.did,
            amount_paise=step_cost_paise,
            currency="INR"
        )

        self.vault.lock_escrow(contract)
        receipt = self.vault.verify_and_settle(contract, task_output)
        
        return {
            "success": True,
            "task": task_name,
            "from": from_role,
            "to": to_role,
            "settled_hash": receipt["settlement_hash"],
            "worker_received_paise": receipt["provider_received_paise"],
            "protocol_fee_paise": receipt["protocol_fee_paise"]
        }
