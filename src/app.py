from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import heapq

app = FastAPI(title="Gujarat Real-World Highway Engine", version="6.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 100% Interconnected Real Gujarat Highway & Railway Topology Network
GUJARAT_MAP = {
    "nodes": {
        # Primary Destinations
        "Ahmedabad_Station": {"lat": 23.0298, "lon": 72.6023, "name": "Ahmedabad Kalupur Junction"},
        "Sardar_Airport": {"lat": 23.0734, "lon": 72.6275, "name": "Ahmedabad International Airport (AMD)"},
        "Statue_of_Unity": {"lat": 21.8380, "lon": 73.7191, "name": "Statue of Unity (Kevadia)"},
        "Gir_National_Park": {"lat": 21.1243, "lon": 70.8242, "name": "Gir Forest Lion Sanctuary"},
        "Somnath_Temple": {"lat": 20.8880, "lon": 70.4012, "name": "Somnath Jyotirlinga Temple"},
        "Dwarka_Temple": {"lat": 22.2442, "lon": 68.9684, "name": "Dwarkadhish Temple"},
        "Surat_Station": {"lat": 21.2049, "lon": 72.8406, "name": "Surat Railway Junction"},
        "Vadodara_Jn": {"lat": 22.3106, "lon": 73.1812, "name": "Vadodara Central Junction"},
        "Rann_of_Kutch": {"lat": 23.8243, "lon": 71.1925, "name": "White Rann of Kutch (Dhordo)"},

        # Real Highway Turn Nodes
        "Bagodara_Chokdi": {"lat": 22.6452, "lon": 72.2461, "name": "Bagodara Highway Junction"},
        "Limbdi_Highway": {"lat": 22.5645, "lon": 71.8021, "name": "Limbdi NH47 Turn"},
        "Chotila_Hill_NH": {"lat": 22.4231, "lon": 71.1945, "name": "Chotila NH47 Track"},
        "Rajkot_Bypass": {"lat": 22.3039, "lon": 70.8022, "name": "Rajkot Highway Bypass Hub"},
        "Jetpur_Junction": {"lat": 21.7584, "lon": 70.6241, "name": "Jetpur NH27 Split"},
        "Junagadh_Bypass": {"lat": 21.5222, "lon": 70.4579, "name": "Junagadh Gir Highway"},
        "Nadiad_Highway": {"lat": 22.6938, "lon": 72.8631, "name": "Nadiad NE1 Entry"},
        "Anand_Highway": {"lat": 22.5645, "lon": 72.9289, "name": "Anand Expressway Exit"},
        "Bharuch_Bridge": {"lat": 21.7051, "lon": 72.9953, "name": "Narmada Bridge Bharuch (NH48)"},
        "Bhuj_Highway_Hub": {"lat": 23.2420, "lon": 69.6669, "name": "Bhuj Entry to Rann link"},
        
        # Fixed Rail Topology link missing pointer
        "Camp_Track_Link": {"lat": 23.0550, "lon": 72.5900, "name": "Sabarmati Western Rail Split"}
    },
    "edges": [
        # === REAL ROAD NETWORK (STRICTLY VIA HIGHWAYS) ===
        {"u": "Ahmedabad_Station", "v": "Sardar_Airport", "dist_m": 7500, "speed_kph": 50, "toll": 0, "type": "road"},
        {"u": "Sardar_Airport", "v": "Ahmedabad_Station", "dist_m": 7500, "speed_kph": 50, "toll": 0, "type": "road"},
        
        {"u": "Ahmedabad_Station", "v": "Nadiad_Highway", "dist_m": 45000, "speed_kph": 100, "toll": 60, "type": "road"},
        {"u": "Nadiad_Highway", "v": "Anand_Highway", "dist_m": 20000, "speed_kph": 100, "toll": 40, "type": "road"},
        {"u": "Anand_Highway", "v": "Vadodara_Jn", "dist_m": 45000, "speed_kph": 100, "toll": 80, "type": "road"},
        {"u": "Vadodara_Jn", "v": "Anand_Highway", "dist_m": 45000, "speed_kph": 100, "toll": 80, "type": "road"},
        {"u": "Anand_Highway", "v": "Nadiad_Highway", "dist_m": 20000, "speed_kph": 100, "toll": 40, "type": "road"},
        {"u": "Nadiad_Highway", "v": "Ahmedabad_Station", "dist_m": 45000, "speed_kph": 100, "toll": 60, "type": "road"},

        {"u": "Vadodara_Jn", "v": "Statue_of_Unity", "dist_m": 90000, "speed_kph": 75, "toll": 0, "type": "road"},
        {"u": "Statue_of_Unity", "v": "Vadodara_Jn", "dist_m": 90000, "speed_kph": 75, "toll": 0, "type": "road"},

        {"u": "Vadodara_Jn", "v": "Bharuch_Bridge", "dist_m": 75000, "speed_kph": 90, "toll": 110, "type": "road"},
        {"u": "Bharuch_Bridge", "v": "Surat_Station", "dist_m": 75000, "speed_kph": 90, "toll": 110, "type": "road"},
        {"u": "Surat_Station", "v": "Bharuch_Bridge", "dist_m": 75000, "speed_kph": 90, "toll": 110, "type": "road"},
        {"u": "Bharuch_Bridge", "v": "Vadodara_Jn", "dist_m": 75000, "speed_kph": 90, "toll": 110, "type": "road"},

        {"u": "Ahmedabad_Station", "v": "Bagodara_Chokdi", "dist_m": 60000, "speed_kph": 80, "toll": 50, "type": "road"},
        {"u": "Bagodara_Chokdi", "v": "Limbdi_Highway", "dist_m": 40000, "speed_kph": 90, "toll": 40, "type": "road"},
        {"u": "Limbdi_Highway", "v": "Chotila_Hill_NH", "dist_m": 55000, "speed_kph": 90, "toll": 0, "type": "road"},
        {"u": "Chotila_Hill_NH", "v": "Rajkot_Bypass", "dist_m": 45000, "speed_kph": 90, "toll": 50, "type": "road"},
        {"u": "Rajkot_Bypass", "v": "Chotila_Hill_NH", "dist_m": 45000, "speed_kph": 90, "toll": 50, "type": "road"},
        {"u": "Chotila_Hill_NH", "v": "Limbdi_Highway", "dist_m": 55000, "speed_kph": 90, "toll": 0, "type": "road"},
        {"u": "Limbdi_Highway", "v": "Bagodara_Chokdi", "dist_m": 40000, "speed_kph": 90, "toll": 40, "type": "road"},
        {"u": "Bagodara_Chokdi", "v": "Ahmedabad_Station", "dist_m": 60000, "speed_kph": 80, "toll": 50, "type": "road"},

        {"u": "Rajkot_Bypass", "v": "Dwarka_Temple", "dist_m": 225000, "speed_kph": 80, "toll": 80, "type": "road"},
        {"u": "Dwarka_Temple", "v": "Rajkot_Bypass", "dist_m": 225000, "speed_kph": 80, "toll": 80, "type": "road"},

        {"u": "Rajkot_Bypass", "v": "Jetpur_Junction", "dist_m": 70000, "speed_kph": 80, "toll": 50, "type": "road"},
        {"u": "Jetpur_Junction", "v": "Junagadh_Bypass", "dist_m": 30000, "speed_kph": 80, "toll": 0, "type": "road"},
        {"u": "Junagadh_Bypass", "v": "Somnath_Temple", "dist_m": 90000, "speed_kph": 75, "toll": 60, "type": "road"},
        {"u": "Somnath_Temple", "v": "Junagadh_Bypass", "dist_m": 90000, "speed_kph": 75, "toll": 60, "type": "road"},
        {"u": "Junagadh_Bypass", "v": "Jetpur_Junction", "dist_m": 30000, "speed_kph": 80, "toll": 0, "type": "road"},
        {"u": "Jetpur_Junction", "v": "Rajkot_Bypass", "dist_m": 70000, "speed_kph": 80, "toll": 50, "type": "road"},

        {"u": "Somnath_Temple", "v": "Gir_National_Park", "dist_m": 50000, "speed_kph": 50, "toll": 0, "type": "road"},
        {"u": "Gir_National_Park", "v": "Somnath_Temple", "dist_m": 50000, "speed_kph": 50, "toll": 0, "type": "road"},
        
        {"u": "Dwarka_Temple", "v": "Somnath_Temple", "dist_m": 230000, "speed_kph": 70, "toll": 0, "type": "road"},
        {"u": "Somnath_Temple", "v": "Dwarka_Temple", "dist_m": 230000, "speed_kph": 70, "toll": 0, "type": "road"},

        {"u": "Somnath_Temple", "v": "Statue_of_Unity", "dist_m": 500000, "speed_kph": 80, "toll": 250, "type": "road"},
        {"u": "Statue_of_Unity", "v": "Somnath_Temple", "dist_m": 500000, "speed_kph": 80, "toll": 250, "type": "road"},

        {"u": "Ahmedabad_Station", "v": "Bhuj_Highway_Hub", "dist_m": 330000, "speed_kph": 80, "toll": 110, "type": "road"},
        {"u": "Bhuj_Highway_Hub", "v": "Rann_of_Kutch", "dist_m": 70000, "speed_kph": 60, "toll": 0, "type": "road"},
        {"u": "Rann_of_Kutch", "v": "Bhuj_Highway_Hub", "dist_m": 70000, "speed_kph": 60, "toll": 0, "type": "road"},
        {"u": "Bhuj_Highway_Hub", "v": "Ahmedabad_Station", "dist_m": 330000, "speed_kph": 80, "toll": 110, "type": "road"},

        # === REAL RAILWAY LINES MATRIX LINK ===
        {"u": "Ahmedabad_Station", "v": "Camp_Track_Link", "dist_m": 5000, "speed_kph": 40, "toll": 0, "type": "train"},
        {"u": "Camp_Track_Link", "v": "Ahmedabad_Station", "dist_m": 5000, "speed_kph": 40, "toll": 0, "type": "train"},
        {"u": "Camp_Track_Link", "v": "Vadodara_Jn", "dist_m": 95000, "speed_kph": 110, "toll": 0, "type": "train"},
        {"u": "Vadodara_Jn", "v": "Camp_Track_Link", "dist_m": 95000, "speed_kph": 110, "toll": 0, "type": "train"},
        
        {"u": "Ahmedabad_Station", "v": "Vadodara_Jn", "dist_m": 100000, "speed_kph": 110, "toll": 0, "type": "train"},
        {"u": "Vadodara_Jn", "v": "Ahmedabad_Station", "dist_m": 100000, "speed_kph": 110, "toll": 0, "type": "train"},
        {"u": "Vadodara_Jn", "v": "Surat_Station", "dist_m": 130000, "speed_kph": 120, "toll": 0, "type": "train"},
        {"u": "Surat_Station", "v": "Vadodara_Jn", "dist_m": 130000, "speed_kph": 120, "toll": 0, "type": "train"}
    ]
}

class FullMatrixRequest(BaseModel):
    source: str
    objective: str
    mode: str

@app.post("/api/v1/matrix")
async def process_complete_matrix(req: FullMatrixRequest):
    nodes = GUJARAT_MAP["nodes"]
    if req.source not in nodes:
        raise HTTPException(status_code=400, detail="Invalid source node identification.")

    allowed_modes = ["road"] if req.mode == "road" else ["train"] if req.mode == "train" else ["road", "train"]
    
    # Secure initialization structure mapping safely across strings
    adj = {n: {} for n in nodes}
    edge_data = {}
    for edge in GUJARAT_MAP["edges"]:
        if req.mode == "plane" or edge["type"] in allowed_modes:
            u, v = edge["u"], edge["v"]
            # Guard checking against untracked layout arrays
            if u in adj and v in adj:
                if req.objective == "time": cost = (edge["dist_m"] / (edge["speed_kph"] * 1000 / 3600)) / 60.0
                elif req.objective == "distance": cost = edge["dist_m"] / 1000.0
                else: cost = edge["toll"] + (edge["dist_m"] * 0.01)
                adj[u][v] = cost
                edge_data[(u, v)] = edge

    matrix_output = {}
    
    for target in nodes.keys():
        if target == req.source:
            matrix_output[target] = {"time_mins": 0, "distance_km": 0, "tolls_paid": 0, "path": [req.source]}
            continue

        if req.mode == "plane":
            R = 6371.0
            loc1, loc2 = nodes[req.source], nodes[target]
            dlat, dlon = math.radians(loc2["lat"] - loc1["lat"]), math.radians(loc2["lon"] - loc1["lon"])
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1 := loc1["lat"])) * math.cos(math.radians(lat2 := loc2["lat"])) * math.sin(dlon/2)**2
            distance_km = 2 * R * math.asin(math.sqrt(a))
            matrix_output[target] = {"time_mins": round((distance_km / 700.0) * 60.0 + 25.0, 2), "distance_km": round(distance_km, 2), "tolls_paid": 0, "path": [req.source, target]}
            continue

        pq = [(0.0, req.source, [])]
        visited = set()
        route_found = False
        
        while pq:
            (cost, current, path) = heapq.heappop(pq)
            if current in visited: continue
            visited.add(current)
            path = path + [current]

            if current == target:
                total_m, total_toll_paid = 0, 0
                for i in range(len(path)-1):
                    e = edge_data.get((path[i], path[i+1]))
                    if e:
                        total_m += e["dist_m"]
                        total_toll_paid += e["toll"]
                
                calculated_mins = cost if req.objective == "time" else (total_m / (75 * 1000 / 3600)) / 60.0
                matrix_output[target] = {"time_mins": round(calculated_mins, 2), "distance_km": round(total_m / 1000.0, 2), "tolls_paid": total_toll_paid, "path": path}
                route_found = True
                break
                
            # Guard against KeyErrors using safe hash dictionary extractions
            for neighbor, weight in adj.get(current, {}).items():
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + weight, neighbor, path))
                    
        if not route_found:
            matrix_output[target] = {"time_mins": "N/A", "distance_km": "N/A", "tolls_paid": "N/A", "path": []}

    return {"status": "SUCCESS", "source": req.source, "matrix_data": matrix_output, "node_details": nodes}