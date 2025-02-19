#!/usr/bin/python
import argparse
import glob
from pathlib import Path
import random

from execution_manager import *
from kr_cbs import KRCBSSolver
from ta_random import TaRandomSolver
from ta_distance import TaDistanceSolver
from visualize import Animation
from single_agent_planner import get_sum_of_cost
from run_experiments import *


#################################################
# Modify here to use your own execution manager.
ExecutionManagerClass = TACBSExecutionManager
# ExecutionManagerClass = WorksReallyWellExecutionManager

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    parser.add_argument('--k', type=int, default=None,
                        help='The parameter for K-Robust KRCBS', required=True)
    parser.add_argument('--batch', action='store_true', default=False,
                        help='Use batch output instead of animation')
    parser.add_argument('--fail_prob', type=float, default=0.0,
                        help='The probability of an agent failing to move')

    args = parser.parse_args()

    result_file = open("results.csv", "w", buffering=1)

    for file in sorted(glob.glob(args.instance)):

        print("***Import an instance***")
        my_map, starts, goals = import_mapf_instance(file)
        print_mapf_instance(my_map, starts, goals)

        # Create execution manager.
        execution_manager = ExecutionManagerClass(my_map, starts, goals, k=args.k)

        # Keep track of the resulting paths.
        paths = [[s] for s in starts]

        # Choose some robots to be broken.
        broken_robots = random.sample(range(len(starts)), len(starts)//2)

        while True:
            # Current positions.
            locations_curr = [path[-1] if path else start for path, start in zip(paths, starts)]

            # Get the next position for all agents.
            locations_next = execution_manager.get_next_location_for_all_agents()

            # Termination condition.
            if not locations_next:
                break

            # Randomly fail some agents. Feedback this information to the execution manager.
            agent_success = []
            for i in range(len(locations_next)):
                if random.random() < args.fail_prob and i in broken_robots:
                    locations_next[i] = locations_curr[i]
                    agent_success.append(False)
                else:
                    agent_success.append(True)

            # Feedback the agents that successfully moved.
            execution_manager.feedback_successful_agent_ids([i for i, success in enumerate(agent_success) if success])

            # Add the next positions to the paths.
            for i, (x, y) in enumerate(locations_next):
                paths[i].append((x, y))

        cost = get_sum_of_cost(paths)
        result_file.write("{},{}\n".format(file, cost))

        if not args.batch:
            print("***Test paths on a simulation***")
            animation = Animation(my_map, starts, goals, paths, k=args.k)
            # animation.save("output.mp4", 1.0)
            animation.show()
    result_file.close()
