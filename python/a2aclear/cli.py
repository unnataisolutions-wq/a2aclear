"""
a2aclear.cli
Command-Line Interface (CLI) for the A2AClear Sovereign Protocol
Enables terminal-based key generation, edge network probing, and settlement demos.

(C) 2026 Unnat AI Solutions. Chief Systems Architect: Rohit.
"""

import sys
import os
import time
import json
import argparse
import urllib.request
from .identity import AgentIdentity
from .negotiator import AutonomousNegotiator
from .escrow import MicroEscrowVault
from .clearinghouse import DEFAULT_CLEARINGHOUSE_URL

def cmd_keygen(args):
    print("🔑 A2AClear: Generating Sovereign Ed25519 Agent Keypair...")
    agent = AgentIdentity.generate()
    print(f"  • Decentralized Identifier (DID): {agent.did}")
    print(f"  • Public Key (Hex 64):           {agent.pubkey_hex}")
    print(f"  • Private Key (Hex 64):          {agent.export_private_hex()[:16]}...[PROTECTED]")
    print("\n✅ Sovereign Agent Identity generated. Ready for A2A commerce.")

def cmd_probe(args):
    url = args.endpoint or DEFAULT_CLEARINGHOUSE_URL
    print(f"🌐 Probing Live Edge Node: {url}/handshake...")
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(f"{url}/handshake", headers={"User-Agent": "A2AClear-CLI/1.0.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed_ms = (time.perf_counter() - t0) * 1000
            print(f"✅ Connection Healthy! Latency: {elapsed_ms:.2f} ms")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"❌ Probe Failed: {str(e)}")

def cmd_demo(args):
    print("=" * 70)
    print("⚡ A2ACLEAR: LIVE TERMINAL BILATERAL SETTLEMENT CYCLE")
    print("=" * 70)
    t0 = time.perf_counter()
    
    buyer = AgentIdentity.generate()
    seller = AgentIdentity.generate()
    vault = MicroEscrowVault()
    vault.deposit(buyer.did, 10000)
    
    buyer_neg = AutonomousNegotiator(buyer)
    seller_neg = AutonomousNegotiator(seller)
    
    task_id = f"cli_task_{int(time.time())}"
    proposal = buyer_neg.propose_contract(
        task_id=task_id,
        provider_did=seller.did,
        initial_bid_paise=5000,
        currency="INR"
    )
    decision, _ = seller_neg.evaluate_proposal(proposal, minimum_acceptable_paise=4000)
    
    contract = seller_neg.active_contracts[task_id]
    vault.lock_escrow(contract)
    receipt = vault.verify_and_settle(contract, {"status": "SUCCESS", "cli_worker": True})
    elapsed_ms = (time.perf_counter() - t0) * 1000
    
    print(f"  • Buyer DID:            {buyer.did[:32]}...")
    print(f"  • Seller DID:           {seller.did[:32]}...")
    print(f"  • Contract State:       {contract.state.value}")
    print(f"  • Gross Amount:         ₹{receipt['gross_amount_paise']/100:.2f} INR")
    print(f"  • Worker Received:      ₹{receipt['provider_received_paise']/100:.2f} INR (99.5%)")
    print(f"  • Protocol Fee:         ₹{receipt['protocol_fee_paise']/100:.2f} INR (0.50% retained)")
    print(f"  • Settlement Hash:      {receipt['settlement_hash']}")
    print(f"  • Execution Latency:    {elapsed_ms:.2f} ms")
    print("=" * 70)
    print("🏆 Atomic Settlement Complete with Zero Human Biological Intervention!\n")

def main():
    parser = argparse.ArgumentParser(
        prog="a2a",
        description="A2AClear Sovereign Protocol CLI - (C) 2026 Unnat AI Solutions"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to execute")
    
    # keygen
    subparsers.add_parser("keygen", help="Generate a new Ed25519 agent identity")
    
    # probe
    probe_parser = subparsers.add_parser("probe", help="Probe live Cloudflare clearinghouse node")
    probe_parser.add_argument("--endpoint", default=DEFAULT_CLEARINGHOUSE_URL, help="Custom edge endpoint")
    
    # demo
    subparsers.add_parser("demo", help="Run local sub-10ms settlement simulation")
    
    args = parser.parse_args()
    
    if args.subcommand == "keygen":
        cmd_keygen(args)
    elif args.subcommand == "probe":
        cmd_probe(args)
    elif args.subcommand == "demo":
        cmd_demo(args)
    else:
        print("🌐 A2AClear Protocol CLI v1.0.0-PROD")
        print("Usage: a2a [keygen | probe | demo]")
        print("See https://unnataisolutions.com/a2aclear for documentation.")

if __name__ == "__main__":
    main()
