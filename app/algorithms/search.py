
from collections import deque
import heapq


def reconstruct_path(parent_map, goal_node):
    if goal_node not in parent_map:
        return []
    path_list = []
    current_node = goal_node
    while current_node is not None:
        path_list.append(current_node)
        current_node = parent_map[current_node]
    path_list.reverse()
    return path_list


def path_distance(graph_data, path_list, weight_key):
    total_val = 0
    if len(path_list) < 2:
        return total_val
    for idx_val in range(len(path_list) - 1):
        node_a = path_list[idx_val]
        node_b = path_list[idx_val + 1]
        total_val += graph_data[node_a][node_b].get(weight_key, 0)
    return round(total_val, 2)


def bfs(graph_data, start_node, goal_node):
    queue_vals = deque([start_node])
    visited_nodes = {start_node}
    parent_map = {start_node: None}
    traversal_order = []
    while queue_vals:
        node_val = queue_vals.popleft()
        traversal_order.append(node_val)
        if node_val == goal_node:
            break
        for neighbor_val in graph_data.get(node_val, {}):
            if neighbor_val not in visited_nodes:
                visited_nodes.add(neighbor_val)
                parent_map[neighbor_val] = node_val
                queue_vals.append(neighbor_val)
    path_list = reconstruct_path(parent_map, goal_node)
    return traversal_order, path_list, path_distance(graph_data, path_list, 'distance')


def dfs(graph_data, start_node, goal_node):
    stack_vals = [start_node]
    visited_nodes = {start_node}
    parent_map = {start_node: None}
    traversal_order = []
    while stack_vals:
        node_val = stack_vals.pop()
        traversal_order.append(node_val)
        if node_val == goal_node:
            break
        neighbors_list = list(graph_data.get(node_val, {}).keys())
        neighbors_list.reverse()
        for neighbor_val in neighbors_list:
            if neighbor_val not in visited_nodes:
                visited_nodes.add(neighbor_val)
                parent_map[neighbor_val] = node_val
                stack_vals.append(neighbor_val)
    path_list = reconstruct_path(parent_map, goal_node)
    return traversal_order, path_list, path_distance(graph_data, path_list, 'distance')


def astar(graph_data, heuristic_map, start_node, goal_node, weight_key='predicted_time'):
    open_heap = [(heuristic_map.get(start_node, 0), start_node)]
    parent_map = {start_node: None}
    g_score_map = {start_node: 0}
    visited_order = []
    closed_nodes = set()
    while open_heap:
        current_f, current_node = heapq.heappop(open_heap)
        if current_node in closed_nodes:
            continue
        closed_nodes.add(current_node)
        visited_order.append(current_node)
        if current_node == goal_node:
            break
        for neighbor_val, edge_data in graph_data.get(current_node, {}).items():
            edge_cost = edge_data.get(weight_key, edge_data.get('distance', 1))
            tentative_score = g_score_map[current_node] + edge_cost
            if neighbor_val not in g_score_map or tentative_score < g_score_map[neighbor_val]:
                g_score_map[neighbor_val] = tentative_score
                parent_map[neighbor_val] = current_node
                next_f = tentative_score + heuristic_map.get(neighbor_val, 0)
                heapq.heappush(open_heap, (next_f, neighbor_val))
    path_list = reconstruct_path(parent_map, goal_node)
    total_cost = None
    if goal_node in g_score_map:
        total_cost = round(g_score_map[goal_node], 2)
    return visited_order, path_list, total_cost
