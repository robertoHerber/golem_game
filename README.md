# Golems Ascendancy

**Gênero:** RTS Idle  
**Plataforma:** Python 3.8+, Pygame CE

Golems Ascendancy é um jogo de estratégia em tempo real com mecânicas *idle*, onde você cria e gerencia golems, coleta recursos e pesquisa tecnologias desde a Idade da Pedra até eras avançadas.

## Estrutura

- **game.py**: define estruturas de dados e inicializa o estado do jogo  
- **update.py**: contém toda a lógica de atualização diária (produção, consumo de fluxo, falhas, desbloqueios)  
- **names.py**: enumerações de recursos, trabalhos, conhecimentos e atributos  
- **gui.py**: interface gráfica em Pygame CE  

## Requisitos

```bash
pip install pygame-ce
```

## Execução

```bash
python gui.py
