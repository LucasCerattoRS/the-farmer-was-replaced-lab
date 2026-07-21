# PESQUISA: distribuicao de petalas do girassol
#
# ALVO: o site trata "15 petalas" como o topo da faixa e a genetica de
# sunflower_15petals.py assume que da pra rerrolar ate sair 15. O que nunca foi
# checado e se a distribuicao e UNIFORME na faixa - se nao for, o custo
# esperado de rerrolar muda, e com ele a estrategia.
#
# METODO: planta um girassol, mede na hora que nasce (measure() devolve a
# contagem de petalas), colhe e repete. Monta um histograma.
#
# COMO RODAR: cole numa janela, Execute, leia o Output.
# AMOSTRAS alto e importante aqui - 300+ pra a cauda da distribuicao aparecer.

AMOSTRAS = 300
PETALA_MIN = 1
PETALA_MAX = 15

histograma = {}

def registrar(p):
	if p in histograma:
		histograma[p] += 1
	else:
		histograma[p] = 1

# --- SETUP ---

set_world_size(3)
clear()

for i in range(AMOSTRAS):
	harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	if get_water() < 0.75:
		use_item(Items.Water)
	if plant(Entities.Sunflower):
		registrar(measure())
	harvest()

# --- RELATORIO ---
# Itera uma faixa fixa em vez do dict: a ordem de iteracao de um dict nao e
# garantida, e o histograma tem que sair ordenado pra ser legivel.

quick_print("petalas | contagem | fracao")
quick_print("-------------------------------------------------")

vistas = 0
for p in range(PETALA_MIN, PETALA_MAX + 1):
	if p in histograma:
		c = histograma[p]
		vistas += c
		quick_print(str(p) + " | " + str(c) + " | " + str(c / AMOSTRAS))

quick_print("-------------------------------------------------")
quick_print("amostras   : " + str(AMOSTRAS))
quick_print("contadas   : " + str(vistas))
quick_print("uniforme daria ~" + str(AMOSTRAS / (PETALA_MAX - PETALA_MIN + 1)) + " por valor")
if vistas != AMOSTRAS:
	quick_print("ATENCAO: " + str(AMOSTRAS - vistas) + " amostras cairam FORA da faixa " + str(PETALA_MIN) + "-" + str(PETALA_MAX) + " - a faixa assumida esta errada.")
