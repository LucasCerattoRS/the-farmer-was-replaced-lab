# =========================================================
# FAZENDA DE ABOBORA 32x32 - 8 DRONES
# Versao Estavel: Checagem Unica no (0,0)
# =========================================================

# Alvo seguro: 1 milhao (ja que a cheia vale 1.8 bilhao)
ALVO_COLHEITA = 1000000

# --- FUNCOES DE TERRENO ---

def garantir_solo():
	if get_ground_type() != Grounds.Soil:
		till()

def regar():
	# Agua alta e crucial para evitar que aboboras morram
	if get_water() < 0.6:
		use_item(Items.Water)

def tratar_terreno():
	# Essa funcao APENAS mantem a abobora viva.
	# Ela NUNCA colhe uma abobora viva.
	garantir_solo()
	regar()
	
	ent = get_entity_type()
	
	if ent == None:
		plant(Entities.Pumpkin)
	elif ent == Entities.Dead_Pumpkin:
		# So colhe se estiver MORTA
		harvest()
		plant(Entities.Pumpkin)

# --- LOGICA DO CHEFE ---

def verificar_mega_abobora():
	# Esta funcao roda EXCLUSIVAMENTE no (0,0)
	if can_harvest():
		tamanho = measure()
		
		if tamanho != None:
			# Se for maior que 1 Milhao, colhe tudo!
			if tamanho > ALVO_COLHEITA:
				harvest()

def loop_chefe_estavel():
	size = get_world_size() # 32
	
	while True:
		# --- COLUNA 1 ---
		for i in range(size):
			# 1. Se estiver no (0,0), verifica se esta pronta
			if get_pos_x() == 0:
				if get_pos_y() == 0:
					verificar_mega_abobora()
			
			# 2. Cuida do terreno (replantar mortas)
			tratar_terreno()
			
			# 3. Move
			if i < size - 1:
				move(North)
		move(East)
		
		# --- COLUNA 2 ---
		for i in range(size):
			tratar_terreno()
			if i < size - 1:
				move(South)
		move(East)
		
		# --- COLUNA 3 ---
		for i in range(size):
			tratar_terreno()
			if i < size - 1:
				move(North)
		move(East)
		
		# --- COLUNA 4 ---
		for i in range(size):
			tratar_terreno()
			if i < size - 1:
				move(South)
		
		# Retorno
		move(West)
		move(West)
		move(West)

# --- MOVIMENTACAO DOS AUXILIARES ---

def worker_comum(col_inicio):
	size = get_world_size()
	
	# Navega ate a coluna de inicio
	tx = col_inicio
	while get_pos_x() < tx:
		move(East)
	while get_pos_x() > tx:
		move(West)
	while get_pos_y() > 0:
		move(South)
		
	while True:
		# Col 1
		for i in range(size):
			tratar_terreno()
			if i < size - 1:
				move(North)
		move(East)
		# Col 2
		for i in range(size):
			tratar_terreno()
			if i < size - 1:
				move(South)
		move(East)
		# Col 3
		for i in range(size):
			tratar_terreno()
			if i < size - 1:
				move(North)
		move(East)
		# Col 4
		for i in range(size):
			tratar_terreno()
			if i < size - 1:
				move(South)
		# Retorno
		move(West)
		move(West)
		move(West)

# --- SETUP ---

def make_runner(col):
	def run():
		worker_comum(col)
	return run

def main():
	clear()
	
	if get_world_size() != 32:
		set_world_size(32)
		
	print("Iniciando Abobora Estavel (32x32)")

	# 1. Spawna os 7 auxiliares (Colunas 4 a 28)
	for i in range(1, 8):
		c = i * 4
		while get_pos_x() < c:
			move(East)
		spawn_drone(make_runner(c))
		
	# 2. Chefe volta para (0,0)
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
		
	# 3. Inicia o loop do Chefe
	loop_chefe_estavel()

main()