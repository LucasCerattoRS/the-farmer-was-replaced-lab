# PESQUISA: tempo real de crescimento por entidade
#
# ALVO: as figuras "~0,5s / ~4s / ~7s / ~6s / ~2s / ~5s / ~1s" que o site afirma
# hoje na pagina Culturas & Economia. Sao aproximadas e nunca foram medidas.
#
# INSTRUMENTO: get_time() devolve segundos de jogo. Cronometra-se do plant()
# ate can_harvest() virar True.
#
# VARIAVEL DE CONFUSAO: agua acelera o crescimento. Este script mantem a agua
# ACIMA DE 0.9 o tempo todo, entao o numero medido e o "tempo com agua alta",
# nao o tempo base. Rodar uma segunda vez sem regar da o outro extremo.
# ARVORES tambem crescem mais devagar perto de outras arvores - aqui a medicao
# e sempre num tile isolado.
#
# COMO RODAR: cole numa janela, Execute, leia o Output. AMOSTRAS controla o N.

AMOSTRAS = 10

def preparar_tile():
	# Solo arado e agua alta, sem entidade em cima.
	harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	while get_water() < 0.9:
		use_item(Items.Water)

def tempo_de_crescimento(entidade, n):
	# Devolve o tempo medio, em segundos de jogo, de plant() ate can_harvest().
	total = 0
	medidas = 0
	for i in range(n):
		preparar_tile()
		if plant(entidade):
			t0 = get_time()
			while not can_harvest():
				# Mantem a agua alta durante o crescimento.
				if get_water() < 0.9:
					use_item(Items.Water)
			t1 = get_time()
			total += t1 - t0
			medidas += 1
			harvest()
	if medidas == 0:
		return -1
	return total / medidas

def relatar(nome, entidade, afirmado):
	medido = tempo_de_crescimento(entidade, AMOSTRAS)
	if medido < 0:
		quick_print(nome + " | NAO PLANTAVEL (falta unlock ou recurso)")
	else:
		quick_print(nome + " | site diz ~" + str(afirmado) + "s | medido " + str(medido) + "s | N=" + str(AMOSTRAS))

# --- SETUP ---

set_world_size(3)
clear()

quick_print("entidade | afirmado no site | medido | N")
quick_print("-------------------------------------------------")

relatar("Grass", Entities.Grass, 0.5)
relatar("Bush", Entities.Bush, 4)
relatar("Tree", Entities.Tree, 7)
relatar("Carrot", Entities.Carrot, 6)
relatar("Pumpkin", Entities.Pumpkin, 2)
relatar("Sunflower", Entities.Sunflower, 5)
relatar("Cactus", Entities.Cactus, 1)

quick_print("-------------------------------------------------")
quick_print("Medido COM agua > 0.9. Rode sem regar pra ver o outro extremo.")
