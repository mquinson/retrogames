.. _Install_Linux:

Installing Python3 on Linux
===========================

If you are serious about computers and computer science, you need a
Linux to play with. Either a native one in partition, or at least a
Linux virtual machine. But don't worry, using Linux is very easy
nowadays. In my opinion, Linux is even much simpler and more intuitive
(once you get the general ideas) than Windows or Mac. If you have
issues mastering your Windows system, then is not just you. Windows is
actually difficult to master. Windows is only easy as long as you're
OK with a limited understanding of what's going on. You should try
Linux to see whether it's a better fit for you.

**That being said, the first steps with Linux may be difficult.** The
strong point of Linux is that there is a philosophy underlying, so
when you start getting it, you get it faster. But there is still a
learning curve. Of course, nobody knows it before getting
introduced to it. But the good news is that I am willing to help you
master your system. **The only stupid questions are the unasked ones.**

This page describes several ways to install Linux:

- `In a partition of your disk <Linux_partition>`_, the prefered way.
- `As the Window's Subsystem Linux <Linux_WSL>`, the fastest way to
   get a Linux working as a part of you Windows. This is the way to go
   if you cannot stop using your Windows.
- `On an USB stick <Linux_stick>`_, if you cannot install anything on
   that computer. 

.. _Linux_partition:
  
Installing Linux in a partition
-------------------------------

Installing Linux in a partition is the most classical approach. Then,
Linux and Windows (or Mac) will share the space on your hard disk, and
you'll have to chose between Linux and Windows when the machine
starts. This approach is advised as you get a "real" Linux, with no
limitation. If you don't know which distribution of Linux to chose
then pick a Ubuntu. I use Debian myself and many of my friends use
Arch Linux or even a venerable Gentoo, but Ubuntu is a good first
choice. If you prefer another distribution, then go for it.

Installing Linux is not very complex nowadays. You should find at
least 20 Gb on your hard disk, backup all your data, download an iso
image of the chosen distribution, burn it on a CD, DVD or USB key, and
reboot your machine. The Ubuntu documentation is `here
<https://help.ubuntu.com/community/CommunityHelpWiki>`_. You want to
make it simple for the first time, so you just have to follow the
instructions of the installer.

But before that, **backup your data before installing Linux**. The
installation is not dangerous if you make it right, but there is no
protection. There are some harmful mistakes that you could do in the
process.

.. _Linux_WSL:

Installing the Windows' subsystem Linux (WSL2)
----------------------------------------------

The `Windows Subsystem Linux <https://docs.microsoft.com/en-us/windows/wsl/>`_
is an official extension of Windows, provided by Microsoft, that
allows to use unmodified Linux applications on a Windows system. Once
installed, you can get *almost* all of the Linux power on your
existing system. 

The main drawback compared to an installation in a partition is that
both OSes share your resources (CPU, memory), so you can easily turn a
nice computer into two laggy machines for advanced uses. But WSL2
remains perfectly OK for the retrogamins project, even with
not-so-recent computers.

If your Windows is too old, WSL may not be an option for you. In this
case, you could turn to another Virtual Machine instead of the WSL.
Unfortunately, these other solutions will probably provide a lesser
integration between Linux and Windows, leading to usability
difficulties where some mouse and keyboards actions are intercepted by
the host OS and thus not possible within the VM. If you are still
interested, here is `an old but interesting tutorial
<http://www.wikihow.com/Install-Ubuntu-on-VirtualBox>`_.  If you have
a better one, please drop me an email.

.. _Linux_stick:

Booting Linux from a USB stick
------------------------------

If you're really short on space on your disk (and cannot make any
room), then you can install Linux on an USB stick. The advantage is
that you can have your Linux always with you, and use it on several
computers. The main drawback is that it is very demanding on the USB
stick. The cheap sticks that you get as goodies here and there will be
slow and break soon, eating all your data! Make sure to use a correct
stick, and to regularly backup your data to another location.

`ClefAgreg <http://clefagreg.dnsalias.org/8.0/>`_ is a very pleasant
solution to build such an USB stick (in French only, sorry). This is
the technical solution used for the Informatics option of the Maths
`Agrégation <https://en.wikipedia.org/wiki/Agr%C3%A9gation>`_. So it
is well tested and very robust, while making it very easy to add new
software to the stick.

`TAILS <https://tails.boum.org/>`_ is another solution for Live USB
Linux. The main goal of that project is not to easily create a
development environment, but it still offers all the features that we
need, with a `persistent storage
<https://tails.boum.org/doc/first_steps/persistence/>`_ on the USB
stick, and the ability to `add extra softwares to the system
<https://tails.boum.org/doc/advanced_topics/additional_software/>`_
(although less efficiently than ClefAgreg). It seems to be more active
and maybe better maintained.

But I cannot tell for sure: I have a real Linux partition and don't use
such solution very often.

