# PESQUISA: payout da colheita em cadeia do cacto vs. ordenacao do campo
#
# ALVO: o site afirma duas regras que nunca foram medidas juntas:
#   1. um cacto sozinho rende tamanho^2;
#   2. colher um cacto colhe em cascata todo vizinho em ordem (crescente ao
#      Norte/Leste, decrescente ao Sul/Oeste), entao um campo ORDENADO paga
#      como se voce tivesse colhido o campo inteiro numa acao so.
#
# METODO: dois experimentos.
#   PARTE 1 - um cacto isolado. Mede o tamanho, colhe, compara o ganho de
#             inventario com tamanho^2.
#   PARTE 2 - campo cheio. Varre e guarda o tamanho de cada tile, calcula um
#             SCORE DE ORDENACAO (fracao de pares adjacentes em ordem), colhe
#             um canto e compara o payout com a soma de tamanho^2 do campo
#             inteiro (o teto teorico, "tudo encadeou").
#
# O par (score, payout/teto) de varias rodadas e o dado que interessa: se a
# regra da cadeia estiver certa, score 1.0 deve dar razao ~1.0.
#
# COMO RODAR: cole numa janela, Execute, leia o Output. RODADAS controla
# quantos campos aleatorios sao amostrados na Parte 2.

TAMANHO = 5
RODADAS = 8

def ir_para_origem():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def preparar_tile():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_water() < 0.75:
		use_item(Items.Water)

def plantar_campo():
	# Varredura em colunas: o mundo e um toro e TAMANHO == lado do mundo,
	# entao subir TAMANHO vezes volta pro mesmo y.
	for x in range(TAMANHO):
		for y in range(TAMANHO):
			harvest()
			preparar_tile()
			plant(Entities.Cactus)
			move(North)
		move(East)

def esperar_maduro():
	pronto = False
	while not pronto:
		pronto = True
		for x in range(TAMANHO):
			for y in range(TAMANHO):
				if not can_harvest():
					pronto = False
				move(North)
			move(East)

def varrer():
	# Devolve {(x, y): tamanho} do campo inteiro.
	campo = {}
	for x in range(TAMANHO):
		for y in range(TAMANHO):
			campo[(get_pos_x(), get_pos_y())] = measure()
			move(North)
		move(East)
	return campo

def score_ordenacao(campo):
	# Fracao de pares adjacentes em ordem crescente ao Norte e ao Leste.
	# Pares que dariam a volta no toro sao ignorados de proposito.
	em_ordem = 0
	total = 0
	for x in range(TAMANHO):
		for y in range(TAMANHO):
			aqui = campo[(x, y)]
			if y + 1 < TAMANHO:
				total += 1
				if campo[(x, y + 1)] >= aqui:
					em_ordem += 1
			if x + 1 < TAMANHO:
				total += 1
				if campo[(x + 1, y)] >= aqui:
					em_ordem += 1
	if total == 0:
		return 0
	return em_ordem / total

def teto_teorico(campo):
	# Soma de tamanho^2 sobre o campo inteiro.
	s = 0
	for chave in campo:
		t = campo[chave]
		s += t * t
	return s

# =====================  PARTE 1 - CACTO ISOLADO  =====================

set_world_size(3)
clear()
ir_para_origem()

preparar_tile()
plant(Entities.Cactus)
while not can_harvest():
	pass

tamanho = measure()
antes = num_items(Items.Cactus)
harvest()
ganho = num_items(Items.Cactus) - antes

quick_print("PARTE 1 - cacto isolado")
quick_print("tamanho medido : " + str(tamanho))
quick_print("esperado t^2   : " + str(tamanho * tamanho))
quick_print("ganho real     : " + str(ganho))
if ganho == tamanho * tamanho:
	quick_print("veredito       : REGRA t^2 CONFIRMADA")
else:
	quick_print("veredito       : DIVERGE <<<")

# =====================  PARTE 2 - CAMPO CHEIO  =====================

quick_print("")
quick_print("PARTE 2 - campo " + str(TAMANHO) + "x" + str(TAMANHO))
quick_print("score | payout | teto (soma t^2) | razao")
quick_print("-------------------------------------------------")

set_world_size(TAMANHO)

for r in range(RODADAS):
	clear()
	ir_para_origem()
	plantar_campo()
	ir_para_origem()
	esperar_maduro()

	ir_para_origem()
	campo = varrer()
	ir_para_origem()

	score = score_ordenacao(campo)
	teto = teto_teorico(campo)

	antes = num_items(Items.Cactus)
	harvest()
	payout = num_items(Items.Cactus) - antes

	razao = 0
	if teto > 0:
		razao = payout / teto

	quick_print(str(score) + " | " + str(payout) + " | " + str(teto) + " | " + str(razao))

quick_print("-------------------------------------------------")
quick_print("Se a regra da cadeia estiver certa, score alto -> razao perto de 1.")
