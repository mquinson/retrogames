# python3 missile.py

import math
import time
import turtle
import random
import engine

# window params

WIDTH = 640
HEIGHT = 480
MAXY = HEIGHT // 2
MINY = -HEIGHT // 2
MAXX = WIDTH // 2
MINX = -WIDTH // 2

# game params

GROUNDY = MINY + HEIGHT // 4
NEWENEMYPROB = 0.01
DEMOFIREPROB = 0.01
XFALLRATE = 1
YFALLRATE = -2
THEMCOLOR = 'purple'
USCOLOR = 'red'
CITYCOLORS = ('green', 'yellow', 'red')
CITYLIVES = len(CITYCOLORS)
EXPLODECOLOR = 'orange'
BGCOLOR = 'black'
GROUNDCOLOR = 'grey'
NCITIES = 6
GUNX = 0
GUNY = GROUNDY
CLIMBRATE = 3 * XFALLRATE
NSTARS = 25

# game objects

class City(engine.GameObject):
	def __init__(self, x, y):
		self.hits = 0
		self.setcolor()
		super().__init__(x, y, 0, 0, 'square', self.color)

	def setcolor(self):
		self.color = CITYCOLORS[self.hits]

	def hit(self):
		self.hits = self.hits + 1
		if self.hits == CITYLIVES:
			engine.del_obj(self)
			citygoboom()
		else:
			self.setcolor()
			self.update()
		
	def isstatic(self):
		return True

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

class Enemy(engine.GameObject):
	def __init__(self, x, y, deltax, deltay):
		super().__init__(x, y, deltax, deltay, 'classic', THEMCOLOR)

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

# finally, code that understands the gravity of the situation
g = 9.81 * 1/20

class Missile(engine.GameObject):
	def __init__(self, x, y, v0, theta):
		deltax = deltay = 0
		self.v0 = v0
		self.theta = theta
		super().__init__(x, y, deltax, deltay, 'classic', USCOLOR)

	def nextpos(self):
		# from http://en.wikipedia.org/w/index.php?title=Projectile_motion&oldid=540166443#Displacement
		t = self.age + 1
		x = self.v0 * t * math.cos(self.theta)
		y = self.v0 * t * math.sin(self.theta) - 0.5 * g * (t ** 2)
		return GUNX + x, GUNY + y

	def move(self):
		# set deltax and deltay for turtle heading retroactively
		# it's close enough and avoids computing nextpos again
		oldx, oldy = self.x, self.y
		self.x, self.y = self.nextpos()
		self.deltax = self.x - oldx
		self.deltay = self.y - oldy

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		# n.b. bigger than enemy circle
		return self.x, self.y, 20

class Boom(engine.GameObject):
	def __init__(self, x, y, maxdiameter):
		self.maxdiameter = maxdiameter
		self.diameter = 0
		super().__init__(x, y, 0, 0, 'circle', EXPLODECOLOR)

	def draw(self):
		oldmode = turtle.resizemode()
		turtle.shapesize(outline=self.diameter)
		id = super().draw()
		turtle.resizemode(oldmode)
		return id
	
	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, self.diameter

	def step(self):
		newsize = abs(math.sin(math.radians(self.age) + 180))
		if newsize < 0.05:
			engine.del_obj(self)
			return
		self.diameter = newsize * (self.maxdiameter * 2)
		super().step()

class Ground(engine.GameObject):
	def __init__(self, ulx, uly, lrx, lry):
		self.groundlevel = uly
		turtle.register_shape('ground', (
			(ulx, uly), (lrx, uly), (lrx, lry), (ulx, lry)
		))
		super().__init__(0, 0, 0, 1, 'ground', GROUNDCOLOR)

	def get_groundlevel(self):
		return self.groundlevel
	def isstatic(self):
		return True

# collision handling

def iscoll_circle(obj1, obj2):
	x1, y1, r1 = obj1.get_bc()
	x2, y2, r2 = obj2.get_bc()

	# from http://devmag.org.za/2009/04/13/basic-collision-detection-in-2d-part-1/
	# take the Euclidean distance between the center points, and if
	# that's less than the sum of the radii, then intersection occurred
	d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
	return d < (r1 + r2)

def coll_groundnoboom2(obj, ground):
	return coll_groundnoboom1(ground, obj)
def coll_groundnoboom1(ground, obj):
	x, y, r = obj.get_bc()
	if y <= ground.get_groundlevel():
		engine.del_obj(obj)

def coll_ground2(obj, ground):
	return coll_ground1(ground, obj)
def coll_ground1(ground, obj):
	x, y, r = obj.get_bc()
	if y <= ground.get_groundlevel():
		engine.add_obj(Boom(x, y, r))
		engine.del_obj(obj)

def coll_city2(obj, city):
	return coll_city1(city, obj)
def coll_city1(city, obj):
	if iscoll_circle(city, obj):
		x, y, r = city.get_bc()
		engine.add_obj(Boom(x, y, r))
		engine.del_obj(obj)
		city.hit()

