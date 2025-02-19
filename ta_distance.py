import copy
import time as timer
import heapq
import random
from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost
from kr_cbs import *
from hungarian import hungarian_algorithm


class TaDistanceSolver(KRCBSSolver):
    """The high-level search of K-Robust CBS with distance-based task assignment."""

    def __init__(self, my_map, starts, goals, k=0):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        k           - the parameter for K-Robust CBS
        """
        super().__init__(my_map, starts, goals, k)

        self.start_time = None
        self.my_map = my_map
        self.starts = starts
        self.num_of_agents = len(starts)

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []

        ##############################
        # Implement Distance-Based Task Assignment
        #           Populate self.goals with one goal for each agent -- matched by their order in the lists.
        #           To do so, please implement the `hungarian_algorithm` function in `hungarian.py`.
        self.goals = []
        raise NotImplementedError("Implement Distance-Based Task Assignment")

        # Compute heuristics for the low-level search.
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

        # The parameter for K-Robust CBS.
        self.k = k
