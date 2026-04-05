"""EU Payment Services Directive 2 / Strong Customer Authentication scanning agent."""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class PSD2Agent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "psd2_questions.yaml"
        )
        super().__init__(questions_path, "PSD2")
