import Vue from 'vue';
import App from './App.vue';
import router from './plugins/router';
import store from './plugins/store';
import vuetify from './plugins/vuetify';
import * as Sentry from "@sentry/browser";
import {Vue as VueIntegration} from "@sentry/integrations/dist/vue";
import {SettingsState} from "@/plugins/store/settings";


Vue.config.productionTip = false;

// @ts-ignore
// global settings are loaded via a separate script tag so that they can be runtime configurable
const settings: SettingsState = window.L2GO_SETTINGS;

if (settings.sentry_dsn != null && settings.sentry_dsn !== '')
    Sentry.init({
        dsn: settings.sentry_dsn,
        environment: settings.environment,
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
