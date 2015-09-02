If you are serious about computers and computer science, you will need
probably have to have a Linux partition at some point, or at least a
Linux virtual machine. But don't worry, using Linux is very easy
nowadays. In my opinion, Linux is even much simpler and more intuitive
(once you get the general ideas) than Windows or Mac. If you have
issues mastering your Windows system, I think that it is not just you.
You should try Linux to see whether it's a better fit for you. 

This page describes several ways to install Linux:
- [[In a partition of your disk|Installing-Python3-on-Linux#installing-linux-in-a-partition]], the prefered way.
- [[As a virtual machine|Installing-Python3-on-Linux#installing-linux-in-a-virtual-machine]], if you cannot stop using Windows yet.
- [[On an USB stick|https://github.com/mquinson/retrogames/wiki/Installing-Python3-on-Linux#booting-linux-from-a-usb-stick]], if you cannot install anything on that computer.

#### Installing Linux in a partition

Installing Linux in a partition is the most classical approach. Then,
Linux and Windows (or Mac) will share the space on your hard disk, and
you'll have to chose between Linux and Windows when the machine
starts. This approach is advised as you get a "real" Linux, with no
limitation. If you don't know which distribution of Linux to chose
then pick a Ubuntu. I use Debian myself and many of my friends use
Arch Linux or even a venerable Gentoo, but Ubuntu is a good first
choice.

Installing Linux is not very complex nowadays. You should find at
least 20 Gb on your hard disk, backup all your data, download an iso
image of the chosen distribution, burn it on a CD, DVD or USB key, and
reboot your machine. The Ubuntu documentation is
[[here|https://help.ubuntu.com/community/CommunityHelpWiki]]. You want
to make it simple for the first time, so you just have to follow the
instructions of the installer.

But before that, **backup your data before installing Linux**. The
installation is not dangerous if you make it right, but there is no
protection. There is many harmful mistakes that you could do in the
process.

#### Installing Linux in a virtual machine
If you want to launch Windows and Linux applications at the same time,
then you have to put either Windows and Linux in a virtual
machine. That guest OS (the one within the VM) will run as an
application of the host OS (the one out of the VM, running on the real
computer). 

Using a VM is not optimal: both OSes share the memory and CPU (so you
turn a nice computer into two laggy machines), some mouse and
keyboards actions are intercepted by the host OS and thus not possible
within the VM. But that's still an interesting approach.

I have a Windows VM on my Linux computer (to test my apps on Windows),
but I guess that you want to install Linux in a VM on your Windows.
I'm not very fluent on Windows but there is a plenty of tutorials for
that. Here is
[[one|http://www.wikihow.com/Install-Ubuntu-on-VirtualBox]]. It's
maybe a bit old (not sure) but seems very detailed. If you have a
better one, please drop me an email.

#### Booting Linux from a USB stick

If you're really short on space on your disk (and cannot make any
room), then you can install Linux on an USB stick. The advantage is
that you can have your Linux always with you, and use it on several
computers. The main drawback is that it is very demanding on the USB
stick. The cheap sticks that you get as goodies here and there will be
slow and break soon, eating all your data! Make sure to use a correct
stick, and to regularly backup your data to another location.

[[ClefAgreg|http://clefagreg.dnsalias.org/8.0/]] is a very pleasant
solution to build such an USB stick (in French only, sorry). This is
the technical solution used for the Informatics option of the Maths
[[Agrégation|https://en.wikipedia.org/wiki/Agr%C3%A9gation]]. So it
is well tested and very robust, while making it very easy to add new
software to the stick.

[[TAILS|https://tails.boum.org/]] is another solution for Live USB
Linux. The main goal of that project is not to easily create a
development environment, but it still offers all the features that we
need, with a [persistent
storage](https://tails.boum.org/doc/first_steps/persistence/) on the
USB stick, and the ability to [add extra softwares to the
system](https://tails.boum.org/doc/advanced_topics/additional_software/)
(although less efficiently than ClefAgreg). It seems to be more active
and maybe better maintained.

But I cannot tell for sure: I have a real Linux partition and don't use
such solution very often.

## Installing a decent editor

There are many sensible editors out there, and you should search for
the one that you prefer.

I often use [[Eclipse|http://www.eclipse.org]] myself (pick the Java
version, then add the
[[PyDev|http://marketplace.eclipse.org/content/pydev-python-ide-eclipse]]
plugin -- prefer a manual download to an Ubuntu package). Agreed, that
software is huge (more than 1.5Gb of RAM), and it's easy to get lost
when you start with it. But if you want to dig a swimming pool, will
you get a light and nice spoon, or an heavy excavator?

Real hackers will certainly prefer Vim. You can be certain that it is
installed on every Unix box that you will ever encounter. Even if I
don't use it when I have the choice, I learned its basic usage over
the years. This [[online game|http://vim-adventures.com/]]
constitutes a perfect introduction to Vim. And it's fun too, so you
can play it even if you don't plan to use Vim on a day-to-day basis :)

When not using Eclipse, I'm an happy
[[Emacs|https://www.gnu.org/software/emacs/]] user. That's another
venerable editor (both emacs and Vim came out in 1976), which main
feature is its configuration power: you can do everything in emacs,
provided that you configured it correctly, or developed the right
plugin. But that's also its main drawback: configuring the perfect
environment can become rather time consuming. For now, if you go for
emacs (which would earn you my respect), you should just add the
following to the file ~/.emacs to enable Ctrl-C and friends.
```(cua-mode t)```
