import { RouteConfig } from 'vue-router';
import Home from '@/views/Home.vue';
import Player from '@/views/Player.vue';

export default [
    {
        path: '/',
        name: 'home',
        component: Home,
    },
    {
        path: '/player',
        name: 'player',
        component: Player,
    },
    {
        path: '/sync/debug',
        name: 'syncdebug',
        component: () => import(/* webpackChunkName: "syncdebug" */ '@/views/SyncControl.vue'),
    },
] as Array<RouteConfig>;
