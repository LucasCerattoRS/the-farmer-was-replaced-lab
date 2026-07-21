clear()
world_size = get_world_size()
change_hat(Hats.Brown_Hat)

companion_mapping = {}
carrot_mapping = {}

def track_companion(curr_x, curr_y):
	global companion_mapping
	global carrot_mapping
	
	result = get_companion()
	if result == None:
		return False
		
	target_entity, (target_x, target_y) = result

	if (target_x, target_y) not in companion_mapping:
		companion_mapping[(target_x, target_y)] = target_entity
		carrot_mapping[(curr_x, curr_y)] = (target_x, target_y)
		return True
	return False


def prepare_and_plant(entity_type):
	if entity_type in (Entities.Carrot, Entities.Bush, Entities.Tree) and get_ground_type() != Grounds.Soil:
		till()
	plant(entity_type)


def drone_carrot_task():
	global world_size
	global companion_mapping
	global carrot_mapping
	
	while True:
		for j in range(world_size):
			curr_x = get_pos_x()
			curr_y = get_pos_y()
			
			harvest()
			
			if (curr_x, curr_y) in companion_mapping:
				target_entity = companion_mapping[(curr_x, curr_y)]
				prepare_and_plant(target_entity)
				
				if target_entity == Entities.Carrot and get_water() < 0.10:
					use_item(Items.Water)
					
			elif (curr_x, curr_y) in carrot_mapping:
				prepare_and_plant(Entities.Carrot)
				
				if get_water() < 0.10:
					use_item(Items.Water)

				companion_pos = carrot_mapping.pop((curr_x, curr_y))
				if companion_pos in companion_mapping:
					companion_mapping.pop(companion_pos)
				
				track_companion(curr_x, curr_y)
				
			else:
				prepare_and_plant(Entities.Carrot)
				
				if get_water() < 0.10:
					use_item(Items.Water)

				track_companion(curr_x, curr_y)
				
			move(North)


NUM_DRONES_TO_SPAWN = world_size - 1

for i in range(NUM_DRONES_TO_SPAWN):
	while num_drones() >= max_drones():
		pass
	spawn_drone(drone_carrot_task)
	move(East)

drone_carrot_task()