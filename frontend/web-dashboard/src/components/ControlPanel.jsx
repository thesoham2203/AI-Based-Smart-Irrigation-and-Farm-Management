import React, { useState } from 'react';

export function ControlPanel() {
  const [eventId, setEventId] = useState(null);
  const start = () => {
    fetch('http://localhost:8000/api/irrigation-events/start/', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({field_id: 'demo-field-1', reason: 'manual'})})
      .then(r => r.json()).then(d => setEventId(d.id));
  };
  const stop = () => {
    if(!eventId) return;
    fetch('http://localhost:8000/api/irrigation-events/stop/', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({event_id: eventId})})
      .then(r => r.json()).then(() => setEventId(null));
  };
  return (
    <div style={{marginTop: 20}}>
      <h4>Manual Control</h4>
      <button onClick={start} disabled={!!eventId}>Start Irrigation</button>
      <button onClick={stop} disabled={!eventId} style={{marginLeft: 10}}>Stop Irrigation</button>
    </div>
  );
}
