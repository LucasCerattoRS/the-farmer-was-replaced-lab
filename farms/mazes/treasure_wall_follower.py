# =========================================================
# SOLUCIONADOR DE LABIRINTO 32x32 - 8 DRONES
# Regra: Comandos em linhas separadas / Sem abreviações
# =========================================================

def create_maze():
	clear()
	plant(Entities.Bush)
	
	# Calculo do custo conforme a Wiki
	lvl = num_unlocked(Unlocks.Mazes)
	substance = get_world_size()
	if lvl > 0:
		substance = get_world_size() * (2 ** (lvl - 1))
		
	use_item(Items.Weird_Substance, substance)
	return True

# --- FUNCOES DE ROTACAO (LINHAS SEPARADAS) ---

def rotate_cw(d):
	if d == North:
		return East
	if d == East:
		return South
	if d == South:
		return West
	if d == West:
		return North
	return d

def rotate_ccw(d):
	if d == North:
		return West
	if d == West:
		return South
	if d == South:
		return East
	if d == East:
		return North
	return d

# --- WORKER DO DRONE ---

def treasure_hunt_worker(start_dir, prefer_cw, warmup):
	curr_dir = start_dir
	
	# Aquecimento/Desincronizacao
	count = 0
	while count < warmup:
		move(curr_dir)
		count = count + 1
		
	while True:
		# Tenta mover na direcao atual
		if move(curr_dir):
			# Se conseguiu mover, tenta virar para manter a "mao na parede"
			# Se prefere CW, vira CCW ao mover (e vice-versa)
			if prefer_cw:
				curr_dir = rotate_ccw(curr_dir)
			else:
				curr_dir = rotate_cw(curr_dir)
		else:
			# Se bateu na parede, vira para o lado de preferencia
			if prefer_cw:
				curr_dir = rotate_cw(curr_dir)
			else:
				curr_dir = rotate_ccw(curr_dir)
			
		# Verifica tesouro
		if get_entity_type() == Entities.Treasure:
			harvest()
			return True

# --- FABRICA DE DRONES ---

def make_run(d_init, p_cw, w_up):
	def run():
		return treasure_hunt_worker(d_init, p_cw, w_up)
	return run

# --- COORDENADOR ---

def treasure_hunt_parallel():
	drones = []
	
	# Lista de direcoes para os 8 drones
	dirs = [North, East, South, West, North, East, South, West]
	
	i = 0
	while i < 8:
		d_start = dirs[i]
		
		# Primeiro 4 drones giram CW, os outros 4 giram CCW
		p_cw = False
		if i >= 4:
			p_cw = True
			
		# Spawn
		func = make_run(d_start, p_cw, i)
		dr = spawn_drone(func)
		if dr != None:
			drones.append(dr)
		i = i + 1
		
	# Espera o sucesso
	found = False
	while not found:
		idx = 0
		while idx < len(drones):
			d = drones[idx]
			if has_finished(d):
				found = True
				break
			idx = idx + 1
			
	return True

# --- LOOP PRINCIPAL ---

def main():
	while True:
		if create_maze():
			treasure_hunt_parallel()

main()