import time
import turtle
import random

# base game object

class GameObject:
	'''
	This is a base game object, suitable for subclassing or wrapping fish.
	'''

	def __init__(self, x, y, deltax, deltay, shape, color):
		'''
		Instantiates a game object at position (x, y) with the
		given shape and color, to move by (deltax, deltay) each
		time step.
		'''
		self.x = x
		self.y = y
		self.shape = shape
		self.color = color
		self.deltax = deltax
		self.deltay = deltay
		self.age = 0
		self.id = self.draw()

	def heading(self):
		'''
		Returns the direction the object should be facing.  By
		default, this is towards where the object will be moving.
		'''
		return turtle.towards(self.x + self.deltax,
				      self.y + self.deltay)

	def draw(self):
		'''
		Draws the object at its current (x, y) coordinates.
		'''
		turtle.goto(self.x, self.y)
		turtle.seth(self.heading())
		turtle.shape(self.shape)
		turtle.color(self.color)
		return turtle.stamp()

	def delete(self):
		'''
		Invoked to delete an object.
		'''
		# not using __del__, to control when this is called
		self.erase()

	def erase(self):
		'''
		Removes the object's image on screen.
		'''
		turtle.clearstamp(self.id)
		self.id = None

	def update(self):
		'''
		Invoked to update the object's image on screen, a
		draw-new-then-erase-old sequence.
		'''
		newid = self.draw()
		self.erase()
		self.id = newid

	def move(self):
		'''
		Invoked to move the object's (x, y) position on each time step.
		'''
		self.x = self.x + self.deltax
		self.y = self.y + self.deltay

	def isstatic(self):
		'''
		Returns a Boolean value: True (static, unmoving object), or
		False (the default, a moving object).
		'''
		return False

	def isoob(self):
		'''
		Returns True/False to indicate if the object is out of bounds
		or not.  By default, the screen height/width and the object's
		(x, y) position are used to determine this.
		'''
		# out of bounds?
		if self.x < MINX or self.x > MAXX or \
		   self.y < MINY or self.y > MAXY:
			return True
		return False

	def step(self):
		'''
		Called by the game engine each time step to allow the
		game object to update accordingly.  The object's age (in
		game time steps) is updated and, if it's a moving object,
		invokes methods to perform the move and update.  Moving
		out of bounds causes the object to be deleted from the game.
		'''
		self.age = self.age + 1
		if not self.isstatic():
			self.move()
			self.update()
			if self.isoob():
				del_obj(self)

# game engine

_ENGINEDELAY = 0.01

# _E and _e are for internal game engine use only
class _E:
	def __init__(self, delay):
		self.L = []			# list of game objects
		self.random = []		# random game events
		self.deleteme = {}		# for safe deletion of objects
		self.collide = {}		# for collision detection
		self.ithinkican = True		# for engine control
		self.ioevents = []		# I/O events
		self.kbdfn = None		# keyboard handler
		self.mousefn = None		# mouse handler
		self.delay = delay		# delay per time step

	# hide these internal routines away as class methods
	def _mouse_cb(x, y):
		_e.ioevents.append((_e.mousefn, (x, y)))
	def _keypress_cb(event):
		_e.ioevents.append((_e.kbdfn, (event.keysym,)))
_e = None

def init_screen(width, height):
	'''
	This should be called once only, before anything in this module
	is used.
	'''
	# initialization to be done once only - rest goes in init_engine()
	turtle.setup(width, height)
	global MAXY, MAXX, MINY, MINX
	MAXY = height // 2
	MINY = -height // 2
	MAXX = width // 2
	MINX = -width // 2

	turtle.tracer(0, 0)	# turn animation and delay off

def init_engine(delay=_ENGINEDELAY):
	'''
	(Re)initializes the game engine.  Only one game engine may exist
	at any one time.  The optional parameter specifies a delay added
	to each game time step, in seconds; the value may be a floating
	point number.
	'''
	global _e
	_e = _E(delay)

	turtle.pu()
	turtle.ht()
	turtle.clear()

def add_random_event(prob, fn):
	'''
	Defines a callback function that is invoked with probability prob
	at each time step.  Multiple random event callback functions may
	be registered at the same time.  The probability must be a float
	in the range [0.0, 1.0].
	'''
	_e.random.append((prob, fn))

def set_keyboard_handler(fn):
	'''
	Sets callback function to invoke when a key is pressed.  The
	function is passed the name of the key pressed as a string.
	Only one keyboard handler may be registered at a time.
	'''
	_e.kbdfn = fn
	# XXX why can't the turtle module just send the !@&^#%$ keysym?
	canvas = turtle.getcanvas()
	canvas.bind('<KeyPress>', _E._keypress_cb)
	turtle.listen()

def set_mouse_handler(fn):
	'''
	Sets callback function to invoke when the mouse button is pressed.
	The function is passed the x and y coordinates where the mouse
	was clicked.  Only one mouse handler may be registered at a time.
	'''
	_e.mousefn = fn
	# XXX turtle.onclick doesn't seem to work here
	turtle.onscreenclick(_E._mouse_cb)

def register_collision(class1, class2, fn):
	'''
	Instructs the game engine to invoke the callback routine fn when
	a collision is detected between an instance of class1 and an
	instance of class2.  Note that there is no ordering guaranteed
	for how game objects are tested for collision, so both combinations
	of class1/class2 and class2/class1 will need to be registered.
	'''
	_e.collide[(class1, class2)] = fn

def add_obj(obj):
	'''
	Adds a GameObject-derived object instance to the game.
	'''
	_e.L.append(obj)

def del_obj(obj):
	'''
	Removes a GameObject-derived object instance from the game.
	'''
	obj.delete()
	_e.deleteme[obj] = True

def exit_engine():
	'''
	Instructs the game engine to exit on the next time step.
	'''
	# XXX can't raise an exception to exit b/c kbd & mouse callbacks
	# XXX are handled in a different context, and the exception isn't
	# XXX caught then - engine will respond on next time step
	_e.ithinkican = False

def engine():
	'''
	Starts the game engine running.
	'''
	while _e.ithinkican:
		# flush out changes
		turtle.update()

		# delay if it's running too fast
		time.sleep(_e.delay)

		# time for random event?
		for prob, fn in _e.random:
			if random.random() < prob:
				fn()

		# move objects
		for obj in _e.L:
			if obj in _e.deleteme:
				continue
			obj.step()
			# note obj may be deleted after calling step()

		# collision detection
		# XXX assumes the class of a game object is the class
		# XXX registered for collisions
		for i in range(len(_e.L)):
			obj1 = _e.L[i]
			if obj1 in _e.deleteme:
				continue
			for j in range(i+1, len(_e.L)):
				obj2 = _e.L[j]
				if obj2 in _e.deleteme:
					continue
				key = (obj1.__class__, obj2.__class__)
				if key in _e.collide:
					_e.collide[key](obj1, obj2)
				if obj1 in _e.deleteme:
					# may have been deleted post-collision
					break

		# handle I/O events
		for fn, args in _e.ioevents:
			fn(*args)
		_e.ioevents = []

		# _L quiescent; do deletions
		_e.L = [obj for obj in _e.L if obj not in _e.deleteme]
		_e.deleteme.clear()

	if _e.kbdfn:
		canvas = turtle.getcanvas()
		canvas.unbind('<KeyPress>', None)
	if _e.mousefn:
		turtle.onscreenclick(None)

__doc__ = '''
A Python3 game engine and base game object, by
John Aycock <aycock@ucalgary.ca>.
'''
