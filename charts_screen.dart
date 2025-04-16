import 'package:flutter/material.dart';
import '../../widgets/chart_container.dart';
import '../../widgets/indicator_selector.dart';
import '../../widgets/timeframe_selector.dart';
import '../../widgets/asset_selector.dart';

class ChartsScreen extends StatefulWidget {
  @override
  _ChartsScreenState createState() => _ChartsScreenState();
}

class _ChartsScreenState extends State<ChartsScreen> {
  String _selectedAsset = 'PETR4';
  String _selectedTimeframe = '5m';
  List<String> _selectedIndicators = ['SMA', 'RSI'];
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Gráficos'),
        actions: [
          IconButton(
            icon: Icon(Icons.save),
            onPressed: () {
              // Salvar configuração do gráfico
            },
          ),
          IconButton(
            icon: Icon(Icons.fullscreen),
            onPressed: () {
              // Expandir gráfico em tela cheia
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Seletores de ativo e timeframe
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: AssetSelector(
                    selectedAsset: _selectedAsset,
                    onChanged: (value) {
                      setState(() {
                        _selectedAsset = value;
                      });
                    },
                  ),
                ),
                SizedBox(width: 8),
                TimeframeSelector(
                  selectedTimeframe: _selectedTimeframe,
                  onChanged: (value) {
                    setState(() {
                      _selectedTimeframe = value;
                    });
                  },
                ),
              ],
            ),
          ),
          
          // Container do gráfico principal
          Expanded(
            flex: 3,
            child: ChartContainer(
              asset: _selectedAsset,
              timeframe: _selectedTimeframe,
              indicators: _selectedIndicators,
            ),
          ),
          
          // Seletor de indicadores
          Padding(
            padding: EdgeInsets.all(8.0),
            child: IndicatorSelector(
              selectedIndicators: _selectedIndicators,
              onChanged: (indicators) {
                setState(() {
                  _selectedIndicators = indicators;
                });
              },
            ),
          ),
          
          // Painel de informações do ativo
          Container(
            padding: EdgeInsets.all(16),
            color: Theme.of(context).cardColor,
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      _selectedAsset,
                      style: Theme.of(context).textTheme.headline3,
                    ),
                    Text(
                      'R\$ 29,45',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.green,
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Variação: +1,25%'),
                    Text('Volume: 15.2M'),
                    Text('Máx: R\$ 29,78'),
                    Text('Mín: R\$ 28,90'),
                  ],
                ),
                SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton.icon(
                      icon: Icon(Icons.trending_up),
                      label: Text('COMPRAR'),
                      style: ElevatedButton.styleFrom(
                        primary: Colors.green,
                      ),
                      onPressed: () {
                        // Executar ordem de compra
                      },
                    ),
                    ElevatedButton.icon(
                      icon: Icon(Icons.trending_down),
                      label: Text('VENDER'),
                      style: ElevatedButton.styleFrom(
                        primary: Colors.red,
                      ),
                      onPressed: () {
                        // Executar ordem de venda
                      },
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
