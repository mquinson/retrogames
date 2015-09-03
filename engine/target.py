# carnival target shooting game in faux 3D
#
# original code - John Aycock; 3D background and timer - Etienne Pitout
#
# target plane is blue background, upon which is layered black strips
# (the windows for the targets to move through) then the targets are
# created, then (and order is important!) background-color-blue strips
# are created that extend from sides of target windows to offscreen;
# these strips are active and stay in front of targets, so target objects
# appear to go behind them, and this is an easy way to have targets not
# visible for a given time
# 
# XXX bug - shooting targets scrolling but not visible works
# XXX bug - shots collide as if only back plane exists

import math
import turtle
import engine
import time

WIDTH = 640
HEIGHT = 480

BGCOLOR = 'lightblue'
TWCOLOR = 'black'			# "TW" = "target window"
TCOLOR = 'green'
GUNCOLOR = 'gray42'
SHOTCOLOR = 'red'
GRCOLOR = 'tan'
WALLCOLOR = 'grey10'
ROOFCOLOR = 'grey30'
NTARGETS = 10

TOPROW = HEIGHT / 2 * 2/3
TOPROWDELTA = -3
BOTROW = HEIGHT / 2 * 1/3
BOTROWDELTA = +1
TWWIDTH = WIDTH * 1/2
TWHEIGHT = HEIGHT // 10
GRHEIGHT = -BOTROW
SPACER = 25				# thin border around target windows

MINALPHA = 10				# alpha is angle of gun
MAXALPHA = 20
STEPALPHA = 1
MINBETA = -45				# beta is L/R angle of gun (0 is center)
MAXBETA = -MINBETA
STEPBETA = 5

GUNLEN = 400
GUNY = -HEIGHT/2 - 25
DISTANCE = 1500				# from gun origin to target plane
					# along ground (adjacent to alpha)

RECOILDIST = 10
RECOILSTEPS = 3
SHOTTIMER = 10

ntargets = NTARGETS * 2			# two rows of NTARGETS
GUNS = {}				# precompute all gun shapes

class TargetWindow(engine.GameObject):
	def __init__(self, y):
		super().__init__(TWWIDTH/-2, y, 0, 0, 'strip', TWCOLOR)
	def isstatic(self):
		return True

class Obscurer(engine.GameObject):
	def __init__(self, x, y):
		super().__init__(x, y, 0, 0, 'strip', BGCOLOR)
	def isoob(self):
		# this is rendered OOB on purpose
		return False

class LeftWall(engine.GameObject):
	def __init__(self):
		super().__init__(-WIDTH//2, HEIGHT//2, 0, 0,
				 'LeftWall', WALLCOLOR)

class RightWall(engine.GameObject):
	def __init__(self):
		super().__init__(WIDTH//2, HEIGHT//2, 0, 0,
				 'RightWall', WALLCOLOR)

class Target(engine.GameObject):
	def __init__(self, x, rowy, deltax):
		super().__init__(x, rowy-TWHEIGHT/2,
				 deltax, 0, 'turtle', TCOLOR)
	def getul(self):
		# sizes via trial and error
		return (self.x - 10, self.y + 10)
	def getlr(self):
		# sizes via trial and error
		return (self.x + 10, self.y - 10)
	def isoob(self):
		# target never goes out of bounds, just wraps around
		# simply shift existing target to entering target's position;
		# this keeps engine from deleting the object and messing up
		# the drawing order
		#
		# doesn't need to be as precise as tile demo, because the
		# movement is hidden behind the obscuring strips
		leftedge = -WIDTH // 2
		rightedge = WIDTH // 2

		if self.x <= leftedge:
			self.x += WIDTH
		elif self.x >= rightedge:
			self.x -= WIDTH
		return False

