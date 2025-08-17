import React, { useState } from 'react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export function ControlPanel({ onUpdate, activeEvents }) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const showMessage = (text, type = 'info') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(''), 3000);
  };

  const sendCommand = async (command, duration = null) => {
    setLoading(true);
    try {
      const payload = { command };
      if (duration) payload.duration = duration;

      const response = await fetch(`${API_BASE}/api/control/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      
      if (response.ok) {
        showMessage(result.message || 'Command sent successfully', 'success');
        if (onUpdate) onUpdate();
      } else {
        showMessage(result.error || 'Command failed', 'error');
      }
    } catch (error) {
      console.error('Control error:', error);
      showMessage('Failed to send command', 'error');
    } finally {
      setLoading(false);
    }
  };

  const hasActiveIrrigation = activeEvents?.some(event => 
    event.event_type === 'irrigation_start' && !event.ended_at
  );

  return (
    <div className="control-panel">
      <h3>🎛️ Manual Controls</h3>
      
      {message && (
        <div className={`alert alert-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="control-buttons">
        <button
          onClick={() => sendCommand('start_irrigation', 300)}
          disabled={loading || hasActiveIrrigation}
          className="btn btn-primary"
          title="Start 5-minute irrigation cycle"
        >
          {loading ? '⏳' : '💧'} Start Irrigation (5min)
        </button>

        <button
          onClick={() => sendCommand('start_irrigation', 600)}
          disabled={loading || hasActiveIrrigation}
          className="btn btn-primary"
          title="Start 10-minute irrigation cycle"
        >
          {loading ? '⏳' : '💧'} Start Irrigation (10min)
        </button>

        {hasActiveIrrigation && (
          <button
            onClick={() => sendCommand('stop_irrigation')}
            disabled={loading}
            className="btn btn-danger"
            title="Stop current irrigation"
          >
            {loading ? '⏳' : '🛑'} Stop Irrigation
          </button>
        )}

        <button
          onClick={() => sendCommand('force_reading')}
          disabled={loading}
          className="btn btn-secondary"
          title="Force sensor reading"
        >
          {loading ? '⏳' : '📊'} Force Reading
        </button>

        <button
          onClick={() => sendCommand('system_status')}
          disabled={loading}
          className="btn btn-secondary"
          title="Check system status"
        >
          {loading ? '⏳' : '🔍'} System Check
        </button>
      </div>

      <div className="irrigation-status">
        {hasActiveIrrigation ? (
          <div className="status-active">
            🟢 Irrigation is currently active
          </div>
        ) : (
          <div className="status-idle">
            ⭕ System ready for irrigation
          </div>
        )}
      </div>

      <div className="control-info">
        <h4>Control Information</h4>
        <ul>
          <li>Manual irrigation overrides automatic decisions</li>
          <li>5-10 minute cycles are recommended for testing</li>
          <li>System will auto-stop after maximum duration</li>
          <li>Force reading updates sensor data immediately</li>
        </ul>
      </div>
    </div>
  );
}
