import { Module } from 'vuex';
import { NewRoomRequest, NewRoomResponse } from '@/api';
import * as socketio from '@/plugins/socket.io';


export class RoomsState {
    /**
     * This is the room id which we are actually connected to.
     * The URL parameter is the one where we _should_ be connected to.
     */
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
        newRoom: (context) => {
            return socketio.createRoom().then(response => {
                context.commit('setRoomId', response.roomId);
            });
        },

        joinRoom: (context, roomId: string) => {
            socketio.joinRoom(roomId).then(response => {
                context.commit('setRoomId', response.roomId);
            });
        },
    },
};
