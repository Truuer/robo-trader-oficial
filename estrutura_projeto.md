# Estrutura do Projeto Flutter para o Robô Trader

Este documento descreve a estrutura básica do projeto Flutter para a interface mobile do robô trader.

## Estrutura de Diretórios

```
robo_trader_app/
├── android/                 # Configurações específicas para Android
├── ios/                     # Configurações específicas para iOS (não será o foco inicial)
├── lib/
│   ├── main.dart            # Ponto de entrada da aplicação
│   ├── config/              # Configurações da aplicação
│   ├── models/              # Modelos de dados
│   ├── screens/             # Telas da aplicação
│   │   ├── dashboard/       # Dashboard principal
│   │   ├── charts/          # Visualização de gráficos
│   │   ├── settings/        # Configurações do robô
│   │   ├── reports/         # Relatórios de desempenho
│   │   └── auth/            # Autenticação (se necessário)
│   ├── services/            # Serviços para comunicação com backend
│   │   ├── api_service.dart # Comunicação com APIs de corretoras
│   │   ├── trading_service.dart # Serviço de execução de ordens
│   │   └── websocket_service.dart # Comunicação em tempo real
│   ├── widgets/             # Widgets reutilizáveis
│   └── utils/               # Utilitários e helpers
├── assets/                  # Recursos estáticos (imagens, fontes, etc.)
└── test/                    # Testes unitários e de integração
```

## Principais Telas

1. **Dashboard**
   - Visão geral do desempenho
   - Posições abertas
   - Sinais ativos
   - Resumo de operações do dia

2. **Gráficos**
   - Visualização de gráficos de preços
   - Indicadores técnicos sobrepostos
   - Sinais de entrada/saída
   - Múltiplos timeframes

3. **Configurações**
   - Parâmetros de estratégias
   - Configurações de gerenciamento de risco
   - Seleção de ativos para monitoramento
   - Horários de operação

4. **Relatórios**
   - Histórico de operações
   - Métricas de desempenho
   - Gráficos de evolução do capital
   - Análise de drawdown

## Fluxo de Navegação

1. Tela de splash/login
2. Dashboard principal
3. Navegação entre telas via bottom navigation bar ou drawer

## Comunicação com Backend

- RESTful API para operações não-críticas
- WebSockets para dados em tempo real e sinais de trading
- Armazenamento local para configurações e cache de dados

## Considerações de UI/UX

- Design responsivo para diferentes tamanhos de tela
- Modo escuro/claro
- Feedback visual para operações críticas
- Notificações push para sinais importantes
