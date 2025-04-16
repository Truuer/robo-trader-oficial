"""
Script para executar testes de paper trading do robô trader

Este script utiliza o módulo de paper trading para simular operações
em tempo real com dados de mercado.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
import os
import time

sys.path.append('/home/ubuntu/robo_trader/src')
from testes.backtesting import PaperTrading
from analise_tecnica.indicadores import IndicadoresTecnicos
from analise_tecnica.estrategias import EstrategiasTrading

# Função para gerar dados simulados em tempo real
def gerar_dados_tempo_real(ativo, intervalo_segundos=5, total_iteracoes=100):
    """
    Gera dados simulados em tempo real para teste de paper trading.
    
    Args:
        ativo (str): Nome do ativo.
        intervalo_segundos (int): Intervalo entre atualizações em segundos.
        total_iteracoes (int): Número total de iterações.
        
    Yields:
        tuple: (timestamp, dados) onde dados é um dicionário com preços.
    """
    # Gerar preço inicial
    np.random.seed(int(time.time()))
    preco_base = 100.0
    volatilidade = 0.002
    
    # Histórico para cálculo de indicadores
    historico = {
        'timestamp': [],
        'open': [],
        'high': [],
        'low': [],
        'close': [],
        'volume': []
    }
    
    for i in range(total_iteracoes):
        timestamp = datetime.now()
        
        # Gerar variação de preço
        variacao = np.random.normal(0, volatilidade)
        
        # Adicionar tendência baseada no índice da iteração
        if i < total_iteracoes / 3:
            # Tendência de alta no início
            tendencia = 0.0005
        elif i < 2 * total_iteracoes / 3:
            # Tendência de baixa no meio
            tendencia = -0.0005
        else:
            # Tendência de alta no final
            tendencia = 0.0003
        
        # Calcular preços
        preco_base *= (1 + variacao + tendencia)
        preco_open = preco_base * (1 + np.random.uniform(-volatilidade/2, volatilidade/2))
        preco_high = max(preco_open, preco_base) * (1 + np.random.uniform(0, volatilidade))
        preco_low = min(preco_open, preco_base) * (1 - np.random.uniform(0, volatilidade))
        preco_close = preco_base
        volume = np.random.uniform(1000, 10000) * (1 + np.abs(variacao) * 10)
        
        # Atualizar histórico
        historico['timestamp'].append(timestamp)
        historico['open'].append(preco_open)
        historico['high'].append(preco_high)
        historico['low'].append(preco_low)
        historico['close'].append(preco_close)
        historico['volume'].append(volume)
        
        # Limitar histórico para cálculo de indicadores
        max_historico = 100
        if len(historico['timestamp']) > max_historico:
            for key in historico:
                historico[key] = historico[key][-max_historico:]
        
        # Criar dados para retorno
        dados = {
            ativo: {
                'open': preco_open,
                'high': preco_high,
                'low': preco_low,
                'close': preco_close,
                'volume': volume
            }
        }
        
        # Calcular indicadores se houver dados suficientes
        if len(historico['close']) >= 26:  # Mínimo para MACD
            # Converter para Series para cálculo de indicadores
            close_series = pd.Series(historico['close'])
            high_series = pd.Series(historico['high'])
            low_series = pd.Series(historico['low'])
            open_series = pd.Series(historico['open'])
            
            # Calcular indicadores
            dados[ativo]['indicadores'] = {
                'sma_9': IndicadoresTecnicos.sma(close_series, 9).iloc[-1],
                'sma_21': IndicadoresTecnicos.sma(close_series, 21).iloc[-1],
                'rsi_14': IndicadoresTecnicos.rsi(close_series, 14).iloc[-1],
                'atr_14': IndicadoresTecnicos.atr(high_series, low_series, close_series, 14).iloc[-1]
            }
            
            # Calcular sinais
            dados[ativo]['sinais'] = {
                'cruzamento_medias': EstrategiasTrading.cruzamento_medias_moveis(close_series, 9, 21).iloc[-1],
                'rsi': EstrategiasTrading.rsi_sobrecomprado_sobrevendido(close_series, 14, 70, 30).iloc[-1],
                'macd': EstrategiasTrading.macd_crossover(close_series, 12, 26, 9).iloc[-1],
                'bollinger': EstrategiasTrading.bollinger_bands_reversal(close_series, 20, 2).iloc[-1]
            }
            
            # Calcular sinal combinado
            pesos = {
                'cruzamento_medias': 1.0,
                'rsi': 1.0,
                'macd': 1.0,
                'bollinger': 0.8,
                'pin_bar': 0.0,  # Não calculado neste exemplo
                'suporte_resistencia': 0.0  # Não calculado neste exemplo
            }
            
            dados[ativo]['sinais']['combinado'] = EstrategiasTrading.estrategia_combinada(
                open_series, high_series, low_series, close_series, pesos
            ).iloc[-1]
        
        yield timestamp, dados
        
        # Aguardar intervalo
        time.sleep(intervalo_segundos)

# Função principal para executar paper trading
def executar_paper_trading(duracao_minutos=30, intervalo_segundos=5):
    """
    Executa simulação de paper trading.
    
    Args:
        duracao_minutos (int): Duração da simulação em minutos.
        intervalo_segundos (int): Intervalo entre atualizações em segundos.
    """
    # Criar diretório para resultados
    os.makedirs('/home/ubuntu/robo_trader/resultados', exist_ok=True)
    
    # Lista de ativos para teste
    ativos = ['PETR4', 'VALE3', 'ITUB4', 'BBDC4']
    
    # Inicializar ambiente de paper trading
    paper_trading = PaperTrading(capital_inicial=10000.0, comissao=0.1)
    
    # Parâmetros de gerenciamento de risco
    risco_por_operacao = 1.0  # 1% do capital por operação
    stop_atr = 2.0  # 2x ATR para stop loss
    take_profit_rr = 2.0  # Relação risco/retorno de 1:2
    
    # Calcular número total de iterações
    total_iteracoes = (duracao_minutos * 60) // intervalo_segundos
    
    print(f"Iniciando simulação de paper trading para {len(ativos)} ativos...")
    print(f"Duração: {duracao_minutos} minutos, Intervalo: {intervalo_segundos} segundos")
    print(f"Capital inicial: R$ {paper_trading.capital_inicial:.2f}")
    
    # Executar simulação para cada ativo
    for ativo in ativos:
        print(f"\nIniciando simulação para {ativo}...")
        
        # Gerar dados em tempo real
        for i, (timestamp, dados) in enumerate(gerar_dados_tempo_real(ativo, intervalo_segundos, total_iteracoes)):
            # Exibir progresso
            if i % 10 == 0:
                print(f"Iteração {i+1}/{total_iteracoes} - {timestamp}")
                print(f"Preço: {dados[ativo]['close']:.2f}, Capital: R$ {paper_trading.capital_atual:.2f}")
            
            # Atualizar preços e verificar stops
            operacoes = paper_trading.atualizar_precos(dados, timestamp)
            
            # Processar operações realizadas
            for op in operacoes:
                print(f"Operação realizada: {op['acao']} {op['symbol']} a {op['preco_saida']:.2f}, Resultado: {op['resultado_percentual']:.2f}%")
            
            # Verificar se há indicadores calculados
            if 'indicadores' in dados[ativo] and 'sinais' in dados[ativo]:
                # Obter sinal da estratégia combinada
                sinal = dados[ativo]['sinais']['combinado']
                
                # Processar sinal
                if sinal != 0:  # Se houver sinal (1 para compra, -1 para venda)
                    estrategia = 'Combinada'
                    confianca = 0.8  # Confiança fixa para este exemplo
                    
                    # Processar sinal
                    resultado = paper_trading.processar_sinal(
                        ativo, sinal, dados[ativo]['close'], timestamp, estrategia, confianca,
                        risco_por_operacao, stop_atr, take_profit_rr, dados[ativo]['indicadores']['atr_14']
                    )
                    
                    # Exibir resultado
                    if resultado['acao'] != 'Nenhuma':
                        print(f"Sinal processado: {resultado['acao']} {ativo} a {dados[ativo]['close']:.2f}")
    
    # Gerar relatório final
    caminho_relatorio = f"/home/ubuntu/robo_trader/resultados/paper_trading_relatorio.md"
    paper_trading.gerar_relatorio(caminho_relatorio)
    
    print("\nSimulação de paper trading concluída.")
    print(f"Capital final: R$ {paper_trading.capital_atual:.2f}")
    print(f"Retorno total: {((paper_trading.capital_atual / paper_trading.capital_inicial) - 1) * 100:.2f}%")
    print(f"Total de operações: {len(paper_trading.historico_operacoes)}")
    print(f"Relatório salvo em {caminho_relatorio}")

if __name__ == "__main__":
    # Executar paper trading por 10 minutos com atualizações a cada 2 segundos
    executar_paper_trading(duracao_minutos=10, intervalo_segundos=2)
