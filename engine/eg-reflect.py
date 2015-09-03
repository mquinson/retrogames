# reflect a moving box off the edges of the screen

import engine

WIDTH = 640
HEIGHT = 480

class Box(engine.GameObject):
	def __init__(self, x, y, deltax, deltay):
		super().__init__(x, y, deltax, deltay, 'square', 'red')
	def move(self):
		newdx = self.deltax
		newdy = self.deltay
		if abs(self.x + self.deltax) >= abs(WIDTH / 2):
			newdx = -newdx
		if abs(self.y + self.deltay) >= abs(HEIGHT / 2):
			newdy = -newdy
		self.deltax = newdx
		self.deltay = newdy
		super().move()

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	box = Box(0, 0, +3, +2)
	engine.add_obj(box)
	engine.engine()
