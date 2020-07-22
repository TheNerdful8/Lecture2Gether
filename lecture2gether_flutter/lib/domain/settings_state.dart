import 'dart:convert';
import 'dart:io';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import 'package:lecture2gether/extensions/http_response_extensions.dart';

class RemoteSettingsModel with ChangeNotifier {
  String _apiRoot;
  String _socketioHost;
  bool _hasUpdated = false;

  String get apiRoot => _apiRoot;

  String get socketioHost => _socketioHost;

  bool get hasUpdated => _hasUpdated;
  
  void _setSocketioHost(String host) {
    _socketioHost = host;
  }

  void updateFromJson(Map<String, dynamic> json) {
    _apiRoot = json['apiRoot'] as String;
    if (json['socketioHost'] != '')
      _socketioHost = json['socketioHost'] as String;

    _hasUpdated = true;
    notifyListeners();
  }
}

class PersistentSettingsModel with ChangeNotifier {
  String host = 'localhost:8080';

  void fetchRemoteSettings(BuildContext context) async {    
    final response = await http.get('http://$host/settings.json').followRedirects();

    if (response.statusCode == HttpStatus.ok) {
      var remoteSettings = context.read<RemoteSettingsModel>();
      remoteSettings._setSocketioHost(host);
      remoteSettings.updateFromJson(jsonDecode(response.body));
    } else {
      throw Exception('Could not fetch settings.json: ${response.statusCode}');
    }
  }
}
