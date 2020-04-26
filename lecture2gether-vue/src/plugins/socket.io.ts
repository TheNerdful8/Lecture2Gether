import io from 'socket.io-client';
import {
    sentEvents,
    receivedEvents,
    JoinRoomRequest,
    JoinRoomResponse,
    LeaveRoomRequest,
    LeaveRoomResponse,
    CreateRoomRequest, CreateRoomResponse, SendVideoStateResponse, SendVideoStateRequest,
} from '@/api';

import Socket = SocketIOClient.Socket;
import {Store} from "vuex";

export let socket: Socket | null = null;

export const connect = (store: Store<any>) => {
    if (store.state.settings.apiRoot.includes('://')) {
        const url = new URL(store.state.settings.apiRoot)
        socket = io(url.host, {
            path: `${url.pathname}socket.io`,
            autoConnect: false,
        })

    } else {
        socket = io({
            path: `${store.state.settings.apiRoot}/socket.io`,
            autoConnect: false,
        });
    }

    socket.on('connect', () => {
        console.debug('socket.io connected');
        store.commit('toggleConnected', true);
    });
    socket.on('connect_error', (e: Error) => {
        console.error(`socket.io connection error: ${e}`);
    });
    socket.on('connect_timeout', (e: Error) => {
        console.error(`socket.io connection timed out: ${e}`);
    });
    socket.on('error', (e: Error) => {
        console.error(`socket.io error ${e}`);
    });
    socket.on('disconnect', (reason: string) => {
        console.error(`socket.io disconnected because ${reason}`);
        store.commit('toggleConnected', false);
    });
    socket.on('reconnect', (attemptNumber: number) => {
        console.error(`socket.io reconnected after ${attemptNumber} attempts`);
    });

    socket.on(receivedEvents.videoStateUpdated, (state: any) => {
        store.commit('setVideoState', {
            seconds: state.seconds,
            paused: state.paused,
        })
        store.commit('setUrl', state.videoUrl)
    });

    socket.connect();
};


const getSafeSocket = (): Socket => {
    if (socket) return socket;
    throw new Error('socket.io socket is not yet connected');
};


export const sendVideoState = (state: SendVideoStateRequest) => {
    console.debug('socket.io send state', state);
    return new Promise((resolve, reject) => {
            getSafeSocket().emit(sentEvents.setVideoState, state, (response: SendVideoStateResponse) => {
            console.debug('socket.io response from sending video state', response)
            if (response.status_code === 200) resolve(response);
            else reject(response);
        });
    });
};


export const joinRoom = (request: JoinRoomRequest): Promise<JoinRoomResponse> => {
    console.debug('socket.io joining room', request)
    return new Promise((resolve, reject) => {
        getSafeSocket().emit(sentEvents.joinRoom, request, (response: JoinRoomResponse) => {
            console.debug(`socket.io response from joining room`, response)
            if (response.status_code === 200) resolve(response);
            else reject(response);
        });
    });
};


export const createRoom = (request: CreateRoomRequest): Promise<CreateRoomResponse> => {
    console.debug('socket.io creating room', request)
    return new Promise<JoinRoomResponse>((resolve, reject) => {
        getSafeSocket().emit(sentEvents.createRoom, request, (response: JoinRoomResponse) => {
            console.debug('socket.io response from creating room', response)
            if (response.status_code === 200) resolve(response)
            else reject(response)
        });
    })
}


export const leaveRoom = (request: LeaveRoomRequest): Promise<LeaveRoomResponse> => {
    console.debug('socket.io leaving room')
    return new Promise<LeaveRoomResponse>((resolve, reject) => {
        getSafeSocket().emit(sentEvents.leaveRoom, request, (response: LeaveRoomResponse) => {
            console.debug('socket.io response from leaving room', response)
            if (response.status_code === 200) resolve(response)
            else reject(response)
        })
    })
}
