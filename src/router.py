import heapq
import math
import networkx as nx
from src.graph_loader import time_cost, distance_cost, money_cost, eco_cost

def run_bfs(G, start):
    visited, queue, order = set([start]), [start], []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

def run_dfs(G, start):
    visited, stack, order = set(), [start], []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in sorted(G.neighbors(node), reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)
    return order

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return 2 * R * math.asin(math.sqrt(a))

def astar_heuristic(G, current, target):
    sample_curr = list(G.out_edges(current, data=True))[0][2]
    sample_targ = list(G.out_edges(target, data=True))[0][2]
    dist = haversine_distance(sample_curr["lat_u"], sample_curr["lon_u"], sample_targ["lat_u"], sample_targ["lon_u"])
    max_mps = 90000 / 3600
    return dist / max_mps

def optimize_path(G, src, dst, objective="time"):
    cost_maps = {"time": time_cost, "distance": distance_cost, "money": money_cost, "eco": eco_cost}
    target_fn = cost_maps.get(objective, time_cost)
    weight_accessor = lambda u, v, attrs: target_fn(attrs)
    
    if objective == "time":
        return nx.astar_path(G, src, dst, heuristic=lambda n1, n2: astar_heuristic(G, n1, n2), weight=weight_accessor)
    else:
        return nx.shortest_path(G, src, dst, weight=weight_accessor)

def compute_path_metrics(G, path):
    total_time, total_dist, total_toll = 0.0, 0.0, 0.0
    for u, v in zip(path[:-1], path[1:]):
        edge = G[u][v]
        total_time += time_cost(edge)
        total_dist += edge["distance_m"]
        total_toll += edge["toll"]
    return {"time_mins": round(total_time / 60, 2), "distance_km": round(total_dist / 1000, 2), "tolls_paid": total_toll}