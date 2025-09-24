from typing import Dict, Any
from src.mcp.server import MCPLikeServer

class PolicyAgent:
    def __init__(self, server: MCPLikeServer):
        self.server = server

    def check(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        platform = intent.get("platform", "UNKNOWN")
        policy = self.server.policy_check(platform=platform)
        summary = f"Policy: export_ok={policy['export_ok']} supplier_risk<={policy['supplier_risk_threshold']}"
        return {
            "summary": summary,
            "tool_calls": 1,
            "tools": ["policy_check"]
        }