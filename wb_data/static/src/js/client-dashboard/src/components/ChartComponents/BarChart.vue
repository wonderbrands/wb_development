<template lang="">
    <div style="width: 100%">
        <h2>{{ chart_data.getTitle() }}</h2>
        <canvas v-bind:ref="`${chart_data.getTitle()}-${index}`"></canvas>
    </div>
</template>
<script>
import Chart from 'chart.js/auto';
export default {
    name: 'BarChart',
    props: ['chart_data', 'index'],
    mounted() {
        const ctx = this.$refs[`${this.chart_data.getTitle()}-${this.index}`];

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['January', 'February', 'March', 'April', 'May', 'June'],
                datasets: [{
                    label: 'Sales 2024',
                    data: [65, 59, 80, 81, 56, 55],
                    backgroundColor: 'rgb(75, 192, 192)',
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 1
                }, {
                    label: 'Sales 2023',
                    data: [45, 49, 60, 71, 46, 45],
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Monthly Sales Comparison'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Sales ($K)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    }
                }
            }
        });

    }
}
</script>
