# moving box that ping-pongs back and forth, the retro Cylon effect

import engine

WIDTH = 640
HEIGHT = 480

class Box(engine.GameObject):
	def __init__(self, x, deltax):
		super().__init__(x, 0, deltax, 0, 'square', 'red')
	def delete(self):
		# just rely on GameObject's out-of-bounds detection;
		# use the old object's values before it gets deleted
		box = Box(self.x, -self.deltax)
		engine.add_obj(box)
		super().delete()

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	box = Box(0, +2)
	engine.add_obj(box)
	engine.engine()
