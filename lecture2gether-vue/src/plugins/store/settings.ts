import Vue from 'vue';
import { Module } from 'vuex';


export class SettingsState {
    apiRoot = '/api'
    socketioHost = ''
    environment = 'dev'
    sentry_dsn = ''
}


export const settingsModule: Module<SettingsState, any> = {
    state: () => new SettingsState(),

    mutations: {
        updateSettings: (state, payload) => {
            for (const p of Object.keys(state)) {
                if (payload[p] !== undefined) {
                    Vue.set(state, p, payload[p]);
                }
            }
        },
    },

    actions: {
        fetchSettings: async (context) => {
            const response = await fetch(new Request('/settings.json', {
                mode: 'same-origin',
            }));
            context.commit('updateSettings', await response.json());
        },
    },
};
