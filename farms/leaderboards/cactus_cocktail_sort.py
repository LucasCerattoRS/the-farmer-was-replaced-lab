clear()

#go_to new position		
def move_to(new_pos_x, new_pos_y):	
	new_pos_x -= get_pos_x()
	new_pos_y -= get_pos_y()	
	if new_pos_x > 16:
		new_pos_x = new_pos_x - 32
	elif new_pos_x < -16:
		new_pos_x = new_pos_x + 32
	if new_pos_y > 16:
		new_pos_y = new_pos_y - 32
	elif new_pos_y < -16:
		new_pos_y = new_pos_y + 32			
	if new_pos_y > 0:
		for i in range(new_pos_y):
			move(North)
	elif new_pos_y < 0:
		for i in range(abs(new_pos_y)):
			move(South)
	if new_pos_x > 0:
		for i in range(new_pos_x):
			move(East)
	elif new_pos_x < 0:
		for i in range(abs(new_pos_x)):
			move(West)

def water():
	if get_water() < 0.5:
		use_item(Items.Water)
	use_item(Items.Fertilizer)	

def PlantCactus():
	if get_ground_type() != Grounds.Soil:
		till()
	while get_entity_type() != Entities.Cactus:
		#harvest()
		plant(Entities.Cactus)
	
def can_swap(direction):
	current = measure()
	neighbor = measure(direction)
	
	# Нельзя свапать, если кто-то не готов
	if current == None or neighbor == None:
		return False	
	elif direction == North and get_pos_y() != get_world_size()-1 or direction == East and get_pos_x() != get_world_size()-1:
		# Текущий должен быть <= соседа
		return current > neighbor  # если НАРУШЕНО — меняем
	elif direction == South and get_pos_y() != 0 or direction == West and get_pos_x() != 0:
		# Текущий должен быть >= соседа
		return current < neighbor  # если НАРУШЕНО — меняем
	else:
		return False
		
def pro_swap(direction):
	if can_swap(direction):
		swap(direction)
		return True
	else:
		return False
		
def pro_cactus_gorizontal():
	WorldSize = get_world_size()
	ind_max = WorldSize - 1
	ind_min = 0	
	while True:	
		swapped = False
		k = 0
		while ind_max > get_pos_x() + 1:
			if pro_swap(East):
				swapped = True
				k = 0
			else:
				k += 1
			if pro_swap(West):
				swapped = True
				k = 0
			else:
				k += 1		
			move(East)					
		if pro_swap(East):
			swapped = True
			k = 0
		else:
			k += 1	
		if pro_swap(West):
			swapped = True
			k = 0
		else:
			k += 1	
		if not swapped:
			break
		if k > 3:
			ind_max -= (k-2) / 2
		ind_max -= 1
		if ind_max <= ind_min:
			break
		swapped = False
		k = 0
		while ind_min < get_pos_x() - 1:			
			if pro_swap(West):
				swapped = True
				k = 0
			else:
				k += 1
			if pro_swap(East):
				swapped = True
				k = 0
			else:
				k += 1			
			move(West)				
		if pro_swap(West):
			swapped = True
			k = 0
		else:
			k += 1			
		if pro_swap(East):
			swapped = True
			k = 0
		else:
			k += 1	
		if k > 3:
			ind_min += (k-2) / 2	
		ind_min += 1
		if not swapped:
			break
		if ind_max <= ind_min:
			break
			
def pro_cactus_vertical():
	WorldSize = get_world_size()
	ind_max = WorldSize - 1
	ind_min = 0		
	for i in range(WorldSize):
		PlantCactus()		
		pro_swap(South)
		move(North)
	while True:		
		swapped = False
		k = 0
		while ind_max > get_pos_y() + 1:
			if pro_swap(South):
				swapped = True
				k = 0
			else:
				k += 1
			if pro_swap(North):
				swapped = True
				k = 0
			else:
				k += 1
			if pro_swap(South):
				swapped = True
				k = 0
			else:
				k += 1			
			move(North)
		if pro_swap(South):
			swapped = True
			k = 0
		else:
			k += 1			
		if pro_swap(North):
			swapped = True
			k = 0
		else:
			k += 1	
		if pro_swap(South):
			swapped = True
			k = 0
		else:
			k += 1
		if k > 4:
			ind_max -= (k-3) / 3
		ind_max -= 1
		if not swapped:
			break
		if ind_max <= ind_min:
			break
		swapped = False
		k = 0
		while ind_min < get_pos_y() - 1:
			if pro_swap(North):				
				swapped = True
				k = 0
			else:
				k += 1
			if pro_swap(South):
				swapped = True	
				k = 0
			else:
				k += 1
			if pro_swap(North):				
				swapped = True
				k = 0
			else:
				k += 1	
			move(South)		
		if pro_swap(North):
			swapped = True
			k = 0
		else:
			k += 1	
		if pro_swap(South):
			swapped = True
			k = 0
		else:
			k += 1
		if pro_swap(North):
			swapped = True
			k = 0
		else:
			k += 1
		if k > 4:
			ind_min += (k-3) / 3		
		ind_min += 1
		if not swapped:
			break
		if ind_max <= ind_min:
			break

while num_items(Items.Cactus) < 33554432:
	for i in range(max_drones()-1):	
		spawn_drone(pro_cactus_vertical)
		move(East)
	pro_cactus_vertical()
	move_to(0, get_pos_y())
	while num_drones() > 1:
		pass	
	
	for i in range(max_drones()-1):	
		spawn_drone(pro_cactus_gorizontal)
		move(North)		
	pro_cactus_gorizontal()
	while num_drones() > 1:
		pass	
	harvest()
	move_to(get_pos_x(), 0)