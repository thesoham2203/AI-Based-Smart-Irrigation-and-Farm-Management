import React, { useEffect, useState } from 'react';

export function LatestReading() {
  const [data, setData] = useState(null);
  useEffect(() => {
    const fetchData = () => {
      fetch('http://localhost:8000/api/readings/latest/')
        .then(r => r.json())
        .then(setData)
        .catch(() => {});
    };
    fetchData();
    const id = setInterval(fetchData, 5000);
    return () => clearInterval(id);
  }, []);
  if (!data || !data.id) return <div>No data yet.</div>;
  return (
    <div style={{marginTop: 10}}>
      <strong>Latest Reading:</strong> Moisture {data.moisture?.toFixed(2)} %, Temp {data.temperature_c?.toFixed?.(1)} °C, Humidity {data.humidity?.toFixed?.(1)} %, Action {data.action}
    </div>
  );
}
