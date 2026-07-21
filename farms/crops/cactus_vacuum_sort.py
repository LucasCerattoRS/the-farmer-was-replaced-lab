# =========================================================
# FAZENDA DE CACTOS 32x32 - 8 DRONES
# CORRECAO: "Teoria do Vacuo" (Preenche buracos vazios)
# =========================================================

WORLD_SIZE = 32
TAMANHO_COLHEITA = 12 # Colhe no meio se for grande
TAMANHO_BORDAS = 6    # Colhe nas bordas para nao entupir

# --- FUNCAO MATEMATICA SEGURA ---

def medir_com_vazio(direcao):
	# Essa funcao trata o VAZIO (None) como -1.
	# Isso forca os cactos a "cairem" para dentro dos buracos.
	if direcao == None:
		val = measure()
	else:
		val = measure(direcao)
		
	if val == None:
		return -1
	return val

# --- MANUTENCAO DO SOLO ---

def garantir_planta():
	# Solo e Agua
	if get_ground_type() != Grounds.Soil:
		till()
	if get_water() < 0.5:
		use_item(Items.Water)
		
	# Se nao tem nada, planta
	if get_entity_type() == None:
		plant(Entities.Cactus)

# --- SISTEMA DE MOVIMENTACAO DE CACTOS ---

def tentar_trocar_norte():
	# Compara: MEU VALOR vs VIZINHO NORTE
	meu_val = medir_com_vazio(None)
	norte_val = medir_com_vazio(North)
	
	# Se eu tenho algo e o vizinho tem menos (ou nada), TROCA!
	# Exemplo: Eu(0) > Norte(-1/Vazio) -> TROCA. O cacto sobe.
	if meu_val > norte_val:
		swap(North)

def tentar_trocar_leste():
	# Compara: MEU VALOR vs VIZINHO LESTE
	meu_val = medir_com_vazio(None)
	leste_val = medir_com_vazio(East)
	
	if meu_val > leste_val:
		swap(East)

def checar_colheita():
	# Mede sem direcao (onde estou)
	val = measure()
	
	if val == None:
		return

	x = get_pos_x()
	y = get_pos_y()

	# Se estou na Borda Final (Topo ou Direita Extrema)
	if x == 31 or y == 31:
		if val >= TAMANHO_BORDAS:
			harvest()
	else:
		# No miolo do mapa
		if val >= TAMANHO_COLHEITA:
			harvest()

def processar_tile():
	# 1. Planta se precisar (Cria materia prima)
	garantir_planta()
	
	# 2. Empurra para o NORTE (Se nao estiver no teto)
	if get_pos_y() < WORLD_SIZE - 1:
		tentar_trocar_norte()
		
	# 3. Empurra para o LESTE (Se nao estiver na parede direita)
	if get_pos_x() < WORLD_SIZE - 1:
		tentar_trocar_leste()
		
	# 4. Verifica se deve colher
	checar_colheita()
	
	# 5. RE-CHECAGEM (O Segredo para nao deixar buracos)
	# Se fizemos uma troca ou colheita, o chao pode ter ficado vazio.
	# Chamamos garantir_planta de novo para deixar uma semente crescendo
	# antes de ir embora para o proximo quadrado.
	garantir_planta()

# --- MOVIMENTACAO (4 COLUNAS) ---

def worker_cacto_v2(col_inicio):
	# Vai para inicio
	tx = col_inicio
	while get_pos_x() < tx:
		move(East)
	while get_pos_x() > tx:
		move(West)
	while get_pos_y() > 0:
		move(South)
		
	while True:
		# Col 1 (Sobe)
		for i in range(WORLD_SIZE):
			processar_tile()
			if i < WORLD_SIZE - 1:
				move(North)
		move(East)
		
		# Col 2 (Desce)
		for i in range(WORLD_SIZE):
			processar_tile()
			if i < WORLD_SIZE - 1:
				move(South)
		move(East)
		
		# Col 3 (Sobe)
		for i in range(WORLD_SIZE):
			processar_tile()
			if i < WORLD_SIZE - 1:
				move(North)
		move(East)
		
		# Col 4 (Desce)
		for i in range(WORLD_SIZE):
			processar_tile()
			if i < WORLD_SIZE - 1:
				move(South)
		
		# Retorno (3 Oeste)
		move(West)
		move(West)
		move(West)

# --- SETUP ---

def make_runner(col):
	def run():
		worker_cacto_v2(col)
	return run

def main():
	if get_world_size() != 32:
		set_world_size(32)
	clear()
	
	print("Cactos V2: Preenchimento de Vacuo...")
	
	# Spawns: 4, 8, 12, 16, 20, 24, 28
	for i in range(1, 8):
		c = i * 4
		while get_pos_x() < c:
			move(East)
		spawn_drone(make_runner(c))
		
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
		
	worker_cacto_v2(0)

main()