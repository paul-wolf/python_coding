Context Dependent Variables
===========================

These variables are complex, like classes that manage some state in a
way that might not be apparent to a user via these means:

-  The state is not stable in the current context. It might change in
   ways that are hard to predict.

-  The state is produced in the first place by means that require
   processes outside the scope of the current program. Ie. it’s not obvious how
   the state was constructed. The variable is intangled with some integration.

-  The variable is an instance of a class with dependencies on code
   outside the PSL

Examples of context dependent variables:

-  Request objects in a web framework

-  A message queue

-  An ORM object that represents and holds state about a database query
   and implements “advanced” features like caching, etc.

In the first instance, a web request, you might change the state by
accessing methods on the object. In addition, it can be difficult to
follow the construction of this object. In the second case, the object’s
state could be changing while you are accessing it.

Avoid passing these variables as parameters any more than necessary to
other functions. If you need to give, for instance, the user object of a
Request to a subroutine, do not do this:

.. code:: python

   # BAD
   permissions = get_permissions(request)

Better:

.. code:: python

   permissions = get_permissions(request.user)

Best:

.. code:: python

   permissions = get_permissions(request.user.id)

Likewise:

.. code:: python

   # BAD
   formatted = format_message(queue)

Better:

.. code:: python

   formatted = format_message(queue.pop())

A good example is the Django ``Request`` class. It has a ``body``
attribute. If you call ``.read()`` or ``.readline()`` on the request
object, these change the state of the ``body`` attribute. If you pass
``request`` to a function, a reader of that function will not be able to
assume the state of the object. It is also much more difficult to
construct test instances of a ``Request`` object than to construct a
user object. You can experiment with calls to ``get_permissions()`` and
``format_message()`` more easily in a repl. You can also use them in a
context that doesn’t require a request at all like if you are building a
command line interface to these functions.

Below we discuss the Context Parameter class pattern. This is a simple
data class, in the sense of the PSL ``dataclasses`` module. This is not
context dependent. It is simple to intialise and simple to understand
the lifecycle of its state. A dataclass or simple class of your own
construction is easy to create.

When trying out or testing code, it is desirable to be able to load,
say, a function and pass parameters to it without excessive preparation
of data needed for arguments.

A practical way to check if a variable is context dependent: Can I
define it in a repl like ipython or a jupyter notebook easily?

