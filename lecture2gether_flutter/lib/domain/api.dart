import 'package:json_annotation/json_annotation.dart';

part 'api.g.dart';

// ======= Supporting types ========

@JsonSerializable(explicitToJson: true)
class VideoMetaData {
  String url;
  String title;
  String creator;
  String creatorLink;
  String date;
  String license;
  String licenseLink;

  VideoMetaData();

  factory VideoMetaData.fromJson(Map<String, dynamic> json) =>
      _$VideoMetaDataFromJson(json);

  Map<String, dynamic> toJson() => _$VideoMetaDataToJson(this);
}

@JsonSerializable(explicitToJson: true)
class VideoMetaDataWithUrl extends VideoMetaData {
  String streamUrl;

  VideoMetaDataWithUrl();

  factory VideoMetaDataWithUrl.fromJson(Map<String, dynamic> json) =>
      _$VideoMetaDataWithUrlFromJson(json);

  @override
  Map<String, dynamic> toJson() => _$VideoMetaDataWithUrlToJson(this);
}

// ======= Requests ========

class VideoStateRequest {
  VideoMetaData videoMetaData;
  String videoUrl;
  bool paused;
  int seconds;
  int playbackRate;
}

class CreateRoomRequest extends VideoStateRequest {}

class JoinRoomRequest {
  String roomId;
}

class LeaveRoomRequest {
  String roomId;
}

class SendVideoStateRequest extends VideoStateRequest {
  String roomId;
}

// ======= Responses ========

class _BaseResponse {
  int statusCode;
}

class CreateRoomResponse extends _BaseResponse {
  String roomId;
}

class JoinRoomResponse extends _BaseResponse {
  String roomId;
}

class LeaveRoomResponse extends _BaseResponse {}

class SendVideoStateResponse extends _BaseResponse {}

// ======= Events ========

class VideoStateEvent {
  static const eventName = 'video_state_event';

  VideoMetaData videoMetaData;
  String videoUrl;
  bool paused;
  int seconds;
  int playbackRate;
  int currentTime;
  int setTime;
  String sender;
}

class RoomUserCountEvent {
  static const eventName = 'room_user_count_update';

  int users;
}
