clear()
world_size = get_world_size()
change_hat(Hats.Brown_Hat)

companion_mapping = {}
hay_mapping = {}

def track_companion(curr_x, curr_y):
	global companion_mapping
	global hay_mapping
	
	result = get_companion()
	if result == None:
		return False
		
	target_entity, (target_x, target_y) = result

	if (target_x, target_y) not in companion_mapping:
		companion_mapping[(target_x, target_y)] = target_entity
		hay_mapping[(curr_x, curr_y)] = (target_x, target_y)
		return True
	return False


def drone_hay_task():
	global world_size
	global companion_mapping
	global hay_mapping
	
	while True:
		for j in range(world_size):
			curr_x = get_pos_x()
			curr_y = get_pos_y()
			
			harvest()
			
			if get_ground_type() == Grounds.Soil:
				till()

			if (curr_x, curr_y) in companion_mapping:
				target_entity = companion_mapping[(curr_x, curr_y)]
				
				if target_entity == Entities.Carrot:
					if get_ground_type() != Grounds.Soil:
						till()
					plant(Entities.Carrot)
				elif target_entity != Entities.Grass:
					plant(target_entity)
			else:
				if (curr_x, curr_y) in hay_mapping:
					companion_pos = hay_mapping.pop((curr_x, curr_y))
					if companion_pos in companion_mapping:
						companion_mapping.pop(companion_pos)
				
				track_companion(curr_x, curr_y)
			
			move(North)


NUM_DRONES_TO_SPAWN = world_size - 1

for i in range(NUM_DRONES_TO_SPAWN):
	while num_drones() >= max_drones():
		pass
	spawn_drone(drone_hay_task)
	move(East)

drone_hay_task()