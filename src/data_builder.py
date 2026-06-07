import csv
import os

def write_grid(n=5, spacing_m=300):
    os.makedirs("data", exist_ok=True)
    rows = []
    node_id = lambda i, j: f"N{i}_{j}"
    coords = {}
    
    for i in range(n):
        for j in range(n):
            lat, lon = 12.90 + i * 0.002, 77.50 + j * 0.002
            coords[node_id(i, j)] = (lat, lon)

    def add_edge(u, v, dist, speed, toll, one_way, road_class):
        lat_u, lon_u = coords[u]
        lat_v, lon_v = coords[v]
        rows.append([u, v, lat_u, lon_u, lat_v, lon_v, dist, speed, toll, one_way, road_class])

    for i in range(n):
        for j in range(n):
            if j + 1 < n:
                u, v = node_id(i, j), node_id(i, j + 1)
                add_edge(u, v, spacing_m, 40, 0, 0, "residential")
                add_edge(v, u, spacing_m, 40, 0, 0, "residential")
            if i + 1 < n:
                u, v = node_id(i, j), node_id(i + 1, j)
                add_edge(u, v, spacing_m, 35, 0, 0, "residential")
                add_edge(v, u, spacing_m, 35, 0, 0, "residential")

    for j in range(n - 1):
        u, v = node_id(2, j), node_id(2, j + 1)
        add_edge(u, v, spacing_m, 80, 5, 0, "primary")
        add_edge(v, u, spacing_m, 80, 5, 0, "primary")

    add_edge(node_id(0, 0), node_id(2, 2), spacing_m * 2.8, 90, 0, 1, "link")

    with open("data/roads.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow("u,v,lat_u,lon_u,lat_v,lon_v,distance_m,speed_kph,toll,one_way,road_class".split(","))
        w.writerows(rows)
    print("[SUCCESS] data/roads.csv initialized successfully with complex network traits.")

if __name__ == "__main__":
    write_grid()