import { Module } from 'vuex';
import { sendVideoState } from '@/plugins/socket.io'

export class PlayerState {
    videoUrl: string = '';
    paused: boolean = false;
    seconds: number = 0;
}


export const playerModule: Module<PlayerState, any> = {
    state: () => new PlayerState(),

    mutations: {
        setUrl: (state, payload: string) => {
            state.videoUrl = payload;
        },
        setVideoState: (state, payload) => {
            state.paused = payload.paused;
            state.seconds = payload.seconds;
        },
    },

    actions: {
        setUrl: async (ctx, payload: string) => {
            ctx.commit('setUrl', payload);
            sendVideoState({
                ...ctx.state,
                roomId: ctx.rootState.rooms.roomId
            });
        },
        setVideoState: async (ctx, state) => {
            ctx.commit('setVideoState', state)
            sendVideoState({
                ...ctx.state,
                roomId: ctx.rootState.rooms.roomId
            });
        },
    },
};
