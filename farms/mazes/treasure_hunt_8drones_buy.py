# ------------------- Configurações e Compras -------------------

def garantir_recursos(quantidade):
	# Compra Weird Substance se o estoque estiver baixo
	if num_items(Items.Weird_Substance) < quantidade:
		# Tenta comprar o necessário para 5 rodadas para economizar tempo
		buy_amount = quantidade * 5
		buy(Items.Weird_Substance, buy_amount)

# ------------------- Geração do labirinto -------------------

def create_maze():
	clear()
	# Garante que o solo está pronto para o arbusto
	if get_ground_type() != Grounds.Soil:
		till()
	
	plant(Entities.Bush)
	
	# Cálculo da substância para o nível máximo desbloqueado
	substance_req = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	
	# Verifica e compra antes de usar
	garantir_recursos(substance_req)
	
	use_item(Items.Weird_Substance, substance_req)
	return True

# ------------------- Helpers de direção -------------------

def next_cw(d):
	if d == North: 
		return East
	if d == East:  
		return South
	if d == South: 
		return West
	if d == West:  
		return North
	return d

def next_ccw(d):
	if d == North: 
		return West
	if d == West:  	
		return South
	if d == South: 	
		return East
	if d == East:  
		return North
	return d

# ------------------- Algoritmo de Caça (Worker) -------------------

def treasure_hunt_worker(start_dir, prefer_cw, warmup):
	dir = start_dir
	# Aquecimento para espalhar os drones no início
	for _ in range(warmup):
		move(dir)

	last_x = get_pos_x()
	last_y = get_pos_y()

	while True:
		move(dir)
		curr_x = get_pos_x()
		curr_y = get_pos_y()

		if curr_x == last_x and curr_y == last_y:
			# BLOQUEADO: Gira conforme a preferência do drone
			if prefer_cw:
				dir = next_cw(dir)
			else:
				dir = next_ccw(dir)
		else:
			# MOVEU: Atualiza posição e gira para o lado oposto (Wall Follower)
			last_x = curr_x
			last_y = curr_y
			if prefer_cw:
				dir = next_ccw(dir)
			else:
				dir = next_cw(dir)

		# Verifica se achou o tesouro
		if get_entity_type() == Entities.Treasure:
			harvest()
			return True

# ------------------- Envoltório para spawn_drone -------------------

def make_runner(start_dir, prefer_cw, warmup):
	def run():
		return treasure_hunt_worker(start_dir, prefer_cw, warmup)
	return run

# ------------------- Coordenador Paralelo -------------------

def treasure_hunt_parallel():
	drones = []
	num_drones_total = 8 # Mapa 22x22 suporta bem 8 drones

	for i in range(num_drones_total):
		# Distribui direções iniciais (N, S, E, W)
		dirs = [North, East, South, West]
		start_dir = dirs[i % 4]
		
		# Alterna lógica de giro (Horário / Anti-horário)
		prefer_cw = (i % 2 == 0)
		
		# Desincroniza os drones
		warmup = i 

		func = make_runner(start_dir, prefer_cw, warmup)
		d = spawn_drone(func)
		if d != None:
			drones.append(d)

	# Monitora até que o primeiro encontre o tesouro
	found = False
	while not found:
		for d in drones:
			if has_finished(d):
				if wait_for(d):
					found = True
					break
	return True

# ------------------- Loop Principal -------------------

while True:
	if create_maze():
		treasure_hunt_parallel()
		# O tesouro foi coletado, o loop recomeça e cria um novo labirinto