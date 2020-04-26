import { Module } from 'vuex';
import { sendVideoState } from '@/plugins/socket.io'

export class PlayerState {
    videoUrl: string = '';
    paused: boolean = false;
    seconds: number = 0;
    password = ''
    auth = AuthState.UNNECESSARY
}

export enum AuthState {
    UNNECESSARY, NECESSARY, CHECKING, FAILURE, SUCCESS
}


export const playerModule: Module<PlayerState, any> = {
    state: () => new PlayerState(),

    mutations: {
        setUrl: (state, payload: string) => {
            state.videoUrl = payload;
        },
        setPassword: (state, payload: string) => {
            state.password = payload;
        },
        setAuthState: (state, payload: AuthState) => {
            state.auth = payload;
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
                videoUrl: ctx.state.videoUrl,
                paused: ctx.state.paused,
                seconds: ctx.state.seconds,
                roomId: ctx.rootState.rooms.roomId
            });
        },
        setVideoState: async (ctx, state) => {
            ctx.commit('setVideoState', state)
            sendVideoState({
                videoUrl: ctx.state.videoUrl,
                paused: ctx.state.paused,
                seconds: ctx.state.seconds,
                roomId: ctx.rootState.rooms.roomId
            });
        },
    },

    getters: {
        authRequired: state =>  {
            return state.auth === AuthState.NECESSARY
                || state.auth === AuthState.CHECKING
                || state.auth === AuthState.FAILURE;
        }
    }
};
