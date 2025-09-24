from typing import Dict, Any
from src.llm.mock_llm import MockLLM
from src.agents.intake_agent import IntakeAgent
from src.agents.parts_agent import PartsAgent
from src.agents.policy_agent import PolicyAgent
from src.mcp.server import MCPLikeServer

class AgentOrchestrator:
    def __init__(self):
        self.llm = MockLLM()
        self.server = MCPLikeServer()
        self.parts = PartsAgent(self.server)
        self.policy = PolicyAgent(self.server)
        self.intake = IntakeAgent(self.llm)

    def handle(self, user: str, text: str) -> Dict[str, Any]:
        intent = self.intake.parse(text)
        telemetry = {"tool_calls": 0, "tools": []}
        answers = []
        seconds_saved = 0

        if intent.get("need_parts"):
            ans = self.parts.query_parts(intent)
            telemetry["tool_calls"] += ans.pop("tool_calls", 0)
            telemetry["tools"].extend(ans.pop("tools", []))
            answers.append(ans["summary"])
            seconds_saved += 90

        if intent.get("need_policy"):
            chk = self.policy.check(intent)
            telemetry["tool_calls"] += chk.pop("tool_calls", 0)
            telemetry["tools"].extend(chk.pop("tools", []))
            answers.append(chk["summary"])
            seconds_saved += 60

        final = self.llm.summarize(answers)
        return {
            "user": user,
            "intent": intent,
            "answer": final,
            "seconds_saved": seconds_saved,
            "telemetry": telemetry
        }