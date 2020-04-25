import io from 'socket.io-client';
import {
    sentEvents, receivedEvents, JoinRoomRequest, JoinRoomResponse,
} from '@/api';

import Socket = SocketIOClient.Socket;

export let socket: Socket | null = null;

export const connect = () => {
    socket = io({
        autoConnect: false,
    });

    socket.on('connect', () => {
        console.log('socket.io connected');
    });
    socket.on('connect_error', (e: any) => {
        console.error(`socket.io connection error: ${e}`);
    });
    socket.on('connect_timeout', (e: any) => {
        console.error(`socket.io connection timed out: ${e}`);
    });
    socket.on('error', (e: any) => {
        console.error(`socket.io error ${e}`);
    });
    socket.on('disconnect', (reason: any) => {
        console.error(`socket.io disconnected because ${reason}`);
    });
    socket.on('reconnect', (attemptNumber: any) => {
        console.error(`socket.io reconnected after ${attemptNumber} attempts`);
    });

    socket.connect();
};

const getSafeSocket = (): Socket => {
    if (socket) return socket;
    throw new Error('socket.io socket is not yet connected');
};

export const joinRoom = (roomId: string): Promise<JoinRoomResponse> => {
    const socket = getSafeSocket();
    return new Promise((resolve, reject) => {
        socket.once(receivedEvents.roomJoined, (response: JoinRoomResponse) => {
            if (response.error_code !== 0) reject(response);
            else resolve(response);
        });
        socket.emit(sentEvents.joinRoom, {
            roomId,
        } as JoinRoomRequest);
    });
};
