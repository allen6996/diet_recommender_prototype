import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static Future<Map<String, dynamic>> getRecommendation(Map<String, dynamic> userData) async {
    var url = Uri.parse('http://127.0.0.1:8000/recommend');
    var res = await http.post(url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(userData),
    );
    if (res.statusCode == 200) {
      return jsonDecode(res.body);
    } else {
      throw Exception('Failed to get recommendation');
    }
  }
}
