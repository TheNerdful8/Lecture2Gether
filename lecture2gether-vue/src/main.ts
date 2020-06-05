import Vue from 'vue';
import App from './App.vue';
import router from './plugins/router';
import store from './plugins/store';
import vuetify from './plugins/vuetify';
import * as Sentry from "@sentry/browser";
import {Vue as VueIntegration} from "@sentry/integrations/dist/vue";


Vue.config.productionTip = false;

// Fetch settings because we can only initialize sentry before Vue      TODO Improve because loading delay
fetch(new Request('/settings.json', {
    mode: 'same-origin',
}))
    .then(response => response.json())
    .then(response => {
        if (response.sentry_dsn !== '')
            Sentry.init({
                dsn: response.sentry_dsn,
                environment: response.environment,
                integrations: [new VueIntegration({
                    // @ts-ignore
                    Vue: Vue,
                    attachProps: true,
                    logErrors: true,
                })],
            });

        new Vue({
            router,
            store,
            vuetify,
            render: (h) => h(App),
        }).$mount('#app');
    });
