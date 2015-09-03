# moving boxes, added in response to space bar being pressed

import engine

WIDTH = 640
HEIGHT = 480

class Box(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, +1, 0, 'square', 'red')

def keyboard_cb(key):
	if key == 'space':
		box = Box()
		engine.add_obj(box)

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(keyboard_cb)
	engine.engine()
