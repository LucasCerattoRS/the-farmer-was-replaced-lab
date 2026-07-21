# Tutorial 05 · Polyculture Optimization

**Goal:** run a companion-driven farm across 8 drones without them fighting each other.
**Requires:** Polyculture, Megafarm, Dictionaries/Lists, Watering.

The mechanic itself is on [Polyculture](../mechanics/polyculture.md). This page is the
engineering: `farms/crops/carrot_polyculture_32x32.py` is a 32×32, 8-drone companion farm,
and it is interesting mostly because of the two bugs it had to fix to work.

## The problem: a request names a tile you are not on

`get_companion()` tells you *which* entity a plant wants and *where* it wants it — and that
tile is almost never the one under the drone. So a request has to be **remembered** until
some drone's sweep reaches that tile. This script keeps one global queue:

```python
pedidos = []   # "requests": list of (x, y, entity_type)
```

`pedidos` is a plain global, which means **all 8 drones share it**. A request logged by the
drone on column 12 gets fulfilled by whichever drone reaches that tile first. That is the
whole coordination model — no messaging, no ownership, just one list.

## Bug 1 — the grass loop

The file's own header records the fix:

```text
# Correcao: Forca o uso de till() para evitar loop de grama
```

Carrots need `Grounds.Soil`. Grass grows on anything. If you plant a carrot without checking
the ground type, the plant silently fails, the tile stays grass, the next sweep sees "not a
carrot" and tries again — **forever**. The drone looks busy and produces nothing.

The fix is to make ground preparation conditional on what you are planting:

```python
def plantar_firme(tipo):
    ent = get_entity_type()
    if ent == tipo:
        return                     # already right — cheapest possible path
    if ent != None:
        harvest()                  # something else is here; clear it

    if tipo == Entities.Grass:
        pass                       # grass grows anywhere
    else:
        garantir_solo_arado()      # everything else demands Soil

    plant(tipo)
    regar_se_preciso()
```

!!! warning "Silent failures are the expensive ones"
    `plant()` returning falsy on the wrong ground does not crash anything — it just makes an
    infinite loop that looks like a working farm. When a farm "runs" but the numbers don't
    move, check that every `plant()` is preceded by the ground check its crop actually needs.

Note the early `return` when the tile is already correct. On a mature field that is the
common case, and skipping straight past `harvest`/`till`/`plant` is most of the throughput.

## Bug 2 — mutating a list while iterating it

Fulfilling a request means removing it from the queue. Doing that inside a loop over the same
list skips elements — the classic mistake. The script iterates a **copy**:

```python
def atender_pedidos():
    x = get_pos_x()
    y = get_pos_y()
    lista_copia = list(pedidos)      # safe copy

    for item in lista_copia:
        px, py, ptype = item
        if px == x and py == y:
            plantar_firme(ptype)
            if item in pedidos:      # another drone may have taken it already
                pedidos.remove(item)
            return True
    return False
```

Two separate protections there, and the second is the one people forget: `if item in pedidos`
before removing. Because the queue is shared, **another drone may have fulfilled and removed
that exact request** between the copy and the removal. Removing blindly would fail.

## Probing: plant, then ask what it wants

```python
def modo_sonda_cenoura():
    plantar_firme(Entities.Carrot)
    comp = get_companion()
    if comp != None:
        tipo_vizinho, (tx, ty) = comp
        ja_existe = False
        for (px, py, _) in pedidos:
            if px == tx and py == ty:
                ja_existe = True
                break
        if not ja_existe:
            pedidos.append((tx, ty, tipo_vizinho))
```

Plant first, *then* read the companion request — a bare tile has nothing to ask for. The
dedup scan matters for the same reason as the removal guard: with 8 drones probing
concurrently, the same target tile gets requested repeatedly, and an unbounded queue would
grow faster than it drains.

## Priority order per tile

The per-tile brain is a strict priority list, and the order is the design:

```python
def processar_bloco():
    x = get_pos_x()

    if x >= 30:                        # last two columns: sunflower strip
        garantir_solo_arado()
        regar_se_preciso()
        if get_entity_type() != Entities.Sunflower:
            plant(Entities.Sunflower)
        else:
            if can_harvest():
                harvest()
        return

    if can_harvest():                  # 1. take what's ready
        harvest()

    fez_pedido = atender_pedidos()     # 2. serve a neighbour's request

    if not fez_pedido:                 # 3. otherwise, be a carrot
        if get_entity_type() != Entities.Carrot:
            modo_sonda_cenoura()
```

Requests outrank planting your own crop. If they didn't, a tile that some carrot is waiting
on would get overwritten with another carrot on every pass and the companion bonus would
never land.

Columns 30–31 are carved out as a **sunflower strip** — Power income running alongside the
carrot polyculture, on the same drones, because Power is what pays for execution speed.

## Deploying the 8 drones

The movement is a boustrophedon over 4 columns (up, east, down, east, up, east, down, then
three steps west to reset), and deployment uses a closure factory:

```python
def criar_runner(col):
    def run():
        worker_4_cols(col)
    return run

for i in range(1, 8):
    c = i * 4
    while get_pos_x() < c:
        move(East)
    spawn_drone(criar_runner(c))
```

The scripts in this repo don't pass arguments to a drone task, so `criar_runner(col)` builds a
zero-argument closure that already knows its column. That pattern shows up across this repo —
its minimal demonstration is on
[Language Quirks](../mechanics/language-quirks.md#closures-are-how-you-parameterize-a-drone).

## When to bother

Polyculture is bookkeeping, and bookkeeping competes with throughput. It wins on flat-yield
crops (carrots, hay) where the companion bonus is the only multiplier available. It loses on
pumpkins and cactus, whose fusion/chain rules already scale super-linearly — see
[when polyculture beats monoculture](../mechanics/polyculture.md#when-polyculture-beats-monoculture).
