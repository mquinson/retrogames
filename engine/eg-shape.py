# This example explores 3 ways of declaring the shapes for your objects.
#
# 'car' is drawn using the turtle primitives (forward, left, right as in LOGO)
# 'ball' is a simple circle. Beware, the circle is not centered at the initial position.
# 'house' is defined as a set of polygons, each of them being defined by its points
#
# See also the eg-poly example, that declares a shape by drawing it with the turtle

import turtle
import engine

WIDTH = 640
HEIGHT = 480

def makeshapes():
	# Draw the 'car' shape using the turtle
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
	
	# Draw the 'ball' shape as a simple circle.
	# (we need to move the position before drawing the circle, because turtle.circle() does not put the circle center at the initial position)
	turtle.begin_poly()
	turtle.left(90)
	turtle.forward(40)    # radius
	turtle.left(90)
	turtle.circle(15,360) # radius, angle
	turtle.end_poly()
	turtle.register_shape('ball', turtle.get_poly())
	
	# Define the 'house' as a set of polygons, each of them being defined by its points
	house = turtle.Shape("compound")
	wall = ((0,-5),(100,-5),(100,-60),(0,-60))
	house.addcomponent(wall, "white", "black")
	door = ((80,-60),(80,-20),(55,-20),(55, -60))
	house.addcomponent(door, "brown", "black")
	window = ((15,-22), (40,-22), (40, -45), (15,-45))
	house.addcomponent(window, "blue", "black")
	roof = ((-10,-5), (110,-5), (50, 30))
	house.addcomponent(roof, "red", "red")
	turtle.register_shape('house', house)

class Car(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, +1, 0, 'car', 'blue')
	def heading(self):
		return 90
class Ball(engine.GameObject):
	def __init__(self):
		super().__init__(-100, 0, +1, 0, 'ball', 'red')
	def heading(self):
		return 90
class House(engine.GameObject):
	def __init__(self):
		super().__init__(0, -150, 0, 0, 'house', 'blue')
	def heading(self):
		return 90


if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	makeshapes()
	engine.add_obj(Car())
	engine.add_obj(Ball())
	engine.add_obj(House())
	engine.engine()
