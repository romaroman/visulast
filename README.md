=================
Table of contents
=================

- `Introduction`

- `Requirements`

- `Installing`

- `Getting started`

  #. `Configuration`

  #. `Learning by example`

  #. `Logging`

  #. `Documentation`

- `Getting help`_

- `Contributing`_

- `License`_

 
============
Introduction
============

This bot provides user-friendly expirience for visualization of <https://last.fm/> library
It's compatible with Python versions 3.3+, Anaconda and `PyPy <http://pypy.org/>`_.

In addition to the pure API implementation, this library features a number of high-level classes to
make the maintaining easy and straightforward.
 
==========
Requirements
==========

All needed packages are listed in `requirements.txt` or in `environment.yml` in case if you use Anaconda.

These requirements can be done with next commands:

In case of pure Python:

.. code:: shell

    $ make install_reqs
    
or with command:

.. code:: shell

    $ pip install -r requirements.txt
    
or with command if you use Anaconda:

.. code:: shell

    $ conda env create -f environment.yml
 
===============
Setup
===============

With next commands you clone repository, installing requirements, configuring entries in json, installing package to system and running bot.

.. code:: shell

    $ git clone https://gitlab.com/romaroman/visulast
    
    $ pip install -r requirements.txt
    
    $ cp config.example.json config.json
    
    $ python setup.py install
    
    $ python visulast/run.py

-------------------
Learning by example
-------------------

We believe that the best way to learn and understand this simple package is by example. So here
are some examples for you to review. Even if it's not your approach for learning, please take a
look at ``samplebot.py``, it is de facto the base for most of the bots out there. Best of all,
the code for these examples are released to the public domain, so you can start by grabbing the
code and building on top of it.

-------
Logging
-------

This library uses the ``logging`` module. To set up logging to standard output, put:

.. code:: python

    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

at the beginning of your script.

You can also use logs in your application by calling ``logging.getLogger()`` and setting the log level you want:

.. code:: python

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

If you want DEBUG logs instead:

.. code:: python

    logger.setLevel(logging.DEBUG)

============
Getting help
============

You can get help in several ways:

1. Typing /help in `@visulast_bot` dialog.

2. Reading documentation and commentaries to code.

3. Getting in touch with me by e-mail or something else.

4. Opening an issue or pull request.

5. Also by telegram nickname is `@plumberphd`

=======
License
=======

You may copy, distribute and modify the software provided that modifications are described and licensed for free under `LGPL-3 <https://www.gnu.org/licenses/lgpl-3.0.html>`_. Derivatives works (including modifications or anything statically linked to the library) can only be redistributed under LGPL-3, but applications that use the library don't have to be.