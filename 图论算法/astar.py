# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 22:30:22 2020

reference: https://zhuanlan.zhihu.com/p/113390876
"""

import heapq
import collections
import copy

class Queue:
    '''
    The queue this code used
    '''
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()
    

class SquareGrid:
    '''
    2-dim grid
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        '''
        To judge whether the coordinate is in bound.
        '''
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0:
            results.reverse() #This step is kind of confusing. Why do this?
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        '''
        The default weight from the to_node is 1.
        '''
        return self.weights.get(to_node, 1)
    

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        '''
        Only get the coordinate.
        '''
        return heapq.heappop(self.elements)[1]
    
    
def reconstruct_path(came_from: dict, start: tuple, goal: tuple):
    current = goal
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()
    return path


def heuristic(a, b):
    '''
    Here we use Manhattan distance. This function can be change if necessary.
    '''
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph: GridWithWeights, start: tuple, goal: tuple):
    '''
    To run A star algorithm.
    '''
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def draw_grid(g: SquareGrid, width: int,
               point_to: list,
               start: tuple,
               goal: tuple,
               path = []):
    '''
    Parameters
    ----------
    g : SquareGrid
        DESCRIPTION.
    width : int
        The width of the gap between two grids in the neighbourhood.
    point_to : list
        The direction of the arrows.
    start : tuple
        The start point.
    goal : tuple
        The goal point.

    '''
    if path:
        path = copy.deepcopy(path)
        path.sort(key = lambda x: x[1])
    for j in range(g.height):
        for i in range(g.width):
            if (i, j) == start:
                print('A' + ' ' * (width - 1), end='')
                if path:
                    path.pop(0)
            elif (i, j) == goal:
                print('Z' + ' ' * (width - 1), end='')
                if path:
                    path.pop(0)
            elif not g.passable((i, j)):
                print('#' * width, end='')
            elif path and (i,j) == path[0]:
                print('@' + ' ' * (width - 1), end='')
                path.pop(0)
            else:
                space = ' ' * (width - 1)
                if (i, j) in point_to:
                    came_from = point_to[(i, j)]
                    if came_from == (i - 1, j):
                        print('<' + space, end='')
                    elif came_from == (i + 1, j):
                        print('>' + space, end='')
                    elif came_from == (i, j - 1):
                        print('^' + space, end='')
                    else:
                        print('V' + space, end='')
                else:
                    print('.' + space, end='')
        print()
        
        
def main():
    g = GridWithWeights(30, 15)
    
    DIAGRAM1_WALLS = [] #墙的位置
    for i in range(3, 5):
        for j in range(3, 12):
            DIAGRAM1_WALLS.append((i, j))

    for i in range(13, 15):
        for j in range(4, 15):
            DIAGRAM1_WALLS.append((i, j))

    for i in range(21, 23):
        for j in range(0, 7):
            DIAGRAM1_WALLS.append((i, j))

    for i in range(23, 26):
        for j in range(5, 7):
            DIAGRAM1_WALLS.append((i, j))
    g.walls = DIAGRAM1_WALLS
    
    parents, cost_so_far = a_star_search(g, (8, 7), (17, 2))
    draw_grid(g, width=2, point_to=parents, start=(8, 7), goal=(17, 2))
    
    print()
    path = reconstruct_path(parents, start = (8,7), goal = (17,2))
    
    draw_grid(g, width=2, point_to=parents, start=(8, 7), goal=(17, 2), path = path)
    
    # print(path)
    total_cost = 0
    for i in range(len(path)-1):
        total_cost += g.cost(path[i], path[i+1])
    print("The total cost is", total_cost)
    '''
    for coordinate in path:
        total_cost += g.cost((), coordinate)
    print("The total cost is", total_cost)
    '''
    
    
if __name__ == '__main__':
    main()