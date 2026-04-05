"""ISO 27001:2022 Information Security Management compliance scanning agent."""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class ISO27001Agent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "iso27001_questions.yaml"
        )
        super().__init__(questions_path, "ISO-27001")
