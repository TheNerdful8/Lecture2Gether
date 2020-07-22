import 'package:clipboard/clipboard.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:share/share.dart';

class L2gShareRoomButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return IconButton(
      onPressed: onPress,
      icon: const Icon(Icons.share),
      tooltip: 'Share Room',
    );
  }

  void onPress() {
    var url = 'https://lecture2gether.eu';  // TODO Actually share url to l2g room

    if (kIsWeb) {
      FlutterClipboard.copy(url);
      print('$url copied to clipboard');  // TODO Display a toast instead
    } else {
      Share.share(url);
    }
  }
}