# python3 asteroids.py
# by Etienne Pitout

import math
import time
import random
import turtle
import engine

WIDTH = 640
HEIGHT = 480
MAXY = HEIGHT // 2
MINY = -HEIGHT // 2
MAXX = WIDTH // 2
MINX = -WIDTH // 2

MYX = 0
MYY = 0
MYDELTA = 0
MYCOLOR = 'white'
MYSHAPE = 'triangle'
THETA = 10

BGCOLOR = 'black'
TEXTCOLOR = 'white'
MYSHOTSPEED = 4
NUMSHOT = 0
MAXAS = 5		#maximum asteroids
CURAS = 0
MAXSHOTS = 5
DECEL = 0.03
SHOTLIFE = 100

# state singleton class

class S:
	def __init__(self):
		self.playing = False	# game state
		self.me = None
		self.shots = 0
		self.curas = 0
		self.score = 0
s = None

# class for throwing an exception

class Replay(BaseException):	pass

# game objects

class Me(engine.GameObject):
	def __init__(self):
		self.dirx = 1.0
		self.diry = 0.0
		self.theta = 0
		super().__init__(MYX, MYY, 0, -MYDELTA, MYSHAPE, MYCOLOR)
		turtle.tiltangle(0)

	def heading(self):
		dx = self.dirx
		dy = self.diry
		return turtle.towards(self.x + dx, self.y + dy)

	def delete(self):
		# this catches OOB cases as well as collisions
		super().delete()
	
	def moveu(self):
		#move forward
		self.deltax += round(self.dirx, 3)
		self.deltay += round(self.diry, 3)

	def movel(self):
		#turn left
		self.theta += THETA
		newdirx = math.cos(math.radians(self.theta))
		newdiry = math.sin(math.radians(self.theta))
		self.dirx = newdirx
		self.diry = newdiry
		#self.moveu() #aligns the ship

	def mover(self):
		#turn right
		self.theta -= THETA
		newdirx = math.cos(math.radians(self.theta))
		newdiry = math.sin(math.radians(self.theta))
		self.dirx = newdirx
		self.diry = newdiry
		#self.moveu()
	
	def move(self):
		#deceleration
		if self.deltax > 0:
			self.deltax -= self.deltax * DECEL
		if self.deltay > 0:
			self.deltay -= self.deltay * DECEL
		if self.deltax < 0:
			self.deltax -= self.deltax * DECEL
		if self.deltay < 0:
			self.deltay -= self.deltay * DECEL
		newdx = self.deltax
		newdy = self.deltay
		#screen wraparound
		if self.x >= WIDTH / 2:
			self.x = -WIDTH / 2
		elif self.x <= -WIDTH / 2:
			self.x = WIDTH / 2 - 2
		elif self.y >= HEIGHT / 2:
			self.y = -HEIGHT / 2
		elif self.y <= -HEIGHT / 2:
			self.y = HEIGHT / 2
		super().move()

	def update(self):
		turtle.shapesize(1,1.4)
		#screen wraparound
		if self.x > WIDTH / 2:
			self.x = WIDTH / 2
		elif self.x < -WIDTH / 2:
			self.x = -WIDTH / 2
		elif self.y > HEIGHT / 2:
			self.y = HEIGHT / 2
		elif self.y < -HEIGHT / 2:
			self.y = -HEIGHT / 2
		super().update()

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

	def getx(self):		return self.x
	def gety(self):		return self.y
	def getdirx(self):	return self.dirx
	def getdiry(self):	return self.diry
	def getdelx(self):	return self.deltax
	def getdely(self):	return self.deltay

class MyShot(engine.GameObject):
	def __init__(self, x, y, deltax, deltay):
		super().__init__(x, y, deltax, deltay,
				 'circle', 'white')

	def delete(self):
		# this catches OOB cases as well as collisions
		super().delete()

	def update(self):
		turtle.shapesize(0.2,0.2)
		turtle.settiltangle(0)
		
		#screen wraparound
		if self.x >= WIDTH / 2:
			self.x = -WIDTH / 2
		elif self.x <= -WIDTH / 2:
			self.x = WIDTH / 2 - 2
		elif self.y >= HEIGHT / 2:
			self.y = -HEIGHT / 2
		elif self.y <= -HEIGHT / 2:
			self.y = HEIGHT / 2
		
		super().update()

		if self.age >= SHOTLIFE:
			engine.del_obj(self)
			s.shots -= 1

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

class Asteroid(engine.GameObject):
	def __init__(self, x, y, deltax, deltay, sizx, sizy):
		super().__init__(x, y, deltax, deltay,
				 'turtle', 'white')
		self.sizex = sizx
		self.sizey = sizy
	
	def delete(self):
		# this catches OOB cases as well as collisions
		super().delete()
	
	def update(self):
		turtle.shapesize(self.sizex, self.sizey)
		turtle.settiltangle(0)
		#screen wraparound
		if self.x >= WIDTH / 2:
			self.x = -WIDTH / 2
		elif self.x <= -WIDTH / 2:
			self.x = WIDTH / 2 - 2
		elif self.y >= HEIGHT / 2:
			self.y = -HEIGHT / 2
		elif self.y <= -HEIGHT / 2:
			self.y = HEIGHT / 2
		super().update()
		turtle.shapesize(0.1, 0.1)

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 10

