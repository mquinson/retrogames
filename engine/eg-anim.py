# animate a sequence of shapes - this example gives a yo-yo-y effect

import turtle
import engine

WIDTH = 640
HEIGHT = 480

SEQ = []
STEP = 7

class Anim(engine.GameObject):
	def __init__(self):
		self.i = 0
		self.count = STEP
		super().__init__(0, 0, +1, 0, SEQ[self.i], 'blue')
	def update(self):
		# change shape once the old one's been onscreen enough
		if self.count == 0:
			self.count = STEP
			self.i = (self.i + 1) % len(SEQ)
			self.shape = SEQ[self.i]
		else:
			self.count -= 1
		super().update()
	def heading(self):
		return 180
	def isoob(self):
		# create ping-pong effect by overriding isoob
		if super().isoob():
			self.deltax *= -1
		return False

def makepoly(B, R, L):
	turtle.home()			# return to known location & orientation

	turtle.begin_poly()
	turtle.lt(90)
	turtle.fd(B / 2)
	for i in range(3):
		turtle.rt(90)
		turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B / 2)
	turtle.lt(90)
	turtle.fd(L)
	turtle.circle(R)
	turtle.end_poly()
	return turtle.get_poly()

def makeshapes():
	B = 25				# base unit size

	for i in range(1, 16):
		name = 'a%d' % i
		turtle.register_shape(name, makepoly(B, B/i, B + B*i*0.2))
		SEQ.append(name)
	
	# flip sequence except for first one
	for i in range(len(SEQ)-1, 0, -1):
		SEQ.append(SEQ[i])

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	makeshapes()
	anim = Anim()
	engine.add_obj(anim)
	engine.engine()
