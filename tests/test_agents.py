from src.graph import AgentOrchestrator

def test_end_to_end():
    orch = AgentOrchestrator()
    res = orch.handle(user="t", text="Find A320 rivets and check policy")
    assert "A320" in str(res["intent"]) or res["intent"].get("need_parts")
    assert res["telemetry"]["tool_calls"] >= 1
    assert res["seconds_saved"] >= 60