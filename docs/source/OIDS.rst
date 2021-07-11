.. _OIDS:

OIDS
====


This one is an open project. The only instruction consists in two
videos presenting the gameplay of the OIDS game, a block buster of the
late eighties (click on the images). 

.. image:: http://img.youtube.com/vi/OrtrdDaKIQY/0.jpg
   :target: https://www.youtube.com/embed/OrtrdDaKIQY

.. image:: http://img.youtube.com/vi/WxhmMGLVjQ4/0.jpg
   :target: https://www.youtube.com/embed/WxhmMGLVjQ4

As you can see, this resembles to what we made before. You are a
little lander exploring a cave, and the gravity tends to let you crash
to the ground. But this time, there is also enemies shooting at you,
little mens that you should save by landing near them (not *on*
them), an armor for your lander, limited amount of fuel, fuel refiles,
teleporters, and much more. 

You are asked to implement something strongly inspired by this game,
with imagination and creativity. But given the short time that you
have to implement this project, you should strive to keep modest and
implement the features one after the other. 

Here are some ideas:

- Several levels: You just have to pass the right set of points when
  creating the ground.
- Keep track of the fuel level: The Up key is ineffective when out of
  fuel. You may use several shapes to represent the fuel level, or
  write it on screen.
- Graphical hints on flat areas that are wide enough to land.
- A campaign mode where the fuel that you save on one map is credited
  on the next map.
- A random terrain generator. `Procedural generation <http://blog.runevision.com/2015/08/procedural-world-potentials-simulation.html>`_
  is very appealing, although a `perlin noise <http://gamedev.stackexchange.com/questions/20588/how-can-i-generate-worms-style-terrain>`_
  may be enough. Of course, there is a lot of other interesting
  technics that you could leverage too.

On the path, try to learn from this experience. Think about the
algorithms that you are using in your game, and try to evaluate how
they behave in practice. Our game engine is not very powerful, so you
will probably have to optimize your code. For each problem that you
face, try to think about the possible alternatives, and how they would
compare. Be prepared to justify your [algorithmic] choices during the
defense.

But don't forget: this is a game! Go and have fun implementing it!


A last word: don't :ref:`spend too much time <TOnotDO>` on this
project. You will have a plenty of nice programming assignments during
the year.

Hall of fame
============

Here are some productions by the students before you.

- Lendy Mulot & Come Neyrand (2019)

.. image:: images/2019-Mulot-Neyrand.gif
   :alt: Lendy Mulot & Come Neyrand (2019)


If you want your name here (it's absolutely optional), you are welcome to return a short video of your game so that I
can integrate it here. ``kazam`` is a nice program to
capture a screencast, while ``ffmpeg`` can be used to
`convert this screencast to a gif <https://askubuntu.com/questions/648603/how-to-create-an-animated-gif-from-mp4-video-via-command-line>`_.
You can add a few sentences to describe your game if you wish