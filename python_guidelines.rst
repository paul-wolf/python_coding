
Basics Python Code Guidelines
=============================

Code reuseability and maintenance is about managing complexity. We don’t
care how hard machines have to work to understand things as long as
time/space tolerances are observed. We want our code to be readable by
human beings. Source code complexity is about the ability of other
developers to understand your code. Scanning is the process of reading
code to understand its consequences. “What is this code doing?” means
what side effects does it have, what data does it produce given specific
inputs or, maybe most often, what is wrong with it? Complexity causes
the reader cognitive load and consequently these questions are hard to
answer. Recommendations in this article are intended to make scanning
easier and to progressively implement code that can be managed, changed
and fixed more easily.


Post hoc Refactoring vs Upfront Design Investment
-------------------------------------------------

It is a common sentiment that it’s better to do the code right or not at
all. I.e. front-load design effort. In contrast, Agile methods prescribe
lower upfront design effort. It’s probably only a slight distoration to
suggest that Agile is based on the notion that the code will not be very
good anyway.

My view is that every development team should devote at least 30% of
scheduled time to refactoring. This does depend on what kind of project
you are working on. If it’s a marketing product web site that has a six
month lifespan, you are not going to feel a burning desire to invest
time into refactoring. But any framework code and long-term product code
probably could use some level of refactoring at any given point. Failure
to formally schedule refactoring time will lead to steady decline in
maintainability of the code base as technical debt rises with no counter
pressure.

Side Effects and State Management
---------------------------------

The most important improvement you will ever achieve in your code is
being clear about changing the state of your data. This affects the
ability to reuse code and avoid bugs more than any other factor.

The `functional <https://docs.python.org/3/howto/functional.html>`__
paradigm is useful here. Implement functions without side-effects as far
as possible. Give data via parameters to a function and get data back
via return values.

Most applications need to have side-effects like sending messages,
writing to databases, etc. But strive to understand where to use these
operations without polluting your code with artefacts of your web
framework or data storage framework. A web view function can and should
call data storage apis. Just don’t pass the objects that represent these
APIs any more than required to other functions.

Python is not a `functional programming
language <https://stackabuse.com/functional-programming-in-python/>`__
but you can apply functional programming principles to a useful extent.
Much of what follows is about state management, the key to readable
code, reuse and reducing errors in software. While functional purity is
relatively easy to grasp for most developers, designing classes often
causes good intentions to crumble. We present a set of guideines below
to deal with class design complexity.

In the following, I prescribe various practices, not always with
detailed explanations as to why. The preference is for conveying a set
of recommendations along with a code review checklist. If you don’t have
that already, this provides you with something ready-to-go. If you don’t
like some of the recommendations, fork the checklist and modify to suits
your needs and opinions.

Likewise, I don’t give too many rules that are already covered by
``black``, ``flake8``, ``pylint``. ``black`` is dictatorial by design.
``flake8`` will patiently explain.

What we do not say:

-  Make your functions only x lines of code and no more?

This is poor advice. We want our functions to be only as complex as
required but no simpler. Lines of code (LoC) does not equal complexity
although LoC is part of any complexity measurement. ``flake8``
completely takes care of this for you. Don’t worry about it. Just do
what ``flake8`` says. You can configure it to adjust complexity
threshold. Be careful about using that. There are cases where you can
skip on an individual file or line basis. Use ``#noqa`` judiciously.

-  Break up your classes to make them all small?

Again, no. Don’t just reduce the size of classes because “smaller is
better”. Apply the below principles to achieve “as complex as required
but no more.” Classes become bloated when they are misused as pure
namespaces. Encapsulation and information hiding are decent concepts but
they are sometimes conflated with namespacing. It’s more important to
think in terms of how variables change over the lifetime of a class
instance.

Dead code
---------

Do not use your code base to store code that was once useful or which
might be useful “one day”. Ruthlessly root out unused code. There are
utilities that can help with this, but you probably can browse your code
base and find unused code easily enough.

Types
-----

Use immutable types whenever you can:

-  ``tuple`` instead of ``list``: like ``(1,2,3)``

-  ``frozenset`` instead of ``set``: ``frozenset({1,2,3})``

Make sure you are not using dicts when you should be using another type,
like one of these:

