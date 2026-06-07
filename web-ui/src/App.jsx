import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Polyline, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function MapController({ points, center }) {
  const map = useMap();
  useEffect(() => {
    if (points && points.length > 0) {
      map.flyToBounds(points, { padding: [80, 80], maxZoom: 10, animate: true, duration: 1.2 });
    } else if (center) {
      map.flyTo(center, 7, { animate: true });
    }
  }, [points, center, map]);
  return null;
}

export default function App() {
  const [source, setSource] = useState('Ahmedabad_Station');
  const [objective, setObjective] = useState('time');
  const [mode, setMode] = useState('road');
  const [matrix, setMatrix] = useState({});
  const [nodesInfo, setNodesInfo] = useState({});
  const [selectedDest, setSelectedDest] = useState('');
  const [geoJsonPath, setGeoJsonPath] = useState([]);
  const [error, setError] = useState('');

  const triggerMatrixRouting = async () => {
    setError('');
    try {
      const res = await fetch('http://localhost:8000/api/v1/matrix', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, objective, mode })
      });
      const data = await res.json();
      if (data.status === 'SUCCESS') {
        setMatrix(data.matrix_data);
        setNodesInfo(data.node_details);
        if (selectedDest && data.matrix_data[selectedDest]?.path.length > 0) {
          drawRoute(data.matrix_data[selectedDest].path, data.node_details);
        } else {
          setGeoJsonPath([]);
        }
      }
    } catch (err) {
      setError('FastAPI Server Offline! Run: uvicorn src.app:app --reload');
    }
  };

  const drawRoute = (path, nodes) => {
    if (!path || path.length === 0) return;
    const coords = path.map(nodeId => [nodes[nodeId].lat, nodes[nodeId].lon]);
    setGeoJsonPath(coords);
  };

  useEffect(() => { 
    triggerMatrixRouting(); 
  }, [source, objective, mode]);

  return (
    <div style={{ display: "grid", gridTemplateColumns: "500px 1fr", height: "100vh", width: "100vw", fontFamily: "Segoe UI, sans-serif", backgroundColor: "#0f172a", color: "white", margin: 0, overflow: "hidden" }}>
      
      {/* SIDEBAR PANEL CONTAINER */}
      <div style={{ padding: "24px", display: "flex", flexDirection: "column", borderRight: "1px solid #334155", backgroundColor: "#1e293b", boxSizing: "border-box", zIndex: 10, height: "100vh", overflowY: "auto" }}>
        <div>
          <h1 style={{ fontSize: "20px", fontWeight: "900", color: "#10b981", margin: "0 0 4px 0" }}>GUJARAT TRANSIT ENGINE V6</h1>
          <p style={{ fontSize: "11px", color: "#94a3b8", margin: "0 0 20px 0" }}>Interconnected Highway Matrix Sandbox</p>
          
          <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginBottom: "20px" }}>
            <div>
              <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#94a3b8", marginBottom: "6px" }}>START LOCATION (SOURCE)</label>
              <select style={{ width: "100%", padding: "10px", backgroundColor: "#334155", border: "1px solid #475569", borderRadius: "6px", color: "white", fontSize: "13px" }} value={source} onChange={e => { setSource(e.target.value); setGeoJsonPath([]); setSelectedDest(''); }}>
                <option value="Ahmedabad_Station">Ahmedabad Kalupur Station Hub</option>
                <option value="Sardar_Airport">Sardar Patel International Airport</option>
                <option value="Statue_of_Unity">Statue of Unity (Kevadia)</option>
                <option value="Gir_National_Park">Gir Forest Lion Sanctuary</option>
                <option value="Somnath_Temple">Somnath Jyotirlinga Temple</option>
                <option value="Dwarka_Temple">Dwarkadhish Temple (Dwarka)</option>
                <option value="Surat_Station">Surat Textile Junction Station</option>
                <option value="Vadodara_Jn">Vadodara Central Junction</option>
                <option value="Rann_of_Kutch">White Rann of Kutch (Dhordo)</option>
              </select>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
              <div>
                <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#94a3b8", marginBottom: "6px" }}>TRANSIT MODE</label>
                <select style={{ width: "100%", padding: "10px", backgroundColor: "#334155", border: "1px solid #475569", borderRadius: "6px", color: "white", fontSize: "13px" }} value={mode} onChange={e => setMode(e.target.value)}>
                  <option value="road">🚗 By Road (Car)</option>
                  <option value="train">🚂 By Train</option>
                  <option value="plane">✈️ By Plane</option>
                  <option value="hybrid">🔀 Road + Train</option>
                </select>
              </div>
              <div>
                <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#94a3b8", marginBottom: "6px" }}>CRITERIA</label>
                <select style={{ width: "100%", padding: "10px", backgroundColor: "#334155", border: "1px solid #475569", borderRadius: "6px", color: "white", fontSize: "13px" }} value={objective} onChange={e => setObjective(e.target.value)}>
                  <option value="time">⏱️ Fastest</option>
                  <option value="distance">🛣️ Shortest</option>
                  <option value="money">💵 Cheapest</option>
                </select>
              </div>
            </div>
          </div>

          {error && <div style={{ padding: "10px", backgroundColor: "rgba(220, 38, 38, 0.2)", border: "1px solid #ef4444", borderRadius: "6px", fontSize: "12px", color: "#fca5a5", marginBottom: "15px" }}>{error}</div>}

          {/* TABLE CONTAINER FOR DESTINATIONS */}
          <div style={{ marginTop: "10px" }}>
            <h3 style={{ fontSize: "12px", fontWeight: "bold", color: "#cbd5e1", textTransform: "uppercase", marginBottom: "10px" }}>Select Destination Target List:</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
              {Object.keys(matrix).map((destKey) => {
                if (destKey === source || destKey.includes('_NH') || destKey.includes('_Chokdi') || destKey.includes('_Highway') || destKey.includes('_Bypass') || destKey.includes('_Link') || destKey.includes('_Bridge') || destKey.includes('_Hub')) return null;
                const targetData = matrix[destKey];
                const isSelected = selectedDest === destKey;
                
                return (
                  <div 
                    key={destKey} 
                    onClick={() => {
                      if (targetData.path.length > 0) {
                        setSelectedDest(destKey);
                        drawRoute(targetData.path, nodesInfo);
                      }
                    }}
                    style={{ 
                      padding: "12px", 
                      backgroundColor: isSelected ? "#047857" : "rgba(15, 23, 42, 0.3)", 
                      border: isSelected ? "1px solid #10b981" : "1px solid #475569", 
                      borderRadius: "6px", 
                      cursor: targetData.path.length > 0 ? "pointer" : "not-allowed"
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                      <span style={{ fontSize: "13px", fontWeight: "bold" }}>{destKey.replace(/_/g, ' ')}</span>
                      <span style={{ fontSize: "12px", fontWeight: "bold", color: "#10b981" }}>{targetData.time_mins !== "N/A" ? `${targetData.time_mins} mins` : "Route Blocked"}</span>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#94a3b8" }}>
                      <span>📏 {targetData.distance_km} km</span>
                      <span>💵 Toll: ${targetData.tolls_paid}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* MAP VIEW CANVAS CONTAINER */}
      <div style={{ width: "100%", height: "100vh", position: "relative" }}>
        <MapContainer center={[22.3094, 72.1362]} zoom={7} style={{ height: "100%", width: "100%" }}>
          {mode === 'plane' ? (
            <TileLayer attribution='&copy; Esri World Imagery' url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" />
          ) : (
            <TileLayer attribution='&copy; OpenStreetMap' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          )}
          <MapController points={geoJsonPath} center={[22.3094, 72.1362]} />
          {geoJsonPath.length > 0 && (
            <Polyline positions={geoJsonPath} color={mode === 'plane' ? "#00ffcc" : "#10b981"} weight={6} opacity={0.9} />
          )}
        </MapContainer>
      </div>
      
    </div>
  );
}