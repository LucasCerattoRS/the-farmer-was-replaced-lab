def newHat():
	hats = [Hats.Gold_Hat, Hats.Golden_Cactus_Hat, Hats.Golden_Carrot_Hat, Hats.Golden_Sunflower_Hat, Hats.Golden_Tree_Hat]
	while True:
		move(North)
		change_hat(hats[get_pos_x() % 5])
	
while True:
	spawn_drone(newHat)
	move(East)