import 'package:flutter/material.dart';

class RiskManagementForm extends StatefulWidget {
  final double riskPerTrade;
  final double maxDailyLoss;
  final double takeProfit;
  final double stopLoss;
  final bool trailingStop;
  final Function(Map<String, dynamic>) onSave;

  const RiskManagementForm({
    Key? key,
    required this.riskPerTrade,
    required this.maxDailyLoss,
    required this.takeProfit,
    required this.stopLoss,
    required this.trailingStop,
    required this.onSave,
  }) : super(key: key);

  @override
  _RiskManagementFormState createState() => _RiskManagementFormState();
}

class _RiskManagementFormState extends State<RiskManagementForm> {
  late double _riskPerTrade;
  late double _maxDailyLoss;
  late double _takeProfit;
  late double _stopLoss;
  late bool _trailingStop;

  @override
  void initState() {
    super.initState();
    _riskPerTrade = widget.riskPerTrade;
    _maxDailyLoss = widget.maxDailyLoss;
    _takeProfit = widget.takeProfit;
    _stopLoss = widget.stopLoss;
    _trailingStop = widget.trailingStop;
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSlider(
              label: 'Risco por Operação (%)',
              value: _riskPerTrade,
              min: 0.1,
              max: 5.0,
              divisions: 49,
              onChanged: (value) {
                setState(() {
                  _riskPerTrade = value;
                });
              },
            ),
            SizedBox(height: 16),
            _buildSlider(
              label: 'Perda Máxima Diária (%)',
              value: _maxDailyLoss,
              min: 1.0,
              max: 10.0,
              divisions: 18,
              onChanged: (value) {
                setState(() {
                  _maxDailyLoss = value;
                });
              },
            ),
            SizedBox(height: 16),
            _buildSlider(
              label: 'Take Profit (R:R)',
              value: _takeProfit,
              min: 1.0,
              max: 5.0,
              divisions: 8,
              onChanged: (value) {
                setState(() {
                  _takeProfit = value;
                });
              },
            ),
            SizedBox(height: 16),
            _buildSlider(
              label: 'Stop Loss (ATR)',
              value: _stopLoss,
              min: 0.5,
              max: 3.0,
              divisions: 5,
              onChanged: (value) {
                setState(() {
                  _stopLoss = value;
                });
              },
            ),
            SizedBox(height: 16),
            SwitchListTile(
              title: Text('Trailing Stop'),
              subtitle: Text('Ajusta o stop loss automaticamente conforme o preço se move a favor'),
              value: _trailingStop,
              onChanged: (value) {
                setState(() {
                  _trailingStop = value;
                });
              },
            ),
            SizedBox(height: 16),
            Align(
              alignment: Alignment.centerRight,
              child: ElevatedButton(
                onPressed: () {
                  widget.onSave({
                    'riskPerTrade': _riskPerTrade,
                    'maxDailyLoss': _maxDailyLoss,
                    'takeProfit': _takeProfit,
                    'stopLoss': _stopLoss,
                    'trailingStop': _trailingStop,
                  });
                },
                child: Text('Salvar'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSlider({
    required String label,
    required double value,
    required double min,
    required double max,
    required int divisions,
    required Function(double) onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label),
            Text(
              value.toStringAsFixed(1),
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          divisions: divisions,
          label: value.toStringAsFixed(1),
          onChanged: onChanged,
        ),
      ],
    );
  }
}
