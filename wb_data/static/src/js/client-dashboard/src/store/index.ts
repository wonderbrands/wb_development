import { createStore } from "vuex";
import { availableDashboardsState, availableDashboardsGetters, availableDashboardsMutations } from "../components/AvailableDashboardsDrawer/available_dashboards";
import { frontendControllersState, frontendControllersGetters, frontendControllersMutations } from "./frontend_controllers";
import { displayedDashboardState, displayedDashboardGetters, displayedDashboardMutations } from "../components/DisplayedDashboard/displayed-dashboard";

const store = createStore({
    state: {
        ...availableDashboardsState,
        ...frontendControllersState,
        ...displayedDashboardState
    },
    mutations: {
        ...availableDashboardsMutations,
        ...frontendControllersMutations,
        ...displayedDashboardMutations
    },
    actions: {},
    getters: {
        ...availableDashboardsGetters,
        ...frontendControllersGetters,
        ...displayedDashboardGetters
    }
})

export default store;