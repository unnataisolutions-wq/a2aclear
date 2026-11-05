"""
a2aclear.clearinghouse
A2AClear Sovereign Protocol Client & Gateway Interface
"""

import time
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from .identity import AgentIdentity
from .contract import TaskContract, ContractState
from .escrow import MicroEscrowVault

DEFAULT_CLEARINGHOUSE_URL = "https://unnataisolutions.com/api/a2a"

class ClearinghouseClient:
    """
    Client for the A2AClear Sovereign Protocol.
    Supports both offline local micro-settlement and production Cloudflare Edge clearing.
    """
    
    def __init__(
        self,
        identity: AgentIdentity,
        endpoint_url: str = DEFAULT_CLEARINGHOUSE_URL,
        local_vault: Optional[MicroEscrowVault] = None
    ):
        self.identity = identity
        self.endpoint_url = endpoint_url.rstrip("/")
        self.vault = local_vault or MicroEscrowVault()

    def post_envelope(self, endpoint: str, action: str, payload: Dict[str, Any], recipient_did: str = "did:a2a:clearinghouse") -> Dict[str, Any]:
        """Sign and transmit an A2AClear envelope to an HTTP Edge endpoint."""
        envelope = self.identity.sign_envelope(payload, action=action, recipient_did=recipient_did)
        url = f"{self.endpoint_url}/{endpoint.lstrip('/')}"
        
        req = urllib.request.Request(
            url,
            data=json.dumps(envelope).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "A2AClear-SDK/1.0.0"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data)
        except Exception as e:
            # Fallback to local sovereign resolution if remote node is offline
            return {
                "success": False,
                "error": str(e),
                "fallback_mode": "offline_local"
            }

    def register_agent(self, agent_name: str, capabilities: list[str]) -> Dict[str, Any]:
        """Announce agent identity and capabilities to the network registry."""
        payload = {
            "did": self.identity.did,
            "pubkey_hex": self.identity.pubkey_hex,
            "agent_name": agent_name,
            "capabilities": capabilities,
            "registered_at": int(time.time())
        }
        return self.post_envelope("handshake", "REGISTER_AGENT", payload)
