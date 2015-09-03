# python3 invader.py

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

GROUNDY = MINY + HEIGHT // 6
MOVELEN = 7
MYSHOTSPEED = 4
INVADERROWS = 5
INVADERCOLS = 6
INVADERSPEED = 2
INVADERHSPACE = 75
INVADERVSPACE = INVADERHSPACE // 2
INVADERSHIFT = INVADERVSPACE // 2
XGRIDSTART = MINX + INVADERHSPACE
YGRIDSTART = MAXY - INVADERVSPACE * 2
FIREPROB = 0.01
BOMBSPEED = 2
THEMCOLOR = 'purple'
MYCOLOR = ('green', 'yellow', 'red')
LIVES = len(MYCOLOR)
BGCOLOR = 'black'
GROUNDCOLOR = 'grey'
UFOPROB = 0.0033
UFOY = MAXY - 25
UFOSPEED = 4

# game objects

class UFO(engine.GameObject):
	def __init__(self, x, y, deltax, deltay):
		super().__init__(x, y, deltax, deltay, 'circle', THEMCOLOR)

	def delete(self):
		s.ufoactive = False
		super().delete()

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

class Invader(engine.GameObject):
	def __init__(self, x, y, deltax, deltay):
		super().__init__(x, y, deltax, deltay, 'turtle', THEMCOLOR)

	def sety(self, y):
		self.y = y

	def move(self):
		self.x = self.x + self.deltax * s.leftright

	def delete(self):
		s.invaders.remove(self)
		super().delete()

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

class Bomb(engine.GameObject):
	def __init__(self, x, y):
		super().__init__(x, y, 0, -BOMBSPEED, 'classic', THEMCOLOR)

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

class MyShot(engine.GameObject):
	def __init__(self, x, y, deltax, deltay):
		super().__init__(x, y, deltax, deltay,
				 'classic', MYCOLOR[s.lostlives])

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

class Me(engine.GameObject):
	def __init__(self, x, y):
		super().__init__(x, y, 0, 1,
				 'triangle', MYCOLOR[s.lostlives])

	def isstatic(self):
		# relatively static, anyway - want to suppress animation
		return True

	def draw(self):
		self.color = MYCOLOR[s.lostlives]
		return super().draw()

	def setx(self, x):
		self.x = x

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

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

def coll_ground2(obj, ground):
	return coll_ground1(ground, obj)
def coll_ground1(ground, obj):
	x, y, r = obj.get_bc()
	if y <= ground.get_groundlevel():
		engine.del_obj(obj)

def coll_air2air_bonus(obj1, obj2):
	coll_air2air(obj1, obj2, 1000)

def coll_air2air(obj1, obj2, points=100):
	if iscoll_circle(obj1, obj2):
		x1, y1, r1 = obj1.get_bc()
		x2, y2, r2 = obj2.get_bc()
		engine.del_obj(obj1)
		engine.del_obj(obj2)
		s.score = s.score + points
		draw_score()

def coll_gameover2(obj, ground):
	return coll_gameover1(ground, obj)
def coll_gameover1(ground, obj):
	x, y, r = obj.get_bc()
	if y <= ground.get_groundlevel():
		s.landed = True

def coll_loselife2(bomb, me):
	return coll_loselife1(me, bomb)
def coll_loselife1(me, bomb):
	if iscoll_circle(me, bomb):
		engine.del_obj(bomb)
		s.lostlives = s.lostlives + 1
		if s.lostlives != LIVES:
			# change color
			me.update()
	
# callback routines

def fire_cb():
	# pick an invader randomly
	obj = random.choice(s.invaders)
	x, y = obj.get_bc()[:2]
	# bombs away!
	engine.add_obj(Bomb(x, y))

def ufo_cb():
	if s.ufoactive:
		return
	s.ufoactive = True
	# change the horizontal direction up
	if random.random() < 0.5:
		engine.add_obj(UFO(MINX, UFOY, UFOSPEED, 0))
	else:
		engine.add_obj(UFO(MAXX, UFOY, -UFOSPEED, 0))

