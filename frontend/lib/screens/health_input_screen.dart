import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'result_screen.dart';

class HealthInputScreen extends StatefulWidget {
  @override
  _HealthInputScreenState createState() => _HealthInputScreenState();
}

class _HealthInputScreenState extends State<HealthInputScreen> {
  int age = 25, diabetes = 0, cholesterol = 0, hypertension = 0;
  double weight = 70, height = 170;
  String gender = 'M', goal = 'Weight Loss';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Enter Health Details')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: ListView(
          children: [
            TextFormField(
              decoration: InputDecoration(labelText: 'Age'),
              initialValue: age.toString(),
              onChanged: (v) => age = int.parse(v),
            ),
            DropdownButtonFormField(
              decoration: InputDecoration(labelText: 'Gender'),
              value: gender,
              items: ['M', 'F'].map((g) => DropdownMenuItem(value: g, child: Text(g))).toList(),
              onChanged: (v) => gender = v!,
            ),
            TextFormField(
              decoration: InputDecoration(labelText: 'Weight'),
              initialValue: weight.toString(),
              onChanged: (v) => weight = double.parse(v),
            ),
            TextFormField(
              decoration: InputDecoration(labelText: 'Height'),
              initialValue: height.toString(),
              onChanged: (v) => height = double.parse(v),
            ),
            DropdownButtonFormField(
              decoration: InputDecoration(labelText: 'Goal'),
              value: goal,
              items: ['Weight Loss', 'Weight Gain', 'Cholesterol Control', 'Diabetes Control', 'Fitness', 'General Health'].map(
                (g) => DropdownMenuItem(value: g, child: Text(g))
              ).toList(),
              onChanged: (v) => goal = v!,
            ),
            SwitchListTile(
              title: Text('Diabetes'), value: diabetes == 1,
              onChanged: (v) => setState(() => diabetes = v ? 1 : 0),
            ),
            SwitchListTile(
              title: Text('Cholesterol'), value: cholesterol == 1,
              onChanged: (v) => setState(() => cholesterol = v ? 1 : 0),
            ),
            SwitchListTile(
              title: Text('Hypertension'), value: hypertension == 1,
              onChanged: (v) => setState(() => hypertension = v ? 1 : 0),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              child: Text('Get Recommendation'),
              onPressed: () async {
                var data = {
                  'age': age, 'gender': gender, 'weight': weight, 'height': height,
                  'diabetes': diabetes, 'cholesterol': cholesterol,
                  'hypertension': hypertension, 'goal': goal
                };
                var result = await ApiService.getRecommendation(data);
                Navigator.push(context, MaterialPageRoute(
                  builder: (_) => ResultScreen(
                    diet: result['recommended_diet'],
                    foods: List<String>.from(result['foods'])
                  )
                ));
              },
            )
          ],
        ),
      ),
    );
  }
}
