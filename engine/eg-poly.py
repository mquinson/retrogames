# complex polygon as shape

import turtle
import engine

WIDTH = 640
HEIGHT = 480

class Car(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, +1, 0, 'car', 'blue')
	def heading(self):
		return 90

def makeshape():
	B = 25				# base unit size
	turtle.begin_poly()
	turtle.fd(B)			# roof
	turtle.rt(45)
	turtle.fd(B * 3/4)		# windshield
	turtle.lt(45)
	turtle.fd(B)			# hood
	turtle.rt(90)
	turtle.fd(B * 3/4)		# front
	turtle.rt(90)
	turtle.fd(B * 1/7)
	turtle.lt(90)
	turtle.circle(-B/2, 180)	# front tire
	turtle.lt(90)
	turtle.fd(B)
	turtle.lt(90)
	turtle.circle(-B/2, 180)	# back tire
	turtle.lt(90)
	turtle.fd(B * 1/7)
	turtle.rt(90)
	turtle.fd(B * 5/6)		# back
	turtle.end_poly()
	poly = turtle.get_poly()
	turtle.register_shape('car', poly)

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	makeshape()
	car = Car()
	engine.add_obj(car)
	engine.engine()
