# =========================================================
# FARM DE WEIRD SUBSTANCE - VERSAO FINAL CORRIGIDA
# =========================================================

def gerenciar_fusao():
	ent = get_entity_type()
	
	# 1. Detectar e colher a Substancia Estranha (Bloco Roxo)
	if ent != None:
		# Se nao e uma das plantas base, e a substancia
		if ent != Entities.Grass:
			if ent != Entities.Bush:
				if ent != Entities.Tree:
					if ent != Entities.Carrot:
						harvest()
						return

	# 2. Logica do Companion
	pedido = get_companion()
	if pedido != None:
		tipo_desejado = pedido[0]
		
		if ent != tipo_desejado:
			# Colhe a planta errada que estava no lugar
			if ent != None:
				harvest()
			
			# Prepara o solo e planta o que foi pedido
			if get_ground_type() != Grounds.Soil:
				till()
			
			plant(tipo_desejado)
			
			# APLICA FERTILIZANTE LOGO APOS PLANTAR
			if num_items(Items.Fertilizer) > 0:
				use_item(Items.Fertilizer)
				
			# Garante agua
			if get_water() < 0.5:
				use_item(Items.Water)
	else:
		# Se nao ha pedido, planta Grama para resetar o ciclo
		if ent == None:
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Grass)
			if num_items(Items.Fertilizer) > 0:
				use_item(Items.Fertilizer)

def worker_policultura():
	n = 32
	# Cada drone identifica onde esta para cuidar de 4 colunas
	col_inicio = get_pos_x()
	
	while True:
		c_count = 0
		while c_count < 4:
			r_count = 0
			while r_count < n:
				gerenciar_fusao()
				
				# Movimento vertical (Norte/Sul)
				if r_count < n - 1:
					if c_count % 2 == 0:
						move(North)
					else:
						move(South)
				r_count = r_count + 1
			
			# Move para a proxima das 4 colunas
			if c_count < 3:
				move(East)
			c_count = c_count + 1
			
		# Retorno para a base do setor do drone
		move(West)
		move(West)
		move(West)

def main():
	clear()
	
	# Configura tamanho 32
	if get_world_size() != 32:
		set_world_size(32)
		
	# Spawn dos 7 auxiliares
	# Eles vao para as colunas: 4, 8, 12, 16, 20, 24, 28
	i = 1
	while i < 8:
		alvo = i * 4
		while get_pos_x() < alvo:
			move(East)
		spawn_drone(worker_policultura)
		i = i + 1
		
	# Drone Principal (Você) volta para 0,0 e assume colunas 0-3
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
	
	# Inicia a logica no drone principal
	worker_policultura()

# Chama a funcao principal para o script iniciar
main()