def coll_air2air(obj1, obj2):
	if iscoll_circle(obj1, obj2):
		x1, y1, r1 = obj1.get_bc()
		x2, y2, r2 = obj2.get_bc()
		engine.add_obj(Boom(x1, y1, r1))
		engine.add_obj(Boom(x2, y2, r2))
		engine.del_obj(obj1)
		engine.del_obj(obj2)
		kill()

# callback routines

def newenemy_cb():
	xpos = random.randint(MINX, MAXX)
	obj = Enemy(xpos, MAXY, math.copysign(XFALLRATE, xpos)*-1.25, YFALLRATE)
	engine.add_obj(obj)

def fire_cb(x, y):
	if y < GUNY:
		return
	theta = math.atan2(y - GUNY, x - GUNX)
	if theta == 0:
		return
	# from http://en.wikipedia.org/w/index.php?title=Projectile_motion&oldid=540166443#The_maximum_height_of_projectile, rearranging for v0
	h = y - GUNY
	v0 = math.sqrt((2 * g * h) / (math.sin(theta) ** 2))
	engine.add_obj(Missile(GUNX, GUNY, v0, theta))
	return

	if x != 0:
		# from http://www.physicsforums.com/showthread.php?t=419561,
		# in part
		m = (y - GUNY) / (x - GUNX)
		if x - GUNX < 0:
			deltax = GUNX - (CLIMBRATE / math.sqrt(1 + m**2))
		else:
			deltax = GUNX + (CLIMBRATE / math.sqrt(1 + m**2))
		deltay = abs(m * deltax)
	else:
		deltax = 0
		deltay = CLIMBRATE
	engine.add_obj(Missile(GUNX, GUNY, deltax, deltay))

def demo_keypress_cb(dummy):
	global exitdemo
	exitdemo = True
	engine.exit_engine()

def demofire_cb():
	x = random.randint(MINX, MAXX)
	y = random.randint(GROUNDY, MAXY)
	fire_cb(x, y)

def demo_postinit_cb():
	engine.add_random_event(DEMOFIREPROB, demofire_cb)
	turtle.goto(0, GROUNDY-75)
	turtle.color('red')
	turtle.write('DEMO', align='center', font=('Arial', 14, 'normal'))

def quit_cb(key):
	if key == 'q' or key == 'Q':
		engine.exit_engine()

# game and demo mode

score = 0
cities = NCITIES

def banner(s):
	turtle.home()
	turtle.color('white')
	turtle.write(s, True, align='center', font=('Arial', 48, 'italic'))
	time.sleep(3)
	turtle.undo()

def draw_score():
	turtle.goto(0, GROUNDY-25)
	turtle.dot(50, GROUNDCOLOR)
	turtle.color('red')
	turtle.write(score, align='center', font=('Arial', 14, 'normal'))

def kill():
	global score
	score = score + 100
	draw_score()

def citygoboom():
	global cities
	cities = cities - 1
	if cities == 0:
		banner('LOSER!')
		engine.exit_engine()

def draw_stars():
	for i in range(NSTARS):
		x = random.randint(MINX, MAXX)
		y = random.randint(GROUNDY, MAXY)
		turtle.goto(x, y)
		turtle.color('white')
		turtle.dot(1)

def play(postfn=None):
	global score, cities

	score = 0
	cities = NCITIES

	engine.add_obj(Ground(MINX, GROUNDY, MAXX, MINY))
	draw_score()

	draw_stars()

	# we built this city on rock and roll
	xcoords = list(range(MINX, MAXX, WIDTH // (NCITIES+1)))[1:-1]
	for x in xcoords:
		engine.add_obj(City(x, GROUNDY))

	engine.add_random_event(NEWENEMYPROB, newenemy_cb)

	engine.register_collision(City, Enemy, coll_city1)
	engine.register_collision(Enemy, City, coll_city2)
	engine.register_collision(Ground, Enemy, coll_ground1)
	engine.register_collision(Enemy, Ground, coll_ground2)
	engine.register_collision(Enemy, Missile, coll_air2air)
	engine.register_collision(Missile, Enemy, coll_air2air)

	engine.register_collision(Ground, Missile, coll_groundnoboom1)
	engine.register_collision(Missile, Ground, coll_groundnoboom2)

	if postfn:
		postfn()
	engine.engine()

def intro_screen():
	banner("Turtle\nCommand")

def demo():
	global exitdemo
	exitdemo = False

	while not exitdemo:
		engine.init_engine()
		engine.set_keyboard_handler(demo_keypress_cb)
		play(demo_postinit_cb)

def game():
	engine.init_engine()
	engine.set_mouse_handler(fire_cb)
	engine.set_keyboard_handler(quit_cb)
	play()

# main routine

if __name__ == '__main__':
	#random.seed(86753)

	engine.init_screen(WIDTH, HEIGHT)
	turtle.bgcolor(BGCOLOR)
	intro_screen()
	turtle.tracer(1000)
	demo()
	banner('Get ready...')
	game()
