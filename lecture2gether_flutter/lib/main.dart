import 'package:flutter/material.dart';
import 'package:lecture2gether/domain/connection_state.dart';
import 'package:lecture2gether/domain/settings_state.dart';
import 'package:lecture2gether/domain/shared_state.dart';
import 'package:lecture2gether/ui/app_bar.dart';
import 'package:provider/provider.dart';

void main() => runApp(
  MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (_) => SharedStateModel()),
      ChangeNotifierProvider(create: (_) => PersistentSettingsModel()),
      ChangeNotifierProvider(create: (_) => ConnectionStateModel()),
    ],
    child: L2gApp(),
  )
);

class L2gApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: L2gAppBar(),
        body: Text("Hello World"),
      ),
    );
  }
}
