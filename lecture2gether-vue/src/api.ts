interface BaseResponse {
    error_code: number;
}


export const sentEvents = {
    joinRoom: 'join',
};

export const receivedEvents = {
    roomJoined: 'join_room',
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
