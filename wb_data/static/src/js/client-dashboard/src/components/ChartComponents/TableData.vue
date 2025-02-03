<template>
    <div style="width: 100%;">
        <h2>{{ chart_data.getTitle() }}</h2>
        <div class="server_parameters_inputs">
            <ServerParameters :server_parameters="chart_data.getSearchParameters()" @update:server_parameters="updateServerParameters($event)" />
        </div>
        <div class="general_search_bar">
            <span class="p-input-icon-left outline">
                <i class="pi pi-search padding_for_icon" />
                <InputText v-model="filters.global.value" placeholder="Search..." />
            </span>
        </div>
        <DataTable :value="rows" tableStyle="min-width: 50rem" paginator :rows="5" :globalFilterFields="table.fields" :filters="filters">
            <Column v-for="col,index in table.fields" :key="index" :field="table.fields[index]" :header="table.columnNames[index]" sortable></Column>
        </DataTable>
    </div>
</template>
<script>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import ServerParameters from '../ServerParameters/ServerParameters.vue';
import { FilterMatchMode } from '@primevue/core/api';
import { TableDataFactory } from '../../data_getter/table_data_handeler';

export default {
    name: 'TableData',
    props: ['chart_data', 'index'],
    data() {
        return {
            filters: {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            },
            table: null,
            rows: []
        }
    },
    methods: {
        updateServerParameters(updatedValues) {
            const data = new TableDataFactory().getInstance(this.chart_data, null, updatedValues);
            this.table = data.processIntoTable()
            this.rows = this.table.rows
        }
    },
    beforeMount() {
        const data = new TableDataFactory().getInstance(this.chart_data, null);
        this.table = data.processIntoTable()
        this.rows = this.table.rows
    },
    components: {
        DataTable,
        Column, 
        InputText, 
        ServerParameters
    }
}
</script>
