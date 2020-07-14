import 'package:flutter/foundation.dart';

class VideoMetaData {
  String url;
  String title;
  String creator;
  String creatorLink;
  String date;
  String license;
  String licenseLink;
}

class VideoMetaDataWithUrl extends VideoMetaData {
  String streamUrl;
}

enum AuthState {
  UNNECESSARY,
  NECESSARY,
  CHECKING,
  FAILURE,
  SUCCESS,
}

class SharedStateModel with ChangeNotifier {
  VideoMetaData videoMetaData;
  String videoUrl;
  bool paused = false;
  int seconds = 0;
  int playbackRate = 1;
  String password = "";
  AuthState auth = AuthState.UNNECESSARY;
  String sender = "";
}
