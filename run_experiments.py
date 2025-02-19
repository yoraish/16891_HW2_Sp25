#!/usr/bin/python
import argparse
import glob
from pathlib import Path
from kr_cbs import KRCBSSolver
from ta_random import TaRandomSolver
from ta_distance import TaDistanceSolver
from ta_cbs import TACBSSolver
from visualize import Animation
from single_agent_planner import get_sum_of_cost

SOLVER = "KRCBS"


def print_mapf_instance(my_map, starts, goals):
    print('Start locations')
    print_locations(my_map, starts)
    print('Goal locations')
    print_locations(my_map, goals)


def print_locations(my_map, locations):
    starts_map = [[-1 for _ in range(len(my_map[0]))] for _ in range(len(my_map))]
    for i in range(len(locations)):
        starts_map[locations[i][0]][locations[i][1]] = i
    to_print = ''
    for x in range(len(my_map)):
        for y in range(len(my_map[0])):
            if starts_map[x][y] >= 0:
                to_print += str(starts_map[x][y]) + ' '
            elif my_map[x][y]:
                to_print += '@ '
            else:
                to_print += '. '
        to_print += '\n'
    print(to_print)


def import_mapf_instance(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: #rows #columns
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    # #rows lines with the map
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    # #agents
    line = f.readline()
    num_agents = int(line)
    # #agents lines with the start/goal positions
    starts = []
    goals = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))
    f.close()
    return my_map, starts, goals


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    parser.add_argument('--k', type=int, default=None,
                        help='The parameter for K-Robust KRCBS', required=True)
    parser.add_argument('--batch', action='store_true', default=False,
                        help='Use batch output instead of animation')
    parser.add_argument('--solver', type=str, required=True,
                        help='The solver to use (KRCBS, TA-RANDOM, TA-DISTANCE, TA-CBS)')

    args = parser.parse_args()

    result_file = open("results.csv", "w", buffering=1)

    for file in sorted(glob.glob(args.instance)):

        print("***Import an instance***")
        my_map, starts, goals = import_mapf_instance(file)
        print_mapf_instance(my_map, starts, goals)

        if args.solver == "KRCBS":
            print("***Run KRCBS***")
            KRCBS = KRCBSSolver(my_map, starts, goals, k=args.k)
            paths = KRCBS.find_solution()

        elif args.solver == "TA-RANDOM":
            print("***Run TA-RANDOM***")
            ta_random = TaRandomSolver(my_map, starts, goals, k=args.k)
            paths = ta_random.find_solution()

        elif args.solver == "TA-DISTANCE":
            print("***Run TA-DISTANCE***")
            ta_distance = TaDistanceSolver(my_map, starts, goals, k=args.k)
            paths = ta_distance.find_solution()

        elif args.solver == "TA-CBS":
            print("***Run TA-CBS***")
            ta_cbs = TACBSSolver(my_map, starts, goals, k=args.k)
            paths = ta_cbs.find_solution()

        else:
            raise RuntimeError("Unknown solver!")

        cost = get_sum_of_cost(paths)
        result_file.write("{},{}\n".format(file, cost))

        if not args.batch:
            print("***Test paths on a simulation***")
            animation = Animation(my_map, starts, goals, paths, k=args.k)
            # animation.save("output.mp4", 1.0)
            animation.show()
    result_file.close()
