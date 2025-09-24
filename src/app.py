from fastapi import FastAPI
from pydantic import BaseModel
from src.graph import AgentOrchestrator
from src.metrics.tracker import MetricsTracker

api = FastAPI(title="MCP Intake Ops")
_orch = AgentOrchestrator()
_metrics = MetricsTracker()

class ChatIn(BaseModel):
    user: str
    message: str

@api.post("/chat")
def chat(inp: ChatIn):
    _metrics.record_event(kind="chat", user=inp.user)
    result = _orch.handle(user=inp.user, text=inp.message)
    _metrics.record_tool_calls(result.get("telemetry", {}))
    _metrics.record_impact(sample_seconds_saved=result.get("seconds_saved", 0))
    return result

@api.get("/metrics/snapshot")
def metrics_snapshot():
    return _metrics.snapshot()