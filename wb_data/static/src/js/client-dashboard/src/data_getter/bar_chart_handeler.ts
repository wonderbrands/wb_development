import { ChartComponent } from "../components/DisplayedDashboard/displayed-dashboard";
import { DataHandler } from "./data_handlers";
import { ExternalLibrary } from "./external_library_enum";


type BarChartDataset = {
    label: string,
    data: number[],
    backgroundColor: string,
    borderColor: string,
    borderWidth: number
}

type AxisTitle = {
    axis: string,
    title: string
}

type ExpectedBarChartPayload = {
    datasets: BarChartDataset[],
    labels: string[],
    xAxisTitle: AxisTitle,
    yAxisTitle: AxisTitle
}


class BarChartHandler extends DataHandler {
    renderer : ExternalLibrary
    type: string = "bar"
    ctx: any

    constructor(component: ChartComponent, renderer: ExternalLibrary, ctx: any) {
        super(component);
        this.renderer = renderer;
        this.ctx = ctx
    }
}


class BarChartHandlerFrontend extends BarChartHandler {
    constructor(component: ChartComponent, renderer: ExternalLibrary, ctx: any) { 
        super(component, renderer, ctx);
    }

    getData(): ExpectedBarChartPayload {
        return {
            datasets: [
                {
                    label: 'Sales 2024',
                    data: [65, 59, 80, 81, 56, 55],
                    backgroundColor: `#${Math.floor(Math.random()*16777215).toString(16)}`,
                    borderColor: `#${Math.floor(Math.random()*16777215).toString(16)}`,
                    borderWidth: 1
                },
                {
                    label: 'Sales 2023',
                    data: [45, 49, 60, 71, 46, 45],
                    backgroundColor: `#${Math.floor(Math.random()*16777215).toString(16)}`,
                    borderColor: `#${Math.floor(Math.random()*16777215).toString(16)}`,
                    borderWidth: 1
                },
                {
                    label: 'Sales 2022',
                    data: [25, 29, 40, 51, 26, 25],
                    backgroundColor: `#${Math.floor(Math.random()*16777215).toString(16)}`,
                    borderColor: `#${Math.floor(Math.random()*16777215).toString(16)}`,
                    borderWidth: 1
                }
            ],
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            xAxisTitle: {
                axis: 'x',
                title: 'Months'
            },
            yAxisTitle: {
                axis: 'y',
                title: 'Sales'
            }
        }
    }
    
    async renderChart(): Promise<void> {
        const chart_data = this.getData();
        if (this.renderer === ExternalLibrary.ChartJs) {
            const { default: Chart } = await import('chart.js/auto');
            new Chart(this.ctx, {
                type: this.type,
                data: {
                    labels: chart_data.labels,
                    datasets: chart_data.datasets
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: chart_data.yAxisTitle.title
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: chart_data.xAxisTitle.title
                            }
                        }
                    }
                }
            });
        }
    }
}

export class BarChartFactory {
    getInstance(component: ChartComponent, context: any): DataHandler | void {
        if (import.meta.env.VITE_DASHBOARD_DATA_ENGINE === 'frontend') {
            return new BarChartHandlerFrontend(component, ExternalLibrary.ChartJs, context )
            
        }
    }
}