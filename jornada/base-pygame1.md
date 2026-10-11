# Base de código do `pygame` (save 1, zerado) → uso no `pygame2`

Estudado em 2026-10-10. Fonte: `Saves/pygame/*.py` (48 scripts + `__builtins__.py`, 5.826 linhas) e `Saves/pygame/save.json` (162 desbloqueios) contra `Saves/pygame2/save.json` (40 desbloqueios hoje).
A coleção curada e traduzida desses scripts está em `../farms/` (ver `../farms/README.md`). Esta página diz **o que cada script exige** e **quando ele passa a rodar** no `pygame2`.

## Como o cruzamento foi feito (e o limite dele)

Os desbloqueios do jogo têm ids com nome de função/palavra da linguagem: `harvest`, `move`, `def`, `for`, `global`, `get_pos_x`, `spawn_drone`, `north`, `bush`, `gray_hat`… O que o `pygame2` tem hoje é pouco: `while`, `if/else/elif`, `true/false`, `break`, `continue`, `loops`, `can_harvest`, `harvest`, `pass`, `do_a_flip`, `pet_the_piggy`, `hats`, `change_hat` e alguns chapéus.

Para cada script, procurei cada palavra dele que também é um id de desbloqueio e vi quais faltam. **É uma heurística:** palavras soltas como `list`, `power`, `gold` usadas como nome de variável contam como exigência, então o número de itens faltando pode ser um pouco maior que o real. **Não confirmado** no jogo que ele realmente bloqueia o uso antes do unlock (no seu `main.py` isso ainda não foi testado com uma função bloqueada).

## Rodam hoje (nada falta)

| Script | O que é |
|---|---|
| `do no.py` | Demo de erro: `pet_the_piggy`, `do_a_flip`, `change_hat`, e chama `Make_Error()` (função que não existe, de propósito). Serve para ver a mensagem de erro do jogo. |

## Falta 1–2 desbloqueios (primeiros a liberar)

| Script | Falta | O que faz |
|---|---|---|
| `f0.py` | `clear` | Uma linha: `clear()`. |
| `f9.py` | `def` | `stack_overflow()` chamando a si mesma, para ver o estouro de pilha. |
| `ImportZyklus.py` + `ImportzyklusZubehör.py` | `def`, `import` | Dois arquivos que se importam em ciclo. Demonstra importação circular. |
| `f5.py`, `f16.py` | `leaderboard_run`, `leaderboards` | Só chamam `leaderboard_run(Leaderboards.Fastest_Reset, nome, 1000)`. |

## Falta 6–15 (meio de partida)

| Script | Falta (resumo) | O que faz |
|---|---|---|
| `Fashionshow.py` | `def`, `move`, `spawn_drone`… | Desfile de chapéus: cada drone troca de chapéu por coluna. |
| `f7.py` | `for`, `def`, `range`, `spawn_drone`… | 32 drones fazendo `do_a_flip()` em loop. Teste de carga. |
| `f6.py` | `plant`, `bush`, `use_item`, `weird_substance`, `num_unlocked` | 3 linhas: planta arbusto e usa Weird Substance (cria labirinto). |
| `f4.py`, `bone_farm.py` | movimento, `set_world_size`, `dinosaur_hat` | Percurso fixo do chapéu de dinossauro para ossos. |
| `plantacoes.py` | `plant`, `till`, `get_water`, `use_item`, enums | Biblioteca de funções `plant_grass/tree/carrot/pumpkin/sunflower/cactus/apple`. É o ponto de partida natural para quando liberar `def`+`plant`. |

## Falta 18–30 (precisa de funções, listas, vários drones)

