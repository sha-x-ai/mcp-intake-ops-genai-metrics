from typing import List, Dict
from src.graph import AgentOrchestrator

CASES = [
    ("vad", "Need A320 rivets stock and export policy check"),
    ("ops", "Inventory for A350 bolts, also check ITAR"),
    ("qa", "Policy check for A320 supplier risk")
]

def run() -> Dict:
    orch = AgentOrchestrator()
    out: List[Dict] = []
    for user, msg in CASES:
        out.append(orch.handle(user, msg))
    return {"runs": out}

if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))