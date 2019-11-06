from utils.pathfinding.priority_queue import PriorityQueue


def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break

        for next_node in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                frontier.put(next_node, priority)
                came_from[next_node] = current

    return came_from, cost_so_far


def reconstruct_path(came_from, start, goal):
    print(f'{start=}, {goal=}')
    current = goal
    path = list()
    path.append(start)  # optional
    i = 0
    for c in sorted(came_from):
        print(f'{c=} {came_from[c]}')
    while current != start and i < 100:
        print(f'{i=}, {current=}')
        i += 1
        path.append(current)
        current = came_from.get(current)

    path.reverse()  # optional
    return path
