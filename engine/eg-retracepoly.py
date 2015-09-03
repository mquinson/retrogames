# line drawing as shape, where drawing doesn't "lift pen from paper"
# coords are given as a list from (0,0), and sublists can be used to
# branch off then return to a particular point
#
# drawing the outline of a polygon, then retracing the steps backwards,
# renders the polygon outline as opposed to filling it

import turtle
import engine

WIDTH = 640
HEIGHT = 480

class Tree(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, 0, 0, 'tree', 'black')
	def heading(self):
		return 90


def makeshape_r(S, L, scale):
	assert type(L) == type( [] )
	for elem in L:
		if type(elem) == type( [] ):
			makeshape_r( [ S[-1] ], elem, scale)
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

def makeshape(name, scale, L):
	turtle.home()
	turtle.begin_poly()
	stack = [ (0, 0) ]
	makeshape_r(stack, L, scale)
	turtle.end_poly()
	poly = turtle.get_poly()
	turtle.register_shape(name, poly)

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	makeshape('tree', 5, [
		(-3,-3), (0.5,0), (4,-2.7), (0.4,-0.5), (0.4,-3),
		(-3.2,-5), (0.4,-3.5), (3.8,-5), (0.45,-4), (0.45,-5.8),
		(-2,-8.2), (0.51,-6.3), (3.9,-8), (0.51,-7),
		# trunk
		(0.55,-8), (0.6,-9), (0.7,-10), (1,-11), (1.1,-12),
		# ground
		(-2,-12.2), (-0.5,-12.5), [ (3,-12.1) ], [ (2,-12) ],
		[ (-1,-12.75), [ (-2.8,-12.6) ], (0.8,-12.7), (2.5,-12.5) ]
	])
	tree = Tree()
	engine.add_obj(tree)
	engine.engine()
