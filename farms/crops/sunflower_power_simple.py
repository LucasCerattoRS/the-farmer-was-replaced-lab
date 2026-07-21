clear()
change_hat(Hats.Purple_Hat)
def Sunflower():
	def harvestColum():
		for _ in range(get_world_size()):
			if get_ground_type()!=Grounds.Soil:
				till()
				plant(Entities.Sunflower)
			if can_harvest():
				harvest()
				plant(Entities.Sunflower)
				move(North)
			else:
				move(North)
			
	while num_items(Items.Power)<40000000:
		if spawn_drone(harvestColum):
			move(East)
Sunflower()