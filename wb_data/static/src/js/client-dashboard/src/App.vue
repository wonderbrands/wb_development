<template>
  <Button @click="$store.commit('showDrawer')">
    <i class="pi pi-bars"></i>
  </Button>
  <AvailableDashboards />
  <DisplayedDashboard />
</template>

<script>
import AvailableDashboards from './components/AvailableDashboardsDrawer/AvailableDashboards.vue';
import DisplayedDashboard from './components/DisplayedDashboard/DisplayedDashboard.vue';
import Button from 'primevue/button';

export default {
  components: {
    AvailableDashboards,
    DisplayedDashboard,
    Button
  }
}
</script>

<style>

</style>
