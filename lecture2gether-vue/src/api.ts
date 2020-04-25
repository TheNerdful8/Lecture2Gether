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


export type NewRoomRequest = {}

export interface NewRoomResponse extends BaseResponse{
    roomId: string;
}

export interface JoinRoomRequest {
    roomId: string;
}

export interface JoinRoomResponse extends BaseResponse {
    roomId: string;
}
