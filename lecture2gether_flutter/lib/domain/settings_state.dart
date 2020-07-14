import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:json_annotation/json_annotation.dart';
import 'package:provider/provider.dart';

class RemoteSettingsModel with ChangeNotifier {
  String _apiRoot;
  String _socketioHost;

  String get apiRoot => _apiRoot;

  String get socketioHost => _socketioHost;

  updateFromJson(Map<String, dynamic> json) {
    _apiRoot = json["apiRoot"] as String;
    _socketioHost = json["socketioHost"] as String;

    notifyListeners();
  }
}

class PersistentSettingsModel with ChangeNotifier {
  String host = "http://localhost:8080";

  void fetchRemoteSettings(BuildContext context) async {
    final response = await http.get("$host/settings.json");
    if (response.statusCode == 200) {
      var remoteSettings = context.read<RemoteSettingsModel>();
      remoteSettings.updateFromJson(jsonDecode(response.body));
    } else {
      throw Exception("Could not fetch settings.json");
    }
  }
}
