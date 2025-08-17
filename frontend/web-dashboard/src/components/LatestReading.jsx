import React from 'react';

export function LatestReading({ data }) {
  if (!data) {
    return (
      <div className="latest-reading">
        <h3>📊 Latest Sensor Reading</h3>
        <div className="no-data">
          No sensor data available yet. The system may be starting up or there could be a connection issue.
        </div>
      </div>
    );
  }

  const getTimeAgo = (timestamp) => {
    const now = new Date();
    const reading = new Date(timestamp);
    const diffMs = now - reading;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    
    return reading.toLocaleDateString();
  };

  const getSoilMoistureStatus = (moisture) => {
    if (moisture < 20) return { status: 'critical', text: 'Very Dry', color: '#dc2626' };
    if (moisture < 30) return { status: 'low', text: 'Dry', color: '#ea580c' };
    if (moisture < 60) return { status: 'good', text: 'Optimal', color: '#16a34a' };
    if (moisture < 80) return { status: 'high', text: 'Moist', color: '#2563eb' };
    return { status: 'saturated', text: 'Very Moist', color: '#7c3aed' };
  };

  const getTemperatureStatus = (temp) => {
    if (temp < 10) return { status: 'cold', text: 'Cold', color: '#2563eb' };
    if (temp < 25) return { status: 'cool', text: 'Cool', color: '#16a34a' };
    if (temp < 30) return { status: 'warm', text: 'Warm', color: '#ea580c' };
    return { status: 'hot', text: 'Hot', color: '#dc2626' };
  };

  // Handle different field names from backend
  const soilMoisture = data.soil_moisture || data.moisture || 0;
  const temperature = data.temperature || data.temperature_c || 0;
  const humidity = data.humidity || 0;

  const moistureStatus = getSoilMoistureStatus(soilMoisture);
  const tempStatus = getTemperatureStatus(temperature);

  return (
    <div className="latest-reading">
      <h3>📊 Latest Sensor Reading</h3>
      
      <div className="reading-header">
        <span className="timestamp">
          🕒 {getTimeAgo(data.timestamp)}
        </span>
        <span className="full-time">
          {new Date(data.timestamp).toLocaleString()}
        </span>
      </div>

      <div className="reading-grid">
        <div className="metric-card">
          <div className="metric-icon">💧</div>
          <div className="metric-content">
            <div className="metric-label">Soil Moisture</div>
            <div className="metric-value" style={{ color: moistureStatus.color }}>
              {soilMoisture?.toFixed(1)}%
            </div>
            <div className="metric-status" style={{ color: moistureStatus.color }}>
              {moistureStatus.text}
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">🌡️</div>
          <div className="metric-content">
            <div className="metric-label">Temperature</div>
            <div className="metric-value" style={{ color: tempStatus.color }}>
              {temperature?.toFixed(1)}°C
            </div>
            <div className="metric-status" style={{ color: tempStatus.color }}>
              {tempStatus.text}
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">🌫️</div>
          <div className="metric-content">
            <div className="metric-label">Air Humidity</div>
            <div className="metric-value">
              {humidity?.toFixed(1)}%
            </div>
            <div className="metric-status">
              {humidity > 60 ? 'Humid' : humidity > 40 ? 'Normal' : 'Dry'}
            </div>
          </div>
        </div>

        {data.action && (
          <div className="metric-card">
            <div className="metric-icon">⚙️</div>
            <div className="metric-content">
              <div className="metric-label">Last Action</div>
              <div className="metric-value">
                {data.action}
              </div>
              <div className="metric-status">
                Automated Decision
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="reading-summary">
        {moistureStatus.status === 'critical' && (
          <div className="alert alert-danger">
            ⚠️ Soil moisture is critically low! Immediate irrigation recommended.
          </div>
        )}
        {moistureStatus.status === 'low' && (
          <div className="alert alert-warning">
            🟡 Soil moisture is low. Consider irrigation soon.
          </div>
        )}
        {moistureStatus.status === 'good' && (
          <div className="alert alert-success">
            ✅ Soil moisture levels are optimal.
          </div>
        )}
      </div>
    </div>
  );
}
