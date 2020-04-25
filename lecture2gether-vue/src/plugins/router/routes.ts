import { RouteConfig } from 'vue-router';
import Home from '@/views/Home.vue';

export default [
    {
        path: '/',
        name: 'home',
        component: Home,
    },

    {
        path: '/sync/debug',
        name: 'syncdebug',
        component: () => import(/* webpackChunkName: "syncdebug" */ '@/views/SyncControl.vue'),
    }
] as Array<RouteConfig>;
