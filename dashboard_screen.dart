import 'package:flutter/material.dart';
import '../../widgets/performance_card.dart';
import '../../widgets/active_positions_list.dart';
import '../../widgets/trading_signals_list.dart';
import '../../widgets/daily_summary_card.dart';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () {
              // Atualizar dados do dashboard
            },
          ),
          IconButton(
            icon: Icon(Icons.notifications),
            onPressed: () {
              // Mostrar notificações
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          // Atualizar dados ao puxar para baixo
          await Future.delayed(Duration(seconds: 1));
        },
        child: SingleChildScrollView(
          padding: EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Visão Geral',
                style: Theme.of(context).textTheme.headline1,
              ),
              SizedBox(height: 16),
              
              // Cards de desempenho
              Row(
                children: [
                  Expanded(
                    child: PerformanceCard(
                      title: 'Lucro Hoje',
                      value: 'R$ 1.250,00',
                      isPositive: true,
                      percentChange: 2.5,
                    ),
                  ),
                  SizedBox(width: 16),
                  Expanded(
                    child: PerformanceCard(
                      title: 'Lucro Mensal',
                      value: 'R$ 8.750,00',
                      isPositive: true,
                      percentChange: 12.3,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16),
              
              // Posições ativas
              Text(
                'Posições Ativas',
                style: Theme.of(context).textTheme.headline2,
              ),
              SizedBox(height: 8),
              ActivePositionsList(
                positions: [
                  {
                    'symbol': 'PETR4',
                    'type': 'Compra',
                    'entryPrice': 28.75,
                    'currentPrice': 29.30,
                    'profit': 1.91,
                  },
                  {
                    'symbol': 'VALE3',
                    'type': 'Venda',
                    'entryPrice': 68.40,
                    'currentPrice': 67.85,
                    'profit': 0.80,
                  },
                ],
              ),
              SizedBox(height: 24),
              
              // Sinais de trading
              Text(
                'Sinais Recentes',
                style: Theme.of(context).textTheme.headline2,
              ),
              SizedBox(height: 8),
              TradingSignalsList(
                signals: [
                  {
                    'symbol': 'ITUB4',
                    'type': 'Compra',
                    'strategy': 'Cruzamento de Médias',
                    'time': '10:45',
                    'confidence': 0.85,
                  },
                  {
                    'symbol': 'BBDC4',
                    'type': 'Venda',
                    'strategy': 'RSI Sobrecomprado',
                    'time': '11:20',
                    'confidence': 0.78,
                  },
                  {
                    'symbol': 'MGLU3',
                    'type': 'Compra',
                    'strategy': 'Suporte Rompido',
                    'time': '13:05',
                    'confidence': 0.92,
                  },
                ],
              ),
              SizedBox(height: 24),
              
              // Resumo do dia
              Text(
                'Resumo do Dia',
                style: Theme.of(context).textTheme.headline2,
              ),
              SizedBox(height: 8),
              DailySummaryCard(
                totalTrades: 12,
                winningTrades: 8,
                losingTrades: 4,
                winRate: 66.7,
                profitFactor: 2.3,
              ),
              SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}
