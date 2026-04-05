"""EU Digital Operational Resilience Act (DORA) compliance scanning agent."""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class DORAAgent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "dora_questions.yaml"
        )
        super().__init__(questions_path, "DORA")
