export interface VideoMetaData {
    Url: string,
    StreamUrl: string,
    Title: string,
    Creator: string,
    CreatorLink: string,
    Date: string,
    License: string,
    LicenseLink: string,
}

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
    roomUserCountUpdated: 'room_user_count_update',
};


export interface VideoStateRequest {
    videoMetaData: VideoMetaData|null;
    paused: boolean;
    seconds: number;
    playbackRate: number;
}

export interface VideoStateEvent {
    videoMetaData: VideoMetaData|null;
    paused: boolean;
    seconds: number;
    playbackRate: number;
    currentTime: number;
    setTime: number;
    sender: string;
}

export interface RoomUserCountEvent {
    users: number;
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
    roomId: string;
}

export interface SendVideoStateResponse extends BaseResponse {}
