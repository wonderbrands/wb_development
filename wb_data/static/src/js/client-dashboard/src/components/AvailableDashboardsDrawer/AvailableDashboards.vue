<template>
  <div>
    <Drawer
      v-model:visible="$store.state.drawerDisplayed"
      header="Tableros disponibles"
    >
      <LoaderComponent v-if="avDashboards.length == 0" />
      <Accordion v-else>
        <AccordionPanel
          v-for="(dashboard, index) in avDashboards"
          :key="index"
          :value="index"
        >
          <AccordionHeader>{{ dashboard.getName() }}</AccordionHeader>
          <AccordionContent>
            <p class="m-0">{{ dashboard.getDescription() }}</p>
            <Button
              severity="secondary"
              aria-label="Bookmark"
              @click="selectDashboard(dashboard)"
            >
              <i class="pi pi-arrow-right"></i>
            </Button>
          </AccordionContent>
        </AccordionPanel>
      </Accordion>
    </Drawer>
  </div>
</template>
<script>
import Drawer from "primevue/drawer";
import Button from "primevue/button";
import Accordion from "primevue/accordion";
import AccordionPanel from "primevue/accordionpanel";
import AccordionHeader from "primevue/accordionheader";
import AccordionContent from "primevue/accordioncontent";
import LoaderComponent from "../LoaderComponent.vue";

export default {
  name: "AvailableDashboards",
  data() {
    return {
      avDashboards: [],
    };
  },
  methods: {
    async selectDashboard(dashboard) {
      this.$store.commit("selectDashboard", dashboard);
      console.log(this.$store.state.userInfo)
      await this.$store.commit("setDisplayedDashboard", {
        dashboard: dashboard, 
        userInfo: this.$store.state.userInfo
      });
      this.$store.commit("hideDrawer");
    },
  }, 
  async beforeMount() {
    this.avDashboards = await this.$store.getters.getAvailableDashboards;
  },
  components: {
    Drawer,
    Accordion,
    AccordionPanel,
    AccordionHeader,
    AccordionContent,
    Button,
    LoaderComponent,
  },
};
</script>
<style lang="scss"></style>
