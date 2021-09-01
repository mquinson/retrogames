.. _code-editor:

Installing a Decent Code Editor
===============================

Any programmer needs a decent code editor. Note that notepad is *not*
a decent code editor, while gedit is only barely decent. There are
many sensible editors out there, and you should search for the one
that you prefer.

.. important::

  Unless you have a good reason, you are strongly advised to use
  `geany <http://www.geany.org/>`_ for this project. The rest of this
  page is there for your erudition.

A lot of people told me that `Atom <ttps://atom.io/>`_ is a very good
code editor, both lightweight and powerful. It still misses some
features so I did not switched myself, but you definitely want to give
it a try.

Personally, I used to code with `Eclipse <http://www.eclipse.org>`_
for years, but I would not advise you to start learning with Eclipse.
That beast is huge (several Gb of RAM), and not very intuitive for
learners. But if you want to dig a swimming pool, will you get a light
and nice spoon, or an heavy-duty excavator? If you decide to go for
the powerful excavator, pick the Java version of eclipse, then add the
`PyDev <http://marketplace.eclipse.org/content/pydev-python-ide-eclipse>`_
plugin.

I am also a happy `Emacs <https://www.gnu.org/software/emacs/>`_ user.
This venerable editor (both emacs and Vim first came out in 1976) is
known for its configuration power: you can do everything in emacs,
provided that you configure it correctly (or develop the right
plugin). But that's also its main drawback: configuring the perfect
environment can become very time consuming. For now, if you go for
emacs (which would earn you my respect), you should just add the
following to the file ~/.emacs to enable Ctrl-C and friends.
``(cua-mode t)``

These days, I often use `Codium <https://github.com/VSCodium/vscodium/>`_,
a Free/Libre Open Source version of VS code (see `here
<https://github.com/VSCodium/vscodium/#why>` for an explanation of why
I'm not using VS code directly), but I'm not sure I'd advise this
powerful tool to learners. The comfort you get from Codium may hinder
your learning experience: as the robot solves all issues for you, you
don't really get to understand these issues and how to fix them by
yourself.

To the other end of the picture, Real Hackers certainly prefer Vim.
You will never find any Unix box where it is not installed. Even if I
avoid this editor when I can, I learned its basic usage over the
years. This `online game <http://vim-adventures.com/>`_ constitutes a
perfect introduction to Vim. And it's fun too, so you can play it even
if you don't plan to use Vim on a day-to-day basis :)

If you are using Mac, then you will probably like `Sublime
Text <http://www.sublimetext.com/>`_. Windows people sometimes prefer
`Code::Blocks <http://www.codeblocks.org/>`_, but I cannot appreciate
any of these tools as I am forbidden to read their source code (ask me
if you want an explanation). 

Finally, the Python documentation lists `several dozen of
editors <https://wiki.python.org/moin/PythonEditors>`_ that you can
choose from.