class Gun(engine.GameObject):
	def __init__(self):
		# starting angles of gun
		self.alpha = MINALPHA
		self.beta = 0
		# recoil animation playing?
		self.anim = False
		super().__init__(0, GUNY, 0, 0, GUNS[self.alpha], GUNCOLOR)
	def isoob(self):
		return False
	def heading(self):
		return 0 - self.beta
	def getalpha(self):
		return self.alpha
	def getbeta(self):
		return self.beta
	def adjustalpha(self, delta):
		newalpha = self.alpha + delta
		if newalpha < MINALPHA or newalpha > MAXALPHA:
			return
		self.alpha = newalpha
		self.shape = GUNS[self.alpha]
		self.update()
	def adjustbeta(self, delta):
		newbeta = self.beta + delta
		if newbeta < MINBETA or newbeta > MAXBETA:
			return
		self.beta = newbeta
		self.update()
	def canshoot(self):
		return not self.anim
	def recoil(self):
		self.anim = True
		self.count = -RECOILSTEPS
		hyp = RECOILDIST / RECOILSTEPS
		betarad = math.radians(-self.beta)
		self.deltax = hyp * math.sin(betarad)
		self.deltay = -hyp * math.cos(betarad)
	def move(self):
		if self.anim:
			self.count += 1
			if self.count == RECOILSTEPS-1:
				self.anim = False
				self.deltax = self.deltay = 0
			elif self.count == 0:
				self.deltax *= -1
				self.deltay *= -1
		super().move()

class Shot(engine.GameObject):
	def __init__(self, x, y):
		self.count = SHOTTIMER
		super().__init__(x, y, 0, 0, 'circle', SHOTCOLOR)
	def isoob(self):
		# shot is OOB in a time sense if its time has elapsed
		self.count -= 1
		return self.count < 0
	def getxy(self):
		return (self.x, self.y)

class Timer(engine.GameObject):
	def __init__(self):
		super().__init__(0, 10, 0, 0, 'circle', BGCOLOR)
		self.time = time.time()
		self.prevTime = 0
	def gettime(self):
		return round(time.time() - self.time)
	def update(self):
		if ntargets == 0:
			# game's done, nothing to see here
			return
		curTime = self.gettime()
		if curTime != self.prevTime:
			# prints time only if it's != prevTime to reduce lag
			draw_score(curTime)
		self.prevTime = curTime
		super().update()

def makeshape():
	turtle.home()			# return to known location & orientation
	turtle.lt(90)			# shapes use initial upward orientation

	turtle.begin_poly()
	for i in range(2):
		turtle.fd(TWWIDTH)
		turtle.rt(90)
		turtle.fd(TWHEIGHT)
		turtle.rt(90)
	turtle.end_poly()
	poly = turtle.get_poly()
	turtle.register_shape('strip', poly)

def makebigrect(starty, height, color):
	# draw a colored rectangle the width of the screen
	turtle.goto(-WIDTH / 2, starty)
	turtle.setheading(0)
	turtle.fillcolor(color)
	turtle.begin_fill()
	for i in range(2):
		turtle.fd(WIDTH)
		turtle.rt(90)
		turtle.fd(height)
		turtle.rt(90)
	turtle.end_fill()

def makescenery():
	turtle.bgcolor(BGCOLOR)
	makeshape()

	# ground
	makebigrect(GRHEIGHT, HEIGHT - abs(GRHEIGHT), GRCOLOR)
	# ceiling
	makebigrect(HEIGHT / 2, HEIGHT / 2 - (TOPROW + SPACER), ROOFCOLOR)

	# top row
	engine.add_obj(TargetWindow(TOPROW))
	for i in range(NTARGETS):
		spacing = WIDTH / NTARGETS
		x = i * spacing - WIDTH / 2
		engine.add_obj(Target(x, TOPROW, TOPROWDELTA))
	engine.add_obj(Obscurer(TWWIDTH/-2 - TWWIDTH, TOPROW))
	engine.add_obj(Obscurer(TWWIDTH/2, TOPROW))
	
	# bottom row
	engine.add_obj(TargetWindow(BOTROW))
	for i in range(NTARGETS):
		spacing = WIDTH / NTARGETS
		x = i * spacing - WIDTH / 2
		engine.add_obj(Target(x, BOTROW, BOTROWDELTA))
	engine.add_obj(Obscurer(TWWIDTH/-2 - TWWIDTH, BOTROW))
	engine.add_obj(Obscurer(TWWIDTH/2, BOTROW))
	
	# walls - need to be created after obscuring panels
	turtle.register_shape("LeftWall", (
		(0,0), (HEIGHT,0), (TWWIDTH, TOPROW - SPACER),
		(BOTROW - SPACER, TOPROW - SPACER)
	))
	turtle.register_shape("RightWall", (
		(0,0), (HEIGHT,0), (TWWIDTH, -TOPROW + SPACER),
		(BOTROW - SPACER, -TOPROW + SPACER)
	))
	engine.add_obj(LeftWall())
	engine.add_obj(RightWall())

