while True:
	WORLD_SIZE = get_world_size()
	MAX_DRONES = max_drones()
	
	def main():
		plant_and_sort_all_rows()
		sort_all_columns()
	 
	 
	def plant_and_sort_all_rows():
		global WORLD_SIZE
		for row in range(WORLD_SIZE):
			if num_drones() >= WORLD_SIZE:
				move_to(0, row)
				pas_current_row()
				break
	 
			move_to(0, row)
			drone = spawn_drone(pas_current_row)
	 
		move_to(0,1)
		while num_drones() > 1:
			pass
	 
	 
	def pas_current_row():
		global WORLD_SIZE
		row = get_pos_y()
		for col in range(WORLD_SIZE):
			move_to(col, row)
			till()
			plant(Entities.Cactus)
			insertion_sort_row_step()
	 
	 
	def insertion_sort_row_step():
		while get_pos_x() > 0:
			if measure() < measure(West):
				swap(West)
				move(West)
			else:
				break
	 
	 
	def sort_all_columns():
		global WORLD_SIZE
		global MAX_DRONES
		for col in range(WORLD_SIZE):
			move_to(col, 1)
			while num_drones() >= MAX_DRONES:
				sort_current_column()
				break
	 
			spawn_drone(sort_current_column)
	 
		while num_drones() > 1:
			pass
	 
	 
	def sort_current_column():
		global WORLD_SIZE
		while get_pos_y() < (WORLD_SIZE - 1):
			insertion_sort_column_step()
		insertion_sort_column_step()
	 
	 
	def insertion_sort_column_step():
		if get_pos_y() == 0:
			move(North)
			return
	 
		if measure() < measure(South):
			swap(South)
			if get_pos_y() > 1:
				move(South)
				insertion_sort_column_step()
				return
	 
		move(North)
	 
	 
	def move_to(x, y):
		global WORLD_SIZE
		dx = x - get_pos_x()
		dy = y - get_pos_y()
	 
		if dx > 0:
			if dx > WORLD_SIZE/2:
				move(West)	
			else:
				move(East)
		elif dx < 0:
			if abs(dx) > WORLD_SIZE/2:
				move(East)		
			else:
				move(West)
	 
		if dy > 0:
			if dy > WORLD_SIZE/2:
				move(South)		
			else:
				move(North)
		elif dy < 0:
			if abs(dy) > WORLD_SIZE/2:
				move(North)
			else:
				move(South)
	 
		if not (get_pos_x() == x and get_pos_y() == y):
			move_to(x, y)
		else:
			return
	 
	 
	if __name__ == "__main__":
		clear()
		main()
		harvest()