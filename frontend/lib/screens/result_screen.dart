import 'package:flutter/material.dart';

class ResultScreen extends StatelessWidget {
  final String diet;
  final List<String> foods;

  ResultScreen({required this.diet, required this.foods});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Recommendation')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Recommended diet: $diet', style: TextStyle(fontSize: 20)),
            SizedBox(height: 16),
            Text('You should eat:', style: TextStyle(fontSize: 18)),
            ...foods.map((food) => Text('- $food', style: TextStyle(fontSize: 16)))
          ],
        ),
      ),
    );
  }
}
