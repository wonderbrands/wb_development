<template>
  <div v-if="$store.getters.getDisplayedDashboard">
    <h1>{{ $store.getters.getDisplayedDashboard.getName() }}</h1>
    <div class="charts">
      <div
        :style="chart.getStyling()"
        v-for="(
          chart, index
        ) in $store.getters.getDisplayedDashboard.getComponents()"
        :key="index"
      >
        <component
          :is="chart.getChartType()"
          :chart_data="chart"
          :index="index"
        />
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from "../ChartComponents/LineChart.vue";
import BarChart from "../ChartComponents/BarChart.vue";
import TableData from "../ChartComponents/TableData.vue";
import BubbleChart from "../ChartComponents/BubbleChart.vue";
import PieChart from "../ChartComponents/PieChart.vue";
import LoaderComponent from "../LoaderComponent.vue";
export default {
  name: "DisplayedDashboard",
  components: {
    LineChart,
    BarChart,
    TableData,
    BubbleChart,
    PieChart,
    LoaderComponent,
  },
};
</script>
