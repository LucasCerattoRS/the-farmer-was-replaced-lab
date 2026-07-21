# Policultura

Plantio com companheiras: certas plantas rendem mais (ou precisam de menos manutenção)
quando uma *outra* planta específica cresce ao lado delas. `Unlocks.Polyculture` transforma
isso de curiosidade em estratégia de cultivo.

## O mecanismo `get_companion()`

```python
def get_companion() -> Tuple[Entity, Tuple[int, int]] | None
```

Chame `get_companion()` na planta sob o drone. Devolve `None` se aquela planta não tem
preferência de companheira agora, ou uma tupla `(tipo_da_companheira, (x, y))` — o tipo de
entidade que ela quer e o tile exato onde plantar. O tile pedido costuma ser adjacente à
planta que fez o pedido, mas a API só garante um par `(x, y)`, não um deslocamento fixo —
sempre leia a posição de volta em vez de assumir uma direção.

```python
companion = get_companion()
if companion != None:
    plant_type, (x, y) = companion
    print("Companheira:", plant_type, "em", x, ",", y)
```

## O padrão de mapeamento de companheiras

Como o pedido aponta um tile que não é aquele onde você está, um drone varrendo o campo não
consegue atender o pedido na hora — ele precisa **lembrar** dele até a varredura chegar
naquele tile. O `farms/crops/carrot_polyculture.py` resolve isso com dois dicionários
compartilhados entre os drones:

```python
companion_mapping = {}   # tile alvo -> tipo de entidade que ele deve virar
carrot_mapping = {}      # tile de origem -> tile alvo da companheira dele (pra limpeza)

def track_companion(curr_x, curr_y):
    result = get_companion()
    if result == None:
        return False
    target_entity, (target_x, target_y) = result
    if (target_x, target_y) not in companion_mapping:
        companion_mapping[(target_x, target_y)] = target_entity
        carrot_mapping[(curr_x, curr_y)] = (target_x, target_y)
        return True
    return False
```

Cada tile que o drone visita é conferido primeiro contra `companion_mapping` (planta o que
foi pedido), depois contra `carrot_mapping` (a companheira deste tile precisa ser religada
depois da colheita), e só cai no plantio de uma `Carrot` nova se nenhum dos dois se aplicar.
Como `companion_mapping`/`carrot_mapping` são globais simples, **todo drone da frota lê e
escreve no mesmo mapa** — um pedido registrado pelo drone 3 é atendido por qualquer drone
cuja varredura chegue naquele tile primeiro.

O `farms/crops/carrot_polyculture_32x32.py` roda a mesma ideia em escala 32×32 com 8 drones,
usando uma lista `pedidos` em vez de dois dicionários, mais uma faixa dedicada de girassóis
nas duas últimas colunas para renda de Power junto com a policultura de cenoura.

`farms/crops/hay_polyculture.py` e `weird_substance_polyculture.py` aplicam o mesmo padrão de
mapeamento para fins diferentes: o primeiro mantém um campo de grama alimentado com
companheiras de cenoura para feno; o segundo planta o que quer que `get_companion()` peça —
grama, arbusto, árvore ou cenoura — e colhe a Weird Substance que resulta disso, que é o
insumo com que os labirintos funcionam (veja [Labirintos & Ouro](mazes.md#cultivando-um-labirinto)).

## Rendimentos

O stub da API não publica um multiplicador exato para o bônus de companheira — encare de
forma qualitativa: uma planta com a companheira satisfeita rende **mais do que a mesma
planta cultivada sozinha**, e é por isso que as farms de cenoura/feno/árvore do end-game se
dão ao trabalho de toda a contabilidade acima em vez de rodar uma varredura de monocultura
lisa.

## Quando policultura ganha da monocultura

- **Vale a pena** assim que `Polyculture` está destravado e o campo é grande o bastante para
  que o overhead por tile (conferir dois dicionários a cada tile) seja barato em relação ao
  throughput de uma varredura multi-drone com divisão por colunas — veja [Drones](drones.md).
- **Não vale** em culturas cujo rendimento já escala de forma super-linear com a quantidade,
  como abóboras fundidas (n³) ou cactos ordenados (n² com colheita em cadeia) — o bônus de
  fusão/cadeia faz o que a companheira somaria parecer nada, e a contabilidade extra só
  compete pela atenção do drone contra o padrão que de fato gera aquele rendimento.
- O rastreamento de companheiras é inerentemente **stateful no campo inteiro**, então ele
  combina melhor com o padrão multi-drone de divisão por colunas, em que todos os workers
  compartilham um mapa global de pedidos, do que com algoritmos (como a ordenação de cactos)
  que exigem isolamento estrito por região entre drones.

Veja também: [Culturas & Economia](crops.md) para o que cada planta elegível a companheira faz
sozinha, e [Drones](drones.md) para a implantação por divisão de colunas em que esses scripts se apoiam.
