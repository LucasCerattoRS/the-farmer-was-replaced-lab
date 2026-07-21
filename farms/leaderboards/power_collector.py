clear()

PLANT_TYPE_TO_UNLOCK_MAPPING = {
	Entities.Bush: Unlocks.Plant,
	Entities.Tree: Unlocks.Trees,
	Entities.Carrot: Unlocks.Carrots,
	Entities.Pumpkin: Unlocks.Pumpkins,
	Entities.Cactus: Unlocks.Cactus,
	Entities.Sunflower: Unlocks.Sunflowers,
}


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


def apply_fertilizer_and_water(use_fertilizer, use_weird_substance, use_water):
	if can_harvest():
		return

	if use_fertilizer and num_unlocked(Unlocks.Fertilizer) != 0 and num_items(Items.Fertilizer) >= 1:
		use_item(Items.Fertilizer)
		if use_weird_substance and num_items(Items.Weird_Substance) >= 1:
			use_item(Items.Weird_Substance)

	if use_water and num_unlocked(Unlocks.Watering) != 0 and get_water() < 1 and num_items(Items.Water) >= 1:
		use_item(Items.Water)


def prepare_soil_and_plant(plant_type):
	current_entity_type = get_entity_type()
	current_ground_type = get_ground_type()

	if plant_type != current_entity_type:
		harvest()

	if plant_type == Entities.Grass:
		if current_ground_type != Grounds.Grassland:
			till()
	else:
		if current_ground_type != Grounds.Soil:
			till()
		if plant_type in PLANT_TYPE_TO_UNLOCK_MAPPING:
			required_unlock = PLANT_TYPE_TO_UNLOCK_MAPPING[plant_type]
			if num_unlocked(required_unlock) != 0:
				plant(plant_type)


def collect_power_with_drones(target_quantity):
	def drone_worker():
		current_drone_id = num_drones()

		if current_drone_id != 1 and get_pos_x() != initial_world_size - 1:
			move(East)
		if current_drone_id != max_drones() and get_pos_x() != initial_world_size - 1:
			spawn_drone(drone_worker)

		while num_items(Items.Power) < target_quantity:
			if can_harvest():
				harvest()
			prepare_soil_and_plant(Entities.Sunflower)
			apply_fertilizer_and_water(False, False, True)
			move(North)

	if num_items(Items.Power) < target_quantity:
		initial_world_size = get_world_size()
		navigate_to_position(0, 0)

		drone_worker()
		while num_drones() != 1:
			pass


collect_power_with_drones(1000000000000)

