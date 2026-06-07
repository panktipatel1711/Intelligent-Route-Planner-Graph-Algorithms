import networkx as nx
from src.graph_loader import time_cost, distance_cost, money_cost

def get_alternative_routes(G, src, dst, k=4):
    raw_paths = list(nx.shortest_simple_paths(G, src, dst, weight=lambda u, v, a: time_cost(a)))[:k]
    scored_profiles = []
    
    for path in raw_paths:
        t = sum(time_cost(G[u][v]) for u, v in zip(path[:-1], path[1:]))
        d = sum(distance_cost(G[u][v]) for u, v in zip(path[:-1], path[1:]))
        m = sum(money_cost(G[u][v]) for u, v in zip(path[:-1], path[1:]))
        scored_profiles.append((path, (t, d, m)))
        
    pareto_set = []
    for candidate_path, candidate_vector in scored_profiles:
        dominated = False
        for comparator_path, comparator_vector in scored_profiles:
            if candidate_path == comparator_path:
                continue
            if all(v_comp <= v_cand for v_comp, v_cand in zip(comparator_vector, candidate_vector)) and                any(v_comp < v_cand for v_comp, v_cand in zip(comparator_vector, candidate_vector)):
                dominated = True
                break
        if not dominated:
            pareto_set.append((candidate_path, candidate_vector))
            
    return pareto_set