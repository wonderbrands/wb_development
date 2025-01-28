import { Dashboard } from "../AvailableDashboardsDrawer/available_dashboards";
class DashboardData extends Dashboard {
    components: ChartComponent[]

    constructor(inherited_dashboard: Dashboard, components: ChartComponent[]){
        super(inherited_dashboard.getName(), inherited_dashboard.getDescription());
        this.components = components
    }

    getComponents(): ChartComponent[]{
        return this.components
    }

    setComponents(components: ChartComponent[]){
        this.components = components
    }

    existComponentByTitle(title: string): boolean{
        const exists = this.getComponents().filter(
            x => x.getTitle() === title
        )
        return exists.length > 0
    }

    getComponentByTitle(title: string): ChartComponent | null{
        if (this.existComponentByTitle(title)){
            const result = this.getComponents().filter(
                x => x.getTitle() === title
            )
            return result[0]
        }
        return null
    }
}

class ChartComponent {
    dashboard: Dashboard
    title: string
    data_source_type: string
    data_source_path: string
    is_realtime: boolean
    chart_type: string

    constructor(dashboard: Dashboard, title: string, data_source_type: string, data_source_path: string, is_realtime: boolean, chart_type: string) {
        this.dashboard = dashboard;
        this.title = title;
        this.data_source_type = data_source_type;
        this.data_source_path = data_source_path;
        this.is_realtime = is_realtime;
        this.chart_type = chart_type
    }

    getDashboard(): Dashboard {
        return this.dashboard;
    }

    setDashboard(dashboard: Dashboard): void {
        this.dashboard = dashboard;
    }

    getTitle(): string {
        return this.title;
    }

    setTitle(title: string): void {
        this.title = title;
    }

    getDataSourceType(): string {
        return this.data_source_type;
    }

    setDataSourceType(data_source_type: string): void {
        this.data_source_type = data_source_type;
    }

    getDataSourcePath(): string {
        return this.data_source_path;
    }

    setDataSourcePath(data_source_path: string): void {
        this.data_source_path = data_source_path;
    }

    getIsRealtime(): boolean {
        return this.is_realtime;
    }

    setIsRealtime(is_realtime: boolean): void {
        this.is_realtime = is_realtime;
    }

    getChartType(): string {
        return this.chart_type;
    }

    setChartType(chart_type: string): void {
        this.chart_type = chart_type;
    }

}

const test_dashboard_data: DashboardData[] = [
    new DashboardData(
        new Dashboard("Dashboard 1"),
        [new ChartComponent(
            new Dashboard("Dashboard 1"), 
            "Line Chart Random Example", 
            "api", 
            "/api/line-chart", 
            false, 
            "LineChart"), 
        new ChartComponent(
            new Dashboard("Dashboard 1"), 
            "Bar Chart Random Example", 
            "api", 
            "/api/bar-chart", 
            false, 
            "BarChart")]
    ),
    new DashboardData(
        new Dashboard("Dashboard 2"),
        [new ChartComponent(
            new Dashboard("Dashboard 2"), 
            "Table Random Example", 
            "api",
            "/api/data-table", 
            false, 
            "TableData"),
        new ChartComponent(
            new Dashboard("Dashboard 2"), 
            "Bubble chart Random Example", 
            "api",
            "/api/bubble-chart", 
            false, 
            "BubbleChart"),
        new ChartComponent(
            new Dashboard("Dashboard 2"), 
            "Pie chart Random Example", 
            "api",
            "/api/pie-chart", 
            false, 
            "PieChart")
        ]
    ),
    new DashboardData(
        new Dashboard("Dashboard 3"),
        []
    )
]

class DashboardDataFactory{
    getInstance(name: string): DashboardData | void {
        if (import.meta.env.VITE_DASHBOARD_DATA_ENGINE === 'frontend') {
            const result = test_dashboard_data.filter(
                x => x.getName() === name
            );
            if (result.length>0){
                return result[0];
            }
        }
    }
}

export let displayedDashboardState = {
    displayedDashboard: null
}

export let displayedDashboardGetters = {
    getDisplayedDashboard: (state) => {
        return state.displayedDashboard;
    }
}

export let displayedDashboardMutations = {
    setDisplayedDashboard: (state, dashboard) => {
        state.displayedDashboard = new DashboardDataFactory().getInstance(dashboard.getName());
    }
}