# python3 nightdriver.py
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
MYY = -200
MYDELTA = 0
MYCOLOR = 'white'
MYSHAPE = 'turtle'

GAMETIME = 60

BGCOLOR = 'black'
TEXTCOLOR = 'white'

# state singleton class

class S:
	def __init__(self):
		self.playing = False	# game state
		self.me = None
		self.score = 0
		self.numPosts = 14
		self.acc = 1		#acceleration
		self.horizonX = 0	#spawn point of posts
		self.horizonY = 130
		self.turnX = 0
		self.space = 20		#space between posts
		self.time = time.time()
		self.state = 0	# 0 = straight away
						# 1 = right turn (random duration)
						# -1 = left turn (random duration)
		self.stateFrames = 0
		
s = None

# class for throwing an exception

class Replay(BaseException):	pass

# game objects

class Me(engine.GameObject):
	def __init__(self):
		super().__init__(MYX, MYY, 0, -MYDELTA, MYSHAPE, MYCOLOR)
		self.prevTime = 0

	def delete(self):
		# this catches OOB cases as well as collisions
		super().delete()
	
	def move(self):
		super().move()

	def update(self):
		turtle.tiltangle(90)
		turtle.shapesize(10,4)

		curTime = round(time.time() - s.time, 0)

		if(curTime == math.ceil(curTime) and curTime != self.prevTime):	#prints time
			draw_score()

		if(GAMETIME - curTime <= 0):
			lose()

		self.prevTime = curTime
		
		super().update()

	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 70

	def getx(self):		return self.x
	def gety(self):		return self.y

class Post(engine.GameObject):
	def __init__(self, x, y, deltax, deltay, side):
		if(side == -1):
			super().__init__(x, y, deltax, deltay,
				 'square', 'white')
		else:
			super().__init__(x, y, deltax, deltay,
				 'square', 'green')
		self.side = side

	def delete(self):
		# this catches OOB cases as well as collisions

		if(s.playing == False):
			super().delete()
			return

		s.numPosts = s.numPosts - 1

		if s.numPosts % 2 == 0:		#handles turns by using turn states
			s.score += 1
			draw_score()
			if(s.stateFrames != 0):
				if(s.stateFrames > 5):
					if(s.state == -1):
						if(s.horizonX < 5 and s.horizonX > -5):
							s.horizonX = -10
						elif(s.horizonX < -5 and s.horizonX > -15):
							s.horizonX = -75
						elif(s.horizonX < -70 and s.horizonX > -80):
							s.horizonX = -160
						elif(s.horizonX < -155 and s.horizonX > -165):
							s.horizonX = -200
						elif(s.horizonX < -195 and s.horizonX > -205):
							s.horizonX = -275
					elif(s.state == 1):
						if(s.horizonX > -5 and s.horizonX < 5):
							s.horizonX = 10
						elif(s.horizonX > 5 and s.horizonX < 15):
							s.horizonX = 75
						elif(s.horizonX > 70 and s.horizonX < 80):
							s.horizonX = 160
						elif(s.horizonX > 155 and s.horizonX < 165):
							s.horizonX = 200
						elif(s.horizonX > 195 and s.horizonX < 205):
							s.horizonX = 275
				else:
					if(s.state == -1):
						if(s.horizonX < -270 and s.horizonX > -280):
							s.horizonX = -200
						elif(s.horizonX < -195 and s.horizonX > -205):
							s.horizonX = -160
						elif(s.horizonX < -155 and s.horizonX > -165):
							s.horizonX = -75
						elif(s.horizonX < -70 and s.horizonX > -80):
							s.horizonX = -10
						elif(s.horizonX < -5 and s.horizonX > -15):
							s.horizonX = 0	
					elif(s.state == 1):
						if(s.horizonX > 270 and s.horizonX < 280):
							s.horizonX = 200
						elif(s.horizonX > 195 and s.horizonX < 205):
							s.horizonX = 160
						elif(s.horizonX > 155 and s.horizonX < 165):
							s.horizonX = 75
						elif(s.horizonX > 70 and s.horizonX < 80):
							s.horizonX = 10
						elif(s.horizonX > 5 and s.horizonX < 15):
							s.horizonX = 0			
				s.stateFrames -= 1 
			else:
				s.state = 0

		spawn_post_cb()		#spawns a new set of posts when this one gets deleted
		super().delete()
	
	def heading(self):
		return turtle.towards(self.x, self.y)
	
	def move(self):
		self.z = self.y + MAXY

		#you do not want to know how I got these formulae....
		#ok fine, I plotted posts with X, Y, sizes and speeds that I thought looked good then plotted these values with respect
		#to the z value (Y + MAXY) then used interpolation to find out what size, speed the post should be at any given z value, gross
		self.deltay = -(((-0.3)*(self.z) + 118)/10)  * 0.5* s.acc
		self.deltax = (((-0.15)*(self.z) + 61.5)/10) * 0.5 * self.side*s.acc		#these were linear interpolations
		if(s.acc < 0):
			s.acc = 0

		if(self.x <= -310):	#keeps posts horizontally on the screen
			self.x = -310
		elif(self.x >= 310):
			self.x = 310

		super().move()

	def update(self):
		turtle.tiltangle(90)

		self.size = (-0.003)*(self.z) + 1.41		# y = mx + b, y=(-0.003)x + 1.41
		turtle.shapesize(self.size*0.7,self.size)

		self.x = self.x + ((s.turnX) * (((-0.3)*(self.z) + 118)/10) * s.acc * 0.1);		#more interpolation

		super().update()
		
	def get_bc(self):
		# bounding circle, for circle-based collision detection
		return self.x, self.y, 20

	def getx(self):		return self.x
	def gety(self):		return self.y