-  `namedtuple <https://docs.python.org/3/library/collections.html#collections.namedtuple>`__
-  `datasets <https://docs.python.org/3/library/dataclasses.html>`__
-  `Enum <https://docs.python.org/3/library/enum.html>`__

In particular don’t use dicts as enumeration types:

.. code:: python

   STATUS = {
       "READY": 0,
       "IN_PROGRESS": 1,
       "DONE": 2,
   }

Use an Enum for this:

.. code:: python

   from enum import Enum
   class Status(Enum):
       READY = 0
       IN_PROGRESS = 1
       DONE = 2

You get better type checking, immutability and excellent ``__repr__``
output.

If you have built a mutable type, like a ``list``, turn it into
``frozenset`` or ``tuple`` if it will be used later without requiring
changes. If you are returning that type and don’t need it to change, it
is better to return the immutable type. If the user will change it, make
them cast it to a mutable type. This will help readers to understand the
developer intends to do state changes on that object.

For ``dataclasses``, make sure you use ``frozen=True``.

One day there will be a ``frozenmap`` type. But you probably want one of
the above anyway. Using immutable types helps readability because the
reader knows to scan past usages of immutable instance types searching
for state changes.

Modules and Packages
--------------------

Use modules and packages as namespaces. Import the module name
preferably and call a function qualified by the module name. Now the the
reader doesn’t have to scroll to the top of the file to find out where
the function comes from. If the function is unqualified, it’s from the
current module.

Python supports a feature to indicate protected and private names, where
you prefix with either a single or double underscore. If you use this
feature, you need to be consistent or it gets very confusing.

You generally want to use module namespaces to convey where things are
coming from. You might want to hide some complexity by importing into
``__init__.py``. The user of that package will then import those
functions or classes without knowing the exact files where the
implementation resides. This is not necessarily a good thing. It
deprives the reader of the code of useful information.

There are diverging opinions about whether ``__init__.py`` should
contain code. On balance, it’s probably better to only have imports and
not implementation code. On anything but very small projects, you will
probably use ``__init__.py`` a lot for refactoring. It’s better to
therefore only have imports.

Be aware that modules and packages are often referred to interchangeably
even in the PSL. It matters little. Technically a package is a directory
and it has a file called ``__init__.py``. What is important is you have
these ways to control access:

-  ``__all__`` in a module governs what is visible outside the module
   during importing with ``import *``

-  Single underscore ``_`` or double underscore ``__`` in front of a
   name governs visibility from outside the module under some
   circumstances

-  What you put in the ``__init__.py`` governs what is visible outside
   the package

Note that “visible” and “accessible” are two different things. Python is
not very rigorous about this. Since Python is a highly permissive
language, rather then relying on some enforcement mechanism, make sure
you adopt your own standards for importing modules.

More importantly, when you use these features, make sure you understand
for whom you are using them: for the user of the module/class? Or for
the reader of the module’s code? Making your code intelligible to
readers should be your highest priority.

Functions
---------

Make functions pure in the functional programming sense, i.e. don’t
write functions with side effects when possible. Do not change the state
of variables outside the function. But you can read data outside the
function, like referencing module variables.

Avoid using closures and nested functions in general unless you have a
compelling use case. Lambdas are too useful to avoid and generally can
enhance readability if not misused. Don’t assign a lambda expression to
a variable; functions already have all the characteristics you need if
you think you want that.

Brevity is not the defining criterion for a well-formed function. So,
what is?

-  Have a function do one well-defined thing.

-  Have manageable state, as few variables as possible to achieve the
   single purpose of the function

-  Make the function pure whenever possible

-  Return immutable types whenever possible

You will sometimes update a mutable variable passed as a parameter
(list, dict, etc.). The convention in Python is to return ``None`` if
you update a list or dict passed to your function. So, that function has
a side-effect. It’s not pure. It is how some PSL (Python Standard
Library) functions work like ``sorted()`` vs ``list.sort()``.

But if you can, don’t change the passed value. Return a new instance of
an immutable type:

.. code:: python

   from typing import Tuple, Sequence
   import random

   def remove_odd(data: Sequence[int]) -> Tuple[int]:
       return tuple(_ for _ in data if not _ % 2)

   d = [random.randint(0, 100) for _ in range(10)]
   even_data = remove_odd(d)

Now ``even_data`` is a tuple. This is good. To be clear, if you are
changing the passed mutable variable, do not also return it.

