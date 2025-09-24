from typing import Dict, Any
from src.mcp.server import MCPLikeServer

class PartsAgent:
    def __init__(self, server: MCPLikeServer):
        self.server = server

    def query_parts(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        platform = intent.get("platform")
        rows = self.server.parts_search(platform=platform)
        top = rows[:5]
        summary = ", ".join([f"{r['part_id']} ({r['description']}) stock={r['stock']} export={r['export_flag']}" for r in top])
        return {
            "summary": f"Parts: {summary}" if summary else "No matching parts",
            "tool_calls": 1,
            "tools": ["parts_search"]
        }