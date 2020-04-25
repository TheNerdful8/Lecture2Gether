import Vue from 'vue';
import Vuex from 'vuex';
import { roomsModule } from '@/plugins/store/rooms';
import { settingsModule } from '@/plugins/store/settings';
import { playerModule } from '@/plugins/store/player';


Vue.use(Vuex);


export class RootState {
    isConnected = false
}


export default new Vuex.Store({
    state: () => new RootState(),
    mutations: {
        toggleConnected: (state, payload?: boolean) => {
            if (payload == null)
                payload = !state.isConnected
            state.isConnected = payload
        }
    },
    actions: {},
    modules: {
        rooms: roomsModule,
        settings: settingsModule,
        player: playerModule,
    },
});
