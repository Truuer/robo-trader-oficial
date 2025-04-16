import 'package:flutter/material.dart';
import '../../widgets/strategy_config_card.dart';
import '../../widgets/risk_management_form.dart';
import '../../widgets/asset_selection_list.dart';
import '../../widgets/trading_hours_selector.dart';

class SettingsScreen extends StatefulWidget {
  @override
  _SettingsScreenState createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _autoTradeEnabled = true;
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Configurações'),
        actions: [
          IconButton(
            icon: Icon(Icons.save),
            onPressed: () {
              // Salvar configurações
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Configurações salvas com sucesso!'))
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Modo de operação
            Card(
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Modo de Operação',
                      style: Theme.of(context).textTheme.headline2,
                    ),
                    SizedBox(height: 16),
                    SwitchListTile(
                      title: Text('Trading Automático'),
                      subtitle: Text(_autoTradeEnabled 
                        ? 'O robô executará operações automaticamente' 
                        : 'O robô apenas enviará alertas'),
                      value: _autoTradeEnabled,
                      onChanged: (value) {
                        setState(() {
                          _autoTradeEnabled = value;
                        });
                      },
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 16),
            
            // Configuração de estratégias
            Text(
              'Estratégias',
              style: Theme.of(context).textTheme.headline1,
            ),
            SizedBox(height: 8),
            StrategyConfigCard(
              title: 'Cruzamento de Médias Móveis',
              isEnabled: true,
              parameters: {
                'Período Curto': 9,
                'Período Longo': 21,
                'Tipo de Média': 'Exponencial',
              },
              onToggle: (enabled) {
                // Ativar/desativar estratégia
              },
              onEdit: () {
                // Editar parâmetros da estratégia
              },
            ),
            SizedBox(height: 8),
            StrategyConfigCard(
              title: 'RSI',
              isEnabled: true,
              parameters: {
                'Período': 14,
                'Sobrecomprado': 70,
                'Sobrevendido': 30,
              },
              onToggle: (enabled) {
                // Ativar/desativar estratégia
              },
              onEdit: () {
                // Editar parâmetros da estratégia
              },
            ),
            SizedBox(height: 8),
            StrategyConfigCard(
              title: 'Bandas de Bollinger',
              isEnabled: false,
              parameters: {
                'Período': 20,
                'Desvios': 2,
              },
              onToggle: (enabled) {
                // Ativar/desativar estratégia
              },
              onEdit: () {
                // Editar parâmetros da estratégia
              },
            ),
            SizedBox(height: 16),
            
            // Gerenciamento de risco
            Text(
              'Gerenciamento de Risco',
              style: Theme.of(context).textTheme.headline1,
            ),
            SizedBox(height: 8),
            RiskManagementForm(
              riskPerTrade: 1.0,
              maxDailyLoss: 3.0,
              takeProfit: 2.0,
              stopLoss: 1.0,
              trailingStop: true,
              onSave: (values) {
                // Salvar configurações de risco
              },
            ),
            SizedBox(height: 16),
            
            // Seleção de ativos
            Text(
              'Ativos Monitorados',
              style: Theme.of(context).textTheme.headline1,
            ),
            SizedBox(height: 8),
            AssetSelectionList(
              selectedAssets: ['PETR4', 'VALE3', 'ITUB4', 'BBDC4'],
              onChanged: (assets) {
                // Atualizar lista de ativos monitorados
              },
            ),
            SizedBox(height: 16),
            
            // Horários de operação
            Text(
              'Horários de Operação',
              style: Theme.of(context).textTheme.headline1,
            ),
            SizedBox(height: 8),
            TradingHoursSelector(
              startTime: TimeOfDay(hour: 9, minute: 30),
              endTime: TimeOfDay(hour: 16, minute: 30),
              onChanged: (start, end) {
                // Atualizar horários de operação
              },
            ),
            SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}