# collision handling

def iscoll_circle(obj1, obj2):
	x1, y1, r1 = obj1.get_bc()
	x2, y2, r2 = obj2.get_bc()

	# from http://devmag.org.za/2009/04/13/basic-collision-detection-in-2d-part-1/
	# take the Euclidean distance between the center points, and if
	# that's less than the sum of the radii, then intersection occurred
	d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
	return d < (r1 + r2)

def col_asteroid2(obj2, obj1):
	return col_asteroid(obj1, obj2)

def col_asteroid(obj1, obj2):
	if iscoll_circle(obj1, obj2):
		x1, y1, r1 = obj1.get_bc()
		x2, y2, r2 = obj2.get_bc()
		engine.del_obj(obj1)
		engine.del_obj(obj2)
		s.shots -= 1
		s.curas -= 1
		s.score += 1
		draw_score()
		#create 2 new asteroids
		if(obj1.sizex > 2 or obj1.sizey > 2):
			xpos = obj1.x
			ypos = obj1.y
			if(obj1.sizex == 1):
				xsize = 1
			else:
				xsize = random.randint(1, obj1.sizex-1)
			if(obj1.sizey == 1):
				ysize = 1
			else:
				ysize = random.randint(1, obj1.sizey-1)
			deltx = random.randint(-1, 1)
			delty = random.randint(-1, 1)
			obj = Asteroid(xpos, ypos, deltx, delty, xsize, ysize)
			engine.add_obj(obj)
			xpos = obj1.x
			ypos = obj1.y
			if(obj1.sizex == 1):
				xsize = 1
			else:
				xsize = random.randint(1, obj1.sizex-1)
			if(obj1.sizey == 1):
				ysize = 1
			else:
				ysize = random.randint(1, obj1.sizey-1)
			deltx = random.randint(-1, 1)
			delty = random.randint(-1, 1)
			obj = Asteroid(xpos, ypos, deltx, delty, xsize, ysize)
			engine.add_obj(obj)

def col_gameover(obj1, obj2):
	if iscoll_circle(obj1, obj2):
		x1, y1, r1 = obj1.get_bc()
		x2, y2, r2 = obj2.get_bc()
		engine.del_obj(obj1)
		engine.del_obj(obj2)
		lose()

# callbacks

def spawn_asteroid_cb():
	if(s.curas >= MAXAS):
		return
	xpos = random.randint(MINX, MAXX)
	ypos = random.randint(MINY, MAXY)
	xsize = random.randint(1, 5)
	ysize = random.randint(1, 5)
	deltx = random.randint(-5, 5)
	delty = random.randint(-5, 5)
	obj = Asteroid(xpos, ypos, deltx, delty, xsize, ysize)
	engine.add_obj(obj)
	s.curas += 1

def input_cb(key):
	if key == 'q' or key == 'Q':
		exit()
	if key == 'space':
		if not s.playing:
			# replay
			raise Replay()
		else:
			if(s.shots <= MAXSHOTS):
				engine.add_obj(MyShot(s.me.getx(), s.me.gety(), MYSHOTSPEED * s.me.getdirx() + s.me.getdelx(), MYSHOTSPEED * s.me.getdiry() + s.me.getdely()))
				s.shots += 1
	if key == 'Up':
		s.me.moveu()
	elif key =='Right':
		s.me.mover()
	elif key =='Left':
		s.me.movel()

# high-level routines: initialization, title screen, gameplay

def init():
	engine.init_screen(WIDTH, HEIGHT)
	turtle.bgcolor(BGCOLOR)

def banner(s, color=TEXTCOLOR):
	turtle.home()
	turtle.color(color)
	turtle.write(s, True, align='center', font=('Arial', 48, 'italic'))
	time.sleep(3)
	turtle.undo()

def title_screen():
	banner('TURTLEOIDS')

def lose():
	s.playing = False
	mesg = 'Score %d - press space to play again' % s.score
	turtle.goto(0, 0)
	turtle.color(TEXTCOLOR)
	turtle.write(mesg, True, align='center', font=('Arial', 24, 'italic'))

def draw_score():
	turtle.goto(0, MAXY-25)
	turtle.dot(50, 'black')
	turtle.color('white')
	turtle.write(s.score, align='center', font=('Arial', 14, 'normal'))

def play():
	global s
	s = S()

	engine.init_engine()
	engine.set_keyboard_handler(input_cb)

	s.me = Me()
	engine.add_obj(s.me)
	
	engine.add_random_event(0.01, spawn_asteroid_cb)

	engine.register_collision(Asteroid, MyShot, col_asteroid)
	engine.register_collision(MyShot, Asteroid, col_asteroid2)
	engine.register_collision(Me, Asteroid, col_gameover)
	engine.register_collision(Asteroid, Me, col_gameover)

	draw_score()

	s.playing = True
	engine.engine()

# main routine

if __name__ == '__main__':
	init()
	title_screen()
	while True:
		try:
			play()
		except Replay:
			pass
