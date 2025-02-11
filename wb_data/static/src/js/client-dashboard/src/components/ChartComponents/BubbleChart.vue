<template>
  <div style="width: 100%">
    <h2>{{ chart_data.getTitle() }}</h2>
    <canvas v-bind:ref="`${chart_data.getTitle()}-${index}`"></canvas>
  </div>
</template>
<script>
import Chart from "chart.js/auto";
export default {
  name: "BubbleChart",
  props: ["chart_data", "index"],
  mounted() {
    const ctx = this.$refs[`${this.chart_data.getTitle()}-${this.index}`];
    new Chart(ctx, {
      type: "bubble",
      data: {
        datasets: [
          {
            label: "Product A",
            data: [
              { x: 20, y: 30, r: 15 }, // x: price, y: sales, r: market share
              { x: 40, y: 10, r: 10 },
              { x: 30, y: 25, r: 8 },
            ],
            backgroundColor: "rgba(75, 192, 192, 0.6)",
          },
          {
            label: "Product B",
            data: [
              { x: 25, y: 35, r: 12 },
              { x: 35, y: 15, r: 14 },
              { x: 45, y: 20, r: 6 },
            ],
            backgroundColor: "rgba(255, 99, 132, 0.6)",
          },
          {
            label: "Product C",
            data: [
              { x: 15, y: 40, r: 10 },
              { x: 30, y: 30, r: 8 },
              { x: 50, y: 25, r: 15 },
            ],
            backgroundColor: "rgba(54, 162, 235, 0.6)",
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
            text: "Product Performance Analysis",
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return `${context.raw.x}$ - Sales: ${context.raw.y}K - Market Share: ${context.raw.r}%`;
              },
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Price ($)",
            },
          },
          y: {
            title: {
              display: true,
              text: "Sales (K)",
            },
          },
        },
      },
    });
  },
};
</script>
