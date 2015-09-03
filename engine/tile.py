# has complex polygon as tile shape, and lots of moving objects

import turtle
import engine
import math

WIDTH = 640
HEIGHT = 480

S = 25					# base unit size for ship
B = 50					# base unit size for tiles

GRIDCOLS = 1 + math.ceil(WIDTH / B) + 1
GRIDROWS = 1 + math.ceil(HEIGHT / B) + 1

SPEED = 3
HEADINGSTEP = 5

heading = 180
deltax = None				# set based on heading and SPEED
deltay = None				# set based on heading and SPEED

class Tile(engine.GameObject):
	def __init__(self, x, y):
		# color is already set for compound object, so 'blue' is ignored
		super().__init__(x, y, deltax, deltay, 'tile', 'blue')
	def heading(self):
		return 90
	def move(self):
		self.x += deltax
		self.y += deltay
	def isoob(self):
		# as part of an "infinite" tile grid, it never really
		# goes out of bounds - simply shift existing tile to
		# entering tile's position; this keeps engine from
		# deleting the object and messing up the drawing order
		leftedge = -WIDTH // 2
		rightedge = WIDTH // 2
		topedge = HEIGHT // 2
		bottomedge = -HEIGHT // 2

		if self.x <= leftedge - B:
			self.x += B * GRIDCOLS
		elif self.x >= rightedge:
			self.x -= B * GRIDCOLS

		if self.y >= topedge + B:
			self.y -= B * GRIDROWS
		elif self.y <= bottomedge:
			self.y += B * GRIDROWS
		return False

class Me(engine.GameObject):
	# add last, after tiles, and don't make it a static object
	# and it stays on top, even if it's not moving - it gets
	# re-rendered each time step
	#
	# complication: this means that tile objects in tile grid
	# need to be recycled so they stay early in the object list,
	# or add_obj needs to be extended to allow insertion at the
	# head of the object list
	def __init__(self):
		super().__init__(10, 10, 0, 0, 'spaceship', 'red')
	def heading(self):
		return heading - 90

def makeshipshape():
	turtle.home()			# return to known location & orientation

	# cockpit is a trapezoid - figure out angles and length of side
	adj = (S / 3 - S / 8) / 2
	thetarad = math.atan2(S, adj)
	theta = math.degrees(thetarad)
	hyp = S / math.sin(thetarad)

	turtle.begin_poly()
	turtle.bk(S * 1/2 / 2)		# origin = center of wing - move to back
	turtle.lt(90)			# left wing
	turtle.fd(S / 2)
	turtle.rt(30)			# left rear turret
	turtle.bk(S / 8)
	turtle.fd(S / 8)
	turtle.rt(60)
	turtle.fd(S * 1/2)
	turtle.rt(60)			# left front turret
	turtle.fd(S / 8)
	turtle.bk(S / 8)
	turtle.rt(30)
	turtle.fd(S / 3)		# join of wing and left side of cockpit
	turtle.lt(theta)		# left side of cockpit
	turtle.fd(hyp)
	turtle.rt(theta)
	turtle.fd(S / 8)		# front of cockpit
	turtle.rt(theta)		# right side of cockpit
	turtle.fd(hyp)
	turtle.lt(theta)		# join of right side of cockpit and wing
	turtle.fd(S / 3)		# right wing
	turtle.rt(30)			# right front turret
	turtle.bk(S / 8)
	turtle.fd(S / 8)
	turtle.rt(60)
	turtle.fd(S * 1/2)
	turtle.rt(60)			# right rear turret
	turtle.fd(S / 8)
	turtle.bk(S / 8)
	turtle.rt(30)
	turtle.fd(S / 2)
	turtle.end_poly()

	poly = turtle.get_poly()
	turtle.register_shape('spaceship', poly)

# tile is a compound shape and can have multiple colors

def maketileshape():
	turtle.home()			# return to known location & orientation

	turtle.begin_poly()		# square
	for i in range(4):
		turtle.fd(B)
		turtle.rt(90)
	turtle.end_poly()
	poly1 = turtle.get_poly()

	# don't put this inside begin_poly...end_poly or it draws an extra line
	turtle.goto( (B / 2, -B * 2/3 - B/6) )

	turtle.begin_poly()		# circle, inside square
	turtle.circle(B / 3)
	turtle.end_poly()
	poly2 = turtle.get_poly()

	cs = turtle.Shape('compound')
	# args are poly, fill color, line color
	cs.addcomponent(poly1, 'gray', 'black')
	cs.addcomponent(poly2, 'blue', 'gray42')

	turtle.register_shape('tile', cs)

def maketilegrid():
	for row in range(GRIDROWS):
		for col in range(GRIDCOLS):
			x = col * B - WIDTH//2
			y = HEIGHT//2 - row * B
			tile = Tile(x, y)
			engine.add_obj(tile)

def recalcdeltas():
	global deltax, deltay
	deltay = SPEED * math.sin(math.radians(heading))
	deltax = SPEED * math.cos(math.radians(heading))

def input_cb(key):
	global heading
	if key == 'q' or key == 'Q':
		engine.exit_engine()
	elif key == 'Left':
		heading = (heading + HEADINGSTEP) % 360
	elif key == 'Right':
		heading = (heading - HEADINGSTEP) % 360

	recalcdeltas()

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine(delay=0)	# no delay needed with so many objects!
	engine.set_keyboard_handler(input_cb)
	recalcdeltas()
	makeshipshape()
	maketileshape()
	maketilegrid()
	engine.add_obj(Me())		# needs to be after tile grid created
	engine.engine()
