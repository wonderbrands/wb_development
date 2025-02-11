<template>
  <div style="width: 100%">
    <h2>{{ chart_data.getTitle() }}</h2>
    <canvas v-bind:ref="`${chart_data.getTitle()}-${index}`"></canvas>
  </div>
</template>
<script>
import Chart from "chart.js/auto";
export default {
  name: "PieChart",
  props: ["chart_data", "index"],
  mounted() {
    const ctx = this.$refs[`${this.chart_data.getTitle()}-${this.index}`];
    const data = {
      labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datasets: [
        {
          label: "My First Dataset",
          data: [12, 19, 3, 5, 2, 3],
          backgroundColor: [
            "rgba(255, 99, 132, 0.6)",
            "rgba(54, 162, 235, 0.6)",
            "rgba(255, 206, 86, 0.6)",
            "rgba(75, 192, 192, 0.6)",
            "rgba(153, 102, 255, 0.6)",
            "rgba(255, 159, 64, 0.6)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    };

    // Configuration options
    const options = {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Pie Chart Example",
        },
      },
    };

    // Create the pie chart
    const myPieChart = new Chart(ctx, {
      type: "pie",
      data: data,
      options: options,
    });
  },
};
</script>
