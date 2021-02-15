Web Frameworks
==============

Web apps are a class of application with sterotypical problems. Many
problems with code complexity come with mixing up the web framework
objects with business logic and service code. One important sign this
happens is passing context dependent variables that represent constructs
of the web framework to subroutines. There are two kinds of context
dependent variables typical of web frameworks:

-  Request and Response objects

-  ORM objects if the web framework has or supports a database
   abstraction framework

You want to minimise passing of these objects through the call graph of
your own code.

The principle feature of a web framework is the view function. The only
relationship you want your view function to have with other parts of
your code is data. The view function passes data to other parts of your
application and gets data back. Passing a user id (int) is better than
passing a User object. But if the called code will immediately again use
that to query the database for user information, you now have an
unnecessary call to the database. But maybe you have the data already,
so pass that (company id?), but not in the form of a context-dependent
variable that may have side effects and couples lower layers to the web
framework. There are various options here but most importantly, you want
to divest your function calls of couplings to your ORM or web framework.

If you end up passing the Request or ORM objects throughout your own
code, far downstream, it will have dire consequences for readability and
maintaining the code base.

If your view function can call the database, apply some business logic,
return results, you are good to go. Don’t try to make the view function
into an abstraction layer that hides everything else. If the
functionality is too complex and would cause ``flake8`` to judge the
functionality of the view function to be over the accepted threshold,
maybe reduce the view function to be short, handling mostly view things
and let subroutines do the complex things. But do not then start
coupling your view with the underlying routines by passing context
dependent variables representing framework features. The benchmark is
that the subroutines should be callable by non-view code. They should be
easy to setup, easy to load in ipdb and ipython and require as few
imports as possible.

If you are tempted to implement abstractions that support the Dependency
Inversion Principle (DIP), be mindful that this can be hard to do when many web
frameworks ensure tight coupling between high-level modules (your domain
entitites and rules) and low level modules like the persistence layer. Fighting
against this to achieve a Clean Architecure can have a high cost. 

