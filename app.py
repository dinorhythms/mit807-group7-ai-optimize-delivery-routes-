from flask import Flask, render_template, request, jsonify
import os
from core.algorithms.search import bfs, dfs, astar
from core.data.network_data import build_base_graph, build_heuristic, get_node_names, COMPANY_NAME, SOURCE_LOCATION
from core.ml.travel_time import build_predicted_graph

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize graph data
base_graph = build_base_graph()
node_names = get_node_names()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html',
                         company_name=COMPANY_NAME,
                         source_location=SOURCE_LOCATION,
                         node_names=node_names)


@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    """Get list of available nodes"""
    return jsonify({'nodes': node_names})


@app.route('/api/run-bfs', methods=['POST'])
def run_bfs():
    """Run BFS algorithm"""
    data = request.json
    source = data.get('source')
    destination = data.get('destination')

    if source == destination:
        return jsonify({'error': 'Source and destination cannot be the same'}), 400

    traversal_order, path_list, total_km = bfs(base_graph, source, destination)

    return jsonify({
        'title': 'Breadth First Search Baseline',
        'traversal_order': traversal_order,
        'path': path_list,
        'total_cost': total_km,
        'cost_label': 'Approx Distance (km)',
        'algorithm': 'BFS'
    })


@app.route('/api/run-dfs', methods=['POST'])
def run_dfs():
    """Run DFS algorithm"""
    data = request.json
    source = data.get('source')
    destination = data.get('destination')

    if source == destination:
        return jsonify({'error': 'Source and destination cannot be the same'}), 400

    traversal_order, path_list, total_km = dfs(base_graph, source, destination)

    return jsonify({
        'title': 'Depth First Search Baseline',
        'traversal_order': traversal_order,
        'path': path_list,
        'total_cost': total_km,
        'cost_label': 'Approx Distance (km)',
        'algorithm': 'DFS'
    })


@app.route('/api/run-astar', methods=['POST'])
def run_astar():
    """Run A* algorithm with dynamic weights"""
    data = request.json
    source = data.get('source')
    destination = data.get('destination')

    if source == destination:
        return jsonify({'error': 'Source and destination cannot be the same'}), 400

    scenario_data = {
        'traffic_level': data.get('traffic_level', 0.55),
        'peak_factor': data.get('peak_factor', 0.35),
        'weather_factor': data.get('weather_factor', 0.10),
        'reroute_factor': data.get('reroute_factor', 0.08)
    }

    weighted_graph = build_predicted_graph(base_graph, scenario_data)
    heuristic_map = build_heuristic(destination)
    traversal_order, path_list, total_cost = astar(weighted_graph, heuristic_map, source, destination, 'predicted_time')

    return jsonify({
        'title': 'A* Intelligent Route Optimization',
        'traversal_order': traversal_order,
        'path': path_list,
        'total_cost': total_cost,
        'cost_label': 'Predicted Travel Time (minutes)',
        'algorithm': 'A*',
        'scenario': scenario_data
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
