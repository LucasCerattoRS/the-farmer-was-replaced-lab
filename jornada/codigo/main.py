while True:
	if can_harvest():
		harvest()
	else:
		change_hat(Hats.Gray_Hat)