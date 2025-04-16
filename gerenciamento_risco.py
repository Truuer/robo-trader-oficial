"""
Módulo de Gerenciamento de Risco para o Robô Trader

Este módulo implementa funções para gerenciamento de risco nas operações de trading,
incluindo cálculo de tamanho de posição, stop loss e take profit.
"""

import pandas as pd
import numpy as np
from .indicadores import IndicadoresTecnicos

class GerenciamentoRisco:
    """
    Classe que implementa funções de gerenciamento de risco para operações de trading.
    """
    
    @staticmethod
    def calcular_tamanho_posicao(capital, risco_percentual, preco_entrada, preco_stop):
        """
        Calcula o tamanho da posição baseado no risco percentual do capital.
        
        Args:
            capital (float): Capital total disponível.
            risco_percentual (float): Percentual do capital a arriscar na operação (ex: 1.0 para 1%).
            preco_entrada (float): Preço de entrada da operação.
            preco_stop (float): Preço do stop loss.
            
        Returns:
            float: Quantidade de unidades/contratos a serem negociados.
        """
        # Calcular valor monetário a arriscar
        valor_risco = capital * (risco_percentual / 100)
        
        # Calcular risco por unidade
        risco_por_unidade = abs(preco_entrada - preco_stop)
        
        # Calcular tamanho da posição
        if risco_por_unidade > 0:
            tamanho_posicao = valor_risco / risco_por_unidade
        else:
            tamanho_posicao = 0
            
        return tamanho_posicao
    
    @staticmethod
    def calcular_stop_loss_atr(dados_high, dados_low, dados_close, preco_entrada, direcao, 
                              multiplicador=2.0, periodo_atr=14):
        """
        Calcula o nível de stop loss baseado no ATR (Average True Range).
        
        Args:
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            preco_entrada (float): Preço de entrada da operação.
            direcao (int): Direção da operação (1 para compra, -1 para venda).
            multiplicador (float): Multiplicador do ATR para definir a distância do stop.
            periodo_atr (int): Período para cálculo do ATR.
            
        Returns:
            float: Preço do stop loss.
        """
        # Calcular ATR
        atr = IndicadoresTecnicos.atr(dados_high, dados_low, dados_close, periodo_atr)
        
        # Obter o valor mais recente do ATR
        atr_atual = atr.iloc[-1]
        
        # Calcular stop loss baseado na direção
        if direcao == 1:  # Compra
            stop_loss = preco_entrada - (multiplicador * atr_atual)
        else:  # Venda
            stop_loss = preco_entrada + (multiplicador * atr_atual)
            
        return stop_loss
    
    @staticmethod
    def calcular_take_profit(preco_entrada, preco_stop, rr_ratio=2.0):
        """
        Calcula o nível de take profit baseado na relação risco/retorno.
        
        Args:
            preco_entrada (float): Preço de entrada da operação.
            preco_stop (float): Preço do stop loss.
            rr_ratio (float): Relação risco/retorno desejada.
            
        Returns:
            float: Preço do take profit.
        """
        # Calcular distância até o stop loss
        distancia_stop = abs(preco_entrada - preco_stop)
        
        # Calcular take profit baseado na direção
        if preco_entrada > preco_stop:  # Compra
            take_profit = preco_entrada + (distancia_stop * rr_ratio)
        else:  # Venda
            take_profit = preco_entrada - (distancia_stop * rr_ratio)
            
        return take_profit
    
    @staticmethod
    def calcular_trailing_stop(dados_close, preco_entrada, direcao, percentual=1.0):
        """
        Calcula o trailing stop baseado em um percentual do movimento favorável.
        
        Args:
            dados_close (pandas.Series): Série de preços de fechamento.
            preco_entrada (float): Preço de entrada da operação.
            direcao (int): Direção da operação (1 para compra, -1 para venda).
            percentual (float): Percentual do movimento favorável para definir o trailing stop.
            
        Returns:
            pandas.Series: Série com os níveis de trailing stop.
        """
        # Inicializar série de trailing stop
        trailing_stop = pd.Series(0.0, index=dados_close.index)
        
        # Calcular trailing stop baseado na direção
        if direcao == 1:  # Compra
            # Calcular preço máximo desde a entrada
            preco_maximo = dados_close.cummax()
            
            # Calcular trailing stop
            trailing_stop = preco_maximo * (1 - percentual/100)
            
            # Garantir que o trailing stop não fique abaixo do preço de entrada
            trailing_stop = trailing_stop.clip(lower=preco_entrada)
        else:  # Venda
            # Calcular preço mínimo desde a entrada
            preco_minimo = dados_close.cummin()
            
            # Calcular trailing stop
            trailing_stop = preco_minimo * (1 + percentual/100)
            
            # Garantir que o trailing stop não fique acima do preço de entrada
            trailing_stop = trailing_stop.clip(upper=preco_entrada)
            
        return trailing_stop
    
    @staticmethod
    def calcular_exposicao_maxima(capital, exposicao_percentual=20.0):
        """
        Calcula a exposição máxima permitida baseada no capital disponível.
        
        Args:
            capital (float): Capital total disponível.
            exposicao_percentual (float): Percentual máximo de exposição do capital.
            
        Returns:
            float: Valor máximo de exposição permitido.
        """
        return capital * (exposicao_percentual / 100)
    
    @staticmethod
    def verificar_horario_operacao(timestamp, inicio_dia='09:30', fim_dia='16:30'):
        """
        Verifica se o horário está dentro do período de operação permitido.
        
        Args:
            timestamp (pandas.Timestamp): Timestamp a ser verificado.
            inicio_dia (str): Horário de início das operações (formato HH:MM).
            fim_dia (str): Horário de fim das operações (formato HH:MM).
            
        Returns:
            bool: True se estiver dentro do horário permitido, False caso contrário.
        """
        # Extrair hora e minuto do timestamp
        hora = timestamp.hour
        minuto = timestamp.minute
        
        # Converter horários de início e fim para minutos
        inicio_minutos = int(inicio_dia.split(':')[0]) * 60 + int(inicio_dia.split(':')[1])
        fim_minutos = int(fim_dia.split(':')[0]) * 60 + int(fim_dia.split(':')[1])
        
        # Converter horário atual para minutos
        atual_minutos = hora * 60 + minuto
        
        # Verificar se está dentro do horário permitido
        return inicio_minutos <= atual_minutos <= fim_minutos
    
    @staticmethod
    def calcular_drawdown(capital_historico):
        """
        Calcula o drawdown máximo baseado no histórico de capital.
        
        Args:
            capital_historico (pandas.Series): Série com o histórico de capital.
            
        Returns:
            tuple: (Drawdown máximo percentual, Drawdown atual percentual)
        """
        # Calcular pico máximo até o momento
        pico_maximo = capital_historico.cummax()
        
        # Calcular drawdown em valor
        drawdown_valor = capital_historico - pico_maximo
        
        # Calcular drawdown percentual
        drawdown_percentual = (drawdown_valor / pico_maximo) * 100
        
        # Obter drawdown máximo e atual
        drawdown_maximo = drawdown_percentual.min()
        drawdown_atual = drawdown_percentual.iloc[-1]
        
        return drawdown_maximo, drawdown_atual
