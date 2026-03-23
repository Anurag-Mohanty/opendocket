"""
FERPA compliance scanning agent.
"""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class FERPAAgent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "ferpa_questions.yaml"
        )
        super().__init__(questions_path, "FERPA")
