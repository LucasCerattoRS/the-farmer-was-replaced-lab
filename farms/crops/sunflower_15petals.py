# Fazenda de Girassois 32x32 - 8 Drones
# ESTRATEGIA: "Quad-Col" (4 Colunas por Drone) + Genetica 15

# --- FUNCOES AUXILIARES ---

def force_15_petals():
	# Roda a roleta genetica ate nascer um 15
	while True:
		ent = get_entity_type()
		if ent == None:
			plant(Entities.Sunflower)
		elif ent == Entities.Sunflower:
			# Mede na hora que nasce
			if measure() == 15:
				return # E um campeao, mantem ele
			else:
				harvest() # Mata o fraco (recicla)
				plant(Entities.Sunflower)

def farm_tile():
	# 1. Solo e Agua
	if get_ground_type() != Grounds.Soil:
		till()
		
	# Mapa 32 e grande, o solo seca rapido. 
	# Prioridade maxima na agua.
	if get_water() < 0.75:
		use_item(Items.Water)

	# 2. Gerenciamento do Girassol
	ent = get_entity_type()
	
	if ent == Entities.Sunflower:
		if can_harvest():
			# Ja sabemos que e um 15 (gracas ao force_15_petals)
			harvest()
			force_15_petals()
	else:
		# Limpa o terreno e inicia o ciclo
		harvest()
		force_15_petals()

def drone_logic():
	while True:
		# --- COLUNA 1 (Sobe) ---
		# Mapa 32 vai de 0 a 31. Range e 31 passos.
		for y in range(31):
			farm_tile()
			move(North)
		farm_tile() # Topo
		move(East)
		
		# --- COLUNA 2 (Desce) ---
		for y in range(31):
			farm_tile()
			move(South)
		farm_tile() # Base
		move(East)
		
		# --- COLUNA 3 (Sobe) ---
		for y in range(31):
			farm_tile()
			move(North)
		farm_tile() # Topo
		move(East)
		
		# --- COLUNA 4 (Desce) ---
		for y in range(31):
			farm_tile()
			move(South)
		farm_tile() # Base (Estamos no chao!)
		
		# --- RETORNO RAPIDO ---
		# Como terminamos no chao da Coluna 4,
		# so precisamos voltar 3 casas para a esquerda
		# para chegar na base da Coluna 1.
		move(West)
		move(West)
		move(West)

# --- SETUP INICIAL ---

set_world_size(32)
clear()

# Configura 8 drones para cobrir 32 colunas
# Cada drone cuida de 4 colunas.
# Spacing = 4

for n in range(1, 8):
	target_x = n * 4
	
	while get_pos_x() < target_x:
		move(East)
	# Garante que esta no chao antes de spawnar
	while get_pos_y() > 0:
		move(South)
		
	spawn_drone(drone_logic)

# Drone principal volta para a origem
while get_pos_x() > 0:
	move(West)
while get_pos_y() > 0:
	move(South)

drone_logic()