# animate a stick person
# stick figure by Sarah Storteboom

import turtle
import engine
import random
import math

WIDTH = 640
HEIGHT = 480

FGCOLOR = 'grey70'
BGCOLOR = 'grey23'

POPCOLOR = 'white'
POPPROB = 0.3
POPDURATION = 1

GROUNDPROB = 0.2
GROUNDX = -WIDTH / 6 + 75
GROUNDY = -HEIGHT / 3 + 27
GROUNDLEN = 200
NGROUNDLINES = 3

FIGUREX = 100
FIGUREY = 50
LONGDISTY = 150
MEDDISTY = 100

NSTEPS = 10			# tweened steps between key frames
UPDATESPERSTEP = 1		# how long to hold each step's position

### trees - code from eg-retracepoly.py

class Tree(engine.GameObject):
	def __init__(self, shape, x, y, deltax, color):
		super().__init__(x, y, deltax, 0, shape, color)
	def heading(self):
		return 90

def maketree_r(S, L, scale):
	assert type(L) == type( [] )
	for elem in L:
		if type(elem) == type( [] ):
			maketree_r( [ S[-1] ], elem, scale)
		else:
			assert type(elem) == type( () )
			assert len(elem) == 2
			elem = (scale * elem[0], scale * elem[1])
			turtle.goto(elem)
			S.append(elem)
	# now unwind backwards
	while len(S) > 0:
		elem = S.pop()
		turtle.goto(elem)

def maketree(name, scale, L):
	turtle.home()
	turtle.begin_poly()
	stack = [ (0, 0) ]
	maketree_r(stack, L, scale)
	turtle.end_poly()
	poly = turtle.get_poly()
	turtle.register_shape(name, poly)

def maketrees():
	L = [
		(-3,-3), (0.5,0), (4,-2.7), (0.4,-0.5), (0.4,-3),
		(-3.2,-5), (0.4,-3.5), (3.8,-5), (0.45,-4), (0.45,-5.8),
		(-2,-8.2), (0.51,-6.3), (3.9,-8), (0.51,-7),
		# trunk
		(0.55,-8), (0.6,-9), (0.7,-10), (1,-11), (1.1,-12),
		# ground
		(-2,-12.2), (-0.5,-12.5), [ (3,-12.1) ], [ (2,-12) ],
		[ (-1,-12.75), [ (-2.8,-12.6) ], (0.8,-12.7), (2.5,-12.5) ]
	]
	maketree('smalltree', 5, L)
	maketree('bigtree', 10, L)

### screen "pop" effect to hint at film

class Pop(engine.GameObject):
	def __init__(self, x, y, size, shape, color):
		super().__init__(x, y, 0, 0, shape, color)
	def isstatic(self):
		return False
	def isoob(self):
		if self.age > POPDURATION:
			# OOB in the temporal sense
			return True
		return False

POPS = []

def makepop(fn, *args):
	turtle.home()
	turtle.begin_poly()
	fn(*args)
	turtle.end_poly()
	name = 'pop%d' % len(POPS)
	turtle.register_shape(name, turtle.get_poly())
	POPS.append(name)

def makepops():
	# a few lines of various heights
	for i in (2, 10, 25, 50):
		makepop(lambda x: turtle.fd(x), i)
	# add some circles - bias so big ones show up more rarely
	for i in (2, 2, 2, 5):
		makepop(lambda x: turtle.circle(x), i)

def pop_cb():
	x = random.randint(-WIDTH / 2, WIDTH / 2)
	y = random.randint(-HEIGHT / 2, HEIGHT / 2)
	kind = random.choice(POPS)
	size = random.randint(1, 3)
	color = random.choice([POPCOLOR, FGCOLOR])
	engine.add_obj(Pop(x, y, size, kind, color))

### ground

GROUND = []

class Ground(engine.GameObject):
	def __init__(self, origx, origy, color):
		self.origx = origx
		self.origy = origy
		self.regenerate()
		super().__init__(self.x, self.y, 0, 0, self.shape, color)
	def heading(self):
		return self.h
	def isstatic(self):
		return False
	def update(self):
		if random.random() < GROUNDPROB:
			self.regenerate()
		super().update()
	def regenerate(self):
		# cue TARDIS whooping noise
		self.x = self.origx + random.randint(-3, +9)
		self.y = self.origy + random.randint(-3, +3)
		self.h = 90 + random.randint(-1, +1)
		self.shape = random.choice(GROUND)
		
