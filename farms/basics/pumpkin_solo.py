WIDTH, HEIGHT = 32, 32

def plant_or_till():
	if not can_harvest():
		plant(Entities.Pumpkin)
	if get_ground_type() == Grounds.Grassland:
		till()
		plant(Entities.Pumpkin)

def check_water():
	if get_water() == 0:
		use_item(Items.Water)

def perform_work():
	while True:
		for row in range(WIDTH):
			for col in range(HEIGHT):
				check_water()
				
				if get_pos_x() == 0 and get_pos_y() == 0 and can_harvest():
					harvest()
				
				plant_or_till()
				move(North)
			
			move(East)

clear()
perform_work()