import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

export function SensorChart({ data = [] }) {
  const chartData = {
    datasets: [
      {
        label: 'Soil Moisture (%)',
        data: data.map(point => ({
          x: new Date(point.timestamp),
          y: point.soil_moisture
        })),
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        yAxisID: 'y',
        tension: 0.1
      },
      {
        label: 'Temperature (°C)',
        data: data.map(point => ({
          x: new Date(point.timestamp),
          y: point.temperature
        })),
        borderColor: '#dc2626',
        backgroundColor: 'rgba(220, 38, 38, 0.1)',
        yAxisID: 'y1',
        tension: 0.1
      },
      {
        label: 'Humidity (%)',
        data: data.map(point => ({
          x: new Date(point.timestamp),
          y: point.humidity
        })),
        borderColor: '#16a34a',
        backgroundColor: 'rgba(22, 163, 74, 0.1)',
        yAxisID: 'y',
        tension: 0.1
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      title: {
        display: true,
        text: 'Sensor Readings - Last 24 Hours'
      },
      legend: {
        position: 'top',
      },
      tooltip: {
        callbacks: {
          title: function(context) {
            return new Date(context[0].parsed.x).toLocaleString();
          }
        }
      }
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'hour',
          displayFormats: {
            hour: 'HH:mm'
          }
        },
        title: {
          display: true,
          text: 'Time'
        }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Moisture & Humidity (%)'
        },
        min: 0,
        max: 100
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: {
          display: true,
          text: 'Temperature (°C)'
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };

  if (!data || data.length === 0) {
    return (
      <div className="chart-container">
        <div className="no-data">
          📈 No sensor data available yet
        </div>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <Line data={chartData} options={options} />
    </div>
  );
}
