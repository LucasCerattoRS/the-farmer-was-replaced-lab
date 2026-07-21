# =========================================================
# FARM DE OSSOS - DRONE ÚNICO (MASTER)
# Mapa: 32x32
# Estratégia: Zig-Zag Total com Limpeza de Rastro
# =========================================================

def limpar_e_mover(direcao):
	# Tenta mover. Se o rastro bloquear, limpa e tenta de novo.
	if not move(direcao):
		if can_harvest():
			harvest()
		move(direcao)

def main():
	# 1. Preparação
	clear()
	if get_world_size() != 32:
		set_world_size(32)
	
	# 2. Veste o chapéu (Apenas uma vez no início do script)
	change_hat(Hats.Dinosaur_Hat)
	
	n = 32
	
	while True:
		for x in range(n):
			# Padrao Serpente (Sobe colunas pares, desce ímpares)
			if x % 2 == 0:
				# Sobe
				for y in range(n - 1):
					if can_harvest():
						harvest()
					limpar_e_mover(North)
			else:
				# Desce
				for y in range(n - 1):
					if can_harvest():
						harvest()
					limpar_e_mover(South)
			
			# Chegou no fim da coluna, move para o Leste (se não for a última)
			if x < n - 1:
				if can_harvest():
					harvest()
				limpar_e_mover(East)
		
		# --- RETORNO AO INÍCIO (0,0) ---
		# Após percorrer o 32x32, volta para a origem para reiniciar
		# Como o rastro está em todo lugar, voltamos limpando
		while get_pos_y() > 0:
			limpar_e_mover(South)
		while get_pos_x() > 0:
			limpar_e_mover(West)

# Executa o programa
main()