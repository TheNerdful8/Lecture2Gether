import 'package:flutter/foundation.dart';
import 'api.dart';

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