def makegunshape(alpha):
	turtle.home()			# return to known location & orientation
	turtle.lt(90)			# shapes use initial upward orientation

	# apparent gun length due to alpha
	alpharad = math.radians(alpha)
	appgunlen = math.sin(alpharad) * GUNLEN

	thetarad = math.atan2(GUNLEN / 6, appgunlen)
	theta = math.degrees(thetarad)
	hyp = GUNLEN/6 / math.sin(thetarad)

	turtle.begin_poly()
	turtle.lt(180)
	turtle.fd(GUNLEN/6)
	turtle.rt(90 + theta)
	turtle.fd(hyp)
	turtle.rt(180 - 2*theta)
	turtle.fd(hyp)
	turtle.rt(90 + theta)
	turtle.fd(GUNLEN/6)
	turtle.end_poly()
	poly = turtle.get_poly()
	name = 'gun%d' % alpha
	turtle.register_shape(name, poly)
	return name
	
def makeguns():
	for alpha in range(MINALPHA, MAXALPHA+STEPALPHA, STEPALPHA):
		GUNS[alpha] = makegunshape(alpha)

def input_cb(key):
	if key == 'q' or key == 'Q':
		engine.exit_engine()
	elif key == 'Up':
		me.adjustalpha(STEPALPHA)
	elif key == 'Down':
		me.adjustalpha(-STEPALPHA)
	elif key == 'Left':
		me.adjustbeta(-STEPBETA)
	elif key == 'Right':
		me.adjustbeta(STEPBETA)
	elif key == 'space':
		if not me.canshoot():
			return
		me.recoil()

		# ignore travel distance and make the bullet instantaneous
		# just need to find the coordinates where it hit
		alpha = me.getalpha()
		beta = me.getbeta()
		alpharad = math.radians(alpha)
		betarad = math.radians(beta)
		# find y using trigonometry from side view
		y = DISTANCE * math.tan(alpharad) + GUNY
		# this calculation isn't correct from a 3D point of view
		# but it looks right onscreen
		x = GUNLEN * math.tan(betarad)
		engine.add_obj(Shot(x, y))

def pointinrect(p, ul, lr):
	x, y = p
	ulx, uly = ul
	lrx, lry = lr
	return ulx <= x <= lrx and lry <= y <= uly

def coll2(target, shot):
	return coll1(shot, target)
def coll1(shot, target):
	global ntargets
	if pointinrect(shot.getxy(), target.getul(), target.getlr()):
		engine.del_obj(target)
		ntargets -= 1
		if ntargets == 0:
			win(timer.gettime())

def draw_score(time):
	turtle.goto(0, HEIGHT//2 - 25)
	turtle.dot(50, ROOFCOLOR)
	turtle.color('black')
	turtle.write(time, align='center', font=('Arial', 14, 'normal'))

def win(time):
	mesg = 'Time to complete: %d' % time
	turtle.goto(0, -30)
	turtle.color('black')
	turtle.write(mesg, True, align='center', font=('Arial', 24, 'italic'))

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(input_cb)
	makescenery()
	makeguns()
	me = Gun()
	engine.add_obj(me)
	timer = Timer()
	engine.add_obj(timer)
	engine.register_collision(Shot, Target, coll1)
	engine.register_collision(Target, Shot, coll2)
	engine.engine()
