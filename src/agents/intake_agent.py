from typing import Dict
from src.llm.mock_llm import MockLLM

class IntakeAgent:
    def __init__(self, llm: MockLLM):
        self.llm = llm

    def parse(self, text: str) -> Dict:
        intent = self.llm.parse_intent(text)
        entities = self.llm.parse_entities(text)
        intent.update(entities)
        return intent