def gridmove_cb():
	# XXX better to keep lm & rm continuously updated instead
	lm = min([obj.get_bc()[0] for obj in s.invaders])
	rm = max([obj.get_bc()[0] for obj in s.invaders])
	if rm + INVADERSPEED >= MAXX or lm - INVADERSPEED <= MINX:
		s.leftright = s.leftright * -1
		for obj in s.invaders:
			y = obj.get_bc()[1]
			obj.sety(y - INVADERSHIFT)

def winlose_cb():
	if len(s.invaders) == 0:
		banner('YOU WIN!')
		exit()
	elif s.landed:
		banner("They're heeeere.")
		banner('GAME OVER')
		exit()
	elif s.lostlives == LIVES:
		banner('GAME OVER')
		exit()
	
def input_cb(key):
	x, y, r = s.me.get_bc()

	if key == 'q' or key == 'Q':
		engine.exit_engine()
	elif key == 'Left' and x - r > MINX:
		s.me.setx(x - MOVELEN)
		s.me.update()
	elif key == 'Right' and x + r < MAXX:
		s.me.setx(x + MOVELEN)
		s.me.update()
	elif key == 'space':
		engine.add_obj(MyShot(x, y, 0, MYSHOTSPEED))

# game state and main game

class S:
	def __init__(self):
		self.me = None
		self.invaders = []
		self.leftright = 1
		self.lostlives = 0
		self.landed = False
		self.ufoactive = False
		self.score = 0
s = None
		
def banner(s):
	turtle.home()
	turtle.color('white')
	turtle.write(s, True, align='center', font=('Arial', 48, 'italic'))
	time.sleep(3)
	turtle.undo()

def title_screen():
	banner('TURTLE\nINVADERS')

def draw_score():
	turtle.goto(0, GROUNDY-25)
	turtle.dot(50, GROUNDCOLOR)
	turtle.color('red')
	turtle.write(s.score, align='center', font=('Arial', 14, 'normal'))

def play():
	global s
	s = S()

	engine.init_engine()
	engine.set_keyboard_handler(input_cb)
	engine.add_obj(Ground(MINX, GROUNDY, MAXX, MINY))

	s.me = Me(0, GROUNDY + 10)
	engine.add_obj(s.me)

	# the grid o' evil
	for i in range(INVADERROWS):
		for j in range(INVADERCOLS):
			enemy = Invader(XGRIDSTART + j * INVADERHSPACE,
					YGRIDSTART - i * INVADERVSPACE,
					INVADERSPEED, 0)
			s.invaders.append(enemy)
			engine.add_obj(enemy)
	engine.add_random_event(FIREPROB, fire_cb)
	engine.add_random_event(UFOPROB, ufo_cb)

	# not quite so random - do this at start of each time step
	# order is important - if no invaders left, gridmove won't be happy
	engine.add_random_event(1.0, winlose_cb)
	engine.add_random_event(1.0, gridmove_cb)

	engine.register_collision(Ground, Bomb, coll_ground1)
	engine.register_collision(Bomb, Ground, coll_ground2)
	engine.register_collision(UFO, MyShot, coll_air2air_bonus)
	engine.register_collision(MyShot, UFO, coll_air2air_bonus)
	engine.register_collision(Invader, MyShot, coll_air2air)
	engine.register_collision(MyShot, Invader, coll_air2air)
	engine.register_collision(Ground, Invader, coll_gameover1)
	engine.register_collision(Invader, Ground, coll_gameover2)
	engine.register_collision(Me, Bomb, coll_loselife1)
	engine.register_collision(Bomb, Me, coll_loselife2)

	draw_score()

	engine.engine()

# main routine

if __name__ == '__main__':
	#random.seed(86753)

	engine.init_screen(WIDTH, HEIGHT)
	turtle.bgcolor(BGCOLOR)
	title_screen()
	play()
