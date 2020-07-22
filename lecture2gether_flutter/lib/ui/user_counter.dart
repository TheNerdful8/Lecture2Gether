import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:lecture2gether/domain/shared_state.dart';
import 'package:provider/provider.dart';

class L2gUserCounter extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<SharedStateModel>(
      builder: (context, value, child) {
        return IconButton(
          icon: Row(
            children: [
              Text('1'),     // TODO Display correct number of users in room
              Icon(Icons.supervisor_account),
            ],
          ),
          tooltip: 'Number of users currently in the Room',
          onPressed: () {},
        );
      },
    );
  }
}
