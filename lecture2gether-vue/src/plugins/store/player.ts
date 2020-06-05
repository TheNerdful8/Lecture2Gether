import { Module } from 'vuex';
import { sendVideoState } from '@/plugins/socket.io'
import { VideoMetaData } from '@/api'

export class PlayerState {
    videoMetaData: VideoMetaData|null = null;
    paused: boolean = false;
    seconds: number = 0;
    playbackRate: number = 1;
    password = ''
    auth = AuthState.UNNECESSARY
    sender = '';
}

export enum AuthState {
    UNNECESSARY, NECESSARY, CHECKING, FAILURE, SUCCESS
}


export const playerModule: Module<PlayerState, any> = {
    state: () => new PlayerState(),

    mutations: {
        setVideoMetaData: (state, payload: VideoMetaData) => {
            state.videoMetaData = payload;
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
            state.playbackRate = payload.playbackRate;
        },
        setSender: (state, payload) => {
            state.sender = payload;
        }
    },

    actions: {
        setVideoMetaData: async (ctx, payload: string) => {
            ctx.commit('setVideoMetaData', payload);
            sendVideoState({
                roomId: ctx.rootState.rooms.roomId,
                videoMetaData: ctx.state.videoMetaData,
                paused: ctx.state.paused,
                seconds: ctx.state.seconds,
                playbackRate: ctx.state.playbackRate,
            });
        },
        setVideoState: async (ctx, state) => {
            ctx.commit('setVideoState', state)
            sendVideoState({
                roomId: ctx.rootState.rooms.roomId,
                videoMetaData: ctx.state.videoMetaData,
                paused: ctx.state.paused,
                seconds: ctx.state.seconds,
                playbackRate: ctx.state.playbackRate,
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
