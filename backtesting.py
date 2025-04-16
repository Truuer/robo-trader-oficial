"""
Módulo de Testes para o Robô Trader

Este módulo implementa funções para testar as estratégias de trading
e avaliar o desempenho do robô em diferentes condições de mercado.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
sys.path.append('/home/ubuntu/robo_trader/src')
from analise_tecnica.indicadores import IndicadoresTecnicos
from analise_tecnica.price_action import PriceAction
from analise_tecnica.estrategias import EstrategiasTrading
from analise_tecnica.gerenciamento_risco import GerenciamentoRisco

class Backtesting:
    """
    Classe para realizar backtesting das estratégias de trading.
    """
    
    def __init__(self, dados_historicos, capital_inicial=10000.0, comissao=0.0):
        """
        Inicializa o ambiente de backtesting.
        
        Args:
            dados_historicos (pandas.DataFrame): DataFrame com dados históricos (OHLCV).
            capital_inicial (float): Capital inicial para simulação.
            comissao (float): Valor da comissão por operação (percentual).
        """
        self.dados = dados_historicos
        self.capital_inicial = capital_inicial
        self.comissao = comissao
        self.resultados = None
    
    def executar_backtest(self, estrategia, params=None, risco_por_operacao=1.0, stop_atr=2.0, take_profit_rr=2.0):
        """
        Executa o backtesting de uma estratégia específica.
        
        Args:
            estrategia (str): Nome da estratégia a ser testada.
            params (dict): Parâmetros específicos da estratégia.
            risco_por_operacao (float): Percentual do capital a ser arriscado por operação.
            stop_atr (float): Multiplicador do ATR para stop loss.
            take_profit_rr (float): Relação risco/retorno para take profit.
            
        Returns:
            dict: Resultados do backtesting.
        """
        # Preparar dados
        dados_open = self.dados['open']
        dados_high = self.dados['high']
        dados_low = self.dados['low']
        dados_close = self.dados['close']
        dados_volume = self.dados['volume']
        
        # Gerar sinais com base na estratégia selecionada
        sinais = self._gerar_sinais(estrategia, dados_open, dados_high, dados_low, dados_close, params)
        
        # Inicializar variáveis para simulação
        capital = self.capital_inicial
        posicao = 0  # 0: sem posição, 1: comprado, -1: vendido
        preco_entrada = 0
        stop_loss = 0
        take_profit = 0
        
        # Registros para análise
        capital_historico = [capital]
        posicoes = []
        operacoes = []
        
        # Simular operações
        for i in range(1, len(sinais)):
            # Verificar se há posição aberta
            if posicao != 0:
                # Verificar se atingiu stop loss
                if (posicao == 1 and dados_low.iloc[i] <= stop_loss) or \
                   (posicao == -1 and dados_high.iloc[i] >= stop_loss):
                    # Fechar posição com stop loss
                    preco_saida = stop_loss
                    resultado = posicao * (preco_saida - preco_entrada) / preco_entrada * 100
                    resultado_liquido = resultado - self.comissao
                    
                    # Atualizar capital
                    capital = capital * (1 + (resultado_liquido / 100) * (risco_por_operacao / 100) * 100)
                    
                    # Registrar operação
                    operacoes.append({
                        'data_entrada': self.dados.index[i-1],
                        'data_saida': self.dados.index[i],
                        'tipo': 'Compra' if posicao == 1 else 'Venda',
                        'preco_entrada': preco_entrada,
                        'preco_saida': preco_saida,
                        'resultado': resultado_liquido,
                        'motivo_saida': 'Stop Loss'
                    })
                    
                    # Resetar posição
                    posicao = 0
                
                # Verificar se atingiu take profit
                elif (posicao == 1 and dados_high.iloc[i] >= take_profit) or \
                     (posicao == -1 and dados_low.iloc[i] <= take_profit):
                    # Fechar posição com take profit
                    preco_saida = take_profit
                    resultado = posicao * (preco_saida - preco_entrada) / preco_entrada * 100
                    resultado_liquido = resultado - self.comissao
                    
                    # Atualizar capital
                    capital = capital * (1 + (resultado_liquido / 100) * (risco_por_operacao / 100) * 100)
                    
                    # Registrar operação
                    operacoes.append({
                        'data_entrada': self.dados.index[i-1],
                        'data_saida': self.dados.index[i],
                        'tipo': 'Compra' if posicao == 1 else 'Venda',
                        'preco_entrada': preco_entrada,
                        'preco_saida': preco_saida,
                        'resultado': resultado_liquido,
                        'motivo_saida': 'Take Profit'
                    })
                    
                    # Resetar posição
                    posicao = 0
                
                # Verificar se há sinal contrário
                elif (posicao == 1 and sinais.iloc[i] == -1) or \
                     (posicao == -1 and sinais.iloc[i] == 1):
                    # Fechar posição com sinal contrário
                    preco_saida = dados_open.iloc[i]
                    resultado = posicao * (preco_saida - preco_entrada) / preco_entrada * 100
                    resultado_liquido = resultado - self.comissao
                    
                    # Atualizar capital
                    capital = capital * (1 + (resultado_liquido / 100) * (risco_por_operacao / 100) * 100)
                    
                    # Registrar operação
                    operacoes.append({
                        'data_entrada': self.dados.index[i-1],
                        'data_saida': self.dados.index[i],
                        'tipo': 'Compra' if posicao == 1 else 'Venda',
                        'preco_entrada': preco_entrada,
                        'preco_saida': preco_saida,
                        'resultado': resultado_liquido,
                        'motivo_saida': 'Sinal Contrário'
                    })
                    
                    # Resetar posição
                    posicao = 0
            
            # Verificar se há sinal para abrir nova posição
            if posicao == 0 and sinais.iloc[i] != 0:
                posicao = sinais.iloc[i]  # 1 para compra, -1 para venda
                preco_entrada = dados_open.iloc[i]
                
                # Calcular stop loss e take profit
                atr = IndicadoresTecnicos.atr(dados_high, dados_low, dados_close, 14).iloc[i]
                
                if posicao == 1:  # Compra
                    stop_loss = preco_entrada - (stop_atr * atr)
                    take_profit = preco_entrada + (stop_atr * atr * take_profit_rr)
                else:  # Venda
                    stop_loss = preco_entrada + (stop_atr * atr)
                    take_profit = preco_entrada - (stop_atr * atr * take_profit_rr)
            
            # Registrar capital e posição
            capital_historico.append(capital)
            posicoes.append(posicao)
        
        # Calcular métricas de desempenho
        resultados = self._calcular_metricas(capital_historico, operacoes)
        self.resultados = resultados
        
        return resultados
    
    def _gerar_sinais(self, estrategia, dados_open, dados_high, dados_low, dados_close, params=None):
        """
        Gera sinais de trading com base na estratégia selecionada.
        
        Args:
            estrategia (str): Nome da estratégia.
            dados_open (pandas.Series): Série de preços de abertura.
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            params (dict): Parâmetros específicos da estratégia.
            
        Returns:
            pandas.Series: Série com sinais de trading (1 para compra, -1 para venda, 0 para neutro).
        """
        if params is None:
            params = {}
        
        if estrategia == 'cruzamento_medias':
            periodo_curto = params.get('periodo_curto', 9)
            periodo_longo = params.get('periodo_longo', 21)
            return EstrategiasTrading.cruzamento_medias_moveis(
                dados_close, periodo_curto, periodo_longo
            )
        
        elif estrategia == 'rsi':
            periodo = params.get('periodo', 14)
            nivel_sobrecomprado = params.get('nivel_sobrecomprado', 70)
            nivel_sobrevendido = params.get('nivel_sobrevendido', 30)
            return EstrategiasTrading.rsi_sobrecomprado_sobrevendido(
                dados_close, periodo, nivel_sobrecomprado, nivel_sobrevendido
            )
        
        elif estrategia == 'macd':
            periodo_rapido = params.get('periodo_rapido', 12)
            periodo_lento = params.get('periodo_lento', 26)
            periodo_sinal = params.get('periodo_sinal', 9)
            return EstrategiasTrading.macd_crossover(
                dados_close, periodo_rapido, periodo_lento, periodo_sinal
            )
        
        elif estrategia == 'bollinger':
            periodo = params.get('periodo', 20)
            desvios = params.get('desvios', 2)
            return EstrategiasTrading.bollinger_bands_reversal(
                dados_close, periodo, desvios
            )
        
        elif estrategia == 'price_action':
            fator_sombra = params.get('fator_sombra', 2.0)
            return EstrategiasTrading.price_action_pin_bar(
                dados_open, dados_high, dados_low, dados_close, fator_sombra
            )
        
        elif estrategia == 'suporte_resistencia':
            periodo = params.get('periodo', 14)
            threshold = params.get('threshold', 0.03)
            return EstrategiasTrading.suporte_resistencia_breakout(
                dados_open, dados_high, dados_low, dados_close, periodo, threshold
            )
        
        elif estrategia == 'combinada':
            pesos = params.get('pesos', {
                'cruzamento_medias': 1.0,
                'rsi': 1.0,
                'macd': 1.0,
                'bollinger': 1.0,
                'pin_bar': 1.0,
                'suporte_resistencia': 1.0
            })
            return EstrategiasTrading.estrategia_combinada(
                dados_open, dados_high, dados_low, dados_close, pesos
            )
        
        else:
            raise ValueError(f"Estratégia '{estrategia}' não reconhecida.")
    
    def _calcular_metricas(self, capital_historico, operacoes):
        """
        Calcula métricas de desempenho com base nos resultados do backtesting.
        
        Args:
            capital_historico (list): Histórico de capital.
            operacoes (list): Lista de operações realizadas.
            
        Returns:
            dict: Métricas de desempenho.
        """
        # Converter para DataFrame
        df_operacoes = pd.DataFrame(operacoes)
        
        # Métricas básicas
        capital_final = capital_historico[-1]
        retorno_total = (capital_final / self.capital_inicial - 1) * 100
        
        # Métricas de operações
        if len(operacoes) > 0:
            total_operacoes = len(operacoes)
            operacoes_ganhadoras = sum(1 for op in operacoes if op['resultado'] > 0)
            operacoes_perdedoras = total_operacoes - operacoes_ganhadoras
            
            win_rate = (operacoes_ganhadoras / total_operacoes) * 100 if total_operacoes > 0 else 0
            
            ganhos = sum(op['resultado'] for op in operacoes if op['resultado'] > 0)
            perdas = abs(sum(op['resultado'] for op in operacoes if op['resultado'] <= 0))
            
            profit_factor = ganhos / perdas if perdas > 0 else float('inf')
            
            media_ganhos = ganhos / operacoes_ganhadoras if operacoes_ganhadoras > 0 else 0
            media_perdas = perdas / operacoes_perdedoras if operacoes_perdedoras > 0 else 0
            
            expectativa = (win_rate / 100 * media_ganhos) - ((100 - win_rate) / 100 * media_perdas)
        else:
            total_operacoes = 0
            operacoes_ganhadoras = 0
            operacoes_perdedoras = 0
            win_rate = 0
            profit_factor = 0
            media_ganhos = 0
            media_perdas = 0
            expectativa = 0
        
        # Calcular drawdown
        capital_historico_series = pd.Series(capital_historico)
        pico_maximo = capital_historico_series.cummax()
        drawdown = (capital_historico_series - pico_maximo) / pico_maximo * 100
        max_drawdown = drawdown.min()
        
        # Calcular volatilidade
        retornos_diarios = np.diff(capital_historico) / capital_historico[:-1]
        volatilidade = np.std(retornos_diarios) * 100
        
        # Calcular Sharpe Ratio (assumindo retorno livre de risco de 0%)
        sharpe_ratio = (np.mean(retornos_diarios) / np.std(retornos_diarios)) * np.sqrt(252) if np.std(retornos_diarios) > 0 else 0
        
        return {
            'capital_inicial': self.capital_inicial,
            'capital_final': capital_final,
            'retorno_total': retorno_total,
            'total_operacoes': total_operacoes,
            'operacoes_ganhadoras': operacoes_ganhadoras,
            'operacoes_perdedoras': operacoes_perdedoras,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'media_ganhos': media_ganhos,
            'media_perdas': media_perdas,
            'expectativa': expectativa,
            'max_drawdown': max_drawdown,
            'volatilidade': volatilidade,
            'sharpe_ratio': sharpe_ratio,
            'capital_historico': capital_historico,
            'operacoes': operacoes
        }
    
    def plotar_resultados(self, titulo=None):
        """
        Plota os resultados do backtesting.
        
        Args:
            titulo (str): Título do gráfico.
        """
        if self.resultados is None:
            raise ValueError("Execute o backtesting primeiro.")
        
        plt.figure(figsize=(12, 8))
        
        # Plotar evolução do capital
        plt.subplot(2, 1, 1)
        plt.plot(self.resultados['capital_historico'])
        plt.title(titulo or 'Evolução do Capital')
        plt.grid(True)
        plt.ylabel('Capital (R$)')
        
        # Plotar drawdown
        capital_historico_series = pd.Series(self.resultados['capital_historico'])
        pico_maximo = capital_historico_series.cummax()
        drawdown = (capital_historico_series - pico_maximo) / pico_maximo * 100
        
        plt.subplot(2, 1, 2)
        plt.fill_between(range(len(drawdown)), 0, drawdown, color='red', alpha=0.3)
        plt.grid(True)
        plt.ylabel('Drawdown (%)')
        plt.xlabel('Dias')
        plt.title('Drawdown')
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/robo_trader/resultados_backtest.png')
        plt.close()
    
    def gerar_relatorio(self, caminho_arquivo):
        """
        Gera um relatório detalhado dos resultados do backtesting.
        
        Args:
            caminho_arquivo (str): Caminho para salvar o relatório.
        """
        if self.resultados is None:
            raise ValueError("Execute o backtesting primeiro.")
        
        with open(caminho_arquivo, 'w') as f:
            f.write("# Relatório de Backtesting\n\n")
            
            f.write("## Métricas de Desempenho\n\n")
(Content truncated due to size limit. Use line ranges to read in chunks)