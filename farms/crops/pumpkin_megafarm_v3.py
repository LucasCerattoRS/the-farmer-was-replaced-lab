clear()
change_hat(Hats.Brown_Hat)
set_world_size(32)
world_size = get_world_size()
first_pass = True


def check_pumpkin():
	if get_pos_x() != 0:
		move(East)

	left_id = measure()
	move(West)
	right_id = measure()
	move(East)

	return left_id == right_id

def wait_for_drones(drones):
	for drone in drones:
		wait_for(drone)


def plant_column():
	global world_size

	for j in range(world_size):
		if get_entity_type() != Entities.Pumpkin:
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)

			if not first_pass:
				while not can_harvest():
					if get_entity_type() == Entities.Dead_Pumpkin:
						plant(Entities.Pumpkin)
					use_item(Items.Fertilizer)
		move(North)
		
def plant_pumpkins():
	global world_size
	#global first_pass
	drones = []

	if get_pos_x() != 0:
		move(East)

	for i in range(world_size - 1):
		drones.append(spawn_drone(plant_column))
		move(East)

	plant_column()
	wait_for_drones(drones)

while True:
	plant_pumpkins()
	first_pass = False

	if check_pumpkin():
		harvest()
		first_pass = True
		move(West)