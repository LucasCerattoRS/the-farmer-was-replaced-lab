# Leaderboards

A meta-camada do end-game: um alvo fixo para um recurso (ou, no caso do `Fastest_Reset`, para
automação completa), cronometrado e rodado isolado do seu save normal.

## Como o `leaderboard_run` funciona

```python
def leaderboard_run(leaderboard: Leaderboard, file_name: str, speedup: float) -> None
```

Inicia uma **run cronometrada e isolada** de `file_name` para o `leaderboard` dado. O
`speedup` define o multiplicador de velocidade inicial (mesma escala de
`set_execution_speed` — `1` é sem boost, mais alto roda mais rápido). Custa 200 ticks para
iniciar e devolve `None` — a run em si executa o arquivo nomeado a partir de um estado limpo
apropriado àquele leaderboard, e o cronômetro que vale pro ranking corre independente do seu
save vivo.

```python
leaderboard_run(Leaderboards.Fastest_Reset, "full_run", 256)
```

O `farms/leaderboards/launcher.py` deste repo é o script de lançamento inteiro de uma
tentativa de `Fastest_Reset`:

```python
leaderboard_run(Leaderboards.Fastest_Reset, "leaderboard_run", 1000)
```

— ele só dispara o `leaderboard_run.py` (a automação de verdade) no speedup inicial máximo.

## Cada board e sua meta

Direto das docstrings de `Leaderboards` no `__builtins__.py`:

| Leaderboard | Meta | Modo |
|---|---|---|
| `Fastest_Reset` | *"A categoria mais prestigiada. Automatize completamente o jogo, de um único canteiro até destravar os leaderboards de novo."* | — |
| `Cactus` | Farmar 33.554.432 cactos | Múltiplos drones |
| `Cactus_Single` | Farmar 131.072 cactos | Um drone, fazenda 8×8 |
| `Carrots` | Farmar 2.000.000.000 cenouras | Múltiplos drones |
| `Carrots_Single` | Farmar 100.000.000 cenouras | Um drone, fazenda 8×8 |
| `Dinosaur` | Farmar 33.488.928 ossos | Múltiplos drones |
| `Hay` | Farmar 2.000.000 de feno | Múltiplos drones |
| `Hay_Single` | Farmar 10.000.000 de feno | Um drone, fazenda 8×8 |
| `Maze` | Farmar 9.863.168 de ouro | Múltiplos drones |
| `Maze_Single` | Farmar 616.448 de ouro | Um drone, fazenda 8×8 |
| `Pumpkins` | Farmar 2.000.000 de abóboras | Múltiplos drones |
| `Pumpkins_Single` | Farmar 1.000.000 de abóboras | Um drone, fazenda 8×8 |
| `Sunflowers` | Farmar 10.000 de power | Múltiplos drones |
| `Sunflowers_Single` | Farmar 10.000 de power | Um drone, fazenda 8×8 |
| `Wood` | Farmar 10.000.000.000 de madeira | Múltiplos drones |
| `Wood_Single` | Farmar 500.000.000 de madeira | Um drone, fazenda 8×8 |

## Regras single vs. multi

Toda categoria com uma contraparte `_Single` roda numa **fazenda 8×8 fixa com exatamente um
drone** — sem truques de throughput de `Megafarm`, sem divisão por colunas. A versão não-`_Single`
da mesma categoria roda no tamanho cheio da sua fazenda com o teto completo de drones e (exceto
em `Sunflowers`, onde as duas variantes dividem a mesma meta de 10.000 de power) mira um número
dramaticamente maior pra compensar a escala extra disponível.

Isso significa que estratégias de um drone e de múltiplos drones para o *mesmo recurso* são
programas genuinamente diferentes: uma run de `Cactus_Single` não pode se apoiar na ordenação
por linha/coluna sincronizada por barreiras descrita em
[Ordenação de Cactos](cactus-sorting.md#ordenacao-multi-drone-com-barreiras) — ela tem que
ordenar e colher em cadeia com um drone só, num tabuleiro bem menor.

## Estrutura prática de uma run

O `farms/leaderboards/leaderboard_run.py` é a automação de referência de `Fastest_Reset`: ele
detecta uma run limpa (`num_unlocked(Unlocks.Speed) == 0 and num_unlocked(Unlocks.Plant) == 0`)
e, se for o caso, dispara o `slowest_automation()` — uma sequência fixa de chamadas de
`unlock_tech()`, cada uma farmando os itens que `get_cost()` exigir antes de gastá-los:

```python
def unlock_tech(tech):
    ct = get_cost(tech)
    for c in ct:
        farm_item(c, ct[c])
    if not unlock(tech):
        unlock_tech(tech)   # tenta de novo — get_cost() pode mudar conforme os preços escalam
```

Se o arquivo for rodado fora de um contexto de `leaderboard_run`/`simulate` (ou seja, essas
contagens de unlock já são diferentes de zero), ele imprime uma mensagem de guarda em vez de
fazer qualquer coisa — o `slowest_automation()` assume um estado limpo e corromperia um save
vivo caso contrário.

Veja também: [Simulação](simulation.md) — o jeito recomendado de ensaiar uma tentativa de
leaderboard antes de gastar um slot real de `leaderboard_run()`, e
[Estratégias de Leaderboard](../guides/leaderboard-strategies.md) para táticas por board tiradas
dos scripts em `farms/leaderboards/`.
