import React from 'react';

export function SystemStatus({ latest, activeEvents }) {
  const getSystemStatus = () => {
    if (!latest) return { status: 'offline', message: 'System Offline' };
    
    const lastReading = new Date(latest.timestamp);
    const now = new Date();
    const timeDiff = (now - lastReading) / 1000 / 60; // minutes
    
    if (timeDiff > 10) {
      return { status: 'warning', message: 'Connection Issues' };
    }
    
    const hasActiveIrrigation = activeEvents?.some(event => 
      event.event_type === 'irrigation_start' && !event.ended_at
    );
    
    if (hasActiveIrrigation) {
      return { status: 'irrigating', message: 'Irrigation Active' };
    }
    
    if (latest.soil_moisture < 30) {
      return { status: 'dry', message: 'Soil Dry - Monitoring' };
    }
    
    return { status: 'good', message: 'System Normal' };
  };

  const { status, message } = getSystemStatus();

  const getStatusIcon = () => {
    switch (status) {
      case 'offline': return '🔴';
      case 'warning': return '🟡';
      case 'irrigating': return '💧';
      case 'dry': return '🟠';
      case 'good': return '🟢';
      default: return '❓';
    }
  };

  const getLastUpdate = () => {
    if (!latest) return 'Never';
    return new Date(latest.timestamp).toLocaleString();
  };

  return (
    <div className="system-status">
      <h3>🌡️ System Status</h3>
      
      <div className={`status-indicator status-${status}`}>
        <span className="status-icon">{getStatusIcon()}</span>
        <span className="status-text">{message}</span>
      </div>

      <div className="status-details">
        <div className="status-item">
          <span className="label">Last Update:</span>
          <span className="value">{getLastUpdate()}</span>
        </div>
        
        {latest && (
          <>
            <div className="status-item">
              <span className="label">Soil Moisture:</span>
              <span className={`value ${latest.soil_moisture < 30 ? 'warning' : ''}`}>
                {latest.soil_moisture?.toFixed(1)}%
              </span>
            </div>
            
            <div className="status-item">
              <span className="label">Temperature:</span>
              <span className="value">{latest.temperature?.toFixed(1)}°C</span>
            </div>
            
            <div className="status-item">
              <span className="label">Humidity:</span>
              <span className="value">{latest.humidity?.toFixed(1)}%</span>
            </div>
          </>
        )}

        {activeEvents && activeEvents.length > 0 && (
          <div className="status-item">
            <span className="label">Active Events:</span>
            <span className="value">{activeEvents.length}</span>
          </div>
        )}
      </div>
    </div>
  );
}
