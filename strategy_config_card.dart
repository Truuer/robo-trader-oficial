import 'package:flutter/material.dart';

class StrategyConfigCard extends StatelessWidget {
  final String title;
  final bool isEnabled;
  final Map<String, dynamic> parameters;
  final Function(bool) onToggle;
  final VoidCallback onEdit;

  const StrategyConfigCard({
    Key? key,
    required this.title,
    required this.isEnabled,
    required this.parameters,
    required this.onToggle,
    required this.onEdit,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                Switch(
                  value: isEnabled,
                  onChanged: onToggle,
                  activeColor: Theme.of(context).primaryColor,
                ),
              ],
            ),
            SizedBox(height: 8),
            Divider(),
            SizedBox(height: 8),
            ...parameters.entries.map((entry) {
              return Padding(
                padding: EdgeInsets.only(bottom: 8.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(entry.key),
                    Text(
                      entry.value.toString(),
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              );
            }).toList(),
            SizedBox(height: 8),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                icon: Icon(Icons.edit),
                label: Text('Editar'),
                onPressed: isEnabled ? onEdit : null,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
