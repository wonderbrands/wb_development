<template>
    <div>
        <Drawer v-model:visible="$store.state.drawerDisplayed" header="Tableros disponibles">
            <Accordion>
                <AccordionPanel v-for="dashboard, index in $store.getters.getAvailableDashboards" :key="index" :value="index">
                    <AccordionHeader>{{ dashboard.getName() }}</AccordionHeader>
                    <AccordionContent>
                        <p class="m-0">{{ dashboard.getDescription() }}</p>
                        <Button severity="secondary" aria-label="Bookmark" @click="selectDashboard(dashboard)" >
                            <i class="pi pi-arrow-right"></i>
                        </Button>
                    </AccordionContent>
                </AccordionPanel>
            </Accordion>
        </Drawer>
    </div>
</template>
<script>
import Drawer from 'primevue/drawer';
import Button from 'primevue/button';
import Accordion from 'primevue/accordion';
import AccordionPanel from 'primevue/accordionpanel';
import AccordionHeader from 'primevue/accordionheader';
import AccordionContent from 'primevue/accordioncontent';

export default {
    name: 'AvailableDashboards',
    methods: {
        selectDashboard(dashboard) {
            this.$store.commit('selectDashboard', dashboard);
            this.$store.commit('setDisplayedDashboard', dashboard);
            this.$store.commit('hideDrawer');
        }
    },
    components: {
        Drawer,
        Accordion,
        AccordionPanel,
        AccordionHeader,
        AccordionContent,
        Button
    }
}
</script>
<style lang="scss">
    
</style>