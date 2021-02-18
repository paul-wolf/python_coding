Python Code Review Checklist
============================

General
-------

-  Code is blackened with ``black``

-  ``flake8`` has been run with no errors

-  ``mypy`` has been run with no errors

-  Function complexity problems have been resolved using the *default*
   complexity index of ``flake8``.

-  Important core code can be loaded in iPython, ipdb easily.

-  There is no dead code

-  Comprehensions or generator expressions are used in place of for
   loops where appropriate

-  Comprehensions and generator expressions produce state but they do
   not have side effects within the expression.

-  Use ``zip()``, ``any()``, ``all()``, etc. instead of for loops where
   appropriate

-  Functions that take as parameters and mutate mutable variables don’t
   return these variables. They return None.

-  Return immutable copies of mutable types instead of mutating the
   instances themselves when mutable types are passed as parameters with
   the intention of returning a mutated version of that variable.

-  Avoid method cascading on objects with methods that return ``self``.

-  Function and method parameters never use empty collection or sequence
   instances like list ``[]`` or dict ``{}``. Instead they must use
   ``None`` to indicate missing input

-  Variables in a function body are initialised with empty sequences or
   collections by callables, ``list()``, ``dict()``, instead of ``[]``,
   ``{}``, etc.

-  Always use the ``Final`` type hint for class instance parameters that
   will not change.

-  Context-dependent variables are not unnecessarily passed between
   functions or methods

-  View functions either implement the business rules the view is
   repsonsible for or it passes data downstream to have this done by
   services and receives non-context dependent data back.

-  View functions don’t pass ``request`` to called functions

-  Functions including class methods don’t have too many local
   parameters or instance variables. Especially a class’ ``__init__()``
   should not have too many parameters.

-  Profiling code is minimal

-  Logging is the minimum required for production use

-  There are no home-brewed solutions for things that already exist in
   the PSL

Imports and modules
-------------------

-  Imports are sorted by ``isort`` or according to some standard that is
   consistent within the team

-  Import packages or modules to qualify the use of functions or classes
   so that unqualified function calls can be assumed to be to functions
   in the current module

Documentation
-------------

-  Modules have docstrings

-  Classes have docstrings unless their purpose is immediately obvious

-  Methods and functions have docstrings

-  Comments and docstrings add non-obvious and helpful information that
   is not already present in the naming of functions and variables

General Complexity
------------------

-  Functions as complex as they need to be but no more (as defined by
   ``flake8``\ ’s default complexity threshold)

-  Classes have only as many methods as required and have a simple
   hierarchy

Context Freedom
---------------

-  All important functionality can be loaded easily in ``ipython``
   without having to construct dummy requests, etc.

-  All important functionality can be loaded in pdb (or a variant, ipdb,
   etc.)

Types
-----

Have immutable types, tuple, frozenset, Enum, etc. been used in place of
mutable types whenever possible?

Functions
---------

Functions are pure wherever possible, i.e. they take input and provide a
return value with no side-effects or reliance on hidden state.

Modules
-------

-  Module level variables do not take context-dependent values like
   connection clients to remote systems unless the client is used
   immediately for another module level variable and not used again

Classes
-------

-  Every class has a single well-defined purpose. That is, the class
   does not mix up different tasks, like remote state acquisition, web
   sockets notification, data formatting, etc.

-  Classes manage state and do not just represent the encapsulation of
   behaviour

-  All methods access either ``cls`` or ``self`` in the body. If a
   method does not access ``cls`` or ``self``, it should be a function
   at module level.

-  ``@classmethod`` is used in preference to ``@staticmethod`` but only
   if the method body accesses ``cls`` otherwise the method should be a
   module level function.

-  Constants are declared at module level not in methods or class level

-  Constants are always upper case

-  Abstract classes are derived from abc: ``from abc import ABC``

-  Abstract methods use the ``@abstractmethod`` decorator

-  Abstract class properties use both ``@abstractmethod`` and
   ``@property`` decorators

-  Classes do not use multiple inheritance

-  Classes do not use mixins (use composition instead) except in rare
   cases

-  Class names do not use the word “Base” to signal they are the single
   ancestor, like “BaseWhatever”

-  Decorators are not used to replace classes as a design pattern

-  ``__init__()`` does not define too many local variables. Use the
   Parameter Consolidation pattern instead.

-  A factory class or function at module level is used for complex class
   construction (see Design Patterns) to achieve composition

-  Classes are not dynamically created from strings except where forward
   reference requires this

Design Patterns
---------------

-  Do not use designs that cause a typical Python developer to have to
   learn new semantics that are unexpected in Python

-  Classes primarily use composition in preference to inheritance

-  Beyond a very small number of simple variables, a class’ purpose is
   to acquire state for another class or it uses another class to
   acquire state in particular if the state is from a remote service.

-  If you use the Context Parameter pattern, it is critical that the
   state of the context does not change after calling its
   ``__init__()``, i.e. it should be immutable

-  If a class’ purpose is to represent an external integration, you
   probably want numerous classes to compose the service:
   RemoteDataClient, DomainManager, ContextManager, Factory,
   NotificationController, DomainResponse, DataFormatter, etc.
