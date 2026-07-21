clear()
hats = [Hats.Green_Hat, Hats.Purple_Hat]

#set_world_size(6)
world_size = get_world_size()


def _shortest_delta(curr, dest):
	size = world_size
	d = (dest - curr) % size
	if d > size / 2:
		d -= size
	return d


def move_to_x_pos(x_target):
	x_curr = get_pos_x()
	moves_needed = _shortest_delta(x_curr, x_target)
	direction = East 
	if moves_needed > 0:
		pass
	else:
		direction = West
	for _ in range(abs(moves_needed)):
		move(direction)


def move_to_y_pos(y_target):
	y_curr = get_pos_y()
	moves_needed = _shortest_delta(y_curr, y_target)
	direction = North
	if moves_needed > 0:
		pass
	else:
		direction = South
	for _ in range(abs(moves_needed)):
		move(direction)


def wait_for_drones(drones):
	for drone in drones:
		wait_for(drone)


def drone_action_plant_cacti():
	global world_size

	change_hat(hats[get_pos_x() % 2])

	for _ in range(world_size):
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
		move(North)


def plant_cacti():
	global world_size

	move_to_x_pos(0)
	move_to_y_pos(0)

	drones = []

	for _ in range(world_size - 1):
		drones.append(spawn_drone(drone_action_plant_cacti))
		move(East)

	drone_action_plant_cacti()

	move(East)
	move(North)

	wait_for_drones(drones)


def shake_row():
	global world_size

	change_hat(hats[get_pos_y() % 2])

	left = 0
	right = world_size - 1

	while left < right:
		move_to_x_pos(left)

		loc_last_swap = left
		x_curr = get_pos_x()

		# Left-to-right pass
		while x_curr < right:
			# If the current element is smaller than the next, swap
			if measure() < measure(East):
				swap(East)
				loc_last_swap = x_curr
			move(East)
			x_curr += 1

		right = loc_last_swap
		if left >= right:
			break

		move_to_x_pos(right)

		loc_last_swap = right
		x_curr = get_pos_x()

		# Right-to-left pass
		while x_curr > left:
			# If the previous element is larger than the current, swap
			if measure(West) > measure():
				swap(West)
				loc_last_swap = x_curr
			move(West)
			x_curr -= 1

		left = loc_last_swap


def shake_col():
	global world_size

	change_hat(hats[get_pos_x() % 2])

	left = 0
	right = world_size - 1

	while left < right:
		move_to_y_pos(left)

		loc_last_swap = left
		y_curr = get_pos_y()

		# Bottom-to-top pass
		while y_curr < right:
			# If the current element is smaller than the one above, swap
			if measure() < measure(North):
				swap(North)
				loc_last_swap = y_curr
			move(North)
			y_curr += 1

		right = loc_last_swap
		if left >= right:
			break

		move_to_y_pos(right)

		loc_last_swap = right
		y_curr = get_pos_y()

		# Top-to-bottom pass
		while y_curr > left:
			# If the element below is larger than the current, swap
			if measure(South) > measure():
				swap(South)
				loc_last_swap = y_curr
			move(South)
			y_curr -= 1

		left = loc_last_swap


def sort_columns():
	global world_size

	move_to_x_pos(0)
	move_to_y_pos(0)

	drones = []

	for _ in range(world_size - 1):
		drones.append(spawn_drone(shake_col))
		move(East)

	shake_col()

	move(East)
	move(North)

	wait_for_drones(drones)


def sort_rows():
	global world_size

	move_to_x_pos(0)
	move_to_y_pos(0)

	drones = []

	for _ in range(world_size - 1):
		drones.append(spawn_drone(shake_row))
		move(North)

	shake_row()

	move(North)
	wait_for_drones(drones)


while True:
	plant_cacti()
	sort_columns()
	sort_rows()
	harvest()