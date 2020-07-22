import 'package:flutter/foundation.dart';
import 'package:lecture2gether/domain/api.dart';
import 'package:lecture2gether/domain/settings_state.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;

class ConnectionStateModel with ChangeNotifier {
  IO.Socket _socket;

  String roomId = '';

  bool get isConnected => _socket != null && _socket.connected;

  void connect(RemoteSettingsModel settings) async {
    assert(!isConnected, 'Socket is already connected so cannot connect again');

    print('Connecting SocketIO to ${settings.socketioHost}');
    _socket = IO.io(settings.socketioHost, <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': false,
    })
      ..on('connect', (_) => _onConnect())
      ..on('disconnect', (_) => _onDisconnect())
      ..on('connect_error', (data) => _onConnectError(data))
      ..on('connect_timeout', (data) => _onConnectTimeout(data))
      ..on('error', (data) => _onError(data))
      ..on(VideoStateEvent.eventName, (data) => _onVideoStateUpdate(data))
      ..on(RoomUserCountEvent.eventName, (data) => _onRoomUserCountUpdate(data))
      ..connect();
  }

  void _onConnect() {
    print('SocketIO connected');
  }

  void _onConnectError(reason) {
    print(reason);
    print('SocketIO connect error');
  }

  void _onConnectTimeout(timeout) {
    print('SocketIO connect timeout');
  }

  void _onDisconnect() {
    print('SocketIO disconnected');
  }

  void _onError(error) {
    print('SocketIO error: $error');
  }

  void _onVideoStateUpdate(String data) {}

  void _onRoomUserCountUpdate(String data) {}
}
