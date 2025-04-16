"""
Script para executar backtesting das estratégias de trading

Este script utiliza o módulo de backtesting para testar as estratégias
implementadas no robô trader com dados históricos.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/home/ubuntu/robo_trader/src')
from testes.backtesting import Backtesting

# Função para gerar dados sintéticos para teste
def gerar_dados_sinteticos(dias=100, volatilidade=0.015, tendencia=0.0005):
    """
    Gera dados sintéticos para teste de backtesting.
    
    Args:
        dias (int): Número de dias a gerar.
        volatilidade (float): Volatilidade diária.
        tendencia (float): Tendência diária (positiva ou negativa).
        
    Returns:
        pandas.DataFrame: DataFrame com dados OHLCV.
    """
    # Gerar datas
    data_final = datetime.now()
    data_inicial = data_final - timedelta(days=dias)
    datas = pd.date_range(start=data_inicial, end=data_final, freq='D')
    
    # Gerar preços de fechamento com caminhada aleatória
    np.random.seed(42)  # Para reprodutibilidade
    retornos = np.random.normal(tendencia, volatilidade, dias)
    precos_close = 100 * (1 + np.cumsum(retornos))
    
    # Gerar preços de abertura, máxima e mínima
    precos_open = precos_close.copy()
    precos_open[1:] = precos_close[:-1]
    precos_open[0] = precos_close[0] * (1 - volatilidade)
    
    precos_high = np.maximum(precos_close, precos_open) * (1 + np.random.uniform(0, volatilidade, dias))
    precos_low = np.minimum(precos_close, precos_open) * (1 - np.random.uniform(0, volatilidade, dias))
    
    # Gerar volume
    volume = np.random.uniform(1000, 10000, dias) * (1 + np.abs(retornos) * 10)
    
    # Criar DataFrame
    df = pd.DataFrame({
        'open': precos_open,
        'high': precos_high,
        'low': precos_low,
        'close': precos_close,
        'volume': volume
    }, index=datas)
    
    return df

# Função para carregar dados reais da API do Yahoo Finance
def carregar_dados_yahoo(symbol, periodo='1y'):
    """
    Carrega dados históricos da API do Yahoo Finance.
    
    Args:
        symbol (str): Símbolo do ativo.
        periodo (str): Período de dados a carregar.
        
    Returns:
        pandas.DataFrame: DataFrame com dados OHLCV.
    """
    try:
        import sys
        sys.path.append('/opt/.manus/.sandbox-runtime')
        from data_api import ApiClient
        
        client = ApiClient()
        dados = client.call_api('YahooFinance/get_stock_chart', query={
            'symbol': symbol,
            'interval': '1d',
            'range': periodo
        })
        
        # Extrair dados do resultado
        if dados and 'chart' in dados and 'result' in dados['chart'] and dados['chart']['result']:
            result = dados['chart']['result'][0]
            timestamps = result['timestamp']
            quote = result['indicators']['quote'][0]
            
            # Criar DataFrame
            df = pd.DataFrame({
                'open': quote['open'],
                'high': quote['high'],
                'low': quote['low'],
                'close': quote['close'],
                'volume': quote['volume']
            }, index=pd.to_datetime([datetime.fromtimestamp(ts) for ts in timestamps]))
            
            # Remover valores NaN
            df = df.dropna()
            
            return df
        else:
            print("Erro ao carregar dados do Yahoo Finance. Usando dados sintéticos.")
            return gerar_dados_sinteticos()
    except Exception as e:
        print(f"Erro ao carregar dados do Yahoo Finance: {e}. Usando dados sintéticos.")
        return gerar_dados_sinteticos()

# Função principal para executar backtesting
def executar_backtesting():
    """
    Executa backtesting de várias estratégias e gera relatórios.
    """
    # Criar diretório para resultados
    os.makedirs('/home/ubuntu/robo_trader/resultados', exist_ok=True)
    
    # Lista de ativos para teste
    ativos = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA']
    
    # Lista de estratégias para teste
    estrategias = [
        {'nome': 'cruzamento_medias', 'params': {'periodo_curto': 9, 'periodo_longo': 21}},
        {'nome': 'rsi', 'params': {'periodo': 14, 'nivel_sobrecomprado': 70, 'nivel_sobrevendido': 30}},
        {'nome': 'macd', 'params': {'periodo_rapido': 12, 'periodo_lento': 26, 'periodo_sinal': 9}},
        {'nome': 'bollinger', 'params': {'periodo': 20, 'desvios': 2}},
        {'nome': 'price_action', 'params': {'fator_sombra': 2.0}},
        {'nome': 'combinada', 'params': {'pesos': {
            'cruzamento_medias': 1.0,
            'rsi': 1.0,
            'macd': 1.0,
            'bollinger': 0.8,
            'pin_bar': 0.8,
            'suporte_resistencia': 0.5
        }}}
    ]
    
    # Parâmetros de gerenciamento de risco
    risco_por_operacao = 1.0  # 1% do capital por operação
    stop_atr = 2.0  # 2x ATR para stop loss
    take_profit_rr = 2.0  # Relação risco/retorno de 1:2
    
    # Resultados consolidados
    resultados_consolidados = []
    
    # Executar backtesting para cada ativo e estratégia
    for ativo in ativos:
        print(f"\nCarregando dados para {ativo}...")
        dados = carregar_dados_yahoo(ativo)
        print(f"Dados carregados: {len(dados)} registros de {dados.index[0]} a {dados.index[-1]}")
        
        for estrategia in estrategias:
            print(f"\nExecutando backtesting de {estrategia['nome']} para {ativo}...")
            
            # Criar instância de backtesting
            backtest = Backtesting(dados, capital_inicial=10000.0, comissao=0.1)
            
            # Executar backtesting
            resultados = backtest.executar_backtest(
                estrategia=estrategia['nome'],
                params=estrategia['params'],
                risco_por_operacao=risco_por_operacao,
                stop_atr=stop_atr,
                take_profit_rr=take_profit_rr
            )
            
            # Plotar resultados
            backtest.plotar_resultados(f"{ativo} - {estrategia['nome']}")
            
            # Gerar relatório
            caminho_relatorio = f"/home/ubuntu/robo_trader/resultados/backtest_{ativo}_{estrategia['nome']}.md"
            backtest.gerar_relatorio(caminho_relatorio)
            
            # Adicionar aos resultados consolidados
            resultados_consolidados.append({
                'ativo': ativo,
                'estrategia': estrategia['nome'],
                'retorno_total': resultados['retorno_total'],
                'win_rate': resultados['win_rate'],
                'profit_factor': resultados['profit_factor'],
                'max_drawdown': resultados['max_drawdown'],
                'sharpe_ratio': resultados['sharpe_ratio'],
                'total_operacoes': resultados['total_operacoes']
            })
            
            print(f"Backtesting concluído. Relatório salvo em {caminho_relatorio}")
    
    # Gerar relatório consolidado
    df_resultados = pd.DataFrame(resultados_consolidados)
    
    # Salvar resultados em CSV
    df_resultados.to_csv('/home/ubuntu/robo_trader/resultados/resultados_consolidados.csv', index=False)
    
    # Gerar relatório em Markdown
    with open('/home/ubuntu/robo_trader/resultados/relatorio_consolidado.md', 'w') as f:
        f.write("# Relatório Consolidado de Backtesting\n\n")
        
        f.write("## Resumo por Estratégia\n\n")
        resumo_estrategia = df_resultados.groupby('estrategia').agg({
            'retorno_total': 'mean',
            'win_rate': 'mean',
            'profit_factor': 'mean',
            'max_drawdown': 'mean',
            'sharpe_ratio': 'mean',
            'total_operacoes': 'sum'
        }).reset_index()
        
        f.write("| Estratégia | Retorno Médio (%) | Win Rate Médio (%) | Profit Factor Médio | Drawdown Máx Médio (%) | Sharpe Ratio Médio | Total Operações |\n")
        f.write("|------------|-------------------|--------------------|--------------------|------------------------|-------------------|----------------|\n")
        
        for _, row in resumo_estrategia.iterrows():
            f.write(f"| {row['estrategia']} | {row['retorno_total']:.2f} | {row['win_rate']:.2f} | {row['profit_factor']:.2f} | {row['max_drawdown']:.2f} | {row['sharpe_ratio']:.2f} | {row['total_operacoes']:.0f} |\n")
        
        f.write("\n## Resumo por Ativo\n\n")
        resumo_ativo = df_resultados.groupby('ativo').agg({
            'retorno_total': 'mean',
            'win_rate': 'mean',
            'profit_factor': 'mean',
            'max_drawdown': 'mean',
            'sharpe_ratio': 'mean',
            'total_operacoes': 'sum'
        }).reset_index()
        
        f.write("| Ativo | Retorno Médio (%) | Win Rate Médio (%) | Profit Factor Médio | Drawdown Máx Médio (%) | Sharpe Ratio Médio | Total Operações |\n")
        f.write("|-------|-------------------|--------------------|--------------------|------------------------|-------------------|----------------|\n")
        
        for _, row in resumo_ativo.iterrows():
            f.write(f"| {row['ativo']} | {row['retorno_total']:.2f} | {row['win_rate']:.2f} | {row['profit_factor']:.2f} | {row['max_drawdown']:.2f} | {row['sharpe_ratio']:.2f} | {row['total_operacoes']:.0f} |\n")
        
        f.write("\n## Resultados Detalhados\n\n")
        f.write("| Ativo | Estratégia | Retorno Total (%) | Win Rate (%) | Profit Factor | Drawdown Máx (%) | Sharpe Ratio | Total Operações |\n")
        f.write("|-------|------------|-------------------|--------------|---------------|------------------|--------------|----------------|\n")
        
        for _, row in df_resultados.iterrows():
            f.write(f"| {row['ativo']} | {row['estrategia']} | {row['retorno_total']:.2f} | {row['win_rate']:.2f} | {row['profit_factor']:.2f} | {row['max_drawdown']:.2f} | {row['sharpe_ratio']:.2f} | {row['total_operacoes']:.0f} |\n")
    
    print("\nBacktesting concluído para todos os ativos e estratégias.")
    print(f"Relatório consolidado salvo em /home/ubuntu/robo_trader/resultados/relatorio_consolidado.md")

if __name__ == "__main__":
    executar_backtesting()