Look for hanging indents that occur after ``for`` or ``if`` expressions.
Very often if there are many lines of code under one of these, this
block can be a separate function.

Reduce the number of separate variables given to a function or created
by a function.

A good quick way to look for complexity is the number of indent changes.
If you have many and variable indent changes in a function, you have
more complexity. This plus LoC (lines of code) taken together gives an
rough idea of complexity.\ ``flake8`` uses a formal complexity analysis
tool but does not provide the sole indicator of complexity. But it is a
great place to start. Reporting on complexity metrics in your CI
pipeline is a great idea.

Default initialisations
-----------------------

Sticking to typical idioms in Python helps others read your code.

You could do this:

.. code:: python

   def foo(default_list=None):
       if not default_list: 
           default_list = list()
       ...

This is better, more idiomatic python:

.. code:: python

   def foo(default_list=None):
       default_list = default_list or list() 
       ...

What you should not do:

.. code:: python

   # BAD
   def foo(default_list=None):
       if not default_list: default_list = list()
       ...

It will work, but there is an idomatic way that is more expected.

If you need to change the value you’ll need to use the more verbose
conditional form:

.. code:: python

   # we want an int that is not zero or else None
   user_id = int(user_id) if user_id else None

If ``foo()`` requires a list:

.. code:: python

   def foo(default_list: List):
       ...

You could call it like this if you think ``my_list`` might be ``None``:

.. code:: python

   foo(my_list or list())

This is a feature of Python not shared with most other languages.

.. code:: python

   None or list()

will get you an empty list

.. code:: python

   list() or None

will result in None.

.. code:: python

   bool(list() or None)

will result in ``False``.

Iterating
---------

Use comprehensions instead of for loops where possible and appropriate.

This is verbose and hard to scan:

.. code:: python

   max_len = 0
   for line in file:
       if line.strip():
           max_len = len(line) if len(line) > max_len else max_len

Compared to:

.. code:: python

   max(len(line) for line in file if line.strip())

This is brief and easier to scan. It does not require the use of a
temporary variable, ``max_len``, to hold state. It is a common idiom
that a reader can rely on to expect no side-effects.

Another example:

.. code:: python

   filtered_events = list()
   for event in events:
       if event.dt >= today and event.dt < tomorrow:
           filtered_events.append(event)
   events = filtered_events

Compared to:

.. code:: python

   events = [e for e in events if e.dt >= today and e.dt < tomorrow]

Prefer the second one because the idiom generally promises no side
effects whereas the ``for`` loop does not. The same goes for
comprehensions. We do not expect side effects in a comprehension (or
generator expression). The knowledge that there are no changes in the
state of the program on the right side of the assignment is critical to
our ability to mentally scan past that code when looking for state
changes.

List comprehensions and higher order functions, ``filter()``, ``map()``,
``reduce()``, etc., do nearly the same thing. Use list comprehensions by
preference but don’t worry if you prefer the higher order functions.

Functions you probably want to use that are not easily replaced with
comprehensions:

-  ``zip()`` `<https://docs.python.org/3/library/functions.html#all>`__
-  ``all()`` `<https://docs.python.org/3/library/functions.html#all>`__
-  ``any()`` `<https://docs.python.org/3/library/functions.html#any>`__

Here’s a hard-to-read prime number check function with *three*
``return`` statements that can be found frequently in the web:

.. code:: python

   def is_prime(x):
       if x >= 2:
           for y in range(2, x):
               if not ( x % y ):
                   return False
       else:
           return False
       return True

Compared to one that is pythonic, easy to read and more correct:

.. code:: python

   def is_prime(n: int) -> bool:
       return all(n % i for i in range(2, n))

And, yes, the pythonic version is faster. You can produce side effects
inside a comprehension but don’t. Do not use comprehensions to loop
through sequences without using the resulting sequence or collection
(list, dict, etc.). If you only want the side effects of such an
operation, use a ``for`` loop.

Gettting a tuple from a comprehesion is not quite consistent with other
forms like dict and list comprehensions. You might think the following
is a tuple comprehension:

.. code:: python

   e = (_ for _ in range(10))

But ``e`` is now a generator expression. Use this if you want a tuple
right away:

.. code:: python

   e = tuple(_ for _ in range(10))

