# Tutorial 01 · Farming Multi-Drone (o padrão de divisão por colunas)

**Objetivo:** transformar qualquer farm de um drone só numa farm de N drones, com ganho quase linear.
**Requer:** unlock de Megafarm (`spawn_drone`), Functions, Loops.

## A ideia

Um drone varrendo um campo 32×32 anda 1024 tiles por passada. Oito drones, cada um dono de
uma **faixa vertical de 4 colunas**, andam 128 tiles cada — em paralelo. Quase toda farm de
end-game deste repo (abóboras, girassóis, cactos, policultura) é construída em cima desse
único padrão.

## Passo 1 — escreva o worker em função da posição dele

O truque: um drone criado começa **onde o spawner está parado**. Então o worker só lê o
próprio `get_pos_x()` e reivindica as colunas a partir dali.

```python
def worker():
    size = get_world_size()
    cols = 4  # colunas por drone
    x0 = get_pos_x()
    while True:
        for dx in range(cols):
            for _ in range(size):
                if can_harvest():
                    harvest()
                if get_water() < 0.5:
                    use_item(Items.Water)
                plant(Entities.Sunflower)
                move(North)
            move(East)
```

## Passo 2 — o spawner caminha e planta drones

```python
def deploy():
    size = get_world_size()
    drones = []
    while get_pos_x() % 4 != 0:
        move(East)
    for i in range(min(max_drones(), size // 4)):
        d = spawn_drone(worker)
        if d != None:
            drones.append(d)
        for _ in range(4):
            move(East)
    return drones

deploy()
```

## Passo 3 — coordenação (opcional, mas poderoso)

- `wait_for(drone)` — bloqueia até um worker retornar (ex.: "colhi minha faixa uma vez").
- `has_finished(drone)` — consulta os workers enquanto um **drone-chefe** faz trabalho global.
  A megafarm de abóbora daqui usa um chefe que só confere a mega-abóbora em (0,0)
  enquanto os workers replantam os tiles mortos.

## Armadilhas aprendidas na marra

1. `spawn_drone` retorna `None` quando você está no teto de drones — sempre confira antes de dar append.
2. O mundo é um **toro**: um worker que passa da própria faixa corrompe a faixa do vizinho.
   Mantenha os loops limitados por `size`, nunca por `while can_move(...)`.
3. Compartilhamento de água: tiles vizinhos equalizam; regar um tile sim, um não é quase tão
   bom e custa metade.

Exemplos completos e funcionando no repo: `farms/crops/sunflower_farm.py`,
`farms/crops/pumpkin_megafarm.py`, `farms/crops/carrot_polyculture_32x32.py`.
