# PESQUISA: taxa de morte da abobora
#
# ALVO: o site afirma "cerca de 1 em 5 aboboras morre ao crescer". Nunca foi
# medido - e a afirmacao numerica mais repetida da pagina de Culturas.
#
# METODO: um unico tile, uma abobora por vez. Tile isolado de proposito:
# aboboras adjacentes e maduras se FUNDEM, e fusao estragaria a contagem.
# Cada rodada termina em um de dois estados observaveis:
#   - Entities.Dead_Pumpkin  -> morreu
#   - can_harvest() == True  -> sobreviveu
# (Dead_Pumpkin nunca fica colhivel, entao os dois estados nao se confundem.)
#
# COMO RODAR: cole numa janela, Execute, leia o Output.
# AMOSTRAS alto da um intervalo melhor - 200+ e o ideal; 100 ja indica.

AMOSTRAS = 200

def uma_abobora():
	# Devolve True se a abobora morreu, False se chegou madura.
	harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	if get_water() < 0.75:
		use_item(Items.Water)
	plant(Entities.Pumpkin)
	while True:
		if get_entity_type() == Entities.Dead_Pumpkin:
			return True
		if can_harvest():
			return False

# --- SETUP ---

set_world_size(3)
clear()

mortas = 0
vivas = 0

for i in range(AMOSTRAS):
	if uma_abobora():
		mortas += 1
	else:
		vivas += 1
	# Relatorio parcial a cada 25, pra dar pra abortar cedo sem perder tudo.
	if (i + 1) % 25 == 0:
		quick_print("parcial N=" + str(i + 1) + " mortas=" + str(mortas) + " taxa=" + str(mortas / (i + 1)))

quick_print("-------------------------------------------------")
quick_print("N total     : " + str(AMOSTRAS))
quick_print("mortas      : " + str(mortas))
quick_print("vivas       : " + str(vivas))
quick_print("taxa medida : " + str(mortas / AMOSTRAS))
quick_print("site afirma : 0.2 (1 em 5)")
