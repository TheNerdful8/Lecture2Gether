import 'package:flutter/material.dart';
import 'package:lecture2gether/domain/connection_state.dart';
import 'package:lecture2gether/domain/settings_state.dart';
import 'package:lecture2gether/domain/shared_state.dart';
import 'package:lecture2gether/ui/app_bar.dart';
import 'package:provider/provider.dart';

void main() =>
    runApp(MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SharedStateModel()),
        ChangeNotifierProvider(create: (_) => PersistentSettingsModel()),
        ChangeNotifierProvider(create: (_) => RemoteSettingsModel()),
        ChangeNotifierProvider(create: (_) => ConnectionStateModel()),
      ],
      child: L2gApp(),
    ));

class L2gApp extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _L2gAppState();
}

class _L2gAppState extends State<L2gApp> {
  @override
  Widget build(BuildContext context) {
    context.watch<RemoteSettingsModel>();

    return MaterialApp(
      home: Scaffold(
        body: CustomScrollView(
          physics: const BouncingScrollPhysics(),
          slivers: [
            L2gAppBar(),
            SliverList(
              delegate: SliverChildListDelegate([
                Placeholder(),
                Placeholder(),
                Placeholder(),
              ]),
            )
          ],
        ),
      ),
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();

    var remoteSettings = context.read<RemoteSettingsModel>();
    var connection = context.read<ConnectionStateModel>();
    if (remoteSettings.hasUpdated && !connection.isConnected) {
      connection.connect(remoteSettings);
    }
  }

  @override
  void initState() {
    super.initState();
    var settings = context.read<PersistentSettingsModel>();
    settings.fetchRemoteSettings(context);
  }
}
