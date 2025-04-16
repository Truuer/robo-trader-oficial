"""
Módulo de Price Action para o Robô Trader

Este módulo implementa as principais técnicas de price action utilizadas para
identificação de padrões e geração de sinais de trading.
"""

import numpy as np
import pandas as pd

class PriceAction:
    """
    Classe que implementa técnicas de price action para análise de mercado.
    """
    
    @staticmethod
    def identificar_suporte_resistencia(dados_high, dados_low, dados_close, periodo=14, threshold=0.03):
        """
        Identifica níveis de suporte e resistência baseados em máximos e mínimos recentes.
        
        Args:
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo (int): Período para análise.
            threshold (float): Limiar percentual para considerar um nível significativo.
            
        Returns:
            tuple: (Níveis de Suporte, Níveis de Resistência)
        """
        suportes = []
        resistencias = []
        
        for i in range(periodo, len(dados_close)):
            # Analisar janela de dados
            janela_low = dados_low.iloc[i-periodo:i]
            janela_high = dados_high.iloc[i-periodo:i]
            
            # Encontrar mínimos locais (potenciais suportes)
            for j in range(1, len(janela_low)-1):
                if janela_low.iloc[j] < janela_low.iloc[j-1] and janela_low.iloc[j] < janela_low.iloc[j+1]:
                    suportes.append(janela_low.iloc[j])
            
            # Encontrar máximos locais (potenciais resistências)
            for j in range(1, len(janela_high)-1):
                if janela_high.iloc[j] > janela_high.iloc[j-1] and janela_high.iloc[j] > janela_high.iloc[j+1]:
                    resistencias.append(janela_high.iloc[j])
        
        # Agrupar níveis próximos
        suportes = PriceAction._agrupar_niveis(suportes, threshold)
        resistencias = PriceAction._agrupar_niveis(resistencias, threshold)
        
        return suportes, resistencias
    
    @staticmethod
    def _agrupar_niveis(niveis, threshold):
        """
        Agrupa níveis próximos para reduzir duplicações.
        
        Args:
            niveis (list): Lista de níveis.
            threshold (float): Limiar percentual para considerar níveis como próximos.
            
        Returns:
            list: Lista de níveis agrupados.
        """
        if not niveis:
            return []
        
        niveis_ordenados = sorted(niveis)
        niveis_agrupados = []
        grupo_atual = [niveis_ordenados[0]]
        
        for nivel in niveis_ordenados[1:]:
            # Verificar se o nível está próximo do último nível do grupo atual
            if abs(nivel - grupo_atual[-1]) / grupo_atual[-1] <= threshold:
                grupo_atual.append(nivel)
            else:
                # Adicionar média do grupo atual aos níveis agrupados
                niveis_agrupados.append(sum(grupo_atual) / len(grupo_atual))
                grupo_atual = [nivel]
        
        # Adicionar o último grupo
        if grupo_atual:
            niveis_agrupados.append(sum(grupo_atual) / len(grupo_atual))
        
        return niveis_agrupados
    
    @staticmethod
    def identificar_tendencia(dados_close, periodo_curto=20, periodo_longo=50):
        """
        Identifica a tendência atual do mercado usando médias móveis.
        
        Args:
            dados_close (pandas.Series): Série de preços de fechamento.
            periodo_curto (int): Período para média móvel de curto prazo.
            periodo_longo (int): Período para média móvel de longo prazo.
            
        Returns:
            pandas.Series: Série com valores indicando a tendência (1 para alta, -1 para baixa, 0 para lateral).
        """
        from .indicadores import IndicadoresTecnicos
        
        ma_curta = IndicadoresTecnicos.media_movel_simples(dados_close, periodo_curto)
        ma_longa = IndicadoresTecnicos.media_movel_simples(dados_close, periodo_longo)
        
        tendencia = pd.Series(0, index=dados_close.index)
        tendencia[ma_curta > ma_longa] = 1  # Tendência de alta
        tendencia[ma_curta < ma_longa] = -1  # Tendência de baixa
        
        return tendencia
    
    @staticmethod
    def identificar_candle_patterns(dados_open, dados_high, dados_low, dados_close):
        """
        Identifica padrões de candles comuns em price action.
        
        Args:
            dados_open (pandas.Series): Série de preços de abertura.
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            
        Returns:
            dict: Dicionário com padrões identificados.
        """
        # Calcular tamanho do corpo e sombras
        corpo = abs(dados_close - dados_open)
        sombra_superior = dados_high - np.maximum(dados_close, dados_open)
        sombra_inferior = np.minimum(dados_close, dados_open) - dados_low
        
        # Determinar se o candle é de alta ou baixa
        candle_alta = dados_close > dados_open
        candle_baixa = dados_close < dados_open
        
        # Identificar padrões
        padroes = {
            'doji': pd.Series(False, index=dados_close.index),
            'martelo': pd.Series(False, index=dados_close.index),
            'martelo_invertido': pd.Series(False, index=dados_close.index),
            'engolfo_alta': pd.Series(False, index=dados_close.index),
            'engolfo_baixa': pd.Series(False, index=dados_close.index),
            'estrela_da_manha': pd.Series(False, index=dados_close.index),
            'estrela_da_noite': pd.Series(False, index=dados_close.index)
        }
        
        # Doji (corpo muito pequeno)
        corpo_medio = corpo.mean()
        padroes['doji'] = corpo < (0.1 * corpo_medio)
        
        # Martelo (sombra inferior longa, corpo pequeno, sombra superior pequena)
        padroes['martelo'] = (sombra_inferior > (2 * corpo)) & (sombra_superior < (0.3 * corpo))
        
        # Martelo invertido (sombra superior longa, corpo pequeno, sombra inferior pequena)
        padroes['martelo_invertido'] = (sombra_superior > (2 * corpo)) & (sombra_inferior < (0.3 * corpo))
        
        # Engolfo de alta (candle atual de alta engole o anterior de baixa)
        for i in range(1, len(dados_close)):
            if (candle_alta.iloc[i] and candle_baixa.iloc[i-1] and 
                dados_open.iloc[i] <= dados_close.iloc[i-1] and 
                dados_close.iloc[i] >= dados_open.iloc[i-1]):
                padroes['engolfo_alta'].iloc[i] = True
        
        # Engolfo de baixa (candle atual de baixa engole o anterior de alta)
        for i in range(1, len(dados_close)):
            if (candle_baixa.iloc[i] and candle_alta.iloc[i-1] and 
                dados_open.iloc[i] >= dados_close.iloc[i-1] and 
                dados_close.iloc[i] <= dados_open.iloc[i-1]):
                padroes['engolfo_baixa'].iloc[i] = True
        
        # Estrela da manhã (padrão de reversão de baixa para alta)
        for i in range(2, len(dados_close)):
            if (candle_baixa.iloc[i-2] and 
                corpo.iloc[i-1] < (0.5 * corpo.iloc[i-2]) and 
                candle_alta.iloc[i] and 
                dados_close.iloc[i] > (dados_open.iloc[i-2] + dados_close.iloc[i-2]) / 2):
                padroes['estrela_da_manha'].iloc[i] = True
        
        # Estrela da noite (padrão de reversão de alta para baixa)
        for i in range(2, len(dados_close)):
            if (candle_alta.iloc[i-2] and 
                corpo.iloc[i-1] < (0.5 * corpo.iloc[i-2]) and 
                candle_baixa.iloc[i] and 
                dados_close.iloc[i] < (dados_open.iloc[i-2] + dados_close.iloc[i-2]) / 2):
                padroes['estrela_da_noite'].iloc[i] = True
        
        return padroes
    
    @staticmethod
    def identificar_pin_bars(dados_open, dados_high, dados_low, dados_close, fator_sombra=2.0):
        """
        Identifica pin bars (barras de reversão) no gráfico.
        
        Args:
            dados_open (pandas.Series): Série de preços de abertura.
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            dados_close (pandas.Series): Série de preços de fechamento.
            fator_sombra (float): Fator que determina quantas vezes a sombra deve ser maior que o corpo.
            
        Returns:
            tuple: (Pin Bars de Alta, Pin Bars de Baixa)
        """
        # Calcular tamanho do corpo e sombras
        corpo = abs(dados_close - dados_open)
        sombra_superior = dados_high - np.maximum(dados_close, dados_open)
        sombra_inferior = np.minimum(dados_close, dados_open) - dados_low
        
        # Pin bar de baixa (sombra superior longa)
        pin_bar_baixa = (sombra_superior > (fator_sombra * corpo)) & (sombra_superior > (fator_sombra * sombra_inferior))
        
        # Pin bar de alta (sombra inferior longa)
        pin_bar_alta = (sombra_inferior > (fator_sombra * corpo)) & (sombra_inferior > (fator_sombra * sombra_superior))
        
        return pin_bar_alta, pin_bar_baixa
    
    @staticmethod
    def identificar_inside_bars(dados_high, dados_low):
        """
        Identifica inside bars (barras internas) no gráfico.
        
        Args:
            dados_high (pandas.Series): Série de preços máximos.
            dados_low (pandas.Series): Série de preços mínimos.
            
        Returns:
            pandas.Series: Série booleana indicando onde ocorrem inside bars.
        """
        inside_bars = pd.Series(False, index=dados_high.index)
        
        for i in range(1, len(dados_high)):
            if (dados_high.iloc[i] <= dados_high.iloc[i-1] and 
                dados_low.iloc[i] >= dados_low.iloc[i-1]):
                inside_bars.iloc[i] = True
        
        return inside_bars
