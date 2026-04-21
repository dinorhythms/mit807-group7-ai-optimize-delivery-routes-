
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from core.algorithms.search import bfs, dfs, astar
from core.data.network_data import build_base_graph, build_heuristic, SOURCE_LOCATION
from core.ml.travel_time import build_predicted_graph


def run_tests():
    base_graph = build_base_graph()
    weighted_graph = build_predicted_graph(base_graph, {
        'traffic_level': 0.55,
        'peak_factor': 0.35,
        'weather_factor': 0.10,
        'reroute_factor': 0.08
    })
    bfs_order, bfs_path, bfs_distance = bfs(base_graph, SOURCE_LOCATION, 'Ajah')
    dfs_order, dfs_path, dfs_distance = dfs(base_graph, SOURCE_LOCATION, 'Ajah')
    astar_order, astar_path, astar_cost = astar(weighted_graph, build_heuristic('Ajah'), SOURCE_LOCATION, 'Ajah', 'predicted_time')
    reroute_order, reroute_path, reroute_cost = astar(weighted_graph, build_heuristic('Alausa, Ikeja'), 'Victoria Island', 'Alausa, Ikeja', 'predicted_time')
    assert bfs_path[0] == SOURCE_LOCATION
    assert bfs_path[-1] == 'Ajah'
    assert dfs_path[0] == SOURCE_LOCATION
    assert dfs_path[-1] == 'Ajah'
    assert astar_path[0] == SOURCE_LOCATION
    assert astar_path[-1] == 'Ajah'
    assert reroute_path[0] == 'Victoria Island'
    assert reroute_path[-1] == 'Alausa, Ikeja'
    assert bfs_distance is not None
    assert dfs_distance is not None
    assert astar_cost is not None
    assert reroute_cost is not None
    print(bfs_order)
    print(bfs_path)
    print(bfs_distance)
    print(dfs_order)
    print(dfs_path)
    print(dfs_distance)
    print(astar_order)
    print(astar_path)
    print(astar_cost)
    print(reroute_order)
    print(reroute_path)
    print(reroute_cost)


if __name__ == '__main__':
    run_tests()
