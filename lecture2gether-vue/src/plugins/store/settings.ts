import { Module } from 'vuex';


export class SettingsState {
    apiRoot = '/api'
    socketioHost = ''
    environment = 'dev'
    sentry_dsn = ''
}


export const settingsModule: Module<SettingsState, any> = {
    // @ts-ignore
    state: () => window.L2GO_SETTINGS,
};
