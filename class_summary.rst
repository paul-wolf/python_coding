# Class simplification rules in Python

Class design is tricky in any language. There is no substitute for
careful consideration of somewhat abstract design principles and your specific
use-case. But here is a formula that can be applied almost mechanically to
simplify class design in Python, making your code easier to read, change and test.

For a full discussion, see this documentation (by the present author):

<https://python-coding-guidelines.readthedocs.io/>

Try making these changes to your class and see what you end up with:

* Remove all constants from the class to the module level or even better to a
file called `constants.py`

* Remove class variables to the module level

* Remove all methods that do not access `cls` or the `self` parameter to the
module level

* Make sure all module level functions are pure, i.e. they have no side-effects

* Make sure any instance variable if initialised via `__init__()` is type
hinted as `Final` if the value will not change during the lifetime of the
class instance

* If `__init__()` has a lot of variables (more than two or three), consider
consolidating those variables into a
[Dataclass](https://docs.python.org/3/library/dataclasses.html) and pass that
class instance as the sole parameter. Ensure that dataclass is frozen so none of
its members can be changed.

* Make sure there are no variables that never change and are not set as
parameters by the class user. These are constants. See above.

* If you are giving your class capabilities (like acquiring state via an
external integration) from parameters to `__init__()`, make sure you have a factory
function that is independent of your class, possibly in a file called
`factories.py`. This factory function or class should construct the class for you.

Remember, `cls` and `self` parameter names are not keywords. They are conventions. 

What you should end up with are classes that are more appropriately sized,
having the methods they actually need. The classes will be more readable (i.e.
you can understand how state changes over time). And it should be easier to
write unit tests.

You might find by applying these rules that you remove all methods from your
class. This is not necessarily a bad thing. There is a special case where the
class might be implementing an interface and you need this interface
implementation. It would be implementing an interface if it derives from an
Abstract Base Class with methods you need on each subclass type. Then you have
to decide what methods actually belong to that interface. 

In general, classes should manage state. They are not for namespacing only
behaviour. Modules already perform that function.

These issues and many more are covered in detail in the guidelines
documentation:

<https://python-coding-guidelines.readthedocs.io/>

