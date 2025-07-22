import 'package:flutter/material.dart';
import 'health_input_screen.dart';

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Center(
        child: ElevatedButton(
          child: Text('Login'),
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => HealthInputScreen())
            );
          },
        ),
      ),
    );
  }
}
