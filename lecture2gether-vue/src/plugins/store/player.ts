import {Module} from 'vuex';
import {NewRoomRequest, NewRoomResponse} from '@/apiTypes';

export class PlayerState {
    videoUrl = ''
}


export const playerModule: Module<PlayerState, any> = {
    state: () => new PlayerState(),

    mutations: {
        setUrl: (state, payload: string) => {
            state.videoUrl = payload;
        },
    },

    actions: {
        setUrl: async (ctx, payload: string) => {
            ctx.commit("setUrl", payload);
        }
    },
};
