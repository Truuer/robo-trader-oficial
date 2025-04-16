import 'package:flutter/material.dart';

class AssetSelector extends StatelessWidget {
  final String selectedAsset;
  final Function(String) onChanged;

  const AssetSelector({
    Key? key,
    required this.selectedAsset,
    required this.onChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final assets = ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'MGLU3', 'WEGE3', 'ABEV3'];

    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: selectedAsset,
          icon: Icon(Icons.arrow_drop_down),
          isExpanded: true,
          hint: Text('Selecionar Ativo'),
          items: assets.map((String asset) {
            return DropdownMenuItem<String>(
              value: asset,
              child: Text(asset),
            );
          }).toList(),
          onChanged: (String? newValue) {
            if (newValue != null) {
              onChanged(newValue);
            }
          },
        ),
      ),
    );
  }
}
