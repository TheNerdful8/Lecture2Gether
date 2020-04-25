import { Module } from 'vuex';
import { NewRoomRequest, NewRoomResponse } from '@/api';
import * as socketio from '@/plugins/socket.io';


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
        newRoom: (context) => {
            return socketio.createRoom().then(response => {
                context.commit('setRoomId', response.roomId)
            });
        },

        joinRoom: (context, roomId: string) => {
            socketio.joinRoom(roomId).then(response => {
                context.commit('setRoomId', response.roomId);
            });
        },
    },
};
