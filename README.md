# README - Robô Trader

## Visão Geral

O Robô Trader é uma aplicação mobile para Android que automatiza operações de day trading em múltiplos mercados (ações, forex, criptomoedas) utilizando técnicas avançadas de análise técnica e price action.

## Principais Funcionalidades

- **Trading Automatizado**: Executa operações de compra e venda sem intervenção manual
- **Múltiplas Estratégias**: Implementa diversas estratégias de análise técnica e price action
- **Gerenciamento de Risco**: Sistema avançado para controle de risco e proteção do capital
- **Interface Intuitiva**: Dashboard completo com gráficos, relatórios e configurações
- **Compatibilidade**: Funciona com diversas corretoras através de APIs

## Estrutura do Projeto

```
robo_trader/
├── src/
│   ├── analise_tecnica/       # Módulos de análise técnica e price action
│   ├── interface_mobile/      # Interface de usuário em Flutter
│   └── testes/                # Módulos de backtesting e paper trading
├── resultados/                # Resultados dos testes realizados
├── manual_usuario.md          # Manual detalhado para o usuário final
├── guia_instalacao.md         # Guia técnico de instalação e configuração
└── arquitetura.md             # Documentação da arquitetura do sistema
```

## Requisitos

- Android 8.0 ou superior
- Conexão estável com a internet
- Conta em corretora compatível com acesso à API

## Instalação

Consulte o arquivo `guia_instalacao.md` para instruções detalhadas sobre como instalar e configurar o aplicativo.

## Uso

Consulte o arquivo `manual_usuario.md` para instruções detalhadas sobre como utilizar o aplicativo.

## Estratégias Implementadas

- Cruzamento de Médias Móveis
- RSI (Índice de Força Relativa)
- MACD (Convergência e Divergência de Médias Móveis)
- Bandas de Bollinger
- Price Action (Pin Bars, Suportes e Resistências)
- Estratégia Combinada (ponderação de múltiplos sinais)

## Testes e Desempenho

O sistema foi testado extensivamente através de:
- Backtesting com dados históricos de múltiplos ativos
- Simulações de paper trading em ambiente controlado

Os resultados dos testes estão disponíveis no diretório `resultados/`.

## Próximos Passos

- Otimização de parâmetros dos indicadores
- Testes em diferentes condições de mercado
- Verificação de desempenho em dispositivos Android reais
- Implementação de novas estratégias

## Aviso Legal

O Robô Trader é uma ferramenta de auxílio para operações de trading. Resultados passados não garantem resultados futuros. Opere com responsabilidade e esteja ciente dos riscos envolvidos em operações financeiras.
