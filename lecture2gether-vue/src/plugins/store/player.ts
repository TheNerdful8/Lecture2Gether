import { Module } from 'vuex';

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
        },
        setVideoState: async (ctx, state) => {
            ctx.commit('setVideoState', state)
        },
    },
};
