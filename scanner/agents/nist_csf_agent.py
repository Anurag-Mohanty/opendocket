"""NIST Cybersecurity Framework 2.0 compliance scanning agent."""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class NISTCSFAgent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "nist_csf_questions.yaml"
        )
        super().__init__(questions_path, "NIST-CSF")
