import { createApp } from 'vue'
import store from './store';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import './style.scss'
import App from './App.vue'

const app = createApp(App)

app.use(store)
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});


app.mount('#app')




