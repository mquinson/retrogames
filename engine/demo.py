# python3 demo.py

import math
import turtle
import random
import engine

# window params

WIDTH = 640
HEIGHT = 480

# test stuff

class Circle(engine.GameObject):
	def __init__(self, x, y, deltax, deltay):
		super().__init__(x, y, deltax, deltay, 'circle', 'blue')
	def move(self):
		super().move()
		if self.age % 10 == 0:
			self.deltax = random.choice([-2, -1, 1, 2])
			self.deltay = random.choice([-2, -1, 1, 2])

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

class DelayedBox(engine.GameObject):
	def __init__(self, x, y, delay):
		super().__init__(x, y, 2, 0, 'square', 'red')
		self.delay = delay

	def move(self):
		if self.age >= self.delay:
			super().move()

class PulsingCircle(engine.GameObject):
	def __init__(self, x, y, maxdiameter):
		self.maxdiameter = maxdiameter
		self.diameter = 0
		super().__init__(x, y, 0, 0, 'circle', 'green')

	def draw(self):
		oldmode = turtle.resizemode()
		turtle.shapesize(outline=self.diameter)
		id = super().draw()
		turtle.resizemode(oldmode)
		return id
	
	def step(self):
		newsize = abs(math.sin(math.radians(self.age)))
		self.diameter = newsize * self.maxdiameter
		super().step()

# this can be written by subclassing PulsingCircle, but not much is
# gained by doing that in this case
#
class Boom(engine.GameObject):
	def __init__(self, x, y, maxdiameter):
		self.maxdiameter = maxdiameter
		self.diameter = 0
		super().__init__(x, y, 0, 0, 'circle', 'orange')

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, self.diameter

	def draw(self):
		oldmode = turtle.resizemode()
		turtle.shapesize(outline=self.diameter)
		id = super().draw()
		turtle.resizemode(oldmode)
		return id
	
	def step(self):
		newsize = abs(math.sin(math.radians(self.age) + 180))
		if newsize < 0.05:
			engine.del_obj(self)
			return
		self.diameter = newsize * (self.maxdiameter * 2)
		super().step()

class BigRect(engine.GameObject):
	_counter = 0

	def __init__(self, ulx, uly, lrx, lry):
		# refer to counter as class variable
		name = 'BigRect.%d' % BigRect._counter
		BigRect._counter = BigRect._counter + 1
		
		turtle.register_shape(name, (
			(ulx, uly), (lrx, uly), (lrx, lry), (ulx, lry)
		))
		super().__init__(0, 0, 0, 1, name, 'yellow')

	def isstatic(self):
		return True

def iscoll_circle(obj1, obj2):
	x1, y1, r1 = obj1.get_bc()
	x2, y2, r2 = obj2.get_bc()

	# from http://devmag.org.za/2009/04/13/basic-collision-detection-in-2d-part-1/
	# take the Euclidean distance between the center points, and if
	# that's less than the sum of the radii, then intersection occurred
	d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
	return d < (r1 + r2)

def coll_circle(obj1, obj2):
	if iscoll_circle(obj1, obj2):
		x1, y1, r1 = obj1.get_bc()
		x2, y2, r2 = obj2.get_bc()
		engine.add_obj(Boom(x1, y1, r1))
		engine.add_obj(Boom(x2, y2, r2))
		engine.del_obj(obj1)
		engine.del_obj(obj2)

def coll_boom2(obj1, obj2):
	return coll_boom1(obj2, obj1)

def coll_boom1(obj1, obj2):
	# circle getting drawn into an explosion in progress - obj1 is Boom inst
	if iscoll_circle(obj1, obj2):
		x, y, r = obj2.get_bc()
		engine.add_obj(Boom(x, y, r))
		engine.del_obj(obj2)

# callbacks

def circle_cb():
	obj = Circle(0, 0, 1, 1)
	engine.add_obj(obj)

def quit_cb(key):
	if key == 'q' or key == 'Q':
		engine.exit_engine()

# main routine

if __name__ == '__main__':
	#random.seed(86753)

	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(quit_cb)
	engine.add_random_event(0.005, circle_cb)
	engine.register_collision(Circle, Circle, coll_circle)
	engine.register_collision(Boom, Circle, coll_boom1)
	engine.register_collision(Circle, Boom, coll_boom2)
	for i in range(4):
		ypos = engine.MAXY - i * HEIGHT/3
		obj = DelayedBox(engine.MINX, ypos, i*250)
		engine.add_obj(obj)
	engine.add_obj(PulsingCircle(50, 50, 100))
	engine.add_obj(BigRect(engine.MINX + 25, 0,
			       engine.MAXX - 25, engine.MINY + 25))
	engine.add_obj(BigRect(0, 100, 25, 25))
	engine.add_obj(BigRect(-200, 150, -100, 125))
	engine.engine()
