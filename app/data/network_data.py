
import math
import pandas as pd
from pathlib import Path

SOURCE_LOCATION = 'Alausa, Ikeja'
COMPANY_NAME = 'MetroSwift Logistics Ltd.'

COORDINATES = {
    'Alausa, Ikeja': (0.0, 0.0),
    'Maryland': (3.0, -2.0),
    'Mushin': (4.0, -5.0),
    'Yaba': (6.0, -8.0),
    'Surulere': (6.0, -6.0),
    'Apapa': (9.0, -10.0),
    'Victoria Island': (12.0, -10.0),
    'Ikoyi': (11.0, -9.0),
    'Lekki Phase 1': (15.0, -11.0),
    'Ajah': (20.0, -12.0),
    'Festac Town': (8.0, -11.0),
    'Ikorodu': (13.0, 2.0),
    'Badagry': (-12.0, -13.0)
}

CONNECTIVITY = {
    'Alausa, Ikeja': ['Maryland', 'Mushin', 'Yaba', 'Ikorodu'],
    'Maryland': ['Alausa, Ikeja', 'Mushin', 'Yaba', 'Surulere'],
    'Mushin': ['Alausa, Ikeja', 'Maryland', 'Surulere', 'Apapa'],
    'Yaba': ['Alausa, Ikeja', 'Maryland', 'Surulere', 'Victoria Island'],
    'Surulere': ['Maryland', 'Mushin', 'Yaba', 'Apapa', 'Festac Town'],
    'Apapa': ['Mushin', 'Surulere', 'Victoria Island', 'Festac Town', 'Badagry'],
    'Victoria Island': ['Yaba', 'Apapa', 'Ikoyi', 'Lekki Phase 1'],
    'Ikoyi': ['Victoria Island', 'Lekki Phase 1'],
    'Lekki Phase 1': ['Victoria Island', 'Ikoyi', 'Ajah'],
    'Ajah': ['Lekki Phase 1'],
    'Festac Town': ['Surulere', 'Apapa', 'Badagry'],
    'Ikorodu': ['Alausa, Ikeja', 'Maryland'],
    'Badagry': ['Festac Town', 'Apapa']
}


def load_destinations_df():
    csv_path = Path(__file__).resolve().parent / 'lagos_destinations.csv'
    return pd.read_csv(csv_path)


def euclidean_distance(node_a, node_b):
    ax_val, ay_val = COORDINATES[node_a]
    bx_val, by_val = COORDINATES[node_b]
    return math.sqrt((ax_val - bx_val) ** 2 + (ay_val - by_val) ** 2)


def build_base_graph():
    graph_data = {node_name: {} for node_name in CONNECTIVITY}
    for node_name, neighbor_list in CONNECTIVITY.items():
        for neighbor_name in neighbor_list:
            road_distance = round(euclidean_distance(node_name, neighbor_name) * 1.8, 2)
            graph_data[node_name][neighbor_name] = {'distance': road_distance}
    return graph_data


def build_heuristic(goal_node):
    heuristic_map = {}
    for node_name in COORDINATES:
        heuristic_map[node_name] = round(euclidean_distance(node_name, goal_node) * 1.5, 2)
    return heuristic_map


def get_node_names():
    return list(COORDINATES.keys())
