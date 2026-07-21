clear()
world_size = get_world_size()
change_hat(Hats.Brown_Hat)

companion_mapping = {}
tree_mapping = {}

def tree_tile(curr_x, curr_y):
	return curr_x % 2 == curr_y % 2


def track_companion(curr_x, curr_y):
	global companion_mapping
	global tree_mapping
	
	result = get_companion()
	if result == None:
		return False
		
	target_entity, (target_x, target_y) = result

	if (target_x, target_y) not in companion_mapping:
		companion_mapping[(target_x, target_y)] = target_entity
		tree_mapping[(curr_x, curr_y)] = (target_x, target_y)
		return True
	return False


def drone_tree_task():
	global world_size
	global companion_mapping
	global tree_mapping
	
	while True:
		for j in range(world_size):
			curr_x = get_pos_x()
			curr_y = get_pos_y()
			
			if tree_tile(curr_x, curr_y):
				if can_harvest():
					harvest()
					plant(Entities.Tree)
				
				if (curr_x, curr_y) in tree_mapping:
					companion_pos = tree_mapping.pop((curr_x, curr_y))
					if companion_pos in companion_mapping:
						companion_mapping.pop(companion_pos)

				track_companion(curr_x, curr_y)
				
				if get_water() < 0.40:
					use_item(Items.Water)
					
			elif (curr_x, curr_y) in companion_mapping:
				target_entity = companion_mapping[(curr_x, curr_y)]
				harvest()
				
				if target_entity == Entities.Grass:
					if get_ground_type() != Grounds.Grassland:
						till()
						
				elif target_entity == Entities.Carrot:
					if get_ground_type() != Grounds.Soil:
						till()

				plant(target_entity)
				
			else:
				harvest()
				plant(Entities.Bush)
				
			move(North)


NUM_DRONES_TO_SPAWN = 31

for i in range(NUM_DRONES_TO_SPAWN):
	while num_drones() >= max_drones():
		pass
	spawn_drone(drone_tree_task)
	move(East)

drone_tree_task()