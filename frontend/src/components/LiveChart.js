import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale);

function LiveChart({ results }) {
  const data = {
    labels: Object.keys(results),
    datasets: [
      {
        label: "Votes",
        data: Object.values(results)
      }
    ]
  };

  return <Bar data={data} />;
}

export default LiveChart;