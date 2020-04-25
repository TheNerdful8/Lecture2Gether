import {Module} from 'vuex';
import {NewRoomRequest, NewRoomResponse} from '@/apiTypes';

export class RoomsState {
    roomId = ''
}


export const roomsModule: Module<RoomsState, any> = {
    state: () => new RoomsState(),

    mutations: {
        setRoomId: (state, payload: string) => {
            state.roomId = payload;
        },
    },

    actions: {
        newRoom: (context) => fetch(new Request(`${context.rootState.settings.apiRoot}/rooms`, {
            method: 'POST',
            body: JSON.stringify(({} as NewRoomRequest)),
        }))
            .then((response) => response.json())
            .then((response: NewRoomResponse) => {
                context.commit('setRoomId', response.roomId);
            }),
    },
};
