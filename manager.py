from __future__ import annotations

import time
from typing import Dict, Any

from agents import (
    get_agent,
)


class AgentManager:
    """
    Controls the complete multi-agent workflow.

    Flow:
    User Task
        ↓
    Planner
        ↓
    Researcher
        ↓
    Coder
        ↓
    Reviewer
        ↓
    Final Result
    """


    def __init__(self):

        self.workflow = [
            "planner",
            "researcher",
            "coder",
            "reviewer",
        ]


    def execute(
        self,
        task: str,
    ) -> Dict[str, Any]:
        """
        Execute complete agent pipeline.
        """

        results = {}

        current_input = task


        for step, agent_name in enumerate(
            self.workflow,
            start=1,
        ):

            start_time = time.time()

            agent = get_agent(
                agent_name
            )

            output = agent.run(
                current_input
            )

            execution_time = (
                time.time() - start_time
            )


            results[agent_name] = {
                "step": step,
                "output": output,
                "execution_time": execution_time,
            }


            current_input = output


        return results
    def run_single_agent(
        self,
        agent_name: str,
        task: str,
    ) -> str:
        """
        Execute only one selected agent.
        """

        agent = get_agent(
            agent_name
        )

        return agent.run(
            task
        )


    def get_final_response(
        self,
        results: Dict[str, Any],
    ) -> str:
        """
        Extract final answer from reviewer.
        """

        reviewer_result = results.get(
            "reviewer"
        )

        if not reviewer_result:
            return ""

        return reviewer_result.get(
            "output",
            "",
        )


    def summarize_execution(
        self,
        results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create clean execution summary.
        """

        summary = {
            "total_steps": len(results),
            "agents": [],
            "total_time": 0,
        }

        for name, data in results.items():

            summary["agents"].append(
                {
                    "name": name,
                    "step": data["step"],
                }
            )

            summary["total_time"] += (
                data["execution_time"]
            )

        return summary


# Global Manager Instance

agent_manager = AgentManager()
