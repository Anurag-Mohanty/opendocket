"""
PCI-DSS compliance scanning agent.

Loads PCI-DSS question library and runs each question against
the target repository to produce findings.
"""

import os
from scanner.agents.base_agent import BaseComplianceAgent


class PCIDSSAgent(BaseComplianceAgent):
    def __init__(self):
        questions_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "pci_dss_questions.yaml"
        )
        super().__init__(questions_path, "PCI-DSS")
