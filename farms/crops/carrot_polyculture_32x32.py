# =========================================================
# POLICULTURA CENOURA 32x32 - 8 DRONES
# Correcao: Forca o uso de till() para evitar loop de grama
# =========================================================

pedidos = []

# --- FUNCOES DE JARDINAGEM ---

def garantir_solo_arado():
	# Se o chao for grama (Grassland) ou Buraco (Turf), a cenoura nao pega.
	# Temos que usar till() para virar Soil.
	if get_ground_type() != Grounds.Soil:
		till()

def regar_se_preciso():
	# Mantem agua para crescer rapido
	if get_water() < 0.6:
		use_item(Items.Water)

def plantar_firme(tipo):
	# 1. Verifica o que ja esta la
	ent = get_entity_type()
	
	# Se ja e o que queremos, sai
	if ent == tipo:
		return
	
	# Se tem outra coisa, tira
	if ent != None:
		harvest()
		
	# 2. PREPARAR O TERRENO (O SEGREDO)
	# Se for plantar Grama, o solo nao importa tanto.
	# Mas para Cenoura, Arvore ou Arbusto, PRECISA ser Solo.
	if tipo == Entities.Grass:
		pass # Grama cresce em qualquer lugar
	else:
		garantir_solo_arado()
	
	# 3. Planta e Rega
	plant(tipo)
	regar_se_preciso()

# --- SISTEMA DE PEDIDOS ---

def atender_pedidos():
	x = get_pos_x()
	y = get_pos_y()
	atendido = False

	# Copia segura da lista
	lista_copia = list(pedidos)
	
	for item in lista_copia:
		px, py, ptype = item
		
		if px == x and py == y:
			plantar_firme(ptype)
			
			# Remove da lista original
			if item in pedidos:
				pedidos.remove(item)
				
			atendido = True
			break
			
	return atendido

def modo_sonda_cenoura():
	# Forca o plantio de Cenoura
	plantar_firme(Entities.Carrot)
	
	# Verifica do que ela precisa (Companion)
	comp = get_companion()
	
	if comp != None:
		tipo_vizinho, (tx, ty) = comp
		
		# Adiciona o pedido do vizinho na lista
		# Verifica duplicidade simples
		ja_existe = False
		for (px, py, _) in pedidos:
			if px == tx and py == ty:
				ja_existe = True
				break
		
		if not ja_existe:
			pedidos.append((tx, ty, tipo_vizinho))

# --- CEREBRO DO DRONE ---

def processar_bloco():
	x = get_pos_x()
	
	# --- COLUNAS 30 e 31: GIRASSOIS ---
	if x >= 30:
		garantir_solo_arado()
		regar_se_preciso()
		
		if get_entity_type() != Entities.Sunflower:
			plant(Entities.Sunflower)
		else:
			if can_harvest():
				harvest()
		return

	# --- RESTO DO MAPA: CENOURAS ---
	
	# 1. Tenta colher o que esta pronto
	if can_harvest():
		harvest()
		
	# 2. Tenta atender pedido de vizinho (ex: arvore para buffar cenoura)
	fez_pedido = atender_pedidos()
	
	# 3. Se nao tem pedido, planta Cenoura
	if not fez_pedido:
		ent = get_entity_type()
		# Se nao for Cenoura, forca a ser
		if ent != Entities.Carrot:
			modo_sonda_cenoura()

# --- MOVIMENTO (4 COLUNAS) ---

def worker_4_cols(col_inicio):
	size = get_world_size() # 32
	
	# Vai para inicio
	tx = col_inicio
	while get_pos_x() < tx:
		move(East)
	while get_pos_x() > tx:
		move(West)
	while get_pos_y() > 0:
		move(South)
		
	while True:
		# Sobe 1
		for i in range(size):
			processar_bloco()
			if i < size - 1:
				move(North)
		move(East)
		
		# Desce 2
		for i in range(size):
			processar_bloco()
			if i < size - 1:
				move(South)
		move(East)
		
		# Sobe 3
		for i in range(size):
			processar_bloco()
			if i < size - 1:
				move(North)
		move(East)
		
		# Desce 4
		for i in range(size):
			processar_bloco()
			if i < size - 1:
				move(South)
		
		# Retorno (3 Oeste)
		move(West)
		move(West)
		move(West)

# --- INICIALIZACAO ---

def criar_runner(col):
	def run():
		worker_4_cols(col)
	return run

def main():
	clear()
	global pedidos
	pedidos = []
	
	# Drones Auxiliares (Colunas 4, 8, 12, 16, 20, 24, 28)
	for i in range(1, 8):
		c = i * 4
		while get_pos_x() < c:
			move(East)
		spawn_drone(criar_runner(c))
		
	# Drone Principal (Colunas 0, 1, 2, 3)
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
		
	worker_4_cols(0)

main()