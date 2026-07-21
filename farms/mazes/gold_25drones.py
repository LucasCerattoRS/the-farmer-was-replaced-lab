def navigate_to_position(target_x, target_y):
	world_size = get_world_size()
	current_position_x = get_pos_x()
	current_position_y = get_pos_y()

	horizontal_distance = (target_x - current_position_x) % world_size
	vertical_distance = (target_y - current_position_y) % world_size

	if horizontal_distance < world_size // 2:
		for _ in range(horizontal_distance):
			move(East)
	else:
		for _ in range(world_size - horizontal_distance):
			move(West)

	if vertical_distance < world_size // 2:
		for _ in range(vertical_distance):
			move(North)
	else:
		for _ in range(world_size - vertical_distance):
			move(South)


def collect_gold_with_drones(target_quantity):
	def drone_worker():
		treasure_count = 0
		current_drone_id = num_drones() - 1

		while num_drones() != 25:
			pass

		while num_items(Items.Gold) < target_quantity:
			if get_entity_type() == Entities.Grass:
				treasure_count = 0

			if current_drone_id == 1 and get_entity_type() == Entities.Grass:
				plant(Entities.Bush)
				use_item(Items.Weird_Substance, 160)

			if get_entity_type() == Entities.Treasure:
				use_item(Items.Weird_Substance, 160)
				treasure_count += 1
				if treasure_count == 45:
					harvest()

	if num_items(Items.Gold) < target_quantity:
		initial_world_size = get_world_size()
		navigate_to_position(0, 0)

		if num_unlocked(Unlocks.Expand) >= 4 and max_drones() >= 25:
			temporary_world_size = 5
		else:
			return
		set_world_size(temporary_world_size)

		for x in range(temporary_world_size):
			for y in range(temporary_world_size):
				if x != temporary_world_size - 1 or y != temporary_world_size - 1:
					spawn_drone(drone_worker)
					move(North)
			if x != temporary_world_size - 1 or y != temporary_world_size - 1:
				move(East)

		drone_worker()
		while num_drones() != 1:
			pass

		set_world_size(initial_world_size)


collect_gold_with_drones(1000000000000)