"""
Módulo de Indicadores Técnicos para o Robô Trader

Este módulo implementa os principais indicadores técnicos utilizados para análise
de mercado e geração de sinais de trading.
"""

import numpy as np
import pandas as pd

class IndicadoresTecnicos:
    """
    Classe que implementa os principais indicadores técnicos para análise de mercado.
    """
    
    @staticmethod
    def media_movel_simples(dados, periodo=20):
        """
        Calcula a Média Móvel Simples (SMA) para uma série de preços.
        
        Args:
            dados (pandas.Series): Série de preços.
            periodo (int): Período para cálculo da média móvel.
            
        Returns:
            pandas.Series: Série com os valores da média móvel.
        """
        return dados.rolling(window=periodo).mean()
    
    @staticmethod
    def media_movel_exponencial(dados, periodo=20):
        """
        Calcula a Média Móvel Exponencial (EMA) para uma série de preços.
        
        Args:
            dados (pandas.Series): Série de preços.
            periodo (int): Período para cálculo da média móvel.
            
        Returns:
            pandas.Series: Série com os valores da média móvel exponencial.
        """
        return dados.ewm(span=periodo, adjust=False).mean()
    
    @staticmethod
    def macd(dados, periodo_rapido=12, periodo_lento=26, periodo_sinal=9):
        """
        Calcula o MACD (Moving Average Convergence Divergence).
        
        Args:
            dados (pandas.Series): Série de preços.
            periodo_rapido (int): Período para a média móvel rápida.
            periodo_lento (int): Período para a média móvel lenta.
            periodo_sinal (int): Período para a linha de sinal.
            
        Returns:
            tuple: (MACD, Sinal, Histograma)
        """
        ema_rapida = IndicadoresTecnicos.media_movel_exponencial(dados, periodo_rapido)
        ema_lenta = IndicadoresTecnicos.media_movel_exponencial(dados, periodo_lento)
        
        macd_linha = ema_rapida - ema_lenta
        sinal = macd_linha.ewm(span=periodo_sinal, adjust=False).mean()
        histograma = macd_linha - sinal
        
        return macd_linha, sinal, histograma
    
    @staticmethod
    def rsi(dados, periodo=14):
        """
        Calcula o RSI (Relative Strength Index).
        
        Args:
            dados (pandas.Series): Série de preços.
            periodo (int): Período para cálculo do RSI.
            
        Returns:
            pandas.Series: Série com os valores do RSI.
        """
        delta = dados.diff()
        
        # Separar ganhos (positivos) e perdas (negativos)
        ganhos, perdas = delta.copy(), delta.copy()
        ganhos[ganhos < 0] = 0
        perdas[perdas > 0] = 0
        perdas = abs(perdas)
        
        # Calcular médias móveis de ganhos e perdas
        media_ganhos = ganhos.rolling(window=periodo).mean()
        media_perdas = perdas.rolling(window=periodo).mean()
        
        # Calcular força relativa
        rs = media_ganhos / media_perdas
        
        # Calcular RSI
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def bandas_bollinger(dados, periodo=20, desvios=2):
        """
        Calcula as Bandas de Bollinger.
        
        Args:
            dados (pandas.Series): Série de preços.
            periodo (int): Período para cálculo da média móvel.
            desvios (int): Número de desvios padrão para as bandas.
            
        Returns:
            tuple: (Banda Superior, Média Móvel, Banda Inferior)
        """
        media_movel = IndicadoresTecnicos.media_movel_simples(dados, periodo)
        desvio_padrao = dados.rolling(window=periodo).std()
        
        banda_superior = media_movel + (desvio_padrao * desvios)
        banda_inferior = media_movel - (desvio_padrao * desvios)
        
        return banda_superior, media_movel, banda_inferior
    
    @staticmethod
    def estocastico(dados_high, dados_low, dados_close, periodo_k=14, periodo_d=3):
        """
        Calcula o Oscilador Estocástico.
        
        Args:
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo_k (int): Período para cálculo do %K.
            periodo_d (int): Período para cálculo do %D.
            
        Returns:
            tuple: (%K, %D)
        """
        # Calcular %K
        minimo_periodo = dados_low.rolling(window=periodo_k).min()
        maximo_periodo = dados_high.rolling(window=periodo_k).max()
        
        k = 100 * ((dados_close - minimo_periodo) / (maximo_periodo - minimo_periodo))
        
        # Calcular %D (média móvel de %K)
        d = k.rolling(window=periodo_d).mean()
        
        return k, d
    
    @staticmethod
    def atr(dados_high, dados_low, dados_close, periodo=14):
        """
        Calcula o ATR (Average True Range).
        
        Args:
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo (int): Período para cálculo do ATR.
            
        Returns:
            pandas.Series: Série com os valores do ATR.
        """
        # Calcular True Range
        dados_close_anterior = dados_close.shift(1)
        
        tr1 = dados_high - dados_low
        tr2 = abs(dados_high - dados_close_anterior)
        tr3 = abs(dados_low - dados_close_anterior)
        
        tr = pd.DataFrame({'TR1': tr1, 'TR2': tr2, 'TR3': tr3}).max(axis=1)
        
        # Calcular ATR (média móvel do True Range)
        atr = tr.rolling(window=periodo).mean()
        
        return atr
