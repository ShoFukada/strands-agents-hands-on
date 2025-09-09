import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from strands import Agent

from config import Settings

agent = Agent()
settings = Settings()

agent("Tell me about agentic AI")
