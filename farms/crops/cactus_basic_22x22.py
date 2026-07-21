# Fazenda de Cactos 22x22 - MODO BASICO (Sem Swap)
# Adaptado para 8 drones cobrirem 22 colunas.

WORLD_SIZE = 22

def ensure_tile():
	if get_ground_type() != Grounds.Soil:
		till()
	
	ent = get_entity_type()
	if ent == None:
		plant(Entities.Cactus)
	elif ent == Entities.Cactus:
		if can_harvest():
			# Substituído 'is not None' por '!= None' para evitar erro
			val = measure()
			if val != None and val >= 6:
				harvest()

def drone_logic():
	start_x = get_pos_x()
	
	# Distribuição para 22 colunas com 8 drones:
	# Os primeiros 6 drones cuidam de 3 colunas, os últimos 2 cuidam de 2.
	num_cols = 3
	if start_x >= 18:
		num_cols = 2
	
	while True:
		for offset in range(num_cols):
			target_x = start_x + offset
			if target_x > 21:
				target_x = 21
			
			while get_pos_x() < target_x:
				move(East)
			while get_pos_x() > target_x:
				move(West)
			
			# Sobe plantando/colhendo
			for y in range(WORLD_SIZE):
				ensure_tile()
				if y < WORLD_SIZE - 1:
					move(North)
			
			# Volta para a base
			while get_pos_y() > 0:
				move(South)

# --- SETUP 22x22 ---
if get_world_size() != WORLD_SIZE:
	set_world_size(WORLD_SIZE)
clear()

# Spawns exatos para cobrir as 22 colunas (0 a 21)
# Drone principal começa em 0. Auxiliares em: 3, 6, 9, 12, 15, 18, 20.
spawns = [3, 6, 9, 12, 15, 18, 20]

for alvo in spawns:
	while get_pos_x() < alvo:
		move(East)
	while get_pos_y() > 0:
		move(South)
	spawn_drone(drone_logic)

# Drone principal (Você) assume as colunas 0, 1 e 2
while get_pos_x() > 0:
	move(West)
while get_pos_y() > 0:
	move(South)

drone_logic()