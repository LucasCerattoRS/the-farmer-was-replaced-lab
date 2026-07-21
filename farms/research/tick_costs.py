# PESQUISA: custo real em ticks por operacao
#
# INSTRUMENTO: get_tick_count() custa 0 ticks (doc oficial), entao a diferenca
# entre duas leituras e o custo EXATO da acao no meio - sem correcao.
#
# METODO: cada medicao roda com o tile num estado conhecido, porque varias
# operacoes tem dois precos ("200 se fez algo, 1 se nao fez nada").
#
# COMO RODAR: cole numa janela, aperte Execute, leia a janela de Output.
# Requer: Debug (quick_print). Nao precisa de drones.

def custo(rotulo, esperado, acao):
	# Mede uma acao de zero argumentos e compara com o custo documentado.
	t0 = get_tick_count()
	acao()
	t1 = get_tick_count()
	real = t1 - t0
	marca = "OK"
	if real != esperado:
		marca = "DIVERGE <<<"
	quick_print(rotulo + " | doc=" + str(esperado) + " | real=" + str(real) + " | " + marca)

# --- ACOES DE ZERO ARGUMENTOS (funcoes sao valores; ver Funcoes & Escopo) ---

def a_mover():
	move(North)

def a_medir():
	measure()

def a_pos():
	get_pos_x()

def a_tipo():
	get_entity_type()

def a_chao():
	get_ground_type()

def a_tamanho_mundo():
	get_world_size()

def a_tempo():
	get_time()

def a_ticks():
	get_tick_count()

def a_plantar_grama():
	plant(Entities.Grass)

def a_colher():
	harvest()

def a_regar():
	use_item(Items.Water)

def a_trocar():
	swap(North)

def a_arar():
	till()

# --- SETUP ---

set_world_size(3)
clear()

quick_print("operacao | custo documentado | custo medido | veredito")
quick_print("-------------------------------------------------")

# --- SENSORES (esperado: 1 tick, e get_tick_count 0) ---

custo("get_tick_count()", 0, a_ticks)
custo("get_pos_x()", 1, a_pos)
custo("get_entity_type()", 1, a_tipo)
custo("get_ground_type()", 1, a_chao)
custo("get_world_size()", 1, a_tamanho_mundo)
# ATENCAO: os dois stubs DISCORDAM aqui. O builtins.py canonico (shipado com a
# doc oficial) diz 0 ticks; o __builtins__.py gerado pelo save diz 1 tick.
# Usamos o canonico como esperado - esta medicao desempata na pratica.
custo("get_time()", 0, a_tempo)
custo("measure() [tile vazio]", 1, a_medir)

# --- MOVIMENTO (esperado: 200 quando o drone se move) ---

custo("move() [livre]", 200, a_mover)

# --- SOLO ---

# Garante Grassland antes de arar, senao o till() volta pra Grassland.
if get_ground_type() == Grounds.Soil:
	till()
custo("till() [Grassland -> Soil]", 200, a_arar)

# --- COLHEITA E PLANTIO ---

# Tile vazio: harvest nao remove nada -> deve ser o preco baixo.
harvest()
custo("harvest() [tile vazio]", 1, a_colher)

custo("plant(Grass) [sucesso]", 200, a_plantar_grama)

# Espera a grama ficar madura pra medir a colheita que REMOVE algo.
while not can_harvest():
	pass
custo("harvest() [removeu planta]", 200, a_colher)

# --- ITENS ---

custo("use_item(Water) [sucesso]", 200, a_regar)

# --- SWAP ---
# Precisa de duas entidades pra troca ser real; planta aqui e ao norte.
if get_ground_type() != Grounds.Soil:
	till()
plant(Entities.Grass)
move(North)
if get_ground_type() != Grounds.Soil:
	till()
plant(Entities.Grass)
move(South)
custo("swap(North) [duas plantas]", 200, a_trocar)

quick_print("-------------------------------------------------")
quick_print("Fim. Anote as linhas DIVERGE - sao as descobertas.")
