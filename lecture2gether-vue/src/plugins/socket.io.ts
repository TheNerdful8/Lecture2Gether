import io from 'socket.io-client';
import {
    sentEvents, receivedEvents, JoinRoomRequest, JoinRoomResponse,
} from '@/api';

import Socket = SocketIOClient.Socket;
import {Store} from "vuex";

export let socket: Socket | null = null;

export const connect = (store: Store<any>) => {
    socket = io({
        path: `${store.state.settings.apiRoot}/socket.io`,
        autoConnect: false,
    });

    socket.on('connect', () => {
        console.log('socket.io connected');
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
    });
    socket.on('reconnect', (attemptNumber: number) => {
        console.error(`socket.io reconnected after ${attemptNumber} attempts`);
    });

    socket.on(receivedEvents.videoStateUpdated, onVideoStateUpdate);

    socket.connect();
};


const getSafeSocket = (): Socket => {
    if (socket) return socket;
    throw new Error('socket.io socket is not yet connected');
};


const onVideoStateUpdate = (state: any) => {
    console.log(`received state: ${state}`);
}


export const joinRoom = (roomId: string): Promise<JoinRoomResponse> => {
    const socket = getSafeSocket();
    return new Promise((resolve, reject) => {
        socket.once(receivedEvents.roomJoined, (response: JoinRoomResponse) => {
            if (response.status_code !== 0) reject(response);
            else resolve(response);
        });

        socket.emit(sentEvents.joinRoom, {
            roomId,
        } as JoinRoomRequest);
    });
};


export const createRoom = (): Promise<JoinRoomResponse> => {
    const socket = getSafeSocket();
    return new Promise<JoinRoomResponse>((resolve, reject) => {
        socket.once(receivedEvents.roomJoined, (response: JoinRoomResponse) => {
            if (response.status_code !== 0) reject(response)
            else resolve(response)
        });

        socket.emit(sentEvents.createRoom, {});
    })
}
