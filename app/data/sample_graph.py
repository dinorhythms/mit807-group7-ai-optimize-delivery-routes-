# Lagos inspired sample graph and heuristic values for demonstration

RAW_GRAPH = {
    'Ikeja': {'Yaba': {'distance': 9}, 'Surulere': {'distance': 12}},
    'Yaba': {'Surulere': {'distance': 7}, 'Victoria Island': {'distance': 14}},
    'Surulere': {'Victoria Island': {'distance': 11}, 'Lekki': {'distance': 20}},
    'Victoria Island': {'Lekki': {'distance': 8}, 'Ajah': {'distance': 18}},
    'Lekki': {'Ajah': {'distance': 10}},
    'Ajah': {}
}

HEURISTIC_TO_AJAH = {
    'Ikeja': 24,
    'Yaba': 18,
    'Surulere': 15,
    'Victoria Island': 10,
    'Lekki': 6,
    'Ajah': 0
}
