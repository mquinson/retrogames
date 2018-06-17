# complex polygon as shape, using turtle.Shape

import turtle
import engine

WIDTH = 640
HEIGHT = 480

class House(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, 0, 0, 'house', 'blue')
	def heading(self):
		return 90

def makeshape():
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

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	makeshape()
	house = House()
	engine.add_obj(house)
	engine.engine()
