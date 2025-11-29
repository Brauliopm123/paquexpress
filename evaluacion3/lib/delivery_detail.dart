import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:geolocator/geolocator.dart';
import '/api_services.dart';

class DeliveryDetail extends StatefulWidget {
  // ignore: library_private_types_in_public_api
  @override _DeliveryDetailState createState() => _DeliveryDetailState();
}

class _DeliveryDetailState extends State<DeliveryDetail> {
  final api = ApiService();
  XFile? _image;
  bool sending = false;

  Future<void> _takePhoto() async {
    final picker = ImagePicker();
    final img = await picker.pickImage(source: ImageSource.camera, imageQuality: 70);
    if (img != null) setState(() => _image = img);
  }

  Future<Position> _getPosition() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) throw Exception('GPS desactivado');
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) permission = await Geolocator.requestPermission();
    if (permission == LocationPermission.deniedForever || permission == LocationPermission.denied) throw Exception('Permiso denegado');
    return await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
  }

  _send(int entregaId) async {
    if (_image == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Toma la foto primero")));
      return;
    }
    setState(() => sending = true);
    try {
      final pos = await _getPosition();
      final ok = await api.deliver(entregaId, _image!.path, pos.latitude, pos.longitude);
      if (ok) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Entrega registrada")));
        Navigator.pop(context);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error al subir entrega")));
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: ${e.toString()}")));
    } finally {
      setState(() => sending = false);
    }
  }

  @override Widget build(BuildContext context) {
    final Map e = ModalRoute.of(context)!.settings.arguments as Map;
    final paquete = e['paquete'];
    return Scaffold(
      appBar: AppBar(title: Text(paquete['tracking_id'] ?? 'Detalle')),
      body: Padding(
        padding: EdgeInsets.all(12),
        child: Column(
          children: [
            Text(paquete['direccion'] ?? ''),
            SizedBox(height: 12),
            _image == null ? Placeholder(fallbackHeight: 180) : Image.file(File(_image!.path), height: 180),
            SizedBox(height: 12),
            ElevatedButton.icon(onPressed: _takePhoto, icon: Icon(Icons.camera_alt), label: Text('Tomar foto')),
            SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: sending ? null : () => _send(e['id']),
              icon: sending ? CircularProgressIndicator() : Icon(Icons.check),
              label: Text('Paquete entregado'),
            )
          ],
        ),
      ),
    );
  }
}