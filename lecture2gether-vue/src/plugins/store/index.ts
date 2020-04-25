import Vue from 'vue';
import Vuex from 'vuex';
import { roomsModule } from '@/plugins/store/rooms';
import { settingsModule } from '@/plugins/store/settings';


Vue.use(Vuex);


export default new Vuex.Store({
    state: {},
    mutations: {},
    actions: {},
    modules: {
        rooms: roomsModule,
        settings: settingsModule,
    },
});
