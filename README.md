# 🗺️ Gujarat Intelligent Multi-Modal Transit Engine

An advanced, industry-grade **Single-Source All-Destinations Logistics Router Sandbox** modeled strictly on real-world geospatial coordinate topology arrays across top landmarks, national highways, and broad-gauge railway infrastructure points in Gujarat, India.

## 🚀 Algorithmic Architecture Inside
- **Dijkstra's Optimization Core:** Custom graph network compilation executing multi-criteria operational cost matrices (Time, Distance, and Surcharges).
- **Asymmetric Topology Matching:** Handled complete structural edge parsing with custom safe-dictionary lookups to prevent layout key exceptions (`KeyError`).
- **Dynamic Frontend Raster Display:** Real-world tracking visualizer built atop React Leaflet with adaptive Esri World Imagery (Satellite) vs OpenStreetMap vector layer switching triggers.

## 🛠️ Multi-Modal Transport Profiles Included
1. **🚗 By Road:** Strictly mapped to state and national expressways passing through key physical checkpoint intersections.
2. **🚂 By Train:** Constrained to broad-gauge Western Railway arterial links.
3. **✈️ By Plane:** Computes high-velocity direct Geodesic Haversine aviation vectors.
4. **🔀 Hybrid Mode:** Fully cohesive multi-hop combination (Road + Train transport chains).

## 💻 Tech Stack Used
- **Backend Architecture:** Python 3, FastAPI, Uvicorn ASGI Web Server Framework.
- **Frontend Layer:** React JS, Leaflet Map Client Canvas wrappers, Standard Vanilla Responsive Inline CSS layouts.

## 🏃‍♂️ Quick Setup Instructions
Clone the repository and spin up both modules:

### Backend Initialization:
```bash
cd Intelligent-Route-Planner-Graph-Algorithms
source venv/bin/activate  # venv\Scripts\activate on Windows
python -m uvicorn src.app:app --reload --port 8000

### Frontend Deployment:
```bash
cd web-ui
npm install
npm run dev
```
