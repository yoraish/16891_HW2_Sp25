# General imports.
from abc import ABC, abstractmethod
from typing import List, Tuple

# Project imports.
from ta_cbs import TACBSSolver
from single_agent_planner import get_location

class ExecutionManager(ABC):
    def __init__(self, my_map, starts, goals, **kwargs):
        # Initialize the execution manager with whichever parameters you need.
        pass

    @abstractmethod
    def get_next_location_for_all_agents(self) -> List[Tuple[int, int]]:
        # An iterator returning the next position for all agents.
        pass

    @abstractmethod
    def feedback_successful_agent_ids(self, agent_ids: List[int]):
        # Feedback for the agents that successfully moved.
        pass


class TACBSExecutionManager(ExecutionManager):
    def __init__(self, my_map, starts, goals, k=0, **kwargs):
        super().__init__(my_map, starts, goals, k=k)
        # Initialize the execution manager with whichever parameters you need.
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.k = k

        self.solver = TACBSSolver(self.my_map, self.starts, self.goals, self.k)

        self.paths = self.solver.find_solution()
        self.t_agent = [0 for _ in range(len(self.paths))]

    def get_next_location_for_all_agents(self) -> List[Tuple[int, int]]:
        # Return the next location for all agents or empty list if done.
        print(self.t_agent, [len(path) - 1 for path in self.paths])
        if all(t > len(path) - 1 for t, path in zip(self.t_agent, self.paths)):
            return []

        locations = []
        for agent_id, path in enumerate(self.paths):
            locations.append(get_location(path, self.t_agent[agent_id]))
        return locations

    def feedback_successful_agent_ids(self, agent_ids: List[int]):
        for agent_id in agent_ids:
            self.t_agent[agent_id] += 1


class WorksReallyWellExecutionManager(ExecutionManager):
    def __init__(self, my_map, starts, goals, **kwargs):
        # Initialize the execution manager with whichever parameters you need.
        super().__init__(my_map, starts, goals, k=k)
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.k = k

    def get_next_location_for_all_agents(self) -> List[Tuple[int, int]]:
        """
        Get the next location for all agents.
        :return: List of tuples, each tuple is the next location for an agent at index i. Return empty list if done.
        """
        ##############################
        # Implement the next location for all agents.
        pass

    def feedback_successful_agent_ids(self, agent_ids: List[int]):
        """
        Feedback for the agents that successfully moved.
        :param agent_ids: List of agent IDs that successfully moved.
        :return: None
        """
        ##############################
        # Implement the feedback for the agents that successfully moved.
        pass