There are going to be times when you want to return a generator and not
a tuple, like when the underlying data is large and requires iteration
by the caller.

Use ``dict.update()`` instead of for loops to update a dictionary where
possible or the merge ``|`` and update ``|=`` operators (from Python
3.9).

Initialisation
--------------

Most python developers know not to use a mutable default value in a
function parameter declaration:

.. code:: python

   # BAD
   def foo(my_list=[]):
       ...

While this does not result in catastrophe every time, you always want
``my_list=None`` and then make whatever changes are required to the
logic in the function body. Also, when initialising in the body, use a
callable instead of an empty list (``[]``):

.. code:: python

   my_list = list()


Stop relying on dicts as parameters
-----------------------------------

Stop using dicts as parameters. Use instead ``dataclasses``. The
``dict.get()`` method is a source of bugs:

.. code:: python

   float(order.get("price", 0)) 

If the “price” key is not present, the value of this expression is 0.0.
All good. The developer thinks all bases are covered. They are not. When
the key is present but has a value of ``None`` this will throw an
exception. The solution is to parse and validate your input.
`PyDantic <https://pydantic-docs.helpmanual.io/>`__ will parse for you.
Dataclasses validate. If you wanted to use a dict nevertheless you are
probably looking for this:

.. code:: python

   float(order.get("price") or 0)

Comments and naming
-------------------

The trend is towards fewer comments based on the assumption that other
factors contribute to telling the reader what is going on. Especially
eschew obvious comments. If you want to drive someone crazy do this:

.. code:: python

   # Bad
   class Address:
       """This class represents an address."""
       ...

Follow the rule that if you have nothing useful to say, say nothing at
all.

Assume you are writing your docstrings and comments first and then
writing the code that implements what is described. You should name
things - variables and functions - so that you can start removing the
comments as the code becomes sufficiently readable that the comments do
not add useful information. Remove any comment that does not add useful
information.

Name variables in a more descriptive way the further they are used from
their first use. If you are looping and using an index:

.. code:: python

   for i, name in enumerate(my_list_of_names):
       ...

``i`` is ok for me if it lasts for very few lines, like three. If there
are more lines of code, you’d be better off doing something like this:

.. code:: python

   for name_index, name in enumerate(my_list_of_names):
       ...

Type hints are a better form of documentation. The convention for a
function docstring is something like:

.. code:: python

   def splice_name(first, last):
       """Return a str representing fullname."""
       return "f{first} {last}"

But now you can write:

.. code:: python

   def splice_name(first, last) -> str:
       """Combine first and last with space inbetween."""
       return "f{first} {last}"

Add more type annotations as necessary. Add a docstring unless it is
immediately obvious what the function does. But don’t bother identifying
the return value type in the docstring if you already use a type hint
for this purpose.

Now look what happens in iPython if I press ``return`` using ``?`` after
the function name:

.. code:: pycon

   In [29]: splice_name?
   Signature: splice_name(first, last) -> str
   Docstring: Combine first and last with space inbetween.
   File:      ~/prj/<ipython-input-28-b0b71e899c5a>
   Type:      function

Likeise if you type ``help(splice_name)``. This is amazingly useful.

Profiling code
--------------

Profiling code should not become a heavy source of technical debt. If a
significant amount of code is just for profiling, this needs to be
removed before production deployment. It’s ok to leave in some code for
timings, but it should be minimal. If you are leaving in too much
profiling code, there is some fundamental design problem.

Don’t reinvent
--------------

Don’t create utilities for things the PSL (Python Standard Library)
already provides. Especially things in ``collections``, ``itertools``,
``functools``. Developers have a tendency to start building small
utilities especially for namespaces that already exist in the PSL. The
PSL versions are better than yours.

Unit tests and Linters
----------------------

Unit testing is a required part of modern software development. It
exposes problems in areas that you think you have not changed,
regressions. It tests your intent versus what the software actually
does. It makes it vastly easier to check your work. Unit testing is
indispensible.

But unit tests are hard work. Whereas running a linter is trivial. It
would be really strange to expend significant time on unit tests (which
you should do) and then not run a linter.

When you write mostly pure functions, it’s easier - much easier - to
write unit tests.

When you refactor functions to satisfy complexity thresholds, you are
making writing unit tests easier.

Also, you should very probably be using
`Hypothesis <https://hypothesis.readthedocs.io/>`__.

