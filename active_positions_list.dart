import 'package:flutter/material.dart';

class ActivePositionsList extends StatelessWidget {
  final List<Map<String, dynamic>> positions;

  const ActivePositionsList({
    Key? key,
    required this.positions,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListView.separated(
        shrinkWrap: true,
        physics: NeverScrollableScrollPhysics(),
        itemCount: positions.length,
        separatorBuilder: (context, index) => Divider(),
        itemBuilder: (context, index) {
          final position = positions[index];
          final isProfit = position['profit'] > 0;
          
          return ListTile(
            leading: CircleAvatar(
              backgroundColor: position['type'] == 'Compra' ? Colors.green[100] : Colors.red[100],
              child: Icon(
                position['type'] == 'Compra' ? Icons.trending_up : Icons.trending_down,
                color: position['type'] == 'Compra' ? Colors.green : Colors.red,
              ),
            ),
            title: Row(
              children: [
                Text(
                  position['symbol'],
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                SizedBox(width: 8),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color: position['type'] == 'Compra' ? Colors.green[50] : Colors.red[50],
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    position['type'],
                    style: TextStyle(
                      fontSize: 12,
                      color: position['type'] == 'Compra' ? Colors.green : Colors.red,
                    ),
                  ),
                ),
              ],
            ),
            subtitle: Text(
              'Entrada: R\$ ${position['entryPrice'].toStringAsFixed(2)}',
            ),
            trailing: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  'R\$ ${position['currentPrice'].toStringAsFixed(2)}',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                Text(
                  '${isProfit ? '+' : ''}${position['profit'].toStringAsFixed(2)}%',
                  style: TextStyle(
                    color: isProfit ? Colors.green : Colors.red,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            onTap: () {
              // Mostrar detalhes da posição
            },
          );
        },
      ),
    );
  }
}
