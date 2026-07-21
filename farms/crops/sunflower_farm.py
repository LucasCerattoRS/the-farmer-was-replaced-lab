# Fazenda de Girassois 32x32 - 8 Drones
# ESTRATEGIA: Volume Puro (Colhe tudo que estiver pronto)

def farm_tile():
	# --- 1. SOLO E AGUA ---
	if get_ground_type() != Grounds.Soil:
		till()
		
	# Mantem a agua alta para garantir velocidade 5x
	# O girassol cresce muito mais rapido assim
	if get_water() < 0.75:
		use_item(Items.Water)

	# --- 2. COLHEITA SIMPLES ---
	ent = get_entity_type()
	
	if ent == Entities.Sunflower:
		# Verifica APENAS se a planta ja cresceu o suficiente (adulta)
		if can_harvest():
			harvest()
			plant(Entities.Sunflower)
			
	elif ent == None:
		plant(Entities.Sunflower)
		
	else:
		# Limpa qualquer coisa que nao seja girassol
		harvest()

def drone_logic():
	while True:
		# --- COLUNA 1 (Sobe) ---
		# Vai do y=0 ao y=31 (31 movimentos)
		for y in range(31):
			farm_tile()
			move(North)
		farm_tile() # Topo da Coluna 1
		move(East)
		
		# --- COLUNA 2 (Desce) ---
		for y in range(31):
			farm_tile()
			move(South)
		farm_tile() # Base da Coluna 2
		move(East)
		
		# --- COLUNA 3 (Sobe) ---
		for y in range(31):
			farm_tile()
			move(North)
		farm_tile() # Topo da Coluna 3
		move(East)
		
		# --- COLUNA 4 (Desce) ---
		for y in range(31):
			farm_tile()
			move(South)
		farm_tile() # Base da Coluna 4 (Chao)
		
		# --- RETORNO ---
		# Como terminamos no chao da Coluna 4,
		# voltamos 3 casas para esquerda para reiniciar na Coluna 1
		move(West)
		move(West)
		move(West)

# --- SETUP INICIAL ---

set_world_size(32)
clear()

# Configura 8 drones para 32 colunas
# Matematica: 32 / 8 = 4 colunas por drone
# Spacing = 4

for n in range(1, 8):
	target_x = n * 4
	
	# Navega ate a coluna certa
	while get_pos_x() < target_x:
		move(East)
		
	# Garante que esta no chao
	while get_pos_y() > 0:
		move(South)
		
	spawn_drone(drone_logic)

# Drone principal volta para a origem (0,0)
while get_pos_x() > 0:
	move(West)
while get_pos_y() > 0:
	move(South)

# Inicia o trabalho
drone_logic()