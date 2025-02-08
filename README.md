# Tibia Guild EXP Calculator

Este script calcula a experiência total (EXP) ganha e perdida por guilds específicas no Tibia, utilizando dados do guildstats.eu e da API oficial do Tibia.

## Funcionalidades

- Coleta dados de EXP ganha do guildstats.eu
- Coleta dados de EXP perdida (mortes) do guildstats.eu
- Usa a API do Tibia para identificar membros das guilds
- Calcula o total de EXP para as guilds selecionadas

## Estrutura do Projeto

O projeto segue os princípios SOLID e está organizado nos seguintes arquivos:

- `main.py`: Ponto de entrada do programa
- `tibia_api_client.py`: Cliente para a API do Tibia
- `exp_data_provider.py`: Provedores de dados de EXP do guildstats.eu
- `guild_exp_calculator.py`: Calculadora de EXP das guilds

## Requisitos

```bash
pip install -r requirements.txt
```

## Como usar

1. Edite o arquivo `main.py` e modifique as seguintes variáveis:
   ```python
   world = "World"  # Nome do mundo do Tibia
   target_guilds = ["Guild 1", "Guild 2"]  # Lista das guilds para monitorar
   ```

2. Execute o script:
   ```bash
   python main.py
   ```

## Extensibilidade

O projeto foi desenvolvido seguindo princípios SOLID, permitindo fácil extensão:

1. Para adicionar uma nova fonte de dados de EXP:
   - Implemente a interface `ExpDataProvider`
   - Adicione a nova implementação na lista `exp_providers` em `main.py`

2. Para usar uma fonte diferente de dados de guild:
   - Implemente a interface `GuildMemberProvider`
   - Use a nova implementação ao criar o `GuildExpCalculator` em `main.py`

## Observações

- O script considera tanto EXP ganha quanto perdida
- Os resultados mostram o balanço total (ganhos - perdas) para cada guild monitorada
- Os resultados são mostrados na saída do terminal
