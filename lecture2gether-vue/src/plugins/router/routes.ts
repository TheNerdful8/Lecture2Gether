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
] as Array<RouteConfig>;
