from typing import List
from swarms.structs.agent import Agent
from swarms.utils.loguru_logger import logger
from swarms.structs.rearrange import AgentRearrange
from swarms.structs.base_swarm import BaseSwarm
from concurrent.futures import ThreadPoolExecutor, as_completed
from swarms.structs.agents_available import showcase_available_agents


class SequentialWorkflow(BaseSwarm):
    """
    Initializes a SequentialWorkflow object, which orchestrates the execution of a sequence of agents.

    Args:
        name (str, optional): The name of the workflow. Defaults to "SequentialWorkflow".
        description (str, optional): A description of the workflow. Defaults to "Sequential Workflow, where agents are executed in a sequence."
        agents (List[Agent], optional): The list of agents in the workflow. Defaults to None.
        max_loops (int, optional): The maximum number of loops to execute the workflow. Defaults to 1.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Raises:
        ValueError: If agents list is None or empty, or if max_loops is 0
    """

    def __init__(
        self,
        name: str = "SequentialWorkflow",
        description: str = "Sequential Workflow, where agents are executed in a sequence.",
        agents: List[Agent] = None,
        max_loops: int = 1,
        *args,
        **kwargs,
    ):
        # self.reliability_check()

        try:
            super().__init__(
                name=name,
                description=description,
                agents=agents,
                *args,
                **kwargs,
            )
            self.name = name
            self.description = description
            self.agents = agents
            self.flow = " -> ".join(
                agent.agent_name for agent in agents
            )
            self.agent_rearrange = AgentRearrange(
                name=name,
                description=description,
                agents=agents,
                flow=self.flow,
                max_loops=max_loops,
                *args,
                **kwargs,
            )

            self.handle_agent_showcase()

        except Exception as e:
            logger.error(
                f"Error initializing SequentialWorkflow: {str(e)}"
            )
            raise

    def reliability_check(self):
        if self.agents is None or len(self.agents) == 0:
            raise ValueError("Agents list cannot be None or empty")

        if self.max_loops == 0:
            raise ValueError("max_loops cannot be 0")

        logger.info("Checks completed your swarm is ready.")

    def handle_agent_showcase(self):
        # Get the showcase string once instead of regenerating for each agent
        showcase_str = showcase_available_agents(self.agents)

        # Append showcase string to each agent's existing system prompt
        for agent in self.agents:
            agent.system_prompt += showcase_str

    def run(self, task: str) -> str:
        """
        Executes a task through the agents in the dynamically constructed flow.

        Args:
            task (str): The task for the agents to execute.

        Returns:
            str: The final result after processing through all agents.

        Raises:
            ValueError: If task is None or empty
            Exception: If any error occurs during task execution
        """
        if not task or not isinstance(task, str):
            raise ValueError("Task must be a non-empty string")

        try:
            logger.info(
                f"Executing task with dynamic flow: {self.flow}"
            )
            return self.agent_rearrange.run(task)
        except Exception as e:
            logger.error(
                f"An error occurred while executing the task: {e}"
            )
            raise

    def run_batched(self, tasks: List[str]) -> List[str]:
        """
        Executes a batch of tasks through the agents in the dynamically constructed flow.

        Args:
            tasks (List[str]): The tasks for the agents to execute.

        Returns:
            List[str]: The final results after processing through all agents.

        Raises:
            ValueError: If tasks is None or empty
            Exception: If any error occurs during task execution
        """
        if not tasks or not all(
            isinstance(task, str) for task in tasks
        ):
            raise ValueError(
                "Tasks must be a non-empty list of strings"
            )

        try:
            logger.info(
                f"Executing batch of tasks with dynamic flow: {self.flow}"
            )
            return [self.agent_rearrange.run(task) for task in tasks]
        except Exception as e:
            logger.error(
                f"An error occurred while executing the batch of tasks: {e}"
            )
            raise

    async def run_async(self, task: str) -> str:
        """
        Executes the task through the agents in the dynamically constructed flow asynchronously.

        Args:
            task (str): The task for the agents to execute.

        Returns:
            str: The final result after processing through all agents.

        Raises:
            ValueError: If task is None or empty
            Exception: If any error occurs during task execution
        """
        if not task or not isinstance(task, str):
            raise ValueError("Task must be a non-empty string")

        try:
            logger.info(
                f"Executing task with dynamic flow asynchronously: {self.flow}"
            )
            return await self.agent_rearrange.run_async(task)
        except Exception as e:
            logger.error(
                f"An error occurred while executing the task asynchronously: {e}"
            )
            raise

    async def run_concurrent(self, tasks: List[str]) -> List[str]:
        """
        Executes a batch of tasks through the agents in the dynamically constructed flow concurrently.

        Args:
            tasks (List[str]): The tasks for the agents to execute.

        Returns:
            List[str]: The final results after processing through all agents.

        Raises:
            ValueError: If tasks is None or empty
            Exception: If any error occurs during task execution
        """
        if not tasks or not all(
            isinstance(task, str) for task in tasks
        ):
            raise ValueError(
                "Tasks must be a non-empty list of strings"
            )

        try:
            logger.info(
                f"Executing batch of tasks with dynamic flow concurrently: {self.flow}"
            )
            with ThreadPoolExecutor() as executor:
                results = [
                    executor.submit(self.agent_rearrange.run, task)
                    for task in tasks
                ]
                return [
                    result.result()
                    for result in as_completed(results)
                ]
        except Exception as e:
            logger.error(
                f"An error occurred while executing the batch of tasks concurrently: {e}"
            )
            raise
