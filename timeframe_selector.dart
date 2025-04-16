import 'package:flutter/material.dart';

class TimeframeSelector extends StatelessWidget {
  final String selectedTimeframe;
  final Function(String) onChanged;

  const TimeframeSelector({
    Key? key,
    required this.selectedTimeframe,
    required this.onChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d'];

    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 0),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: selectedTimeframe,
          icon: Icon(Icons.arrow_drop_down),
          isDense: true,
          hint: Text('Timeframe'),
          items: timeframes.map((String timeframe) {
            return DropdownMenuItem<String>(
              value: timeframe,
              child: Text(timeframe),
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
