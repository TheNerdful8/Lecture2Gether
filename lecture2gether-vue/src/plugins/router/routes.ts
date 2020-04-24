import { RouteConfig } from 'vue-router';
import Home from '@/views/Home.vue';

export default [
    {
        path: '/',
        name: 'home',
        component: Home,
    },
] as Array<RouteConfig>;
