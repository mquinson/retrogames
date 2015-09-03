# moving box, shifting colors by overriding draw() method
# XXX doesn't work if draw() is used instead; internal turtle module issue?

import random
import engine

WIDTH = 640
HEIGHT = 480

class Box(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, +1, 0, 'square', 'red')
	def update(self):
		if random.random() < 0.1:
			self.color = random.choice([
				'red', 'blue', 'green', 'yellow',
				'black', 'orange', 'purple'
			])
		super().update()

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	box = Box()
	engine.add_obj(box)
	engine.engine()
