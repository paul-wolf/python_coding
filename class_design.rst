Class Design
============

Class design is non-trivial. It's where developers start having the most
problems. Signs of class design problems:

-  Using base classes as utilities for subclasses

-  Swiss army knife syndrome, the class does a variety of things

-  Complex parameterisation of ``__init__()``

-  Too many class instance variables

-  You are having to create too many subclasses

Classes are for managing state, not behaviour. If you have a class that only has
behaviour, it should probably be a module with one exception: when you need to
define an interface. But in general, don’t use a class as a namespace for
behaviour only. Modules already do that.

Follow these basic rules for classes:

-  A class should do one thing only

-  A subclass should be a more specific instance of a parent class

-  Minimise use of inheritance

-  Avoid where reasonably possible multiple inheritance

-  Use composition, not inheritance to acquire capabilities

-  Avoid class variables

-  Don’t define constants in classes

-  Don’t have class methods that don’t access ``cls`` or ``self``

This last point helps you reduce class size using a reasonable rule.
Move methods that don’t access class or instance data to the module
level as functions. This way, other developers can see immediately that
they don’t access or modify class state. If you think that method is
part of the interface of the class, there is probably a design error
since classes are used to manage state.

As mentioned above, use a file/module if all you want is a namespace for
behaviour. If you have state to manage, then a class might be
appropriate.

Any class state that does not change should be either a class variable
or module level variable, preferably a constant. But consider moving
that class constant outside of the class, since while applying the rule
above, you will reduce the number of unneeded class methods. Class
methods always invite the need to scan for state changes in the class
instance variables. This is cognitive overhead that you want to reduce.

It’s really ok if your classes dissolve into a series of pure functions
in a module. This is a good thing because it’s easier to understand provided
each function does not operate on the same data repeatedly. If
the functions mostly work on the same data and it’s awkward to make them
be outside a class, maybe a class is better.

-  Variables should become constants if they don’t ever change and the
   value is known before runtime.

-  Constants should be moved out of classes.

-  Constants should be moved out of modules into their own module if
   they are part of a general convention or protocol in your
   application, especially if they are used by multiple packages since
   this will help avoid cyclical imports.

You may find yourself moving towards a package structure like this:

-  constants.py

-  factories.py

-  models.py # not ORM models, but common data structures as
   datacalasses

-  [domain].py # where ``domain`` is the name describing what you are
   doing

Factories help to reduce dependencies when using composition. Constants
help define common protocols and remove unchanging state from classes.
Models are declarations of domain objects that have no framework or
integration dependencies.

SOLID principles
----------------

* Single Responsibility Principle (SRP)
* Open/Closed Principle
* Liskov’s Substitution Principle (LSP)
* Interface Segregation Principle (ISP)
* Dependency Inversion Principle (DIP)

