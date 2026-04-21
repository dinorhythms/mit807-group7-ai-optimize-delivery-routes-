

def predict_edge_time(distance_km, traffic_level=0.55, peak_factor=0.35, weather_factor=0.10, reroute_factor=0.08):
    base_speed = 32.0
    base_minutes = (distance_km / base_speed) * 60.0
    congestion_multiplier = 1.0 + traffic_level + peak_factor + weather_factor + reroute_factor
    return round(base_minutes * congestion_multiplier, 2)


def build_predicted_graph(graph_data, scenario_data=None):
    if scenario_data is None:
        scenario_data = {}
    traffic_level = float(scenario_data.get('traffic_level', 0.55))
    peak_factor = float(scenario_data.get('peak_factor', 0.35))
    weather_factor = float(scenario_data.get('weather_factor', 0.10))
    reroute_factor = float(scenario_data.get('reroute_factor', 0.08))
    weighted_graph = {}
    for node_name, neighbor_map in graph_data.items():
        weighted_graph[node_name] = {}
        for neighbor_name, edge_vals in neighbor_map.items():
            distance_km = edge_vals.get('distance', 0)
            predicted_time = predict_edge_time(distance_km, traffic_level, peak_factor, weather_factor, reroute_factor)
            weighted_graph[node_name][neighbor_name] = {
                'distance': distance_km,
                'predicted_time': predicted_time
            }
    return weighted_graph
