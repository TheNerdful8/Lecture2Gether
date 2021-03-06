import { Module } from 'vuex';
import { CreateRoomRequest, CreateRoomResponse } from '@/api';
import * as socketio from '@/plugins/socket.io';


export class RoomsState {
    /**
     * This is the room id which we are actually connected to.
     * The URL parameter is the one where we _should_ be connected to.
     */
    roomId = ''
    userCount = 0
}


export const roomsModule: Module<RoomsState, any> = {
    state: () => new RoomsState(),

    mutations: {
        setRoomId: (state, payload: string) => {
            state.roomId = payload;
        },
        setUserCount: (state, payload: number) => {
            state.userCount = payload;
        },
    },

    actions: {
        newRoom: (context) => {
            return socketio.createRoom(context.rootState.player).then(response => {
                context.commit('setRoomId', response.roomId);
            });
        },

        joinRoom: (context, roomId: string) => {
            socketio.joinRoom({roomId}).then(response => {
                context.commit('setRoomId', response.roomId);
            });
        },

        leaveRoom: (context) => {
            socketio.leaveRoom({
                roomId: context.state.roomId
            }).then(response => {
                context.commit('setRoomId', '')
            })
        }
    },
};
