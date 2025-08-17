import React, { useEffect, useState } from 'react';
import { LatestReading } from './components/LatestReading';
import { ControlPanel } from './components/ControlPanel';
import { SensorChart } from './components/SensorChart';
import { SystemStatus } from './components/SystemStatus';
import './styles.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function App() {
  const [systemData, setSystemData] = useState({
    latest: null,
    chartData: [],
    activeEvents: [],
    loading: true,
    error: null
  });

  // Fetch all system data
  const fetchSystemData = async () => {
    try {
      const [latestRes, chartRes, eventsRes] = await Promise.all([
        fetch(`${API_BASE}/api/readings/latest/`),
        fetch(`${API_BASE}/api/readings/chart-data/`),
        fetch(`${API_BASE}/api/irrigation-events/active/`)
      ]);

      const latest = latestRes.ok ? await latestRes.json() : null;
      const chartData = chartRes.ok ? await chartRes.json() : [];
      const activeEvents = eventsRes.ok ? await eventsRes.json() : [];

      setSystemData({
        latest,
        chartData,
        activeEvents,
        loading: false,
        error: null
      });
    } catch (error) {
      console.error('Error fetching system data:', error);
      setSystemData(prev => ({
        ...prev,
        loading: false,
        error: 'Failed to connect to irrigation system'
      }));
    }
  };

  useEffect(() => {
    fetchSystemData();
    const interval = setInterval(fetchSystemData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  if (systemData.loading) {
    return (
      <div className="container">
        <div className="loading">Loading irrigation system data...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <header className="header">
        <h1>🌱 Precision Irrigation System</h1>
        <p>Real-time monitoring and automated irrigation control</p>
      </header>

      {systemData.error && (
        <div className="alert alert-warning">
          {systemData.error}
        </div>
      )}

      <div className="grid">
        <div className="card">
          <SystemStatus 
            latest={systemData.latest} 
            activeEvents={systemData.activeEvents}
          />
        </div>
        
        <div className="card">
          <ControlPanel 
            onUpdate={fetchSystemData}
            activeEvents={systemData.activeEvents}
          />
        </div>
      </div>

      <div className="card">
        <h3>📊 Sensor Data Trends</h3>
        <SensorChart data={systemData.chartData} />
      </div>

      <div className="card">
        <LatestReading data={systemData.latest} />
      </div>
    </div>
  );
}
