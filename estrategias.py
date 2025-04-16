"""
Módulo de Estratégias de Trading para o Robô Trader

Este módulo implementa estratégias de trading que combinam indicadores técnicos
e análise de price action para gerar sinais de compra e venda.
"""

import pandas as pd
import numpy as np
from .indicadores import IndicadoresTecnicos
from .price_action import PriceAction

class EstrategiasTrading:
    """
    Classe que implementa estratégias de trading para day trading.
    """
    
    @staticmethod
    def cruzamento_medias_moveis(dados_close, periodo_curto=9, periodo_longo=21):
        """
        Estratégia baseada no cruzamento de médias móveis.
        
        Args:
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo_curto (int): Período para média móvel de curto prazo.
            periodo_longo (int): Período para média móvel de longo prazo.
            
        Returns:
            pandas.Series: Série com sinais de trading (1 para compra, -1 para venda, 0 para neutro).
        """
        ma_curta = IndicadoresTecnicos.media_movel_simples(dados_close, periodo_curto)
        ma_longa = IndicadoresTecnicos.media_movel_simples(dados_close, periodo_longo)
        
        # Inicializar série de sinais
        sinais = pd.Series(0, index=dados_close.index)
        
        # Gerar sinais de cruzamento
        for i in range(1, len(dados_close)):
            # Cruzamento para cima (compra)
            if ma_curta.iloc[i] > ma_longa.iloc[i] and ma_curta.iloc[i-1] <= ma_longa.iloc[i-1]:
                sinais.iloc[i] = 1
            
            # Cruzamento para baixo (venda)
            elif ma_curta.iloc[i] < ma_longa.iloc[i] and ma_curta.iloc[i-1] >= ma_longa.iloc[i-1]:
                sinais.iloc[i] = -1
        
        return sinais
    
    @staticmethod
    def rsi_sobrecomprado_sobrevendido(dados_close, periodo=14, nivel_sobrecomprado=70, nivel_sobrevendido=30):
        """
        Estratégia baseada em níveis de sobrecompra e sobrevenda do RSI.
        
        Args:
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo (int): Período para cálculo do RSI.
            nivel_sobrecomprado (int): Nível que indica sobrecompra.
            nivel_sobrevendido (int): Nível que indica sobrevenda.
            
        Returns:
            pandas.Series: Série com sinais de trading (1 para compra, -1 para venda, 0 para neutro).
        """
        rsi = IndicadoresTecnicos.rsi(dados_close, periodo)
        
        # Inicializar série de sinais
        sinais = pd.Series(0, index=dados_close.index)
        
        # Gerar sinais baseados em níveis de RSI
        for i in range(1, len(dados_close)):
            # Sinal de compra: RSI saindo da região de sobrevenda
            if rsi.iloc[i] > nivel_sobrevendido and rsi.iloc[i-1] <= nivel_sobrevendido:
                sinais.iloc[i] = 1
            
            # Sinal de venda: RSI saindo da região de sobrecompra
            elif rsi.iloc[i] < nivel_sobrecomprado and rsi.iloc[i-1] >= nivel_sobrecomprado:
                sinais.iloc[i] = -1
        
        return sinais
    
    @staticmethod
    def macd_crossover(dados_close, periodo_rapido=12, periodo_lento=26, periodo_sinal=9):
        """
        Estratégia baseada no cruzamento da linha MACD com a linha de sinal.
        
        Args:
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo_rapido (int): Período para a média móvel rápida.
            periodo_lento (int): Período para a média móvel lenta.
            periodo_sinal (int): Período para a linha de sinal.
            
        Returns:
            pandas.Series: Série com sinais de trading (1 para compra, -1 para venda, 0 para neutro).
        """
        macd_linha, sinal, _ = IndicadoresTecnicos.macd(
            dados_close, periodo_rapido, periodo_lento, periodo_sinal
        )
        
        # Inicializar série de sinais
        sinais = pd.Series(0, index=dados_close.index)
        
        # Gerar sinais de cruzamento
        for i in range(1, len(dados_close)):
            # Cruzamento para cima (compra)
            if macd_linha.iloc[i] > sinal.iloc[i] and macd_linha.iloc[i-1] <= sinal.iloc[i-1]:
                sinais.iloc[i] = 1
            
            # Cruzamento para baixo (venda)
            elif macd_linha.iloc[i] < sinal.iloc[i] and macd_linha.iloc[i-1] >= sinal.iloc[i-1]:
                sinais.iloc[i] = -1
        
        return sinais
    
    @staticmethod
    def bollinger_bands_reversal(dados_close, periodo=20, desvios=2):
        """
        Estratégia de reversão baseada nas Bandas de Bollinger.
        
        Args:
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo (int): Período para cálculo das Bandas de Bollinger.
            desvios (int): Número de desvios padrão para as bandas.
            
        Returns:
            pandas.Series: Série com sinais de trading (1 para compra, -1 para venda, 0 para neutro).
        """
        banda_superior, _, banda_inferior = IndicadoresTecnicos.bandas_bollinger(
            dados_close, periodo, desvios
        )
        
        # Inicializar série de sinais
        sinais = pd.Series(0, index=dados_close.index)
        
        # Gerar sinais baseados em toques nas bandas
        for i in range(1, len(dados_close)):
            # Preço toca ou cruza a banda inferior (compra)
            if dados_close.iloc[i-1] <= banda_inferior.iloc[i-1]:
                sinais.iloc[i] = 1
            
            # Preço toca ou cruza a banda superior (venda)
            elif dados_close.iloc[i-1] >= banda_superior.iloc[i-1]:
                sinais.iloc[i] = -1
        
        return sinais
    
    @staticmethod
    def price_action_pin_bar(dados_open, dados_high, dados_low, dados_close, fator_sombra=2.0):
        """
        Estratégia baseada em pin bars (barras de reversão).
        
        Args:
            dados_open (pandas.Series): Série de preços de abertura.
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            fator_sombra (float): Fator que determina quantas vezes a sombra deve ser maior que o corpo.
            
        Returns:
            pandas.Series: Série com sinais de trading (1 para compra, -1 para venda, 0 para neutro).
        """
        pin_bar_alta, pin_bar_baixa = PriceAction.identificar_pin_bars(
            dados_open, dados_high, dados_low, dados_close, fator_sombra
        )
        
        # Inicializar série de sinais
        sinais = pd.Series(0, index=dados_close.index)
        
        # Gerar sinais baseados em pin bars
        sinais[pin_bar_alta] = 1  # Pin bar de alta (sinal de compra)
        sinais[pin_bar_baixa] = -1  # Pin bar de baixa (sinal de venda)
        
        return sinais
    
    @staticmethod
    def suporte_resistencia_breakout(dados_open, dados_high, dados_low, dados_close, periodo=14, threshold=0.03):
        """
        Estratégia baseada em rompimentos de níveis de suporte e resistência.
        
        Args:
            dados_open (pandas.Series): Série de preços de abertura.
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo (int): Período para análise.
            threshold (float): Limiar percentual para considerar um nível significativo.
            
        Returns:
            pandas.Series: Série com sinais de trading (1 para compra, -1 para venda, 0 para neutro).
        """
        # Inicializar série de sinais
        sinais = pd.Series(0, index=dados_close.index)
        
        # Analisar janelas móveis para identificar rompimentos
        for i in range(periodo, len(dados_close)):
            # Obter níveis de suporte e resistência para a janela atual
            janela_high = dados_high.iloc[i-periodo:i]
            janela_low = dados_low.iloc[i-periodo:i]
            
            suportes, resistencias = PriceAction.identificar_suporte_resistencia(
                janela_high, janela_low, dados_close.iloc[i-periodo:i], periodo, threshold
            )
            
            # Verificar rompimentos
            if suportes and resistencias:
                # Rompimento de resistência (compra)
                if dados_close.iloc[i] > min(resistencias) * (1 + threshold/2):
                    sinais.iloc[i] = 1
                
                # Rompimento de suporte (venda)
                elif dados_close.iloc[i] < max(suportes) * (1 - threshold/2):
                    sinais.iloc[i] = -1
        
        return sinais
    
    @staticmethod
    def estrategia_combinada(dados_open, dados_high, dados_low, dados_close, pesos=None):
        """
        Estratégia combinada que utiliza múltiplos indicadores e técnicas de price action.
        
        Args:
            dados_open (pandas.Series): Série de preços de abertura.
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            pesos (dict): Dicionário com pesos para cada estratégia.
            
        Returns:
            pandas.Series: Série com sinais de trading (1 para compra, -1 para venda, 0 para neutro).
        """
        if pesos is None:
            pesos = {
                'cruzamento_medias': 1.0,
                'rsi': 1.0,
                'macd': 1.0,
                'bollinger': 1.0,
                'pin_bar': 1.0,
                'suporte_resistencia': 1.0
            }
        
        # Obter sinais de cada estratégia
        sinais_cruzamento = EstrategiasTrading.cruzamento_medias_moveis(dados_close)
        sinais_rsi = EstrategiasTrading.rsi_sobrecomprado_sobrevendido(dados_close)
        sinais_macd = EstrategiasTrading.macd_crossover(dados_close)
        sinais_bollinger = EstrategiasTrading.bollinger_bands_reversal(dados_close)
        sinais_pin_bar = EstrategiasTrading.price_action_pin_bar(dados_open, dados_high, dados_low, dados_close)
        sinais_sr = EstrategiasTrading.suporte_resistencia_breakout(dados_open, dados_high, dados_low, dados_close)
        
        # Combinar sinais com pesos
        sinais_combinados = (
            pesos['cruzamento_medias'] * sinais_cruzamento +
            pesos['rsi'] * sinais_rsi +
            pesos['macd'] * sinais_macd +
            pesos['bollinger'] * sinais_bollinger +
            pesos['pin_bar'] * sinais_pin_bar +
            pesos['suporte_resistencia'] * sinais_sr
        )
        
        # Normalizar sinais
        soma_pesos = sum(pesos.values())
        sinais_combinados = sinais_combinados / soma_pesos
        
        # Converter para sinais discretos
        sinais = pd.Series(0, index=dados_close.index)
        sinais[sinais_combinados > 0.3] = 1  # Sinal forte de compra
        sinais[sinais_combinados < -0.3] = -1  # Sinal forte de venda
        
        return sinais
