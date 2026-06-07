import csv
import networkx as nx

def load_graph(csv_path="data/roads.csv"):
    G = nx.DiGraph()
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u, v = row["u"], row["v"]
            attrs = {
                "lat_u": float(row["lat_u"]), "lon_u": float(row["lon_u"]),
                "lat_v": float(row["lat_v"]), "lon_v": float(row["lon_v"]),
                "distance_m": float(row["distance_m"]),
                "speed_kph": float(row["speed_kph"]),
                "toll": float(row["toll"]),
                "one_way": int(row["one_way"]),
                "road_class": row["road_class"],
                "traffic_factor": 1.0
            }
            attrs["base_sec"] = attrs["distance_m"] / (attrs["speed_kph"] * 1000 / 3600)
            G.add_edge(u, v, **attrs)
    return G

def time_cost(e): 
    return e["base_sec"] * e.get("traffic_factor", 1.0)

def distance_cost(e): 
    return e["distance_m"]

def money_cost(e): 
    return e["toll"]

def eco_cost(e): 
    multiplier = 0.85 if e["road_class"] == "primary" else 1.05
    return time_cost(e) * multiplier