Single Responsibility Principle (SRP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your class should do one thing. Don’t ask a class to do more than one of
these things:

* Acquire state
* Persist state
* Send messages (like Websockets, emails, events, etc.)
* Render context-specific representations of data
* etc (i.e. not a complete list)

Open-Closed Principle
~~~~~~~~~~~~~~~~~~~~~

Open for extension but closed to modification. When you create a class,
your users should not need to change it to add features or adapt to a
very specific case. But they should be able to extend that class. 

Liskov Substitution Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sounds fancy, but you already know about this: if you have an abstract
base class, your subclasses should act like that abstract class would
act (if it were not abstract). Same for a non-abstract base class and
children.

Interface Segregation Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It’s harder to do this in Python because Python does not have an
interface language feature. If you do define an interface via an Abstract
Base Class, do not force every implementing class to implement functionality not
relevant to them. This hardly applies to Python because a class should do only
one thing and subclasses should do that one thing in a way that is specialised.

Dependency Inversion Principle (DIP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"High-level modules should not depend on low-level modules.
Both should depend on abstractions."

"Abstractions should not depend on details. Details should
depend on abstractions."

–Agile Software Development; Robert C. Martin; Prentice Hall, 2003

You don't want your business rules and entity definitions to reference or be
dependent on implementation details, like persistence frameworks, IO mechanisms
or other low level things. 

In summary:

The SOLID principles are valid, but strive for simplicity and appreciate the
costs entailed by abstractions. There is such as thing as too much abstraction.

Don't introduce a dependency injection library in your project if you can get
away with adding and modifying entities in your view function.

Frameworks with Object Relational Mappers make it very hard to keep to this
principle because they closely couple two things: low level persistence details
and the high-level domain entities. Trying to apply DIP here can cause things to
get complicated very fast, i.e. techncial debt could spiral out of control. You
might need to live with something that is imperfect. 

There are many things to consider in building class hierarchies. The
most important thing is to keep things simple. Secondly, always consider
when you use a language feature if you are doing it for the class user
or for the reader of the class code. The latter should be prioritised.

Composition and inheritance as competing design patterns is one of the
most important things you can learn about how to use classes in Python:

`Brandon Rhodes’ guide to design
patterns <https://python-patterns.guide/>`__

Class naming
------------

When naming a class, avoid using the word “Base” as a prefix for the
earliest ancestor. It’s better to choose a name that expresses what the
class is because that will help you concentrate on the purpose of the
class and subclasses. If you have a “Fish” hierarchy, you would not say

.. code:: text

   BaseFish
       FinFish
       ShellFish

You want the base class to be called “Fish”. This also means you won’t
need to rename your class later when you find out you want to make your
Fish class hierarchy derive from “Animal”.

Abstract classes
----------------

Use the ABC class to create an abstract class. Then use the
``@abstractmethod`` decorator for your abstract methods. Make sure you
make properties abstract when they should be abstract. Abstract
properties are awkward in Python, but the following works.

.. code:: python

   from abc import ABC, abstractmethod

   class A(ABC):
       @property
       @abstractmethod
       def a(self):
           pass

       @abstractmethod
       def b(self):
           pass

   class B(A):
       a = 1

       def b(self):
           pass

Remember when creating and passing class types, Python won’t check type
identity when operating on what purports to be a specific object type.
As long as one class seems to have the same behaviour as another class,
it all works out. That’s duck typing. This lets any type of object
impersonate any other type as long as it supports the same methods and
properties that are used in the code that is handling these type
instances.

Class Initialisation
--------------------

Remember when you start initialising class instance properties the
reader will ask herself which one of these stateful properties will be
modified during the lifetime of the object. You need to make this easy,
not hard.

If you assign a ``self.myvar``, the reader cannot be certain of what
happens later with that variable. Therefore, don’t use instance
properties for constants. If you have a “base_url” that won’t change and
is not initialised from a parameter, define it at module level or class
level (a class property vs instance property). Reducing the number of
class instance variables, reduces complexity of the class.

If you have a variable at module level in all upper case, it seems like
overkill to also type hint it with ``Final``. But using the type hint
``Final`` when assigning class instance variables is incredibly useful.

.. code:: python

   class Fish:
       def __init__(self, base_url):
           self.base_url: Final = base_url # good to know!

We always want to assume that a class property will never change. This
might not be the case but almost always will be. There is rarely a good
case for mutable class variables. If you want a singleton class pattern,
remember this pattern already exists in Python in the form of module
level variables. Don’t implement it in a class.

If you are defining constants closely associated with a class, it is
probably still better to define them in a ``constants.py`` file.

Parameter Consolidation
~~~~~~~~~~~~~~~~~~~~~~~

Often, you start with a reasonably simple initialisation:

.. code:: python

   def __init__(self, name):
       ...

and later, it gets more complicated:

.. code:: python

   def __init__(self, name, street, postcode, town, country):
       ...

You then end up having many class instance variables that you have to manage.
This causes a reader to have to scan the code more intensively to find out which
variables get changed and when. It significantly degrades scanability of your
code. It is better to use a Parameter Consolidation variable:

.. code:: python

   class Person:
      name
      street
      postcode
      town
      country

Now we initialise the class like this:

.. code:: python

   m = SnailMail(Person(data))

Or, even better, create it with a factory function or class.

.. code:: python

   m = snail_mail_factory(person=None):
       return SnailMail(person or Person())

There should be no obscurity about how this is constructed or any danger
of the state changing after being passed to ``__init__()``. It must be
immutable. Python ``dataclasses``
(https://docs.python.org/3/library/dataclasses.html) are ideal for this,
or use the Pydantic package (https://pydantic-docs.helpmanual.io/).

Class Factoring
---------------

Let’s assume we need a class or classes to represent an integration with
a remote service. How many classes will we have? Let’s assume we need to
represent getting variations of a data type from the same endpoint.

What you should not do: create an abstract base class that is a service
provider or utility for subclasses.

-  Remoteclient: Separate out the acquisition of state into a class that
   does only that. You can have different versions that implement
   caching or other pure state management functions.

-  DomainManager: A class that manages the state in the sense of
   implementing any business rules.

-  Formatter: A class or module level function that implements
   transformations on the data to make it fit specific usage scenarios.

-  Factory: A class or module level function that creates appropriate
   DomainManager subclass and injecting the appropriate RemoteClient

Then only the DomainManger gets subclassed for specific kinds of data.
If you need to parameterise any of these with complex set of data, use a
Parameter Consolidation class.

Again, don’t have any ``@staticmethod``\ s. Have only
``@classmethod``\ s that access the ``cls`` variable. But most of these
can probably be module level functions which makes it easier to read the
code, since they will be pure functions and your class will be smaller.

``self`` and ``cls`` parameter names are conventions, not keywords. Be
aware if some developer is using a different convention.

See the sample project for more information: 

`<https://github.com/paul-wolf/python_coding/tree/main/fish>`_
