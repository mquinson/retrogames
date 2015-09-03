# resizing and shearing example
# XXX doesn't work if this is done around draw/erase

import turtle
import engine

WIDTH = 640
HEIGHT = 480

class Box(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, +1, 0, 'square', 'red')
		self.size = 1.0
		self.shear = 0.0
	def update(self):
		# adjust shear and size
		turtle.shearfactor(self.shear)
		turtle.shapesize(self.size, 1.0)

		self.shear = self.shear + 0.05
		self.size = self.size + 0.05

		super().update()

		# restore original values
		turtle.shapesize(1.0, 1.0)
		turtle.shearfactor(0.0)

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	box = Box()
	engine.add_obj(box)
	engine.engine()
