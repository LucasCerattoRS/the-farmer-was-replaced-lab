# Fazenda de Cactos 22x22 - 8 Drones
# Divisao: 6 drones (3 cols) + 2 drones (2 cols) = 22 colunas.

WORLD_SIZE = 22

def ensure_tile():
	if get_ground_type() != Grounds.Soil:
		till()
	ent = get_entity_type()
	if ent == None:
		plant(Entities.Cactus)

def drone_logic():
	start_x = get_pos_x()
	
	# Determina quantas colunas este drone vai cobrir
	# Se comecar nas colunas finais (18 ou 20), pega 2. Senao, 3.
	num_cols = 3
	if start_x >= 18:
		num_cols = 2
	
	while True:
		for offset in range(num_cols):
			target_x = start_x + offset
			if target_x > 21:
				target_x = 21
			
			# Movimentacao segura para a coluna
			while get_pos_x() < target_x:
				move(East)
			while get_pos_x() > target_x:
				move(West)
			
			# --- SUBIDA (Ordenacao Vertical) ---
			for y in range(WORLD_SIZE):
				ensure_tile()
				
				if y < (WORLD_SIZE - 1):
					v_atual = measure()
					v_norte = measure(North)
					
					if v_atual != None and v_norte != None:
						if v_atual > v_norte:
							swap(North)
					
					move(North)
			
			# --- DESCIDA (Ordenacao Horizontal) ---
			for y in range(WORLD_SIZE - 1):
				if get_pos_x() < (WORLD_SIZE - 1):
					v_atual = measure()
					v_leste = measure(East)
					
					if v_atual != None and v_leste != None:
						if v_atual > v_leste:
							swap(East)
				
				move(South)
			
			# Reset de segurança na linha 0
			while get_pos_y() > 0:
				move(South)

		# Colheita automatica quando o cacto estiver pronto
		if can_harvest():
			harvest()

# --- SETUP DO MAPA 22x22 ---
if get_world_size() != WORLD_SIZE:
	set_world_size(WORLD_SIZE)
clear()

# --- SPAWN ORGANIZADO (8 Drones total) ---
# Alvos de spawn para cobrir o mapa 22x22 perfeitamente:
# Drone 0 (voce) em 0
# Auxiliares comecam em: 3, 6, 9, 12, 15, 18, 20
spawns = [3, 6, 9, 12, 15, 18, 20]

for alvo in spawns:
	while get_pos_x() < alvo:
		move(East)
	while get_pos_y() > 0:
		move(South)
	spawn_drone(drone_logic)

# --- DRONE PRINCIPAL (VOCE) ---
while get_pos_x() > 0:
	move(West)
while get_pos_y() > 0:
	move(South)

# Assume as colunas 0, 1 e 2
drone_logic()