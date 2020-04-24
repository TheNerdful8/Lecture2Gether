import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import routes from '@/plugins/router/routes';


Vue.use(VueRouter);
const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;
