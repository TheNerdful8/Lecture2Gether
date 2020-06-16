import io from 'socket.io-client';
import {
    sentEvents,
    receivedEvents,
    JoinRoomRequest,
    JoinRoomResponse,
    LeaveRoomRequest,
    LeaveRoomResponse,
    CreateRoomRequest,
    CreateRoomResponse,
    SendVideoStateResponse,
    SendVideoStateRequest,
    VideoStateEvent,
    RoomUserCountEvent,
} from '@/api';

import Socket = SocketIOClient.Socket;
import {Store} from "vuex";

export let socket: Socket | null = null;

export const connect = (store: Store<any>) => {
    if (store.state.settings.socketioHost === '') {
        socket = io({
            autoConnect: false
        });
    } else {
        socket = io(store.state.settings.socketioHost, {
            autoConnect: false
        })
    }

    socket.on('connect', () => {
        console.debug('socket.io connected');
        store.commit('toggleConnected', true);
        store.commit('setSocketId', getSafeSocket().id)
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
        joinRoom({roomId: store.state.rooms.roomId});
        store.commit('setSocketId', getSafeSocket().id)
    });

    socket.on(receivedEvents.videoStateUpdated, (state: VideoStateEvent) => {
        let seconds = state.seconds;
        if (store.state.player.seconds === seconds) {
            // You might ask what happens here, and I cannot blame you.
            // The seconds are changed to re-trigger the onSecondsChange watcher in Player.vue.
            // It is necessary to set the video to the correct time after you join a paused video.
            seconds += 0.000001
        }
        if (!state.paused) {
            seconds = Math.max(0, (state.currentTime - state.setTime) * state.playbackRate + state.seconds);
        }
        store.commit('setSender', state.sender);
        store.commit('setVideoState', {
            seconds,
            paused: state.paused,
            playbackRate: state.playbackRate,
        })
        store.commit('setVideoMetaData', state.videoMetaData)
        store.commit('setUrl', state.videoUrl)
    });

    socket.on(receivedEvents.roomUserCountUpdated, (event: RoomUserCountEvent) => {
        store.commit('setUserCount', event.users);
    });

    socket.connect();
};


const getSafeSocket = (): Socket => {
    if (socket) return socket;
    throw new Error('socket.io socket is not yet connected');
};


export const sendVideoState = (state: SendVideoStateRequest) => {
    let sendState = {
        ...state,
        sender: getSafeSocket().id,
    }
    console.debug('socket.io send state', sendState);
    return new Promise((resolve, reject) => {
            getSafeSocket().emit(sentEvents.setVideoState, sendState, (response: SendVideoStateResponse) => {
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

export const disconnect = () => {
    console.debug('socket.io closing the socket')
    getSafeSocket().disconnect();
}
