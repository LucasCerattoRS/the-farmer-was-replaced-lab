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


def collect_cactus_solo(target_quantity):
	import no_polyculture_solo
	no_polyculture_solo.cactus(target_quantity)


def collect_bone_with_drones(target_quantity):
	def move_in_row(direction, count):
		global length
		global next_x
		global next_y
		global close
		for _ in range(count):
			if get_entity_type() == Entities.Apple:
				next_x, next_y = measure()
				length += 1
			if move(direction) == False:
				change_hat(Hats.Gray_Hat)
				close = True

	def fast_back():
		move_in_row(West, get_pos_x())
		move_in_row(South, get_pos_y())

	def stage1():
		old_x = next_x
		old_y = next_y
		if old_x < border:
			old_x = border
		if old_y < border:
			old_y = border
		move_in_row(East, old_x)

		if initial_world_size - offset - 1 >= old_y:
			if old_x + old_y > length + 3 and (get_pos_x() + get_pos_y() > length + 3):
				move_in_row(North, old_y)
				fast_back()
			else:
				move_in_row(North, initial_world_size - offset - 1)
				stage2()
		else:
			move_in_row(North, initial_world_size - offset - 1)
			stage2()

	def stage2():
		global next_x
		global next_y
		global offset
		start_y = get_pos_y()
		rows = (initial_world_size - 1) - start_y
		for i in range(rows + 1):
			row_y = start_y + i
			if (
				((next_y > get_pos_y()) or (next_x == 0) or (next_y < get_pos_y()))
				and (get_pos_y() < initial_world_size - offset - 1)
				and (get_pos_x() > 0)
				and (get_pos_y() % 2 == next_y % 2)
				and (offset < initial_world_size / 4)
			):
				move_in_row(North, 1)
			else:
				if row_y % 2 == 0:
					move_in_row(East, (initial_world_size - 1) - get_pos_x())
				else:
					target_left_steps = get_pos_x() - border
					if target_left_steps > 0:
						move_in_row(West, target_left_steps)
				if i != rows:
					move_in_row(North, 1)
		move_in_row(West, 1)
		move_in_row(South, initial_world_size - 1)

	if num_items(Items.Bone) < target_quantity:
		clear()
		initial_world_size = get_world_size()
		apple_cost = get_cost(Entities.Apple)

		while num_items(Items.Bone) < target_quantity:
			required_cacti = apple_cost[Items.Cactus] * (initial_world_size * initial_world_size)
			if num_items(Items.Cactus) < required_cacti:
				collect_cactus_solo(required_cacti)

			close = False
			next_x = 0
			next_y = 0
			length = 0
			offset = 0
			border = 1
			move_in_row(East, 1)
			change_hat(Hats.Dinosaur_Hat)
			while close == False:
				threshold = initial_world_size * 2
				if length > (threshold - 8) + (offset * (initial_world_size - 2)):
					offset += 1
				if offset < initial_world_size / 16:
					stage1()
				else:
					stage2()


collect_bone_with_drones(1000000000000)

