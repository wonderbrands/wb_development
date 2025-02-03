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

export enum parameterType{
    string = 0,
    number = 1,
    date = 2,
    datetime = 3,
    boolean = 4,
    selection = 5
}

class ServerParameters{
    name: string
    value: string
    type: parameterType
    available_values: string[]
    default_value: string

    constructor(name: string, 
                value: string, 
                type: parameterType,
                default_value: string = "", 
                available_values: string[] = []){
        this.name = name
        this.value = value
        this.type = type
        this.default_value = default_value
        this.available_values = available_values
    }

    getName(): string{
        return this.name
    }

    setName(name: string){
        this.name = name
    }

    setValue(value: string){
        this.value = value
    }

    getValue(): string{
        return this.value
    }

    setValueType(type: parameterType){
        this.type = type
    }

    getType(): parameterType{
        return this.type
    }

    setAvailableValues(available_values: string[]){
        this.available_values = available_values
    }

    getAvailableValues(): string[]{
        return this.available_values
    }

    setDefaultValue(default_value: string){
        this.default_value = default_value
    }

    getDefaultValue(): string{
        return this.default_value
    }
}

export class ChartComponent {
    dashboard: Dashboard
    title: string
    data_source_type: string
    data_source_path: string
    is_realtime: boolean
    chart_type: string
    search_parameters: ServerParameters[]
    styling: string

    constructor(dashboard: Dashboard, 
                title: string, 
                data_source_type: string, 
                data_source_path: string, 
                is_realtime: boolean, 
                chart_type: string,
                search_parameters: ServerParameters[],
                styling: string){
        this.dashboard = dashboard;
        this.title = title;
        this.data_source_type = data_source_type;
        this.data_source_path = data_source_path;
        this.is_realtime = is_realtime;
        this.chart_type = chart_type
        this.search_parameters = search_parameters
        this.styling = styling
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

    getSearchParameters(): ServerParameters[] {
        return this.search_parameters;
    }

    setSearchParameters(search_parameters: ServerParameters[]): void {
        this.search_parameters = search_parameters;
    }

    getSearchParameterByName(name: string): ServerParameters | void {
        const result = this.getSearchParameters().filter(
            x => x.getName() === name
        );
        if (result.length>0){
            return result[0];
        }
    }

    getStyling(): string {
        return this.styling;
    }

    setStyling(styling: string): void {
        this.styling = styling;
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
            "LineChart",
            [],
            "width: 50%; height: 50%;"
        ), 
        new ChartComponent(
            new Dashboard("Dashboard 1"), 
            "Bar Chart Random Example", 
            "api", 
            "/api/bar-chart", 
            false, 
            "BarChart",
            [],
            "width: 50%; height: 50%;"
        )]
    ),
    new DashboardData(
        new Dashboard("Dashboard 2"),
        [new ChartComponent(
            new Dashboard("Dashboard 2"), 
            "Table Random Example", 
            "api",
            "/api/data-table", 
            false, 
            "TableData",
            [
                new ServerParameters("parameter1", "abcdefg", parameterType.string, "abcdefg"),
                new ServerParameters("parameter2", "123456", parameterType.number, "123456"),
                new ServerParameters("parameter3", "2023-01-01", parameterType.date, "2023-01-01"),
                new ServerParameters("parameter4", "2023-01-01 00:00:00", parameterType.datetime, "2023-01-01 00:00:00"),
                new ServerParameters("parameter5", "true", parameterType.boolean, "true"),
                new ServerParameters("parameter6", "value1", parameterType.selection, "value1",["value1", "value2", "value3"])
            ],
            "width: 50%; height: 50%;"
        ),
        new ChartComponent(
            new Dashboard("Dashboard 2"), 
            "Bubble chart Random Example", 
            "api",
            "/api/bubble-chart", 
            false, 
            "BubbleChart",
            [],
            "width: 50%; height: 50%;"
        ),
        new ChartComponent(
            new Dashboard("Dashboard 2"), 
            "Pie chart Random Example", 
            "api",
            "/api/pie-chart", 
            false, 
            "PieChart",
            [],
            "width: 50%; height: 50%;"
            )
        ]
    ),
    new DashboardData(
        new Dashboard("Dashboard 3"),
        []
    )
]

class DashboardDataFactory{
    async getInstance(name: string): DashboardData | void {
        switch (import.meta.env.VITE_DASHBOARD_DATA_ENGINE){
            case 'frontend':
                await setTimeout(() => {
                    console.log("Emulating server responce time latency")
                }, 2000);
                const result = await test_dashboard_data.filter(
                    x => x.getName() === name
                );
                if (result.length>0){
                    return result[0];
                }
                break
            case 'backend_odoo':
                try {
                    const response = await fetch(`/wb_data/get_dashboard?name=${name}`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-Requested-With": "XMLHttpRequest",
                        },
                        body: JSON.stringify({}),
                    });
                    const data = await response.json();
                    console.log(data.result)
                } catch (error) {
                    console.error('Error fetching dashboard data:', error);
                }
                break
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