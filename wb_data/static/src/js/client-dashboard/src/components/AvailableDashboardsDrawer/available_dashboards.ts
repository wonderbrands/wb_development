export class Dashboard {
    name: string;
    selected: boolean = false;
    description: string = "lorem ipsum dolor sit amet";

    constructor(name: string, description: string = "lorem ipsum dolor sit amet") {
        this.description = description;
        this.name = name;
    }

    getName(): string {
        return this.name;
    }

    setName(name: string): void {
        this.name = name;
    }

    isSelected(): boolean {
        return this.selected;
    }

    setSelected(selected: boolean): void {
        this.selected = selected;
    }

    getDescription(): string {
        return this.description;
    }

    setDescription(description: string): void {
        this.description = description;
    }
}

class AvailableDashboards {
    availableDashboards: Dashboard[] = [];

    getAvailableDashboards(): Dashboard[] {
        return this.availableDashboards;
    }

    resetAvailableDashboards(): void {
        this.availableDashboards = [];
    }

    selectDashboard(dashboard: Dashboard): void {
        this.getAvailableDashboards().forEach(d => {
            if (d.name === dashboard.name) {
                d.selected = true;
            } else {
                d.selected = false;
            }
        })
    }
}

class AvailableDashboardsFrontend extends AvailableDashboards{
    constructor() {
        super();
        this.availableDashboards = [
            new Dashboard("Dashboard 1"),
            new Dashboard("Dashboard 2"),
            new Dashboard("Dashboard 3"),
        ];
    }
}

class AvailableDashboardsFactory {
    getInstance(): AvailableDashboards | void {
        if (import.meta.env.VITE_AVAILABLE_DASHBOARD_ENGINE === 'frontend') {
            return new AvailableDashboardsFrontend();
        }
    }
}
    
export let availableDashboardsState = {
    availableDashboards: new AvailableDashboardsFactory().getInstance()
}

export let availableDashboardsGetters = {
    getAvailableDashboards(state) {
        return state.availableDashboards.getAvailableDashboards();
    },
    getSelectedDashboard(state) {
        return state.availableDashboards.getAvailableDashboards().find(d => d.selected);
    }
}

export let availableDashboardsMutations = {
    resetAvailableDashboards(state) {
        state.availableDashboards.resetAvailableDashboards();
    },
    selectDashboard(state, dashboard: Dashboard) {
        state.availableDashboards.selectDashboard(dashboard);
    }
}
