import 'package:flutter/material.dart';
import '/api_services.dart';

class LoginScreen extends StatefulWidget {
  @override _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _user = TextEditingController();
  final _pass = TextEditingController();
  final api = ApiService();
  bool loading = false;

  void _login() async {
    setState(() => loading = true);
    bool ok = await api.login(_user.text.trim(), _pass.text);
    setState(() => loading = false);
    if (ok) Navigator.pushReplacementNamed(context, '/deliveries');
    else ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Login falló")));
  }

  @override Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Paquexpress - Login')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(children: [
          TextField(controller: _user, decoration: InputDecoration(labelText: 'Usuario')),
          TextField(controller: _pass, decoration: InputDecoration(labelText: 'Contraseña'), obscureText: true),
          SizedBox(height: 20),
          ElevatedButton(onPressed: loading ? null : _login, child: loading ? CircularProgressIndicator() : Text('Entrar'))
        ]),
      ),
    );
  }
}
