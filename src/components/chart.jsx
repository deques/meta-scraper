import React from "react";
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

const BarChart = ({ data }) => {
    const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Bar Chart',
      },
    }
  };
  return (
    <>
      <h1>Chart</h1>
      <div className="chart-container">
        <h2 style={{textAlign: "center" }}>Bar chart</h2>
        <Bar data={data} options={options} />
      </div>
    
    </>
  )
}

export default BarChart;