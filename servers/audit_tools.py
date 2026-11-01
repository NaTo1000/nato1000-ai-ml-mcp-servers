"""
NATO1000 Audit & Provenance MCP Server
Hash-linked event logging and chain validation for governance.
"""
from fastmcp import FastMCP
from typing import Dict, List
import hashlib
import json
from datetime import datetime

mcp = FastMCP(name="NATO1000 Audit Tools")

AUDIT_LOG: List[Dict] = []

def _hash_event(event: Dict) -> str:
    return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()[:16]

@mcp.tool()
def log_audit_event(action: str, actor: str, details: Dict, previous_hash: str = "genesis") -> Dict:
    """Append a hash-linked audit event."""
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "actor": actor,
        "details": details,
        "previous_hash": previous_hash
    }
    event["event_hash"] = _hash_event(event)
    AUDIT_LOG.append(event)
    return event

@mcp.tool()
def validate_audit_chain() -> Dict:
    """Validate the integrity of the in-memory audit chain."""
    if not AUDIT_LOG:
        return {"valid": True, "length": 0, "message": "Empty log"}
    prev = "genesis"
    for i, event in enumerate(AUDIT_LOG):
        if event.get("previous_hash") != prev:
            return {"valid": False, "broken_at": i, "expected": prev, "found": event.get("previous_hash")}
        prev = event["event_hash"]
    return {"valid": True, "length": len(AUDIT_LOG), "last_hash": prev}

@mcp.tool()
def get_recent_events(n: int = 5) -> List[Dict]:
    """Return the most recent N audit events."""
    return AUDIT_LOG[-n:]

if __name__ == "__main__":
    mcp.run()
