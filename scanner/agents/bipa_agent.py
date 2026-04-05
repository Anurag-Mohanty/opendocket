"""Illinois Biometric Information Privacy Act (BIPA) compliance scanning agent."""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class BIPAAgent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "bipa_questions.yaml"
        )
        super().__init__(questions_path, "BIPA")
