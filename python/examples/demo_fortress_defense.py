#!/usr/bin/env python3
"""
A2AClear Fortress Defense Verification Script
Empirically tests LangChain tools, CrewAI swarms, Reputation scoring,
and Sovereign Banking Bridge.

(C) 2026 Unnat AI Solutions. Chief Systems Architect: Rohit.
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from a2aclear import (
    AgentIdentity,
    AutonomousNegotiator,
    MicroEscrowVault,
    AgentReputationLedger,
    SovereignFiatBridge
)
from a2aclear.integrations import A2AClearLangChainTool, A2ACrewSettlementHandler

def main():
    print("=" * 80)
    print("🛡️ A2ACLEAR FORTRESS DEFENSE & ECOSYSTEM VERIFICATION")
    print("   Testing Moats: LangChain Tool, CrewAI Swarm, Reputation, and Banking Bridge")
    print("=" * 80)

    # 1. Test LangChain Tool
    print("\n[Moat 1] Verifying LangChain Agent Tool Integration...")
    lc_tool = A2AClearLangChainTool()
    lc_tool.vault.deposit(lc_tool.identity.did, 20000)
    balance_resp = json.loads(lc_tool.run("GET_BALANCE"))
    print(f"  • LangChain Agent DID: {balance_resp['agent_did'][:32]}...")
    print(f"  • Vault Balance:       {balance_resp['balance_inr']}")
    assert balance_resp["balance_paise"] == 20000
    print("  ✅ LangChain Integration: PASSED")

    # 2. Test CrewAI Swarm Settlement
    print("\n[Moat 2] Verifying CrewAI Multi-Agent Swarm Settlement...")
    crew_handler = A2ACrewSettlementHandler(crew_name="EnterpriseLeadsCrew")
    researcher = crew_handler.register_crew_agent("lead_researcher", 15000)
    parser = crew_handler.register_crew_agent("document_parser", 0)

    step_result = crew_handler.settle_crew_step(
        from_role="lead_researcher",
        to_role="document_parser",
        task_name="extract_gst_records",
        step_cost_paise=3500, # ₹35.00
        task_output={"gstins": ["06AABCU1234F1Z5"], "status": "VERIFIED"}
    )
    print(f"  • Crew Step Settlement Hash: {step_result['settled_hash'][:32]}...")
    print(f"  • Worker Received:           ₹{step_result['worker_received_paise']/100:.2f} INR")
    print(f"  • Protocol Toll Collected:   ₹{step_result['protocol_fee_paise']/100:.2f} INR (0.50%)")
    assert step_result["protocol_fee_paise"] == 17 # 3500 * 0.005 = 17.5 -> 17 paise
    print("  ✅ CrewAI Swarm Settlement: PASSED")

    # 3. Test Reputation Engine & Slashing Defense
    print("\n[Moat 3] Verifying Sovereign Reputation & Slashing Engine...")
    rep_ledger = AgentReputationLedger()
    good_agent = AgentIdentity.generate()
    bad_agent = AgentIdentity.generate()

    # Good agent completes 10 tasks with fast latency
    for _ in range(10):
        rep_ledger.record_settlement(good_agent.did, volume_paise=5000, latency_ms=8.2, sla_target_ms=50.0)
    good_score = rep_ledger.records[good_agent.did]["reputation_score"]
    print(f"  • Honest Agent ({good_agent.did[:24]}...) Score: {good_score}%")

    # Bad agent stakes collateral and gets slashed
    rep_ledger.stake_collateral(bad_agent.did, 50000) # ₹500 collateral
    slashed = rep_ledger.record_slash(bad_agent.did, reason="MALICIOUS_PROMPT_INJECTION_DETECTED")
    bad_score = rep_ledger.records[bad_agent.did]["reputation_score"]
    print(f"  • Rogue Agent ({bad_agent.did[:24]}...) Slashed: ₹{slashed/100:.2f} INR | New Score: {bad_score}% | Blacklisted: {rep_ledger.records[bad_agent.did]['is_blacklisted']}")
    assert bad_score == 0.0
    print("  ✅ Reputation & Slashing Moat: PASSED")

    # 4. Test Sovereign Banking & UPI AutoPay Bridge
    print("\n[Moat 4] Verifying Sovereign Banking & UPI AutoPay Bridge...")
    bridge = SovereignFiatBridge()
    van_info = bridge.provision_agent_virtual_account(good_agent.did)
    print(f"  • Assigned Virtual VPA:      {van_info['virtual_upi_vpa']}")
    print(f"  • Assigned Bank Account:     {van_info['virtual_account_no']} (IFSC: {van_info['ifsc']})")

    topup_result = bridge.simulate_upi_autopay_topup(good_agent.did, 500.0) # ₹500.00
    print(f"  • Autonomous UPI Mandate:    {topup_result['mandate_id']}")
    print(f"  • Human OTP Required:        {topup_result['human_otp_required']}")
    print(f"  • Bank Tx Reference:         {topup_result['bank_tx_reference']}")
    assert topup_result["human_otp_required"] is False
    print("  ✅ Banking & AutoPay Bridge: PASSED")

    print("\n" + "=" * 80)
    print("🏆 ALL 4 FORTRESS DEFENSE MOATS VERIFIED OPERATIONAL!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
