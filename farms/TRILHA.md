# Trilha de scripts — do mais simples ao avançado

Uma ordem de estudo para os scripts de `farms/`. Cada degrau tem **um conceito central**, o
script para ler e **3 exercícios**. Os exercícios são propostas de prática (não há gabarito no
repo); rode sempre no jogo, num save que você não se importe de bagunçar.

Antes de qualquer degrau, confira a API em [`lib/__builtins__.py`](lib/__builtins__.py) —
`python tools/validar_stub.py <arquivo>` avisa se você chamou algo que o stub não tem.

| # | Script | Conceito |
|---|---|---|
| 1 | `jornada/codigo/main.py` | laço infinito + decisão com `if` |
| 2 | `basics/experiments/hat_parade.py` | funções, `spawn_drone` e `%` |
| 3 | `basics/plant_helpers.py` | funções reutilizáveis e preparo do solo |
| 4 | `basics/pumpkin_solo.py` | varredura 2D com um drone |
| 5 | `crops/sunflower_power_simple.py` | divisão por colunas com vários drones |
| 6 | `crops/pumpkin_megafarm_v3.py` | sincronizar drones com `wait_for` |
| 7 | `crops/cactus_insertion_sort.py` | algoritmo clássico no mundo físico |
| 8 | `crops/carrot_polyculture.py` | estado entre iterações e `get_companion` |
| 9 | `mazes/treasure_wall_follower.py` | busca em labirinto sem mapa |
| 10 | `dinosaur/apple_solver.py` | planejar uma rota inteira |
| 11 | `leaderboards/fastest_reset.py` | automação completa do zero |

## 1. Laço e decisão — `jornada/codigo/main.py`
**Conceito:** `while True` mantém o drone trabalhando; `can_harvest()` decide entre colher e
fazer outra coisa. Sem `move`, o drone fica parado no mesmo tile.
**Exercícios:**
1. Troque o `else` para plantar `Entities.Grass` em vez de trocar de chapéu.
2. Faça o drone andar um tile para o `North` a cada volta e observe o que acontece na borda.
3. Conte quantas colheitas fez e use `print` a cada 10.

## 2. Funções e múltiplos drones — `basics/experiments/hat_parade.py`
**Conceito:** `spawn_drone(f)` recebe uma função sem argumentos; `get_pos_x() % 5` escolhe um
item da lista pela coluna.
**Exercícios:**
1. Use `get_pos_y()` em vez de `get_pos_x()` e compare o resultado.
2. Limite o número de drones a `max_drones()` testando o retorno de `spawn_drone`.
3. Faça cada drone andar `East` em vez de `North`.

## 3. Helpers de plantio — `basics/plant_helpers.py`
**Conceito:** isolar "preparar o solo + plantar" em funções pequenas
(`get_ground_type`, `till`, `plant`).
**Exercícios:**
1. Escreva `plant_cactus()` seguindo o mesmo molde.
2. Crie `plant_any(entidade)` que escolhe o solo certo para cada cultura.
3. Adicione rega condicional com `get_water()` a um helper que ainda não rega.

## 4. Varredura 2D — `basics/pumpkin_solo.py`
**Conceito:** dois `for` aninhados percorrem o campo; `get_world_size()` evita números fixos.
**Exercícios:**
1. Troque as constantes `WIDTH, HEIGHT` por `get_world_size()`.
2. Faça a varredura em zigue-zague (sem voltar ao início da coluna).
3. Meça os ticks de uma volta completa com `get_tick_count()`.

## 5. Divisão por colunas — `crops/sunflower_power_simple.py`
**Conceito:** um drone por coluna; o drone "mãe" avança `East` e deixa um filho em cada uma.
**Exercícios:**
1. Adapte para cenouras mantendo a divisão por colunas.
2. Faça cada drone cuidar de duas colunas.
3. Pare o laço quando `num_items(Items.Power)` chegar a um alvo menor que o do script.

## 6. Sincronização — `crops/pumpkin_megafarm_v3.py`
**Conceito:** `wait_for(drone)` bloqueia até o drone terminar; `measure()` compara ids para
saber se abóboras se fundiram.
**Exercícios:**
1. Guarde os retornos de `wait_for` e imprima-os.
2. Troque a espera por `has_finished` num laço e compare o custo.
3. Reduza o mundo com `set_world_size` e veja o que quebra primeiro.

## 7. Ordenação de cactos — `crops/cactus_insertion_sort.py`
**Conceito:** ordenação por inserção usando `swap(direction)` e `measure()`; depois compare
com `cactus_shaker_sort.py`.
**Exercícios:**
1. Escreva em papel a ordem de trocas para a linha `[3, 1, 2]`.
2. Conte as trocas feitas numa linha e compare com o shaker sort.
3. Implemente um bubble sort por linha e compare com `cactus_bubble_22x22.py`.

## 8. Estado e policultura — `crops/carrot_polyculture.py`
**Conceito:** `get_companion()` devolve `(entidade, (x, y))`; dicionários guardam o que cada
tile precisa.
**Exercícios:**
1. Registre quantas vezes `get_companion()` devolveu `None`.
2. Faça um mapa só de leitura: percorra o campo e imprima o dicionário.
3. Compare com `hay_polyculture.py` e liste o que muda.

## 9. Labirinto sem mapa — `mazes/treasure_wall_follower.py`
**Conceito:** regra da mão na parede, com `can_move` e giros horário/anti-horário; vários
drones com preferências diferentes.
**Exercícios:**
1. Escreva `rotate_ccw` espelhando `rotate_cw`.
2. Rode com 1 drone e depois com 8 e compare os ticks.
3. Leia `treasure_hunt_8drones_buy.py` e explique por que o estoque de Weird Substance
   precisa ser checado antes de `use_item`.

## 10. Planejar rota — `dinosaur/apple_solver.py`
**Conceito:** fila de posições, estágios (rota "ondulada" e depois agressiva) e conjuntos de
colunas proibidas.
**Exercícios:**
1. Desenhe a rota do primeiro estágio num tabuleiro 6×6.
2. Teste com `set_world_size(6)` e veja quando o jogo termina.
3. Compare com `bone_snake_solo.py` (zigue-zague fixo).

## 11. Automação completa — `leaderboards/fastest_reset.py`
**Conceito:** orquestrar desbloqueios (`unlock`, `get_cost`) e várias lavouras em sequência.
**Exercícios:**
1. Liste, só lendo, a ordem dos desbloqueios e justifique-a.
2. Troque um desbloqueio de lugar e preveja o efeito no tempo total.
3. Use `simulate` (veja o stub) para comparar duas ordens sem gastar o save.
