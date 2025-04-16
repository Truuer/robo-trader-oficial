import 'package:flutter/material.dart';

class TradingSignalsList extends StatelessWidget {
  final List<Map<String, dynamic>> signals;

  const TradingSignalsList({
    Key? key,
    required this.signals,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListView.separated(
        shrinkWrap: true,
        physics: NeverScrollableScrollPhysics(),
        itemCount: signals.length,
        separatorBuilder: (context, index) => Divider(),
        itemBuilder: (context, index) {
          final signal = signals[index];
          
          return ListTile(
            leading: CircleAvatar(
              backgroundColor: signal['type'] == 'Compra' ? Colors.green[100] : Colors.red[100],
              child: Icon(
                signal['type'] == 'Compra' ? Icons.trending_up : Icons.trending_down,
                color: signal['type'] == 'Compra' ? Colors.green : Colors.red,
              ),
            ),
            title: Row(
              children: [
                Text(
                  signal['symbol'],
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                SizedBox(width: 8),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color: signal['type'] == 'Compra' ? Colors.green[50] : Colors.red[50],
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    signal['type'],
                    style: TextStyle(
                      fontSize: 12,
                      color: signal['type'] == 'Compra' ? Colors.green : Colors.red,
                    ),
                  ),
                ),
              ],
            ),
            subtitle: Text(
              signal['strategy'],
              style: TextStyle(fontSize: 12),
            ),
            trailing: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  signal['time'],
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                ),
                SizedBox(height: 4),
                _buildConfidenceIndicator(signal['confidence']),
              ],
            ),
            onTap: () {
              // Mostrar detalhes do sinal
            },
          );
        },
      ),
    );
  }
  
  Widget _buildConfidenceIndicator(double confidence) {
    Color color;
    if (confidence >= 0.8) {
      color = Colors.green;
    } else if (confidence >= 0.6) {
      color = Colors.orange;
    } else {
      color = Colors.red;
    }
    
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          'Confiança: ',
          style: TextStyle(fontSize: 12),
        ),
        Container(
          width: 50,
          height: 6,
          decoration: BoxDecoration(
            color: Colors.grey[300],
            borderRadius: BorderRadius.circular(3),
          ),
          child: FractionallySizedBox(
            alignment: Alignment.centerLeft,
            widthFactor: confidence,
            child: Container(
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
