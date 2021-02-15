Tools
=====

Repls and debuggers
-------------------

Every Python developer should be competent with these tools:

-  `ipython <https://ipython.org/>`__: This is the standard
   `repl <https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop>`__
   these days

-  `Jupyter Notebooks <https://jupyter.org/>`__: a notebook that uses
   iPython at its core

-  `ipdb <https://github.com/gotcha/ipdb>`__: the command line debugger
   of iPython or some pdb variant.

It should be easy - very easy - to load code into each of these tools
not just load into *your* IDE’s debugger or repl. If it’s hard to do
this, it’s usually because context-dependent variables (see below) are
being passed excessively in the call graph making setup for the
debugging session complicated and time intensive. It will also make
writing unit tests a lot more difficult.

For the purposes of this article, it is irrelevant what code editor you
use, VSCode, PyCharm, Sublime, VIM, Emacs, etc. But be aware that just
because it’s easy to jump between definitions and usages of a function,
class, method, etc. does not mean your code is well structured. Don’t
make familiarity with your IDE an assumption in the code design.

Code Improvement Utilities
--------------------------

Some popular tools provide the best indication of things to fix or even
fix things automatically on your behalf. This is the easy part. Run
these tools always before pushing code:

-  ``black`` `<https://github.com/psf/black>`__: you run this and agree
   that everyone in the team follows the style laid down by ``black``.
   It is the basis for applying other tools mentioned below. Always run
   this first because it will fix a ton of things that would otherwise
   be flagged by ``flake8``.

-  ``flake8`` `<https://flake8.pycqa.org/en/latest/>`__: This tool wraps
   three other tools. The best thing about it is the defaults are
   immediately useful. Run this and fix *every* raised issue. You can
   configure it to skip some checks but mostly skipping checks is useful
   only for an exisiting code base. For new code, it is important to not
   play with the default for function complexity before pushing code.
   ``flake8`` wraps other tools and has default settings that let you
   use it with minimal configuration effort for a big return on
   investment.

If you don’t already run these tools, your code will experience a
massive improvement after fixing issues identified by ``flake8``.

Other tools you should consider:

-  ```mypy`` <http://mypy-lang.org/>`__: this tool will find bugs but
   also forces you to not do things that work but which are bad
   practices, like having functions that return unexpected types. But it
   also improves readability massively, IMHO. Fix *everything* flagged
   by ``mypy``. ``mypy`` is useless unless you use type hints in your
   code. While there is vigorous debate about the benefits of type
   hints, I personally find them unquestionably useful when used
   appropriately. If you have no type hints, running ``mypy`` will find
   no problems. If you have type hints but never run ``mypy`` (or one of
   the other type checkers), you will find many problems upon finally
   doing so. Better to run it consistently after adding your first type
   hint. Fix every raised issue.

-  ```pylint`` <https://www.pylint.org/>`__: This is a great tool and
   should be used on any significant project. But configuration is
   non-trivial. At first you will get more out of ``flake8`` plus
   ``mypy``. You can start using ``pylint`` and gradually build a
   configuration that works for you.

You’ll notice, I don’t talk about line length or how to format
comprehensions or imports or other style issues. That’s because you are
running ``black`` and that tool decides for you. Style preferences of
individual programmers creates unneeded scanning overhead that you can
get rid of instantly with ``black``.

One thing you should definitely not do is use type hints and then never
run ``mypy``. Why? Because your type hints will be wrong. This is wrong:

.. code:: python

   def foo(a) -> str:
       try:
           return bar(a)
       except Exception:
           return None

The type hint should say ``Optional[str]`` because it might return
``None``. If this kind of thing accumulates, you have a mess on your
hands. If you use type hints, you need to run ``mypy`` and fix
everything every time. This will not be onerous at all if you are
consistent.

Use https://pre-commit.com/ to run tools automatically before a
``git commit``.

