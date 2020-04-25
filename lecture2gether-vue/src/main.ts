import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './plugins/router';
import store from './plugins/store';
import vuetify from './plugins/vuetify';


Vue.config.productionTip = false;

import 'video.js/dist/video-js.css'
import VueVideoPlayer from 'vue-video-player'
Vue.use(VueVideoPlayer)

new Vue({
    router,
    store,
    vuetify,
    render: (h) => h(App),
}).$mount('#app');
