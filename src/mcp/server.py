from typing import List, Dict
from .tools import PartsStore, PolicyStore

class MCPLikeServer:
    """Minimal shim that looks like an MCP capability registry."""
    def __init__(self):
        self.parts = PartsStore()
        self.policies = PolicyStore()

    def parts_search(self, platform: str | None = None) -> List[Dict]:
        return self.parts.search(platform=platform)

    def policy_check(self, platform: str) -> Dict:
        return self.policies.check(platform)