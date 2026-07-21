ws = get_world_size()
rws = range(ws)
# Maze
leftOf = {North:West, East:North, South:East, West:South}
rightOf = {North:East, East:South, South:West, West:North}
oppositeOf = {North:South, East:West, South:North, West:East}
currentDirection = North
l = -1
substance = -1
# Dinosaur
dinLoop = [East, North, North, East, South, South, East,
North, North, North, West, West, West, South, South, South]

def slowest_automation():
	s = get_time()
	quick_print("Slowest Reset")
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Plant)
	unlock_tech(Unlocks.Carrots)
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Watering)
	unlock_tech(Unlocks.Trees)
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Expand)
	unlock_tech(Unlocks.Expand)
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Fertilizer)
	unlock_tech(Unlocks.Pumpkins)
	unlock_tech(Unlocks.Expand)
	unlock_tech(Unlocks.Fertilizer)
	unlock_tech(Unlocks.Fertilizer)
	unlock_tech(Unlocks.Grass)
	unlock_tech(Unlocks.Trees)
	unlock_tech(Unlocks.Carrots)
	unlock_tech(Unlocks.Speed)
	unlock_tech(Unlocks.Watering)
	unlock_tech(Unlocks.Fertilizer)
	unlock_tech(Unlocks.Grass)
	unlock_tech(Unlocks.Trees)
	unlock_tech(Unlocks.Carrots)
	unlock_tech(Unlocks.Pumpkins)
	unlock_tech(Unlocks.Watering)
	unlock_tech(Unlocks.Cactus)
	unlock_tech(Unlocks.Cactus)
	unlock_tech(Unlocks.Dinosaurs)
	unlock_tech(Unlocks.Dinosaurs)
	unlock_tech(Unlocks.Mazes)
	unlock_tech(Unlocks.Leaderboard)
	s = get_time() - s
	d = s // 86400
	s -= d * 86400
	h = s // 3600
	s -= h * 3600
	m = s // 60
	s -= m * 60
	s = s // 1
	do_a_flip()
	quick_print("Leaderboard unlocked: " + str(d) + "d " + pad(h) + "h " + pad(m) + "m " + pad(s) + "s")

def unlock_tech(tech):
	ct = get_cost(tech)
	for c in ct:
		farm_item(c, ct[c])
	if not unlock(tech):
		unlock_tech(tech)
	pet_the_piggy()
	if tech == Unlocks.Expand:
		global ws
		global rws
		ws = get_world_size()
		rws = range(ws)

def pad(c):
	s = str(c)
	l = len(s)
	if l <= 1:
		s = "0" + s
	return s

def farm_item(item, num):
	while num_items(item) < num:
		if item == Items.Hay:
			farm_grass()
		elif item == Items.Wood:
			if num_unlocked(Unlocks.Trees) > 0:
				farm_trees()
			else:
				farm_bushes()
		elif item == Items.Carrot:
			farm_carrots(num - num_items(item))
		elif item == Items.Pumpkin or item == Items.Weird_Substance:
			farm_pumpkins(num - num_items(item))
		elif item == Items.Cactus:
			farm_cactus(num - num_items(item))
		elif item == Items.Bone:
			farm_bones(((num - num_items(item)) // ((ws**2 - 1)**2)) * (ws**2 - 1) * 2**(num_unlocked(Unlocks.Dinosaurs) - 1) // 4 * 2)
		elif item == Items.Gold:
			farm_gold(num)

def farm_grass():
	for _ in rws:
		for _ in rws:
			sow_tile(True, False, Entities.Grass)
			move(East)
		move(North)

def farm_bushes():
	sow_tile(True, False, Entities.Bush)

def farm_trees():
	for _ in rws:
		for _ in rws:
			if (get_pos_x() + get_pos_y()) % 2 == 0:
				sow_tile(True, True, Entities.Tree)
			move(East)
		move(North)

def farm_carrots(num):
	get_resources_for(Entities.Carrot, num // (2**(num_unlocked(Unlocks.Carrots) - 1)))
	for _ in rws:
		for _ in rws:
			sow_tile(True, True, Entities.Carrot)
			move(East)
		move(North)

def farm_pumpkins(num):
	get_resources_for(Entities.Pumpkin, num // (2*2**(num_unlocked(Unlocks.Pumpkins) - 1)))
	for x in rws:
		for y in rws:
			sow_tile(x == 0  and y == 0, True, Entities.Pumpkin)
			if num_unlocked(Unlocks.Fertilizer) > 0:
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
			move(East)
		move(North)

def farm_cactus(num):
	get_resources_for(Entities.Cactus, num // (2**(num_unlocked(Unlocks.Cactus) - 1)))
	for _ in rws:
		for _ in rws:
			sow_tile(True, True, Entities.Cactus)
			move(East)
		move(North)

def farm_bones(num):
	get_resources_for(Entities.Apple, num // (2**(num_unlocked(Unlocks.Cactus) - 1)))
	clear()
	growing = True
	change_hat(Hats.Dinosaur_Hat)
	while growing:
		for d in dinLoop:
			if not move(d):
				change_hat(Hats.Straw_Hat)
				growing = False
				break

def farm_gold(limit):
	global l
	global substance
	global currentDirection

	l = limit
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)

	clear()
	while num_items(Items.Gold) < l and num_items(Items.Weird_Substance) >= substance:
		currentDirection = North
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, substance)
		search_maze()

	clear()
	if not num_items(Items.Gold) >= l:
		farm_item(Items.Weird_Substance, (l - num_items(Items.Gold)) // (ws**2 / substance))

def sow_tile(to_harvest, water, entity):
	if (to_harvest and can_harvest()) or get_entity_type() != entity:
		harvest()
	if get_ground_type() != get_ground(entity):
		till()
	if water and num_unlocked(Unlocks.Watering) > 0 and get_ground_type() == Grounds.Soil:
		while get_water() < 0.5 and num_items(Items.Water) > 0:
			use_item(Items.Water)
	if get_entity_type() != entity:
		plant(entity)

def get_resources_for(item, nb = ws**2):
	while not can_harvest() and get_entity_type() not in (None, Entities.Dead_Pumpkin):
		pass

	nb = max(ws**2, nb)
	ci = get_cost(item)
	for c in ci:
		if num_items(c) < ci[c] * nb:
			farm_item(c, ci[c] * nb)

def get_ground(entity):
	if entity == Entities.Grass or entity == Entities.Bush:
		return Grounds.Grassland
	else:
		return Grounds.Soil

def search_maze():
	global currentDirection
	global path
	global l

	while num_items(Items.Gold) < l and num_items(Items.Weird_Substance) >= substance:

		while get_entity_type() == Entities.Hedge:
			# Search
			if move(rightOf[currentDirection]):
				currentDirection = rightOf[currentDirection]
			elif move(currentDirection):
				pass
			elif move(leftOf[currentDirection]):
				currentDirection = leftOf[currentDirection]
			else:
				currentDirection = oppositeOf[currentDirection]
				move(currentDirection)

		if get_entity_type() == Entities.Treasure:
			harvest()
			clear()
			plant(Entities.Bush)
			use_item(Items.Weird_Substance, substance)
			currentDirection = North

if num_unlocked(Unlocks.Speed) == 0 and num_unlocked(Unlocks.Plant) == 0:
	slowest_automation()
else:
	print("You need to call this script")
	print("from a 'leaderboard_run' or 'simulate'")