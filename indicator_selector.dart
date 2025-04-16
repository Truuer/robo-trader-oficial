import 'package:flutter/material.dart';

class IndicatorSelector extends StatefulWidget {
  final List<String> selectedIndicators;
  final Function(List<String>) onChanged;

  const IndicatorSelector({
    Key? key,
    required this.selectedIndicators,
    required this.onChanged,
  }) : super(key: key);

  @override
  _IndicatorSelectorState createState() => _IndicatorSelectorState();
}

class _IndicatorSelectorState extends State<IndicatorSelector> {
  final List<String> availableIndicators = [
    'SMA', 'EMA', 'MACD', 'RSI', 'Bollinger', 'Estocástico', 'ATR', 'Volume'
  ];

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Indicadores',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: availableIndicators.map((indicator) {
              final isSelected = widget.selectedIndicators.contains(indicator);
              return FilterChip(
                label: Text(indicator),
                selected: isSelected,
                onSelected: (selected) {
                  List<String> newSelection = List.from(widget.selectedIndicators);
                  if (selected) {
                    if (!newSelection.contains(indicator)) {
                      newSelection.add(indicator);
                    }
                  } else {
                    newSelection.remove(indicator);
                  }
                  widget.onChanged(newSelection);
                },
                selectedColor: Theme.of(context).primaryColor.withOpacity(0.2),
                checkmarkColor: Theme.of(context).primaryColor,
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}
