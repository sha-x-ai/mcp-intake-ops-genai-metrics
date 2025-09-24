from typing import List, Dict

class MockLLM:
    """Deterministic LLM stand-in for offline demos. Replace with a real provider later."""
    def parse_intent(self, text: str) -> Dict[str, bool]:
        t = text.lower()
        return {
            "need_parts": any(k in t for k in ["part", "stock", "inventory", "rivets", "bolt", "screw"]),
            "need_policy": any(k in t for k in ["policy", "export", "itars", "compliance", "policy check"]) or "check" in t
        }

    def parse_entities(self, text: str) -> Dict[str, str]:
        # naive extraction; keeps it simple but testable
        out = {}
        for token in text.replace(",", " ").split():
            if token.upper().startswith("A3"):
                out["platform"] = token.upper()
        return out

    def summarize(self, lines: List[str]) -> str:
        return " | ".join([l.strip() for l in lines if l]).strip() or "No result"

    def __call__(self, prompt: str) -> str:
        return "OK"