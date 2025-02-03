<template lang="">
    <div style="width: 100%">
        <h2>{{ chart_data.getTitle() }}</h2>
        <canvas v-bind:ref="`${chart_data.getTitle()}-${index}`"></canvas>
    </div>
</template>
<script>
import { BarChartFactory } from '../../data_getter/bar_chart_handeler';
export default {
    name: 'BarChart',
    props: ['chart_data', 'index'],
    async mounted() {
        const ctx = this.$refs[`${this.chart_data.getTitle()}-${this.index}`];
        const barChart = new BarChartFactory().getInstance(this.chart_data, ctx);
        await barChart.renderChart();
    }
}
</script>
