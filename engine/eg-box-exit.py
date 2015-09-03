# moving box - exit engine when it goes out of bounds

import engine

WIDTH = 640
HEIGHT = 480

class Box(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, +1, 0, 'square', 'red')

	def delete(self):
		super().delete()
		engine.exit_engine()

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	box = Box()
	engine.add_obj(box)
	engine.engine()
