import { RouteConfig } from 'vue-router';
import Home from '@/views/Home.vue';
import Room from '@/views/Room.vue';

export default [
    {
        path: '/',
        name: 'home',
        component: Home,
    },
    {
        path: '/l/:roomId',
        name: 'room',
        component: Room,
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
