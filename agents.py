from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict

from gemini import gemini_client


# ==========================================================
# Base Agent
# ==========================================================

class BaseAgent(ABC):
    """
    Base class for all AI agents.
    """

    name: str = "BaseAgent"


    def __init__(self):
        self.client = gemini_client


    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Return agent instruction.
        """
        pass


    def run(
        self,
        task: str,
    ) -> str:
        """
        Execute agent task.
        """

        return self.client.safe_generate(
            prompt=task,
            system_instruction=self.get_system_prompt(),
        )


# ==========================================================
# Planner Agent
# ==========================================================

class PlannerAgent(BaseAgent):

    name = "Planner"


    def get_system_prompt(self) -> str:

        return """
You are a Planning Agent.

Your job:
- Understand user requirements.
- Break complex tasks into steps.
- Create a clear execution plan.
- Do not write final code.
"""


# ==========================================================
# Research Agent
# ==========================================================

class ResearchAgent(BaseAgent):

    name = "Researcher"


    def get_system_prompt(self) -> str:

        return """
You are a Research Agent.

Your job:
- Analyze required information.
- Explain important concepts.
- Provide technical research notes.
- Focus on accuracy.
"""
# ==========================================================
# Coding Agent
# ==========================================================

class CodingAgent(BaseAgent):

    name = "Coder"


    def get_system_prompt(self) -> str:

        return """
You are a Senior Software Engineer.

Your job:
- Write clean production-ready code.
- Follow best practices.
- Explain important implementation decisions.
- Avoid unnecessary complexity.
"""


# ==========================================================
# Reviewer Agent
# ==========================================================

class ReviewerAgent(BaseAgent):

    name = "Reviewer"


    def get_system_prompt(self) -> str:

        return """
You are a Code Review Agent.

Your job:
- Review generated solutions.
- Find bugs and improvements.
- Suggest security and performance improvements.
- Provide final quality feedback.
"""


# ==========================================================
# Agent Registry
# ==========================================================

AGENT_REGISTRY: Dict[str, BaseAgent] = {
    "planner": PlannerAgent(),
    "researcher": ResearchAgent(),
    "coder": CodingAgent(),
    "reviewer": ReviewerAgent(),
}


def get_agent(
    agent_name: str,
) -> BaseAgent:
    """
    Get agent instance by name.
    """

    agent = AGENT_REGISTRY.get(
        agent_name.lower()
    )

    if agent is None:
        raise ValueError(
            f"Agent '{agent_name}' not found."
        )

    return agent   
