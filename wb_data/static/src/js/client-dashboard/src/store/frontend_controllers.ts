export let frontendControllersState = {
  drawerDisplayed: true,
};

export let frontendControllersGetters = {
  isDrawerShown: (state) => {
    return state.drawerDisplayed;
  },
};

export let frontendControllersMutations = {
  hideDrawer(state) {
    state.drawerDisplayed = false;
  },
  showDrawer(state) {
    state.drawerDisplayed = true;
  },
};
