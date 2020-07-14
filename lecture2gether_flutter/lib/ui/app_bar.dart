import 'package:flutter/material.dart';
import 'package:lecture2gether/ui/share_room_button.dart';
import 'package:lecture2gether/ui/user_counter.dart';

class L2gAppBar extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SliverAppBar(
      pinned: true,
      expandedHeight: 150.0,
      flexibleSpace: const FlexibleSpaceBar(
        title: Text("Lecture2Gether"),
        centerTitle: true,
      ),
      actions: [
        L2gUserCounter(),
        L2gShareRoomButton(),
        IconButton(
          icon: const Icon(Icons.settings),
          tooltip: "Settings",
          onPressed: () {},
        )
      ],
    );
  }
}