# collision handling

def iscoll_circle(obj1, obj2):
	x1, y1, r1 = obj1.get_bc()
	x2, y2, r2 = obj2.get_bc()

	# from http://devmag.org.za/2009/04/13/basic-collision-detection-in-2d-part-1/
	# take the Euclidean distance between the center points, and if
	# that's less than the sum of the radii, then intersection occurred
	d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
	return d < (r1 + r2)

def col_post2(obj2, obj1):
	return col_post(obj1, obj2)

def col_post(obj1, obj2):
	if iscoll_circle(obj1, obj2):
		s.acc = 0
		s.turnX = 0
		if(obj2.side == 1):
			s.turnX += 3
		else:
			s.turnX -= 3
		s.acc += 1

# callbacks

#Used to set the default postion of posts at the start of a new game
def place_default_post_cb():

	ddy = 13
	dy = 0
	y = 126

	ddx = 6
	dx= 0
	x = 10

	dds = 0.03
	ds = 0
	s = 0.3

	count = 0
	while(count < 7):
		obj = Post(x, y, 0, 0, 1)
		engine.add_obj(obj)
		obj = Post(-x, y, 0, 0, -1)
		engine.add_obj(obj)

		dy += ddy
		y -= dy

		dx += ddx
		x += dx

		ds += dds
		s += ds

		count += 1

def spawn_post_cb():
	#only spawns when an even number of posts exists
	if s.numPosts % 2 == 0:
		obj = Post(s.horizonX+10 - s.space, s.horizonY, 0, 0, -1)
		engine.add_obj(obj)
		obj = Post(s.horizonX+10, s.horizonY, 0, 0, 1)
		engine.add_obj(obj)
		s.numPosts = s.numPosts + 2

def rightturn_straight_cb():
	num = random.randint(11,20)
	if(s.state == 0):
		s.state = 1
		s.stateFrames = num

def leftturn_straight_cb():
	num = random.randint(11,20)
	if(s.state == 0):
		s.state = -1
		s.stateFrames = num

def input_cb(key):
	if key == 'q' or key == 'Q':
		exit()
	if key == 'space':
		if not s.playing:
			# replay
			raise Replay()
	if key == 'Up':
		if(s.acc < 5):
			s.acc += 1
	elif key == 'Left':
		if(s.acc > 0):
			s.horizonX += 2 * (((-0.3)*(s.horizonY + MAXY) + 118)/10) * 2 * 0.01
			s.turnX += 2
	elif key == 'Right':
		if(s.acc > 0):
			s.horizonX += -2 * (((-0.3)*(s.horizonY + MAXY) + 118)/10) * 2 * 0.01
			s.turnX -= 2
	elif key == 'Down':
		if(s.acc > 0):
			s.acc -= 1

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
	banner('NIGHT TURTLER')

def lose():
	s.playing = False
	mesg = 'Score %d - press space to play again' % s.score
	turtle.goto(0, 0)
	turtle.color(TEXTCOLOR)
	turtle.write(mesg, True, align='center', font=('Arial', 24, 'italic'))
	engine.del_obj(s.me)

def draw_text():
	turtle.goto(-100, MAXY-25)
	turtle.color('white')
	turtle.write("Score: ", align='center', font=('Arial', 14, 'normal'))

	turtle.goto(100, MAXY-25)
	turtle.color('white')
	turtle.write("Time: ", align='center', font=('Arial', 14, 'normal'))

def draw_score():
	turtle.goto(-50, MAXY-25)
	turtle.dot(50, 'black')
	turtle.color('white')
	turtle.write(str(s.score), align='center', font=('Arial', 14, 'normal'))

	curTime = round(time.time() - s.time, 0)
	scoreTime = GAMETIME - curTime

	turtle.goto(150, MAXY-25)
	turtle.dot(50, 'black')
	turtle.color('white')
	turtle.write(scoreTime, align='center', font=('Arial', 14, 'normal'))

def play():
	global s
	s = S()

	engine.init_engine()
	engine.set_keyboard_handler(input_cb)

	s.me = Me()
	engine.add_random_event(0.01, leftturn_straight_cb)
	engine.add_random_event(0.01, rightturn_straight_cb)
	engine.add_obj(s.me)

	place_default_post_cb()

	engine.register_collision(Me, Post, col_post)
	engine.register_collision(Post, Me, col_post2)

	draw_text()
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
