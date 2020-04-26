interface BaseResponse {
    status_code: number;
}


export const sentEvents = {
    createRoom: 'create',
    joinRoom: 'join',
    leaveRoom: 'leave',
    setVideoState: 'video_state_set',
};

export const receivedEvents = {
    videoStateUpdated: 'video_state_update',
};


export interface VideoStateRequest {
    videoUrl: string;
    paused: boolean;
    seconds: number;
    playbackRate: number;
}

export interface VideoStateEvent {
    videoUrl: string;
    paused: boolean;
    seconds: number;
    playbackRate: number;
    currentTime: number;
    setTime: number;
    sender: string;
}


export interface CreateRoomRequest extends VideoStateRequest {}

export interface CreateRoomResponse extends BaseResponse{
    roomId: string;
}

export interface JoinRoomRequest {
    roomId: string;
}

export interface JoinRoomResponse extends BaseResponse {
    roomId: string;
}

export type LeaveRoomRequest = {
    roomId: string;
}

export interface LeaveRoomResponse extends BaseResponse {}

export interface SendVideoStateRequest extends VideoStateRequest {
    roomId:string;
}

export interface SendVideoStateResponse extends BaseResponse {}
