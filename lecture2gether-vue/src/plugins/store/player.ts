import Vue from 'vue';
import { Module } from 'vuex';


export class PlayerState {
    /**
     * Whether the player is currently playing or not
     */
    playing: boolean = false

    /**
     * Timestamp in the video (0 = start of video) which is up to 5 seconds off from the real timestamp.
     */
    roughTimestamp: number = 0
}


export const playerModule: Module<PlayerState, any> = {
    state: () => new PlayerState(),

    mutations: {
        togglePlaying: (state, payload?: boolean) => {
            if (payload) {
                state.playing = payload
            } else {
                state.playing = !state.playing
            }
        }
    },

    actions: {
        togglePlaying: (context, payload?: boolean) => {
            if (!payload)
                payload = !context.state.playing;


        }
    },
};