def makeground():
	for i in range(GROUNDLEN-3, GROUNDLEN+9):
		turtle.home()
		turtle.begin_poly()
		turtle.fd(i)
		turtle.end_poly()
		name = 'gr%d' % i
		turtle.register_shape(name, turtle.get_poly())
		GROUND.append(name)

### tweening and figure classes

def makenothing():
	# there's much ado about it
	turtle.begin_poly()
	turtle.end_poly()
	turtle.register_shape('none', turtle.get_poly())

class Bird(engine.GameObject):
	# note that this class can't be static, because the segments
	# look to it for current x and y values
	def __init__(self, L, x, y, color):
		# keep weak references to component segments; it doesn't
		# prevent GC from removing them, but allows us to keep
		# this parent class around until all the segments are gone -
		# otherwise, the Bird parent class gets deleted once it's
		# OOB, and the last part of the flapping wing (no longer
		# seeing the parent's motion updates) just stays at the
		# edge of the screen flapping away
		import weakref
		self.components = weakref.WeakSet()

		# init parent object first
		super().__init__(x, y, -0.1, -0.025, 'none', BGCOLOR)

		# create all segments; see comments in Figure class
		for i in range(len(L[0])):
			segL = [ X[i] for X in L ]
			seg = Segment(segL, self, color)
			engine.add_obj(seg)
			self.components.add(seg)
	def isoob(self):
		if len(self.components) > 0:
			return False
		return True

class Figure(engine.GameObject):
	# note that this class can't be static, because the segments
	# look to it for current x and y values
	def __init__(self, L, x, y, color):
		# init parent object first
		super().__init__(x, y, 0, 0, 'none', BGCOLOR)

		# create all segments; each segment gets a list of just
		# its tweening data - ideally a game object should be
		# able to catch notifications of being added to the
		# game engine and we could move the add_obj to there,
		# but that doesn't happen at present
		for i in range(len(L[0])):
			segL = [ X[i] for X in L ]
			seg = Segment(segL, self, color)
			engine.add_obj(seg)

		# create head
		engine.add_obj(Head(self, color))

class Head(engine.GameObject):
	def __init__(self, parent, color):
		self.parent = parent
		super().__init__(parent.x-7, parent.y+9,
				 parent.deltax, parent.deltay, 'circle', color)

class Segment(engine.GameObject):
	def __init__(self, L, parent, color):
		self.i = 0
		self.L = L
		self.count = UPDATESPERSTEP
		self.stepcount = NSTEPS
		self.parent = parent
		t = L[self.i]
		self.h = t.heading
		super().__init__(t.x + parent.x, t.y + parent.y,
				 parent.deltax, parent.deltay, t.name, color)
	def heading(self):
		return self.h
	def update(self):
		# XXX should apply parent's delta x/y
		if self.count == 0:
			self.count = UPDATESPERSTEP
			t = self.L[self.i]
			self.h += t.dh
			self.x += t.dx
			self.y += t.dy
			if self.stepcount == 0:
				self.stepcount = NSTEPS
				# switch to next shape and reset params
				self.i = (self.i + 1) % len(self.L)
				t = self.L[self.i]
				self.x = t.x + self.parent.x
				self.y = t.y + self.parent.y
				self.h = t.heading
				self.shape = t.name
			else:
				self.stepcount -= 1
		else:
			self.count -= 1
		super().update()

# bird key frame data

BKF1 = (
	[ (0,0), (3,0) ],		# right inner wing
	[ (3,0), (6,1) ],		# right outer wing
	[ (0,0), (-3,0) ],		# left inner wing
	[ (-3,0), (-6,1) ],		# left outer wing
)

BKF2 = (
	[ (0,0), (3,-1) ],		# right inner wing
	[ (3,-1), (6,0) ],		# right outer wing
	[ (0,0), (-3,-1) ],		# left inner wing
	[ (-3,-1), (-6,0) ],		# left outer wing
)

BKF3 = (
	[ (0,0), (3,-2) ],		# right inner wing
	[ (3,-2), (6,-1) ],		# right outer wing
	[ (0,0), (-3,-2) ],		# left inner wing
	[ (-3,-2), (-6,-1) ],		# left outer wing
)

