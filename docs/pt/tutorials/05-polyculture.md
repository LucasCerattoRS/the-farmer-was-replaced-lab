# Tutorial 05 · Otimização de Policultura

**Objetivo:** rodar uma farm guiada por companheiras em 8 drones sem que eles briguem entre si.
**Requer:** Polyculture, Megafarm, Dictionaries/Lists, Watering.

O mecanismo em si está em [Policultura](../mechanics/polyculture.md). Esta página é a
engenharia: o `farms/crops/carrot_polyculture_32x32.py` é uma farm de companheiras 32×32 com
8 drones, e ela é interessante principalmente por causa dos dois bugs que precisou corrigir
pra funcionar.

## O problema: o pedido aponta um tile onde você não está

O `get_companion()` diz *qual* entidade uma planta quer e *onde* ela quer — e esse tile quase
nunca é o que está sob o drone. Então um pedido precisa ser **lembrado** até a varredura de
algum drone chegar naquele tile. Este script mantém uma fila global:

```python
pedidos = []   # lista de (x, y, tipo_de_entidade)
```

`pedidos` é uma global simples, o que significa que **os 8 drones compartilham ela**. Um pedido
registrado pelo drone da coluna 12 é atendido por qualquer drone que chegue naquele tile
primeiro. Esse é o modelo de coordenação inteiro — sem mensagens, sem dono, só uma lista.

## Bug 1 — o loop da grama

O próprio cabeçalho do arquivo registra a correção:

```text
# Correcao: Forca o uso de till() para evitar loop de grama
```

Cenoura precisa de `Grounds.Soil`. Grama cresce em qualquer coisa. Se você planta cenoura sem
conferir o tipo de chão, o plantio falha silenciosamente, o tile continua grama, a varredura
seguinte vê "não é cenoura" e tenta de novo — **pra sempre**. O drone parece ocupado e não
produz nada.

A correção é tornar o preparo do terreno condicional ao que você vai plantar:

```python
def plantar_firme(tipo):
    ent = get_entity_type()
    if ent == tipo:
        return                     # ja esta certo — o caminho mais barato possivel
    if ent != None:
        harvest()                  # tem outra coisa aqui; tira

    if tipo == Entities.Grass:
        pass                       # grama cresce em qualquer lugar
    else:
        garantir_solo_arado()      # todo o resto exige Soil

    plant(tipo)
    regar_se_preciso()
```

!!! warning "Falha silenciosa é a cara"
    `plant()` devolvendo falso no chão errado não quebra nada — só cria um loop infinito que
    parece uma farm funcionando. Quando uma farm "roda" mas os números não mexem, confira se
    todo `plant()` é precedido pela checagem de chão que aquela cultura realmente exige.

Repare no `return` logo no começo, quando o tile já está correto. Num campo maduro esse é o
caso comum, e pular direto por cima de `harvest`/`till`/`plant` é a maior parte do throughput.

## Bug 2 — mutar uma lista enquanto itera nela

Atender um pedido significa removê-lo da fila. Fazer isso dentro de um loop sobre a mesma
lista pula elementos — o erro clássico. O script itera sobre uma **cópia**:

```python
def atender_pedidos():
    x = get_pos_x()
    y = get_pos_y()
    lista_copia = list(pedidos)      # copia segura

    for item in lista_copia:
        px, py, ptype = item
        if px == x and py == y:
            plantar_firme(ptype)
            if item in pedidos:      # outro drone pode ja ter pegado
                pedidos.remove(item)
            return True
    return False
```

São duas proteções separadas ali, e a segunda é a que as pessoas esquecem: o `if item in
pedidos` antes de remover. Como a fila é compartilhada, **outro drone pode ter atendido e
removido exatamente aquele pedido** entre a cópia e a remoção. Remover às cegas falharia.

## Sondagem: planta, depois pergunta o que ela quer

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

Planta primeiro, *depois* lê o pedido de companheira — um tile vazio não tem o que pedir. A
varredura de duplicidade importa pelo mesmo motivo da guarda na remoção: com 8 drones sondando
ao mesmo tempo, o mesmo tile-alvo é pedido repetidamente, e uma fila sem limite cresceria mais
rápido do que esvazia.

## Ordem de prioridade por tile

O cérebro por tile é uma lista de prioridade estrita, e a ordem é o projeto:

```python
def processar_bloco():
    x = get_pos_x()

    if x >= 30:                        # duas ultimas colunas: faixa de girassol
        garantir_solo_arado()
        regar_se_preciso()
        if get_entity_type() != Entities.Sunflower:
            plant(Entities.Sunflower)
        else:
            if can_harvest():
                harvest()
        return

    if can_harvest():                  # 1. pega o que esta pronto
        harvest()

    fez_pedido = atender_pedidos()     # 2. atende pedido de vizinho

    if not fez_pedido:                 # 3. senao, seja cenoura
        if get_entity_type() != Entities.Carrot:
            modo_sonda_cenoura()
```

Pedidos têm prioridade sobre plantar a própria cultura. Se não tivessem, um tile que alguma
cenoura está esperando seria sobrescrito com outra cenoura a cada passada, e o bônus de
companheira nunca aconteceria.

As colunas 30–31 são separadas como **faixa de girassóis** — renda de Power correndo junto com
a policultura de cenoura, nos mesmos drones, porque é Power que paga a velocidade de execução.

## Implantando os 8 drones

O movimento é um bustrofédon sobre 4 colunas (sobe, leste, desce, leste, sobe, leste, desce, e
três passos a oeste pra voltar), e a implantação usa uma closure factory:

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

Os scripts deste repo não passam argumentos pra uma task de drone, então `criar_runner(col)`
constrói uma closure de zero argumentos que já sabe a própria coluna. Esse padrão aparece por todo o
repo — a demonstração mínima dele está em
[Peculiaridades da Linguagem](../mechanics/language-quirks.md#closures-sao-como-se-parametriza-um-drone).

## Quando vale o trabalho

Policultura é contabilidade, e contabilidade compete com throughput. Ela ganha em culturas de
rendimento plano (cenoura, feno), onde o bônus de companheira é o único multiplicador
disponível. Ela perde em abóbora e cacto, cujas regras de fusão/cadeia já escalam de forma
super-linear — veja
[quando policultura ganha da monocultura](../mechanics/polyculture.md#quando-policultura-ganha-da-monocultura).
