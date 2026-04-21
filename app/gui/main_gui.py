
import tkinter as tk
from tkinter import ttk
from app.algorithms.search import bfs, dfs, astar
from app.data.network_data import build_base_graph, build_heuristic, get_node_names, COMPANY_NAME, SOURCE_LOCATION
from app.ml.travel_time import build_predicted_graph


def format_result(title_txt, traversal_order, path_list, total_cost=None, cost_label='Total Cost'):
    lines_list = []
    lines_list.append(title_txt)
    lines_list.append('')
    lines_list.append('Traversal Order')
    lines_list.append(' -> '.join(traversal_order) if traversal_order else 'No traversal result')
    lines_list.append('')
    lines_list.append('Best Path')
    lines_list.append(' -> '.join(path_list) if path_list else 'No path found')
    if total_cost is not None:
        lines_list.append('')
        lines_list.append(cost_label + ': ' + str(total_cost))
    return '\n'.join(lines_list)


def launch_app():
    base_graph = build_base_graph()
    node_names = get_node_names()

    root_app = tk.Tk()
    root_app.title('MetroSwift Logistics AI Route Optimizer')
    root_app.geometry('1040x900')

    title_label = ttk.Label(root_app, text='MetroSwift Logistics Ltd. - Lagos Route Optimization System', font=('Times New Roman', 16, 'bold'))
    title_label.pack(pady=10)

    sub_label = ttk.Label(root_app, text='Primary depot: ' + SOURCE_LOCATION + ' | Dynamic sources supported for rerouting and return-to-base operations', font=('Times New Roman', 11))
    sub_label.pack(pady=4)

    input_frame = ttk.Frame(root_app)
    input_frame.pack(pady=10)

    ttk.Label(input_frame, text='Source').grid(row=0, column=0, padx=8, pady=6)
    start_var = tk.StringVar(value=SOURCE_LOCATION)
    start_box = ttk.Combobox(input_frame, textvariable=start_var, values=node_names, state='readonly', width=24)
    start_box.grid(row=0, column=1, padx=8, pady=6)

    ttk.Label(input_frame, text='Destination').grid(row=0, column=2, padx=8, pady=6)
    goal_var = tk.StringVar(value='Ajah')
    goal_box = ttk.Combobox(input_frame, textvariable=goal_var, values=node_names, state='readonly', width=24)
    goal_box.grid(row=0, column=3, padx=8, pady=6)

    ttk.Label(input_frame, text='Traffic').grid(row=1, column=0, padx=8, pady=6)
    traffic_var = tk.DoubleVar(value=0.55)
    ttk.Scale(input_frame, from_=0.10, to=1.00, variable=traffic_var, orient='horizontal', length=180).grid(row=1, column=1, padx=8, pady=6)

    ttk.Label(input_frame, text='Peak').grid(row=1, column=2, padx=8, pady=6)
    peak_var = tk.DoubleVar(value=0.35)
    ttk.Scale(input_frame, from_=0.00, to=1.00, variable=peak_var, orient='horizontal', length=180).grid(row=1, column=3, padx=8, pady=6)

    ttk.Label(input_frame, text='Weather').grid(row=2, column=0, padx=8, pady=6)
    weather_var = tk.DoubleVar(value=0.10)
    ttk.Scale(input_frame, from_=0.00, to=0.60, variable=weather_var, orient='horizontal', length=180).grid(row=2, column=1, padx=8, pady=6)

    ttk.Label(input_frame, text='Reroute Impact').grid(row=2, column=2, padx=8, pady=6)
    reroute_var = tk.DoubleVar(value=0.08)
    ttk.Scale(input_frame, from_=0.00, to=0.50, variable=reroute_var, orient='horizontal', length=180).grid(row=2, column=3, padx=8, pady=6)

    output_box = tk.Text(root_app, wrap='word', font=('Times New Roman', 12), height=20, width=110)
    output_box.pack(padx=12, pady=12)

    def current_weighted_graph():
        scenario_data = {
            'traffic_level': traffic_var.get(),
            'peak_factor': peak_var.get(),
            'weather_factor': weather_var.get(),
            'reroute_factor': reroute_var.get()
        }
        return build_predicted_graph(base_graph, scenario_data)

    def validate_nodes():
        if start_var.get() == goal_var.get():
            output_box.delete('1.0', tk.END)
            output_box.insert(tk.END, 'Source and destination cannot be the same. Choose different nodes.')
            return False
        return True

    def show_bfs():
        if not validate_nodes():
            return
        traversal_order, path_list, total_km = bfs(base_graph, start_var.get(), goal_var.get())
        output_box.delete('1.0', tk.END)
        output_box.insert(tk.END, format_result('Breadth First Search Baseline', traversal_order, path_list, total_km, 'Approx Distance km'))

    def show_dfs():
        if not validate_nodes():
            return
        traversal_order, path_list, total_km = dfs(base_graph, start_var.get(), goal_var.get())
        output_box.delete('1.0', tk.END)
        output_box.insert(tk.END, format_result('Depth First Search Baseline', traversal_order, path_list, total_km, 'Approx Distance km'))

    def show_astar():
        if not validate_nodes():
            return
        weighted_graph = current_weighted_graph()
        heuristic_map = build_heuristic(goal_var.get())
        traversal_order, path_list, total_cost = astar(weighted_graph, heuristic_map, start_var.get(), goal_var.get(), 'predicted_time')
        output_box.delete('1.0', tk.END)
        output_box.insert(tk.END, format_result('A star Intelligent Route Optimization', traversal_order, path_list, total_cost, 'Predicted Travel Time minutes'))

    button_frame = ttk.Frame(root_app)
    button_frame.pack(pady=8)

    ttk.Button(button_frame, text='Run BFS', command=show_bfs).grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text='Run DFS', command=show_dfs).grid(row=0, column=1, padx=10)
    ttk.Button(button_frame, text='Run A star', command=show_astar).grid(row=0, column=2, padx=10)

    intro_txt = 'Use A star as the primary AI route optimizer. The source is dynamic, so a rider can start from the depot or from any delivery node for rerouting and return-to-base operations.'
    output_box.insert(tk.END, intro_txt)
    root_app.mainloop()
