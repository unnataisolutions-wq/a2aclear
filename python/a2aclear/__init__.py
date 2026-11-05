"""
A2AClear: Sovereign Agent-to-Agent Clearinghouse & Settlement Protocol SDK
(C) 2026 Unnat AI Solutions. Chief Systems Architect: Rohit.
Licensed under BSL 1.1 (Business Source License).
"""

from .identity import AgentIdentity
from .contract import TaskContract, ContractState, PROTOCOL_INTERCHANGE_BPS
from .negotiator import AutonomousNegotiator
from .escrow import MicroEscrowVault
from .clearinghouse import ClearinghouseClient, DEFAULT_CLEARINGHOUSE_URL
from .reputation import AgentReputationLedger
from .fiat_bridge import SovereignFiatBridge
from .security import (
    EncryptedKeyStore,
    ReplayDefenseValidator,
    PayloadSanitizer,
    SovereignCryptographicWatermark,
    ReplayAttackException,
    MaliciousPayloadException
)

__version__ = "1.0.0"
__all__ = [
    "AgentIdentity",
    "TaskContract",
    "ContractState",
    "PROTOCOL_INTERCHANGE_BPS",
    "AutonomousNegotiator",
    "MicroEscrowVault",
    "ClearinghouseClient",
    "DEFAULT_CLEARINGHOUSE_URL",
    "AgentReputationLedger",
    "SovereignFiatBridge",
    "EncryptedKeyStore",
    "ReplayDefenseValidator",
    "PayloadSanitizer",
    "SovereignCryptographicWatermark",
    "ReplayAttackException",
    "MaliciousPayloadException",
]