BKF4 = (
	[ (0,0), (3,-2) ],		# right inner wing
	[ (3,-2), (6,-2.5) ],		# right outer wing
	[ (0,0), (-3,-2) ],		# left inner wing
	[ (-3,-2), (-6,-2.5) ],		# left outer wing
)

BKF5 = (
	[ (0,0), (3,-2) ],		# right inner wing
	[ (3,-2), (6,-4) ],		# right outer wing
	[ (0,0), (-3,-2) ],		# left inner wing
	[ (-3,-2), (-6,-4) ],		# left outer wing
)

BKF6 = (
	[ (0,0), (3,-1) ],		# right inner wing
	[ (3,-1), (6,-2.5) ],		# right outer wing
	[ (0,0), (-3,-1) ],		# left inner wing
	[ (-3,-1), (-6,-2.5) ],		# left outer wing
)

BKF7 = (
	[ (0,0), (3,0) ],		# right inner wing
	[ (3,0), (6,-1) ],		# right outer wing
	[ (0,0), (-3,0) ],		# left inner wing
	[ (-3,0), (-6,-1) ],		# left outer wing
)

BKF8 = (
	[ (0,0), (3,0) ],		# right inner wing
	[ (3,0), (6,0) ],		# right outer wing
	[ (0,0), (-3,0) ],		# left inner wing
	[ (-3,0), (-6,0) ],		# left outer wing
)

# figure key frame data

KF1 = (
	[ (700,225), (717,454) ],	# body
	[ (717,454), (717,598) ],	# top of moving leg
	[ (717,598), (819,698) ],	# bottom of moving leg
	[ (717,454), (731,595) ],	# top of standing leg
	[ (731,595), (744,734) ]	# bottom of standing leg
)

KF2 = (
	[ (698,223), (718,456) ],	# body
	[ (718,456), (637,584) ],	# top of moving leg
	[ (637,584), (601,737) ],	# bottom of moving leg
	[ (718,456), (728,593) ],	# top of standing leg
	[ (728,593), (742,731) ]	# bottom of standing leg
)

KF3 = (
	[ (699,225), (718,457) ],	# body
	[ (718,457), (657,593) ],	# top of moving leg
	[ (657,593), (604,738) ],	# bottom of moving leg
	[ (718,457), (769,587) ],	# top of standing leg
	[ (769,587), (825,732) ]	# bottom of standing leg
)

KF4 = (
	[ (697,224), (717,462) ],	# body
	[ (717,462), (730,592) ],	# top of moving leg
	[ (730,592), (744,732) ],	# bottom of moving leg
	[ (717,462), (787,583) ],	# top of standing leg
	[ (787,583), (895,712) ]	# bottom of standing leg
)

# at KF5, the legs swap positions, i.e., KF5 is a modified KF1, KF6
# is a modified KF2, &c.
KF5 = (
	[ (700,225), (717,454) ],	# body
	[ (717,454), (731,595) ],	# top of standing leg
	[ (731,595), (744,734) ],	# bottom of standing leg
	[ (717,454), (717,598) ],	# top of moving leg
	[ (717,598), (819,698) ]	# bottom of moving leg
)

KF6 = (
	[ (698,223), (718,456) ],	# body
	[ (718,456), (728,593) ],	# top of standing leg
	[ (728,593), (742,731) ],	# bottom of standing leg
	[ (718,456), (637,584) ],	# top of moving leg
	[ (637,584), (601,737) ]	# bottom of moving leg
)

KF7 = (
	[ (699,225), (718,457) ],	# body
	[ (718,457), (769,587) ],	# top of standing leg
	[ (769,587), (825,732) ],	# bottom of standing leg
	[ (718,457), (657,593) ],	# top of moving leg
	[ (657,593), (604,738) ]	# bottom of moving leg
)

KF8 = (
	[ (697,224), (717,462) ],	# body
	[ (717,462), (787,583) ],	# top of standing leg
	[ (787,583), (895,712) ],	# bottom of standing leg
	[ (717,462), (730,592) ],	# top of moving leg
	[ (730,592), (744,732) ]	# bottom of moving leg
)

_kfsegments = 0

