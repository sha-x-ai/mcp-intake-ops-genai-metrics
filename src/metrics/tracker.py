from typing import Dict
import time

class MetricsTracker:
    def __init__(self):
        self.state = {
            "utilization": {"events": 0, "tool_calls": 0, "tools": {}},
            "impact": {"seconds_saved": 0},
            "cost": {"ai_spend_usd": 0.0, "agent_hourly_rate": 0.0}
        }
        self.started = time.time()

    def record_event(self, kind: str, user: str):
        self.state["utilization"]["events"] += 1

    def record_tool_calls(self, telemetry: Dict):
        n = int(telemetry.get("tool_calls", 0))
        self.state["utilization"]["tool_calls"] += n
        for t in telemetry.get("tools", []):
            self.state["utilization"]["tools"][t] = self.state["utilization"]["tools"].get(t, 0) + 1
        # cost proxy: $0.0005 per tool call (tunable)
        self.state["cost"]["ai_spend_usd"] += n * 0.0005

    def record_impact(self, sample_seconds_saved: int):
        self.state["impact"]["seconds_saved"] += max(0, int(sample_seconds_saved))

    def snapshot(self) -> Dict:
        hours = (time.time() - self.started)/3600
        heh = self.state["impact"]["seconds_saved"]/3600  # human-equivalent hours
        spend = self.state["cost"]["ai_spend_usd"] or 0.0001
        self.state["cost"]["agent_hourly_rate"] = round(heh / spend, 4)
        return {
            "uptime_hours": round(hours, 2),
            **self.state
        }