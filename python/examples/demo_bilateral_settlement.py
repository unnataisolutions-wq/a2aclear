#!/usr/bin/env python3
"""
A2AClear Bilateral Settlement Demo
Demonstrates autonomous negotiation, escrow locking, deliverable verification,
and 0.50% protocol fee clearing between two autonomous AI agents in under 10ms.

(C) 2026 Unnat AI Solutions. Chief Systems Architect: Rohit.
"""

import sys
import os
import time
import json

# Ensure a2aclear is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from a2aclear import (
    AgentIdentity,
    AutonomousNegotiator,
    MicroEscrowVault,
    ContractState,
    PROTOCOL_INTERCHANGE_BPS
)

def main():
    print("=" * 80)
    print("🌐 A2ACLEAR: SOVEREIGN AGENT-TO-AGENT SETTLEMENT PROTOCOL (RFC-0001)")
    print("   Standard Protocol Engine - (C) 2026 Unnat AI Solutions | Rohit")
    print("=" * 80)
    
    start_time = time.perf_counter()
    
    # 1. Initialize Autonomous Identities (Ed25519)
    print("\n[Step 1] Initializing Autonomous Agent Identities...")
    agent_originator = AgentIdentity.generate()
    agent_provider = AgentIdentity.generate()
    clearinghouse_master = AgentIdentity.generate()
    
    print(f"  • Buyer Agent (LeadGen AI)  DID: {agent_originator.did[:32]}...")
    print(f"  • Seller Agent (Parser AI)  DID: {agent_provider.did[:32]}...")
    print(f"  • Clearinghouse Master      DID: {clearinghouse_master.did[:32]}...")
    
    # 2. Setup Shared Sovereign Micro-Escrow Vault
    print("\n[Step 2] Provisioning Sovereign Micro-Escrow Vault...")
    vault = MicroEscrowVault(treasury_did=clearinghouse_master.did)
    
    # Pre-fund Buyer Agent with ₹100.00 (10,000 paise)
    vault.deposit(agent_originator.did, 10000, funding_source="UPI_AUTONOMOUS_AUTOPAY")
    print(f"  • Buyer Agent Vault Balance: ₹{vault.get_balance(agent_originator.did)/100:.2f} INR")
    print(f"  • Seller Agent Vault Balance: ₹{vault.get_balance(agent_provider.did)/100:.2f} INR")
    print(f"  • Protocol Treasury Balance: ₹{vault.get_balance(clearinghouse_master.did)/100:.2f} INR")
    
    # 3. Autonomous Negotiation Protocol (ANP)
    print("\n[Step 3] Autonomous Bilateral Contract Negotiation...")
    buyer_negotiator = AutonomousNegotiator(agent_originator)
    seller_negotiator = AutonomousNegotiator(agent_provider)
    
    task_id = "task_jamabandi_b2b_extract_8901"
    task_spec = {
        "service": "HARYANA_JAMABANDI_DEEP_PARSE",
        "tehsil": "Pehowa",
        "khasra_no": "12//4/1",
        "format": "JSON_CANONICAL"
    }
    
    # Buyer proposes contract for ₹50.00 (5,000 paise)
    proposal_envelope = buyer_negotiator.propose_contract(
        task_id=task_id,
        provider_did=agent_provider.did,
        initial_bid_paise=5000,
        currency="INR",
        sla_timeout_seconds=60,
        task_spec=task_spec
    )
    print(f"  • Buyer broadcasted signed proposal envelope (Action: {proposal_envelope['action']})")
    
    # Seller evaluates proposal (minimum acceptable = ₹40.00)
    decision, response_envelope = seller_negotiator.evaluate_proposal(
        proposal_envelope,
        minimum_acceptable_paise=4000
    )
    print(f"  • Seller evaluated proposal -> Decision: {decision}")
    
    agreed_contract = seller_negotiator.active_contracts[task_id]
    print(f"  • Bilateral contract agreed! State: {agreed_contract.state.value}")
    print(f"    - Agreed Price: ₹{agreed_contract.amount_paise / 100:.2f}")
    print(f"    - Protocol Clearing Fee (0.50%): ₹{agreed_contract.protocol_fee_paise / 100:.2f}")
    print(f"    - Seller Payout (99.50%): ₹{agreed_contract.provider_payout_paise / 100:.2f}")
    
    # 4. Lock Programmable Micro-Escrow
    print("\n[Step 4] Locking Funds in Programmable Micro-Escrow...")
    escrow_record = vault.lock_escrow(agreed_contract)
    print(f"  • Escrow ID: {escrow_record['escrow_id']}")
    print(f"  • Status: {escrow_record['status']}")
    print(f"  • Buyer Remaining Balance: ₹{vault.get_balance(agent_originator.did)/100:.2f}")
    
    # 5. Agent Provider Executes Task & Generates Deliverable
    print("\n[Step 5] Autonomous Worker Execution...")
    deliverable = {
        "status": "SUCCESS",
        "khasra_no": "12//4/1",
        "owner": "Sovereign Enterprise",
        "area_gaj": 4840,
        "encumbrance": "CLEAN_TITLED",
        "parsed_by": agent_provider.did
    }
    print(f"  • Worker computed payload: {json.dumps(deliverable)[:60]}...")
    
    # 6. Atomic Cryptographic Settlement
    print("\n[Step 6] Atomic Verification & Protocol Clearing...")
    settlement_receipt = vault.verify_and_settle(
        contract=agreed_contract,
        deliverable_artifact=deliverable,
        clearinghouse_identity=clearinghouse_master
    )
    
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    print("\n" + "=" * 80)
    print("✅ SETTLEMENT COMPLETE — CRYPTOGRAPHIC RECEIPT")
    print("=" * 80)
    print(f"  • Settlement Hash:        {settlement_receipt['settlement_hash']}")
    print(f"  • Deliverable SHA-256:     {settlement_receipt['deliverable_hash']}")
    print(f"  • Gross Amount:            ₹{settlement_receipt['gross_amount_paise'] / 100:.2f} INR")
    print(f"  • Seller Received (99.5%): ₹{settlement_receipt['provider_received_paise'] / 100:.2f} INR")
    print(f"  • A2AClear Protocol Fee:   ₹{settlement_receipt['protocol_fee_paise'] / 100:.2f} INR (0.50% retained)")
    print(f"  • Clearinghouse Signature: {settlement_receipt['clearinghouse_signature'][:40]}...")
    print(f"  • Total Pipeline Latency:  {elapsed_ms:.2f} ms")
    
    print("\n[Final Balances]")
    print(f"  • Buyer Agent Balance:     ₹{vault.get_balance(agent_originator.did)/100:.2f}")
    print(f"  • Seller Agent Balance:    ₹{vault.get_balance(agent_provider.did)/100:.2f}")
    print(f"  • Protocol Treasury:       ₹{vault.get_balance(clearinghouse_master.did)/100:.2f} (Permanent protocol tollgate)")
    print("=" * 80)
    print("🏆 A2AClear verified operational: Autonomous Agent Commerce Rail is LIVE!\n")

if __name__ == "__main__":
    main()
