<template>
    <div style="width: 100%;">
        <h2>{{ chart_data.getTitle() }}</h2>
        <DataTable :value="products" tableStyle="min-width: 50rem" paginator :rows="5" :globalFilterFields="['code', 'name', 'category', 'quantity']" :filters="filters">
            <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText v-model="filters.global.value" placeholder="Search..." />
            </span>
            <Column field="code" header="Code" sortable></Column>
            <Column field="name" header="Name" sortable></Column>
            <Column field="category" header="Category" sortable></Column>
            <Column field="quantity" header="Quantity" sortable></Column>
        </DataTable>
    </div>
</template>
<script>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import { FilterMatchMode } from '@primevue/core/api';

export default {
    name: 'TableData',
    props: ['chart_data', 'index'],
    data() {
        return {
            filters: {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            },
            products: [
                {code: 'R01', name: 'Product 1', category: 'Category 1', quantity: 10},
                {code: 'R02', name: 'Product 2', category: 'Category 2', quantity: 20},
                {code: 'R03', name: 'Product 3', category: 'Category 3', quantity: 30},
                {code: 'R04', name: 'Product 4', category: 'Category 4', quantity: 40},
                {code: 'R05', name: 'Product 5', category: 'Category 5', quantity: 50},
                {code: 'R06', name: 'Product 6', category: 'Category 6', quantity: 60},
                {code: 'R07', name: 'Product 7', category: 'Category 7', quantity: 70},
                {code: 'R08', name: 'Product 8', category: 'Category 8', quantity: 80},
                {code: 'R09', name: 'Product 9', category: 'Category 9', quantity: 90},
                {code: 'R10', name: 'Product 10', category: 'Category 10', quantity: 100}
            ]
        }
    },
    components: {
        DataTable,
        Column, 
        InputText
    }
}
</script>