def getheading(x1, y1, x2, y2):
#	return 90 - math.degrees(math.atan2(y2 - y1, x2 - x1))
	# math tweak because key frame coords assume (0,0) at top left
	return 90 + math.degrees(math.atan2(y2 - y1, x2 - x1))
def getkfstart(kf):
	# starting x, y are all relative to the first segment in list
	return kf[0][0]
def normalize(kf, i, scale):
	# adjust coords to be relative to start of key frame segments
	startx, starty = getkfstart(kf)
	[ (x1, y1), (x2, y2) ] = kf[i]
#	return [ ( (x1 - startx)*scale, (y1 - starty)*scale ),
#		 ( (x2 - startx)*scale, (y2 - starty)*scale ) ]
	# math tweak because key frame coords assume (0,0) at top left
	return [ ( (x1 - startx)*scale, -(y1 - starty)*scale ),
		 ( (x2 - startx)*scale, -(y2 - starty)*scale ) ]

class Tween:
	# just a container for all this data
	def __init__(self):
		self.name = ''
		self.x = self.y = self.heading = 0
		self.dx = self.dy = self.dh = 0

def maketweendata(kf1, kf2, steps, scale):
	global _kfsegments
	assert len(kf1) == len(kf2)	# must be able to match segments up

	L = []
	for i in range(len(kf1)):
		[ (x1, y1), (x2, y2) ] = normalize(kf1, i, scale)

		# Euclidean distance gives segment length
		seglen = ( (x2 - x1) ** 2 + (y2 - y1) ** 2 ) ** 0.5

		# make line segment into shape
		turtle.home()
		turtle.begin_poly()
		turtle.fd(seglen)
		turtle.end_poly()
		name = 'kf%d' % _kfsegments
		_kfsegments += 1
		turtle.register_shape(name, turtle.get_poly())

		# and compute initial heading
		heading = getheading(x1, y1, x2, y2)

		# extract out corresponding segment from key frame 2
		[ (x1b, y1b), (x2b, y2b) ] = normalize(kf2, i, scale)

		# use it to compute deltas for x, y, and heading; this is
		# where we need to be after N steps
		dx = x1b - x1
		dy = y1b - y1
		dh = getheading(x1b, y1b, x2b, y2b) - heading
		# weird special case that cropped up between BKF3 and BKF4 of
		# bird flap, where the computed delta in the heading takes the
		# long way around, as it were - adjust it to compensate
		if dh > 180:
			dh = dh - 360
		elif dh < -180:
			dh = dh + 360
		dx /= steps
		dy /= steps
		dh /= steps

		# place everything in a container
		c = Tween()
		c.name = name
		c.x, c.y = x1, y1
		c.heading = heading
		c.dx, c.dy = dx, dy
		c.dh = dh
		L.append(c)

	return L

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	turtle.bgcolor(BGCOLOR)
	engine.add_random_event(POPPROB, pop_cb)
	makepops()

	# parallax scrolling
	maketrees()
	# distant background
	engine.add_obj(Tree('smalltree', -50, LONGDISTY, +0.1, FGCOLOR))
	# medium-distance background
	engine.add_obj(Tree('bigtree', -WIDTH/2, MEDDISTY, +0.5, FGCOLOR))

	# ground
	makeground()
	for i in range(NGROUNDLINES):
		engine.add_obj(Ground(GROUNDX, GROUNDY, FGCOLOR))

	# precompute tweening data from key frames and add figure object
	makenothing()

	T = []
	KFL = [KF1, KF2, KF3, KF4, KF5, KF6, KF7, KF8]
	for (kf1, kf2) in zip(KFL, KFL[1:] + [KFL[0]]):
		T.append(maketweendata(kf1, kf2, NSTEPS, 0.35))
	engine.add_obj(Figure(T, FIGUREX, FIGUREY, FGCOLOR))

	# precompute tweening data from key frames and add bird object
	# slowly increase its size each animation cycle so it appears
	# to fly closer
	BT = []
	KFL = [BKF1, BKF2, BKF3, BKF4, BKF5, BKF6, BKF7, BKF8]
	for i in range(10, 50):
		for (kf1, kf2) in zip(KFL, KFL[1:] + [KFL[0]]):
			BT.append(maketweendata(kf1, kf2, NSTEPS, i / 10.0))
	engine.add_obj(Bird(BT, -100, 200, FGCOLOR))

	engine.engine()
