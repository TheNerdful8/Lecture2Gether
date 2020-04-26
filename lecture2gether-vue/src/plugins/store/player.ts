import { Module } from 'vuex';

export class PlayerState {
    videoUrl = ''
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
        }
    },

    actions: {
        setUrl: async (ctx, payload: string) => {
            ctx.commit('setUrl', payload);
        },
    },
};
