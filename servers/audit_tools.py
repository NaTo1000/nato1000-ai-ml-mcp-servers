"""
Security, Governance & Audit MCP Server for NATO1000
Tools for hash-linked audit logging, provenance, and validation.
"""
from fastmcp import FastMCP
from typing import Dict, Any, List
import hashlib
import json
from datetime import datetime

mcp = FastMCP(name="NATO1000 Audit Tools")

audit_log: List[Dict] = []

@mcp.tool()
def log_audit_event(event_type: str, actor: str, details: Dict[str, Any], previous_hash: str = "") -> Dict:
    """Log a hash-linked audit event for provenance."""
    timestamp = datetime.utcnow().isoformat()
    payload = {
        "timestamp": timestamp,
        "event_type": event_type,
        "actor": actor,
        "details": details,
        "previous_hash": previous_hash
    }
    payload_str = json.dumps(payload, sort_keys=True)
    event_hash = hashlib.sha256(payload_str.encode()).hexdigest()
    event = {**payload, "hash": event_hash}
    audit_log.append(event)
    return event

@mcp.tool()
def get_audit_log(limit: int = 10) -> List[Dict]:
    """Retrieve recent audit events."""
    return audit_log[-limit:]

@mcp.tool()
def validate_chain() -> Dict[str, Any]:
    """Validate the hash chain integrity of the audit log."""
    if not audit_log:
        return {"valid": True, "message": "Empty log"}
    valid = True
    for i, event in enumerate(audit_log):
        if i == 0:
            continue
        if event.get("previous_hash") != audit_log[i-1].get("hash"):
            valid = False
            break
    return {"valid": valid, "n_events": len(audit_log)}

if __name__ == "__main__":
    mcp.run()
