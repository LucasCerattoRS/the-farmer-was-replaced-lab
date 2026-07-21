clear()
maze_size = 8
grid_size = 4

def move_to(x,y):
	while x != get_pos_x():
		move(East)
	while y != get_pos_y():
		move(North)

def collect_treasure():
	substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

def makemaze():
	plant(Entities.Bush)
	collect_treasure()

directions = [North, East, South, West]
offsets = {North:(0,1), South:(0,-1), East:(1,0), West:(-1,0)}

def next_maze_move(heading):
	for i in [1, 0, 3, 2]:
		if can_move(directions[(heading+i) % 4]):
			return directions[(heading+i) % 4]

def maze_move(heading):
	for i in [1, 0, 3, 2]:
		if move(directions[(heading+i) % 4]):
			return (heading+i) % 4

def get_moves():
	moves = {}
	for d in directions:
		if can_move(d):
			moves[(get_pos_x() + offsets[d][0], get_pos_y() + offsets[d][1])] = d
	return moves

def path_move(paths, from_loc, to_loc, depth, visited):
	if to_loc in visited:
		return False
	else:
		visited[to_loc] = True
	for loc in paths[to_loc]:
		if loc == from_loc:
			move(paths[loc][to_loc])
			return True
		elif depth > 0:
			if path_move(paths, from_loc, loc, depth - 1, visited):
				move(paths[loc][to_loc])
				return True
	return False
			
def path_distance(location):
	return abs(get_pos_x() - location[0]) + abs(get_pos_y() - location[1])
	
def hunt():
	heading = 0
	start_x = get_pos_x()
	start_y = get_pos_y()
	paths = {}
	route = []
	while path_distance((start_x, start_y)) > 0 or len(paths) < maze_size * maze_size:
		route.append(next_maze_move(heading))
		paths[(get_pos_x(), get_pos_y())] = get_moves()
		heading = maze_move(heading)
	found = 0
	while found < 200:
		for d in route:
			if get_entity_type() == Entities.Treasure:
				collect_treasure()
				found = found + 1
			move(d)
	for d in route:
		paths[(get_pos_x(), get_pos_y())] = get_moves()
		move(d)
	while True:
		i = path_distance(measure())
		while not path_move(paths, (get_pos_x(), get_pos_y()), measure(), i, {}):
			i = i + 1
		collect_treasure()

def drone_cycle(x, y):
	def task():
		move_to(x, y)
		do_a_flip()
		makemaze()
		hunt()	
	return task

for i in range(grid_size):
	for j in range(grid_size):
		spawn_drone(drone_cycle(i*maze_size+maze_size/2, j*maze_size+maze_size/2))