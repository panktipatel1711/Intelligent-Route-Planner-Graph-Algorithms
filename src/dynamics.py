def inject_traffic_spike(G, u, v, factor=2.5):
    if G.has_edge(u, v):
        G[u][v]["traffic_factor"] = factor

def register_road_closure(G, u, v):
    if G.has_edge(u, v):
        G.remove_edge(u, v)