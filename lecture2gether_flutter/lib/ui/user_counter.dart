import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:lecture2gether/domain/shared_state.dart';
import 'package:provider/provider.dart';

class L2gUserCounter extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<SharedStateModel>(
      builder: (context, value, child) {
        return Row(
          children: [
            Text("1"),  // TODO Put correct user number in app-bar
            Icon(Icons.account_box)
          ],
        );
      },
    );
  }
}
