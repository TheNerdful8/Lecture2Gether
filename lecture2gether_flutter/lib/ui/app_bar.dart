import 'package:flutter/material.dart';
import 'package:lecture2gether/ui/user_counter.dart';

class L2gAppBar extends StatefulWidget implements PreferredSizeWidget {
  L2gAppBar({Key key}) : super(key: key);

  @override
  _L2gAppBarState createState() => _L2gAppBarState();

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}

class _L2gAppBarState extends State<L2gAppBar> {
  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: Text("Lecture2Gether"),
      actions: [
        L2gUserCounter()
      ],
    );
  }
}
