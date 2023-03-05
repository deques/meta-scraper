import React from "react";
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

const Givers = ({ data }) => {
    const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Meta-Giveaway',
      },
    }
  };
  return (
    <>
      <h1>Chart</h1>
      <div className="chart-container">
        <Bar data={data} options={options} />
      </div>
    
    </>
  )
}

export default Givers;