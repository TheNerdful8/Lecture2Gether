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
        path: '/l/:roomId',
        name: 'player',
        component: Player,
    },
    {
        path: '/sync/debug',
        name: 'syncdebug',
        component: () => import(/* webpackChunkName: "syncdebug" */ '@/views/SyncControl.vue'),
    },

    {
        path: '*',
        redirect: '/'
    }
] as Array<RouteConfig>;
