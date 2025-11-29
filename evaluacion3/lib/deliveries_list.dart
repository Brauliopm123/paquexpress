import 'package:flutter/material.dart';
import 'api_services.dart';

class DeliveriesList extends StatefulWidget {
  @override _DeliveriesListState createState() => _DeliveriesListState();
}

class _DeliveriesListState extends State<DeliveriesList> {
  final api = ApiService();
  List<dynamic> items = [];
  bool loading = true;

  @override void initState() {
    super.initState();
    _load();
  }

  void _load() async {
    try {
      final list = await api.getAssigned();
      setState(() { items = list; loading = false; });
    } catch (e) {
      setState(() => loading = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error cargando entregas")));
    }
  }

  @override Widget build(BuildContext context) {
    if (loading) return Scaffold(appBar: AppBar(title: Text('Entregas')), body: Center(child: CircularProgressIndicator()));
    return Scaffold(
      appBar: AppBar(title: Text('Entregas asignadas')),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (_, i) {
          final e = items[i];
          final paquete = e['paquete'];
          return ListTile(
            title: Text(paquete['tracking_id'] ?? 'Paquete'),
            subtitle: Text(paquete['direccion'] ?? ''),
            trailing: Text(e['estado'] ?? ''),
            onTap: () => Navigator.pushNamed(context, '/delivery_detail', arguments: e),
          );
        },
      ),
    );
  }
}