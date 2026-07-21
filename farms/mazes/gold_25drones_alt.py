# =========================================================
# PADRÃO DINOSSAURO - VERSÃO CORRIGIDA E SEM ERROS
# Regra: Direções individuais / Linhas separadas
# =========================================================

def calculate_pair_steps(size):
	# Cálculo de passos para o padrão de serpente
	return ((size - 6) // 2 + 2)

def move_home():
	# Retorna para (0,0)
	while get_pos_x() != 0:
		move(West)
	while get_pos_y() != 0:
		move(South)

def repeat_move(direction, steps):
	# Move um número específico de vezes
	# Retorna False se bater em algo (útil para reset)
	i = 0
	while i < steps:
		if move(direction):
			i = i + 1
		else:
			# Se falhar o movimento, algo bloqueou
			return False
	return True

def perform_dino_pattern():
	size = get_world_size()
	max_idx = size - 1
	
	# 1. Movimento Inicial (Norte -> Leste -> Sul 1)
	if not repeat_move(North, max_idx):
		return False
	if not repeat_move(East, max_idx):
		return False
	if not repeat_move(South, 1):
		return False

	# 2. Padrão de Serpente (Zigue-zague West/East)
	# Corrigido: Não passamos listas, usamos loops simples
	num_pairs = calculate_pair_steps(size)
	p = 0
	while p < num_pairs:
		# Move para Oeste
		if not repeat_move(West, max_idx - 1):
			return False
		if not repeat_move(South, 1):
			return False
			
		# Move para Leste
		if not repeat_move(East, max_idx - 1):
			return False
		if not repeat_move(South, 1):
			return False
			
		p = p + 1

	# 3. Retorno para o início da linha
	if not repeat_move(West, max_idx):
		return False
	
	return True

# --- INICIALIZAÇÃO ---

# Ajuste de tamanho para par (necessário para o Dino)
ws = get_world_size()
if ws % 2 == 1:
	set_world_size(ws - 1)

# Reset inicial
change_hat(Hats.Straw_Hat)
move_home()
change_hat(Hats.Dinosaur_Hat)

# Loop Infinito de Execução
while True:
	sucesso = perform_dino_pattern()
	if not sucesso:
		# Se falhar, volta para casa e reinicia
		change_hat(Hats.Straw_Hat)
		move_home()
		change_hat(Hats.Dinosaur_Hat)