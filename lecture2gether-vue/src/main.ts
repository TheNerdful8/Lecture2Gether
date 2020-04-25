import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './plugins/router';
import store from './plugins/store';
import vuetify from './plugins/vuetify';
import './plugins/player';


Vue.config.productionTip = false;

new Vue({
    router,
    store,
    vuetify,
    render: (h) => h(App),
}).$mount('#app');
