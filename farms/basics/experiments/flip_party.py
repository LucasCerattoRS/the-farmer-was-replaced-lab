clear()

def flip_forever():

	while True:
		do_a_flip()


def make_drone(offset):

	def drone_behavior():
		for step in range(offset):
			move(East)
		while True:
			do_a_flip()

	return drone_behavior


def main():
	number_of_drones = 32

	for i in range(number_of_drones):
		spawn_drone(make_drone(i))

	flip_forever()

main()