# Simulação

`Unlocks.Simulation` — *"Destrava funções de simulação para testes e otimização."*
`simulate()` roda uma instância headless e descartável de um arquivo com um estado inicial
escolhido, e devolve só o resultado de tempo — a ferramenta para testar uma estratégia sem
encostar no seu save vivo nem gastar uma tentativa real de `leaderboard_run()`.

## Assinatura

```python
def simulate(
    filename: str,
    sim_unlocks: Dict[Unlocks, float] | Iterable[Unlocks] | type[Unlocks],
    sim_items: Dict[Item, float],
    sim_globals: Dict[str, Any],
    seed: float,
    speedup: float,
) -> float
```

Custa 200 ticks para iniciar; devolve o **tempo decorrido da simulação** (um `float`, nas
mesmas unidades de `get_time()`).

## Parâmetros

| Parâmetro | Tipo | Significado |
|---|---|---|
| `filename` | `str` | O arquivo a rodar, exatamente como o `leaderboard_run` recebe. |
| `sim_unlocks` | dict de `Unlocks -> nível`, um iterável de `Unlocks`, ou a classe `Unlocks` inteira | O estado inicial de unlocks. Um dict deixa você definir níveis específicos (ex.: `{Unlocks.Speed: 3}`); um iterável/classe pura concede os unlocks no nível base. |
| `sim_items` | `Dict[Item, float]` | Inventário inicial — mapeia cada item para uma quantidade de partida. |
| `sim_globals` | `Dict[str, Any]` | Valores iniciais das variáveis globais no escopo de `filename` — permite injetar estado que o script espera sem editar o arquivo. |
| `seed` | número | A semente aleatória. **Precisa ser um inteiro positivo.** Controla toda chamada de `random()` dentro da simulação, tornando reprodutíveis os resultados de fusão de abóbora, o timing de crescimento de cacto, os sorteios de pétala de girassol etc. |
| `speedup` | número | Multiplicador inicial de velocidade de execução, mesma escala de `set_execution_speed`. |

## Exemplo de chamada

Direto do stub da API:

```python
filename = "f1"
sim_unlocks = Unlocks
sim_items = {Items.Carrot: 10000, Items.Hay: 50}
sim_globals = {"a": 13}
seed = 0
speedup = 64
run_time = simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)
```

## Casos de uso

- **Teste A/B de estratégia.** Rode o mesmo script alvo duas vezes com dois `sim_globals`
  diferentes (ex.: larguras de coluna diferentes para uma implantação de drones, ou limiares
  de água diferentes) e compare os tempos devolvidos direto — sem precisar resetar uma
  fazenda real entre as tentativas.
- **Caça a seeds.** Como `seed` é um parâmetro obrigatório e explícito, dá pra iterar sobre
  seeds candidatas e guardar as que produzem resultados aleatórios favoráveis logo cedo (uma
  sequência de sorte na fusão de abóboras, um girassol de 15 pétalas cedo, conforme
  [Culturas & Economia](crops.md#girassois-power-petalas)) antes de se comprometer com aquela
  seed numa run de verdade.
- **Ensaio de leaderboard.** Como `simulate()` compartilha o formato de `filename`/injeção de
  estado com `leaderboard_run()`, é o jeito natural de ensaiar um script de leaderboard —
  alimente com os mesmos unlocks/itens iniciais que uma tentativa real teria, e leia o tempo
  antes de gastar uma run viva. Veja [Leaderboards](leaderboards.md#como-o-leaderboard_run-funciona).

## Limites

- `seed` precisa ser um inteiro positivo — não existe modo "sem semente"; toda simulação é
  reprodutível por construção.
- A simulação é limitada ao que `filename` de fato faz — não é um sandbox genérico de
  "e se"; ela *executa* o script alvo sob as condições iniciais dadas e reporta só o tempo
  decorrido, não um traço do estado intermediário. Se você precisa de visibilidade
  intermediária, instrumente o próprio script alvo (ex.: via `sim_globals` ou `quick_print`)
  em vez de depender só do retorno de `simulate()`.
- Exige `Unlocks.Simulation`, o que restringe essa ferramenta a uma fase de late-game — veja o
  [guia de Progressão](../guides/progression.md).

Veja também: [Leaderboards](leaderboards.md) e
[Estratégias de Leaderboard](../guides/leaderboard-strategies.md) para scripts concretos que
valem um ensaio com `simulate()` antes de uma tentativa real.
