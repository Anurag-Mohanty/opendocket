"""EU Artificial Intelligence Act compliance scanning agent."""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class EUAIActAgent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "eu_ai_act_questions.yaml"
        )
        super().__init__(questions_path, "EU-AI-ACT")