`Girassol.py` (colunas de girassol com `spawn_drone`), `f8.py` (abóboras em varredura 32×32), `Hay.py`/`Carrot.py`/`Wood.py` (plantio por **companheiro** com `get_companion`, dicionários de mapeamento e 31 drones), `abobora.py` (megaabóbora: confere duas casas com `measure()` e fertiliza), `Cactus.py`, `testecacto1/2.py`, `cactus_farm.py`, `Wrong Order.py` (cacto ordenado por insertion sort / cocktail sort com 32 drones), `sunflower_farm.py`, `sunflower_farm15.py` (quer 15 pétalas, bônus ×5), `Labyrinthmaster.py`, `maze_farm.py`, `maze.py`, `2MGOLD.py`, `f2/f3/f10…f17.py` (labirinto e ouro com muitos drones), `Weird_Substance_Farm.py`, `polyculture_farm_c.py`, `pumpkin_farm.py`, `dino.py` (jogo do dinossauro, 235 linhas).

## Falta 40–56 (fim de jogo)

`f14.py`, `leaderboard_run.py`, `BASIC_FULL_RESET.py`, `simulate.py` (os dois últimos são cópias idênticas): o script que **joga o jogo inteiro do zero**.

## O que o `BASIC_FULL_RESET.py` ensina sobre ordem de desbloqueio

Ele roda com `Speed` e `Plant` em zero e desbloqueia nesta ordem (isso é a ordem de uma corrida otimizada, **não** uma obrigação):
`Speed → Plant → Carrots → Speed → Watering → Trees → Speed → Expand → Expand → Speed → Fertilizer → Pumpkins → Expand → Fertilizer ×2 → Grass → Trees → Carrots → Speed → Watering → Fertilizer → Grass → Trees → Carrots → Pumpkins → Watering → Cactus ×2 → Dinosaurs ×2 → Mazes → Leaderboard`

Padrões úteis que o script mostra:
- `get_cost(tech)` devolve o custo (dict item→quantidade) e `unlock(tech)` compra.
- `sow_tile(...)`: **preparar o solo** (`till()` só se o solo estiver errado), **regar** só se `get_water() < 0.5`, **plantar** só se não houver a planta certa. Ele checa antes de agir para não gastar 200 ticks à toa.
- Grama e arbusto vão em grassland; o resto em soil (`get_ground(entity)`).
- Labirinto pelo método da "mão na parede": tenta virar à direita, depois seguir, depois à esquerda, depois voltar.
- Dinossauro: percurso fixo `dinLoop` de direções.

## Padrões que se repetem nos scripts (vale aprender)

1. **Checar antes de agir:** `if get_ground_type() != Grounds.Soil: till()` e `if can_harvest(): harvest()`. Cada ação que dá certo custa 200 ticks; a que falha, 1.
2. **Vários drones por coluna:** `for i in range(get_world_size()-1): spawn_drone(tarefa); move(East)` e depois a tarefa roda no drone principal. Enquanto `num_drones() >= max_drones()`, espera.
3. **`wait_for(drone)`** em vez de laço de espera ocupada, quando precisa juntar os drones.
4. **Mover pelo caminho curto** (`Wrong Order.py`, `_shortest_delta`): como o mapa dá a volta, a distância é `(destino - atual) % tamanho`, e se passar da metade vai pelo outro lado.
5. **Companheiro:** `get_companion()` devolve `(entidade, (x, y))`; os scripts guardam isso em dicionários para plantar a cultura que a planta pede.
6. **Cactos** só rendem se estiverem em ordem; por isso a ordenação (insertion / cocktail) com `measure()` e `swap()`.

## Plano de uso

- Conforme o `pygame2` liberar uma função, olhe a tabela acima: o script que passar a ter 0 faltando é o próximo para testar. **Antes de rodar, ler, entender e reescrever com suas palavras** (a ideia é aprender, não copiar).
- Os scripts do `pygame` são do seu save; o código descompilado do jogo é do Timon e fica só local (regra do `jornada/README.md`).
- Quando você liberar `plant` e `def`, o primeiro candidato é `plantacoes.py`. Depois `f6.py` e `Girassol.py`.
