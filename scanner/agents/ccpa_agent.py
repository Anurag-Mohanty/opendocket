"""
CCPA/CPRA compliance scanning agent.

Loads CCPA question library and runs each question against
the target repository to produce findings.
"""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class CCPAAgent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "ccpa_questions.yaml"
        )
        super().__init__(questions_path, "CCPA/CPRA")
