"""
SOC 2 compliance scanning agent.

Loads SOC2 question library and runs each question against
the target repository to produce findings.
"""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class SOC2Agent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "soc2_questions.yaml"
        )
        super().__init__(questions_path, "SOC2")
