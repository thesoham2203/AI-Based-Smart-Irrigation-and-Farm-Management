import React, { useEffect, useState } from 'react';
import { LatestReading } from './components/LatestReading';
import { ControlPanel } from './components/ControlPanel';

export default function App() {
  return (
    <div style={{ fontFamily: 'sans-serif', padding: 20 }}>
      <h2>Precision Irrigation Dashboard</h2>
      <LatestReading />
      <ControlPanel />
    </div>
  );
}
