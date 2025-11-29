// lib/api_services.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // CAMBIA AQUÍ SI USAS EL EMULADOR O TU PC
  final String baseUrl = "http://127.0.0.1:8000"; // Emulador Android → tu PC
  // final String baseUrl = "http://127.0.0.1:8000"; // Si pruebas en físico o Chrome

  Future<bool> login(String email, String password) async {
    final url = Uri.parse("$baseUrl/auth/login");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "email": email,      // ← AQUÍ ESTABA EL ERROR (antes era "username")
        "password": password
      }),
    );

    if (response.statusCode == 200) {
      final body = jsonDecode(response.body);
      final token = body['access_token'];
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('jwt', token);
      return true;
    }
    return false;
  }

  Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('jwt');
  }

  Future<List<dynamic>> getAssignedDeliveries() async {
    final token = await _getToken();
    final url = Uri.parse("$baseUrl/deliveries/assigned");
    final response = await http.get(
      url,
      headers: {"Authorization": "Bearer $token"},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Error ${response.statusCode}: ${response.body}");
    }
  }

  Future<bool> deliverDelivery(
    int entregaId,
    String filePath,
    double lat,
    double lon,
  ) async {
    final token = await _getToken();
    final url = Uri.parse("$baseUrl/deliveries/$entregaId/deliver");

    var request = http.MultipartRequest('POST', url);
    request.headers['Authorization'] = 'Bearer $token';
    request.fields['lat'] = lat.toString();
    request.fields['lon'] = lon.toString();
    request.files.add(await http.MultipartFile.fromPath('file', filePath));

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    return response.statusCode == 200;
  }
}