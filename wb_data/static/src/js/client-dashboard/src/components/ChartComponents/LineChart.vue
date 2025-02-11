<template>
  <div style="width: 100%">
    <h2>{{ chart_data.getTitle() }}</h2>
    <canvas v-bind:ref="`${chart_data.getTitle()}-${index}`"></canvas>
  </div>
</template>
<script>
import Chart from "chart.js/auto";
export default {
  name: "LineChart",
  props: ["chart_data", "index"],
  mounted() {
    const ctx = this.$refs[`${this.chart_data.getTitle()}-${this.index}`];
    new Chart(ctx, {
      type: "line",
      data: {
        labels: ["January", "February", "March", "April", "May", "June"],
        datasets: [
          {
            label: "Website Traffic 2024",
            data: [3000, 3500, 4200, 4800, 5300, 6000],
            borderColor: "rgb(75, 192, 192)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            tension: 0.3,
            fill: true,
          },
          {
            label: "Website Traffic 2023",
            data: [2800, 3200, 3800, 4100, 4600, 5200],
            borderColor: "rgb(255, 99, 132)",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            tension: 0.3,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Monthly Website Traffic",
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Visitors",
            },
          },
          x: {
            title: {
              display: true,
              text: "Month",
            },
          },
        },
      },
    });
  },
};
</script>
