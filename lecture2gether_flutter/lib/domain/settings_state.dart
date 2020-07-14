import 'package:flutter/foundation.dart';

class PersistentSettingsModel with ChangeNotifier {
  String host = "localhost";
}

class DerivedSettingsModel with ChangeNotifier {
  String apiRoot = "/api";
  String socketIoHost = "";
}
