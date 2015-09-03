# python3 flappy.py

import time
import random
import turtle
import engine

WIDTH = 640
HEIGHT = 480

MYX = 0 - WIDTH // 3 // 2
MYY = 0
MYDELTA = 2
MYMAXMOVE = 25
MYCOLOR = 'black'
MYSHAPE = 'triangle'

PIPEDELTA = 1
PIPEWIDTH = 15
PIPEFREQ = 125
PIPECOLOR = 'darkgreen'
PIPEUNIT = 20
PIPEUNITS = HEIGHT // PIPEUNIT
PIPEGAP = 5			# in PIPEUNITs
PIPEMIN = 2			# in PIPEUNITs

BGCOLOR = 'lightblue'
TEXTCOLOR = 'black'

# state singleton class

class S:
	def __init__(self):
		self.playing = False	# game state
		self.me = None
		self.score = 0
		self.pipecounter = 0
s = None

# class for throwing an exception

class Replay(BaseException):	pass

# game objects

class Pipe(engine.GameObject):
	def __init__(self, shape, height, y, scoredelta):
		self.height = height
		self.scoredelta = scoredelta
		super().__init__(engine.MAXX-PIPEWIDTH, y,
				 -PIPEDELTA, 0, shape, PIPECOLOR)

	def move(self):
		oldx = self.x
		super().move()
		if oldx > MYX and self.x <= MYX:
			# cleared a pipe
			s.score += self.scoredelta

	# XXX assumes the rectangle is an AABB
	def xyinrect(self, x, y):
		if self.x <= x <= self.x+PIPEWIDTH and \
		   self.y <= y <= self.y+self.height:
			return True
		return False

def upperpipe(shape, height):
	return Pipe(shape, height, engine.MAXY-height, 0)
def lowerpipe(shape, height):
	return Pipe(shape, height, engine.MINY, 1)

class Me(engine.GameObject):
	def __init__(self):
		super().__init__(MYX, MYY, 0, -MYDELTA, MYSHAPE, MYCOLOR)
		self.uptime = -1

	def delete(self):
		# this catches OOB cases as well as collisions
		super().delete()
		lose()

	def flap(self):
		self.deltay = +MYDELTA
		self.uptime = MYMAXMOVE

	def move(self):
		self.uptime -= 1
		if self.uptime < 0:
			self.deltay = -MYDELTA
		super().move()

	def getx(self):		return self.x
	def gety(self):		return self.y

# callbacks

def input_cb(key):
	if key == 'q' or key == 'Q':
		exit()
	if key == 'space':
		if not s.playing:
			# replay
			raise Replay()
		else:
			s.me.flap()

def newpipe_cb():
	s.pipecounter -= 1
	if s.pipecounter <= 0:
		s.pipecounter = PIPEFREQ
		lheight = random.randint(PIPEMIN, PIPEUNITS-PIPEGAP-PIPEMIN)
		uheight = PIPEUNITS-lheight-PIPEGAP
		l = lowerpipe(ht2name(lheight), lheight*PIPEUNIT)
		u = upperpipe(ht2name(uheight), uheight*PIPEUNIT)
		engine.add_obj(l)
		engine.add_obj(u)

def coll_cb(me, pipe):
	if pipe.xyinrect(me.getx(), me.gety()):
		engine.del_obj(me)
		lose()
def coll_cb2(pipe, me):
	return coll_cb(me, pipe)

# high-level routines: initialization, title screen, gameplay

def ht2name(n):
	return str(n)

def makepipes():
	for i in range(PIPEMIN, PIPEUNITS):
		name = ht2name(i)
		ulx = i * PIPEUNIT
		lrx = 0
		uly = 0
		lry = PIPEWIDTH
		turtle.register_shape(name, (
			(ulx, uly), (lrx, uly), (lrx, lry), (ulx, lry)
		))

def init():
	engine.init_screen(WIDTH, HEIGHT)
	turtle.bgcolor(BGCOLOR)
	makepipes()

def banner(s, color=TEXTCOLOR):
	turtle.home()
	turtle.color(color)
	turtle.write(s, True, align='center', font=('Arial', 48, 'italic'))
	time.sleep(3)
	turtle.undo()

def title_screen():
	banner('FLAPPY\nTURTLE')

def lose():
	s.playing = False
	mesg = 'Score %d - press space to play again' % s.score
	turtle.goto(0, 0)
	turtle.color(TEXTCOLOR)
	turtle.write(mesg, True, align='center', font=('Arial', 24, 'italic'))

def play():
	global s
	s = S()

	engine.init_engine()
	engine.set_keyboard_handler(input_cb)
	engine.add_random_event(1.0, newpipe_cb)
	engine.register_collision(Me, Pipe, coll_cb)
	engine.register_collision(Pipe, Me, coll_cb2)

	s.me = Me()
	engine.add_obj(s.me)

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
