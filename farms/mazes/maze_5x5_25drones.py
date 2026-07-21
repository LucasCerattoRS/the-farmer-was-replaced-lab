def generate_maze():
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

def maze():
	while True:
		if num_drones() == 25:
			if get_entity_type() == Entities.Treasure:
				harvest()
			generate_maze()

clear()
set_world_size(5)
list = []

while num_drones() < 26:
	pos_x = get_pos_x()
	pos_y = get_pos_y()
	current = (pos_x, pos_y)
	if current not in list:
		list.append(current)
		spawn_drone(maze)
		move(North)
	else:
		move(East)