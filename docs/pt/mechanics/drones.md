# Drones

Tudo depois do começo do jogo é um problema de throughput multi-drone. Esta página cobre as
primitivas (`spawn_drone`, `wait_for`, `has_finished`, `max_drones`) e os dois padrões
construídos em cima delas que aparecem em quase todo script de `farms/`.

## As primitivas

| Função | Comportamento |
|---|---|
| `spawn_drone(function)` | Cria um drone novo **na posição do drone que chamou**, rodando `function`. Devolve um handle, ou `None` se você já estiver no teto. Custa 200 ticks se um drone foi criado, 1 caso contrário. |
| `wait_for(drone)` | Bloqueia até `drone` terminar, e devolve o que a função dele retornou. 1 tick se já terminou. |
| `has_finished(drone)` | Checagem de término que não bloqueia — `True`/`False`. Use pra consultar os workers enquanto faz outra coisa. |
| `max_drones()` / `num_drones()` | Teto / contagem ativa no momento. |

## Herança da posição de spawn

O fato mais importante de todos: **um drone criado começa exatamente onde o criador está
parado.** Não existe chamada "spawn em (x, y)" — você chega lá *andando com o criador até o
tile certo antes de chamar* `spawn_drone`. Todo loop de implantação deste repo é uma
variação de:

```python
for n in range(1, num_workers):
    target_x = n * cols_per_drone
    while get_pos_x() < target_x:
        move(East)
    spawn_drone(worker)
```

Como o worker herda o tile de spawn, ele consegue descobrir a própria região só com
`get_pos_x()` / `get_pos_y()` na largada — nenhuma coordenada precisa ser passada como
argumento (funções passadas pra `spawn_drone` não recebem parâmetros).

## O padrão de divisão por colunas

O padrão cavalo-de-batalha por trás de `sunflower_farm.py`, `pumpkin_megafarm.py`,
`carrot_polyculture_32x32.py` e da maior parte de `farms/crops/`: divide um campo de largura
N em `N / cols_per_drone` faixas verticais, um drone por faixa, cada um varrendo a sua com
um caminho bustrofédon (sobe-desce-sobe-desce) pra nunca precisar de movimento diagonal:

```python
def worker():
    size = get_world_size()
    cols = 4
    x0 = get_pos_x()
    while True:
        for dx in range(cols):
            for _ in range(size):
                if can_harvest():
                    harvest()
                plant(Entities.Sunflower)
                move(North)
            move(East)
```

8 drones × 4 colunas cobrem um campo 32×32 com ganho quase linear sobre um drone só.
Veja o [Tutorial 01 · Farming Multi-Drone](../tutorials/01-multi-drone.md) para o passo a passo completo.

## O padrão drone-chefe

Alguns trabalhos precisam de exatamente **um** drone dono de um pedaço de estado global —
por exemplo, decidir quando uma mega-abóbora fundida está grande o bastante pra colher.
`pumpkin_megafarm.py` e `pumpkin_megafarm_v2.py` dedicam a essa checagem o drone que fica em
`(0,0)`, enquanto todo drone operário só replanta tiles mortos e nunca colhe a mega-abóbora
viva:

```python
def verificar_mega_abobora():
    # Roda exclusivamente em (0,0)
    if can_harvest():
        tamanho = measure()
        if tamanho != None and tamanho > ALVO_COLHEITA:
            harvest()
```

O chefe faz a própria varredura do campo como qualquer worker, mas só *este* drone chama
`measure()`/`harvest()` no tile da fusão — evitando uma corrida em que dois drones decidem
colher a mesma mega-abóbora no meio da fusão.

`wait_for()` e `has_finished()` generalizam isso em barreiras de sincronização: os scripts de
ordenação de cactos criam um drone por linha, dão `wait_for` em todos, *aí* criam um por
coluna para a fase seguinte — veja [Ordenação de Cactos](cactus-sorting.md#ordenacao-multi-drone-com-barreiras).

## Armadilhas aprendidas na marra

1. **`spawn_drone` devolve `None` no teto de drones.** Todo loop de implantação deveria
   conferir o retorno (ou checar `num_drones() < max_drones()`) antes de assumir que o worker
   existe — dar append de `None` numa lista de drones e depois chamar `wait_for(None)` quebra.
2. **O mundo é um toro.** `move()` dá a volta nas bordas em vez de falhar. Um worker com o
   limite do loop errado por um, ou que faz loop em `while can_move(...)` em vez de um
   `range(size)` fixo, entra direto na faixa do drone vizinho e corrompe ela. Todo worker de
   divisão por colunas acima limita os loops internos por `get_world_size()`, nunca por uma
   checagem de movimento bem-sucedido.
3. **Água/fertilizante são por tile.** Um drone só afeta o tile onde está pisando — não há
   área de efeito, então a conta de cobertura (quantos tiles por drone, de quanto em quanto
   tempo ele revisita) tem que considerar a água secando em tiles por onde o drone não passa
   há um tempo.
4. **Funções passadas pra `spawn_drone` não recebem argumentos.** Pra parametrizar um worker
   (ex.: "comece na coluna N"), os scripts ou leem `get_pos_x()` na largada (o truque de
   herança acima) ou constroem a função dinamicamente — veja as closures `make_runner(col)`
   em `pumpkin_megafarm_v2.py` e `sunflower_15petals.py`.

## Scripts de referência

- [`farms/crops/sunflower_farm.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/crops/sunflower_farm.py) — divisão por colunas com 8 drones, limpa, sem chefe.
- [`farms/crops/pumpkin_megafarm.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/crops/pumpkin_megafarm.py) — padrão drone-chefe para colheita de fusão.

Veja também: [Culturas & Economia](crops.md) para o que esses drones estão de fato cultivando, e
[Simulação](simulation.md) para ensaiar uma implantação de drones antes de rodar pra valer.
