# faster moving box, shows some (more) inheritance

import engine

WIDTH = 640
HEIGHT = 480

class Box(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, +1, 0, 'square', 'red')

class FastBox(Box):
	def move(self):
		super().move()
		self.y = self.y + 2

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	box = FastBox()
	engine.add_obj(box)
	engine.engine()
