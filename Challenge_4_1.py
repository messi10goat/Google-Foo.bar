'''

Running with Bunnies
====================

You and your rescued bunny prisoners need to get out of this collapsing death trap of a space station - and fast! Unfortunately, some of the bunnies have been weakened by their long imprisonment and can't run very fast. Their friends are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can and get through the bulkheads before they close. 

The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ..., last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave - you can move to and from the bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact with the space station's security checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is traversed, the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest prisoner IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by prisoner ID, with the first bunny being 0. There are at most 5 bunnies, and time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best combination for this space station hallway, so the answer is [1, 2].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 1, 1, 1, 1}, {1, 0, 1, 1, 1}, {1, 1, 0, 1, 1}, {1, 1, 1, 0, 1}, {1, 1, 1, 1, 0}}, 3)
Output:
    [0, 1]

Input:
Solution.solution({{0, 2, 2, 2, -1}, {9, 0, 2, 2, -1}, {9, 3, 0, 2, -1}, {9, 3, 2, 0, -1}, {9, 3, 2, 2, 0}}, 1)
Output:
    [1, 2]

-- Python cases --
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output:
    [0, 1]
    
    
'''

# Solution:

import copy
from itertools import permutations
def powerset(list):
    """
    :param list: The list to generate subsets of.
    :return: A generator that produces all subsets of this set.
    """
    x = len(list)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, list) if i & mask]


def getneighbourindex(neighbour, graphsize):
    if neighbour == "Bulkhead":
        return graphsize - 1
    elif neighbour == "Start":
        return 0
    else:
        return int(neighbour)+1


def matrix2graph(matrix):
    """
    This helper function turns our matrix into a graph that's a little easier to work with using Bellman-Ford.
    :param matrix: The original matrix.
    :return: matrix in dictionary format.
    """
    keys = ["Start"]
    for num in range(1, len(matrix)-1):
        keys.append(num-1)
    keys.append("Bulkhead")
    graph = dict(zip(keys, matrix))
    return graph


# Step 1: Initialize graph
def initialize(graph, source):
    """
    Step 1 of the Bellman-Ford algorithm.
    """
    distance = {}
    predecessor = {}
    for node in graph:
        # We start off assuming all nodes are too far away!
        distance[node] = 1000
        predecessor[node] = None
    distance[source] = 0 # For the source we know how to reach
    return distance, predecessor


def relax(node, neighbour, graph, distance, predecessor):
    nidx = getneighbourindex(neighbour, len(graph))
    if distance[node] + graph[node][nidx] < distance[neighbour]:
        distance[neighbour] = distance[node] + graph[node][nidx]
        predecessor[neighbour] = node


def bellman_ford(matrix, graph, time_limit, source):
    dist, pred = initialize(graph, source)
    for num in range(len(graph)-1):
        for node in graph:
            temp = dict(graph)
            del temp[node]
            for neighbour in temp:
                # Step 2: Relax edges repeatedly
                relax(node, neighbour, graph, dist, pred)

    # Step 3: Check for negative-weight cycles
    for node in graph:
        for neighbour in graph:
            nidx = getneighbourindex(neighbour, len(graph))
            if dist[node] + graph[node][nidx] < dist[neighbour]:
                # We found a negative cycle. Since the door is open forever, free all the bunnies!~
                return [num for num in range(0, len(graph)-2)]

    # If we reach this point, it's time to employ floyd and also enumerate path lengths.
    spaths = floyd(matrix)
    # Uncomment the below code to see the floyd algorithm printed in a nice format.
    # for i in range(len(spaths)):
    #     print(spaths[i])
    return find_most_bunnies(matrix, spaths, time_limit)


def floyd(matrix):
    """
    Floyd's algorithm, straight from a textbook. Floyd's algorithm transforms a weight matrix
    into a matrix of shortest paths, such that the shortest path from node M to node N is
    equal to matrix[m][n]
    :return: An array of shortest-path distance calculations.
    """
    n = len(matrix)
    spaths = copy.deepcopy(matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if spaths[i][k] + spaths[k][j] < spaths[i][j]:
                    spaths[i][j] = spaths[i][k] + spaths[k][j]
    return spaths


def find_most_bunnies(matrix, spaths, time_limit):
    """
    And now, yet more inefficient bruteforcing to solve our NP-Hard problem. Enumerate all possible subsets,
    and then evaluate all their permutations to find the most efficient path.
    :param matrix: The original weighted matrix we will analyze with our algorithm.
    :param spaths: An array of shortest paths generated by the floyd's algorithm.
    :param time_limit: The time limit each subset is tested against.
    :return: The lexicographically least subset of bunnies that can escape.
    """
    n = len(matrix)-2
    bunnyids = []
    for num in range(n):
        bunnyids.append(num)
    pset = powerset(bunnyids)
    pset = sorted(pset)
    # Now that I've got all our possible subsets, I can calculate the distance of each path and determine which is
    # optimal.
    optimal_bunnies = []
    for sub in pset:
        for permutation in permutations(sub):
            # print(permutation)
            subsum = 0
            prev = 0
            next = len(matrix)-1
            for bunnyid in permutation:
                next = bunnyid+1
                subsum += spaths[prev][next]
                prev = next
            subsum += spaths[prev][len(matrix)-1]
            if subsum <= time_limit and len(sub) > len(optimal_bunnies):
                optimal_bunnies = sub
                if len(optimal_bunnies) == n:
                    break
            else:
                # Either rescue takes too long, or lexicographically lesser solution of same length exists.
                pass
    return optimal_bunnies


def solution(times, time_limit):
    # I was told when I got my degree I would never be asked to solve the Traveling Salesman Problem.
    # I was misinformed, but this was fun!
    if len(times) <= 2:
        return []
    graph = matrix2graph(times)
    return bellman_ford(times, graph, time_limit, "Start")

