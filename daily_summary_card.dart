import 'package:flutter/material.dart';

class DailySummaryCard extends StatelessWidget {
  final int totalTrades;
  final int winningTrades;
  final int losingTrades;
  final double winRate;
  final double profitFactor;

  const DailySummaryCard({
    Key? key,
    required this.totalTrades,
    required this.winningTrades,
    required this.losingTrades,
    required this.winRate,
    required this.profitFactor,
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
                _buildSummaryItem(
                  context,
                  'Total',
                  totalTrades.toString(),
                  Icons.swap_horiz,
                  Colors.blue,
                ),
                _buildSummaryItem(
                  context,
                  'Ganhos',
                  winningTrades.toString(),
                  Icons.check_circle,
                  Colors.green,
                ),
                _buildSummaryItem(
                  context,
                  'Perdas',
                  losingTrades.toString(),
                  Icons.cancel,
                  Colors.red,
                ),
              ],
            ),
            SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildSummaryItem(
                  context,
                  'Win Rate',
                  '${winRate.toStringAsFixed(1)}%',
                  Icons.pie_chart,
                  Colors.purple,
                ),
                _buildSummaryItem(
                  context,
                  'Profit Factor',
                  profitFactor.toStringAsFixed(1),
                  Icons.trending_up,
                  Colors.orange,
                ),
              ],
            ),
            SizedBox(height: 16),
            Text(
              'Taxa de Acerto',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            LinearProgressIndicator(
              value: winRate / 100,
              backgroundColor: Colors.red[100],
              valueColor: AlwaysStoppedAnimation<Color>(Colors.green),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSummaryItem(
    BuildContext context,
    String label,
    String value,
    IconData icon,
    Color color,
  ) {
    return Column(
      children: [
        Icon(icon, color: color, size: 24),
        SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(fontSize: 12, color: Colors.grey[600]),
        ),
        SizedBox(height: 4),
        Text(
          value,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }
}
