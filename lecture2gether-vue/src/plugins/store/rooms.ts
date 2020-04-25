import {Module} from "vuex";

export class RoomsState {
    roomId: string = ''
}


export const roomsModule: Module<RoomsState, any> = {
    state: () => new RoomsState(),

    mutations: {
        setRoomId: (state, payload: string) => {
            state.roomId = payload
        }
    },

    actions: {
        newRoom: (context) => {
            return fetch(new Request("/api/rooms", {
                method: "POST",
            }))
        }
    }
};
