import 'package:flutter/material.dart';
import '../../widgets/trade_history_list.dart';
import '../../widgets/performance_chart.dart';
import '../../widgets/statistics_card.dart';
import '../../widgets/drawdown_chart.dart';

class ReportsScreen extends StatefulWidget {
  @override
  _ReportsScreenState createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  String _selectedPeriod = 'Hoje';
  
  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }
  
  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Relatórios'),
        bottom: TabBar(
          controller: _tabController,
          tabs: [
            Tab(text: 'Desempenho'),
            Tab(text: 'Operações'),
            Tab(text: 'Estatísticas'),
          ],
        ),
        actions: [
          PopupMenuButton<String>(
            onSelected: (value) {
              setState(() {
                _selectedPeriod = value;
              });
            },
            itemBuilder: (context) => [
              PopupMenuItem(value: 'Hoje', child: Text('Hoje')),
              PopupMenuItem(value: 'Semana', child: Text('Esta Semana')),
              PopupMenuItem(value: 'Mês', child: Text('Este Mês')),
              PopupMenuItem(value: 'Ano', child: Text('Este Ano')),
              PopupMenuItem(value: 'Tudo', child: Text('Todo o Período')),
            ],
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  Text(_selectedPeriod),
                  Icon(Icons.arrow_drop_down),
                ],
              ),
            ),
          ),
        ],
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          // Tab de Desempenho
          SingleChildScrollView(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Evolução do Capital',
                  style: Theme.of(context).textTheme.headline2,
                ),
                SizedBox(height: 8),
                Container(
                  height: 250,
                  child: PerformanceChart(
                    period: _selectedPeriod,
                  ),
                ),
                SizedBox(height: 24),
                Text(
                  'Drawdown',
                  style: Theme.of(context).textTheme.headline2,
                ),
                SizedBox(height: 8),
                Container(
                  height: 200,
                  child: DrawdownChart(
                    period: _selectedPeriod,
                  ),
                ),
                SizedBox(height: 24),
                Row(
                  children: [
                    Expanded(
                      child: StatisticsCard(
                        title: 'Lucro Total',
                        value: 'R$ 12.450,00',
                        isPositive: true,
                        icon: Icons.trending_up,
                      ),
                    ),
                    SizedBox(width: 16),
                    Expanded(
                      child: StatisticsCard(
                        title: 'Drawdown Máx',
                        value: '8,2%',
                        isPositive: false,
                        icon: Icons.trending_down,
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: StatisticsCard(
                        title: 'Retorno Mensal',
                        value: '15,3%',
                        isPositive: true,
                        icon: Icons.calendar_today,
                      ),
                    ),
                    SizedBox(width: 16),
                    Expanded(
                      child: StatisticsCard(
                        title: 'Fator de Lucro',
                        value: '2,4',
                        isPositive: true,
                        icon: Icons.assessment,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          
          // Tab de Operações
          TradeHistoryList(
            period: _selectedPeriod,
            trades: [
              {
                'symbol': 'PETR4',
                'type': 'Compra',
                'entryPrice': 28.75,
                'exitPrice': 29.30,
                'profit': 1.91,
                'date': '16/04/2025',
                'time': '10:15',
                'strategy': 'Cruzamento de Médias',
              },
              {
                'symbol': 'VALE3',
                'type': 'Venda',
                'entryPrice': 68.40,
                'exitPrice': 67.85,
                'profit': 0.80,
                'date': '16/04/2025',
                'time': '11:30',
                'strategy': 'RSI Sobrecomprado',
              },
              {
                'symbol': 'ITUB4',
                'type': 'Compra',
                'entryPrice': 32.10,
                'exitPrice': 31.85,
                'profit': -0.78,
                'date': '16/04/2025',
                'time': '13:45',
                'strategy': 'Suporte Rompido',
              },
              {
                'symbol': 'BBDC4',
                'type': 'Venda',
                'entryPrice': 25.30,
                'exitPrice': 25.80,
                'profit': -1.98,
                'date': '16/04/2025',
                'time': '14:20',
                'strategy': 'Bandas de Bollinger',
              },
              {
                'symbol': 'MGLU3',
                'type': 'Compra',
                'entryPrice': 15.40,
                'exitPrice': 15.95,
                'profit': 3.57,
                'date': '16/04/2025',
                'time': '15:10',
                'strategy': 'MACD Crossover',
              },
            ],
          ),
          
          // Tab de Estatísticas
          SingleChildScrollView(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Métricas de Desempenho',
                  style: Theme.of(context).textTheme.headline2,
                ),
                SizedBox(height: 16),
                Card(
                  child: Padding(
                    padding: EdgeInsets.all(16),
                    child: Column(
                      children: [
                        _buildStatRow('Total de Operações', '45'),
                        _buildStatRow('Operações Vencedoras', '32 (71,1%)'),
                        _buildStatRow('Operações Perdedoras', '13 (28,9%)'),
                        _buildStatRow('Melhor Operação', '+5,2%'),
                        _buildStatRow('Pior Operação', '-2,8%'),
                        _buildStatRow('Média de Ganho', '+2,1%'),
                        _buildStatRow('Média de Perda', '-1,5%'),
                        _buildStatRow('Expectativa Matemática', '1,05%'),
                      ],
                    ),
                  ),
                ),
                SizedBox(height: 24),
                
                Text(
                  'Desempenho por Estratégia',
                  style: Theme.of(context).textTheme.headline2,
                ),
                SizedBox(height: 16),
                Card(
                  child: Padding(
                    padding: EdgeInsets.all(16),
                    child: Column(
                      children: [
                        _buildStrategyRow('Cruzamento de Médias', 18, 75.0, 2.8),
                        _buildStrategyRow('RSI', 12, 66.7, 1.9),
                        _buildStrategyRow('Bandas de Bollinger', 8, 62.5, 1.7),
                        _buildStrategyRow('MACD', 7, 85.7, 3.2),
                      ],
                    ),
                  ),
                ),
                SizedBox(height: 24),
                
                Text(
                  'Desempenho por Ativo',
                  style: Theme.of(context).textTheme.headline2,
                ),
                SizedBox(height: 16),
                Card(
                  child: Padding(
                    padding: EdgeInsets.all(16),
                    child: Column(
                      children: [
                        _buildAssetRow('PETR4', 10, 80.0, 'R$ 3.250,00'),
                        _buildAssetRow('VALE3', 8, 62.5, 'R$ 1.850,00'),
                        _buildAssetRow('ITUB4', 7, 71.4, 'R$ 2.100,00'),
                        _buildAssetRow('BBDC4', 6, 66.7, 'R$ 1.450,00'),
                        _buildAssetRow('MGLU3', 5, 80.0, 'R$ 2.800,00'),
                      ],
                    ),
                  ),
                ),
                SizedBox(height: 16),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildStatRow(String label, String value) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: TextStyle(fontSize: 16)),
          Text(value, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
  
  Widget _buildStrategyRow(String strategy, int trades, double winRate, double profitFactor) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(strategy, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          SizedBox(height: 4),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Operações: $trades'),
              Text('Win Rate: ${winRate.toStringAsFixed(1)}%'),
              Text('Profit Factor: ${profitFactor.toStringAsFixed(1)}'),
            ],
          ),
          SizedBox(height: 8),
          LinearProgressIndicator(
            value: winRate / 100,
            backgroundColor: Colors.red[100],
            valueColor: AlwaysStoppedAnimation<Color>(Colors.green),
          ),
          SizedBox(height: 8),
          Divider(),
        ],
      ),
    );
  }
  
  Widget _buildAssetRow(String asset, int trades, double winRate, String profit) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(asset, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          SizedBox(height: 4),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Operações: $trades'),
              Text('Win Rate: ${winRate.toStringAsFixed(1)}%'),
              Text('Lucro: $profit'),
            ],
          ),
          SizedBox(height: 8),
          Divider(),
        ],
      ),
    );
  }
}
