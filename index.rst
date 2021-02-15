Python Coding Guidelines
========================

This is a set of guidelines to make Python code more readable, easier to
maintain and easier to reuse.

The concentration is on sound coding rather than big issues around
architecture. We don’t pay much attention to how to make code faster.
We’re more interested in the process of efficient code production and
code maintenance. Writing idiomatic Python is a sound basis for
efficient code.

If you struggle with too many bugs and maintanance problems in your
project, applying the following recommendations might have a big
positive effect. The intent is to bring together many well-known good
practices in a checklist form to provide a toolkit for code reviews.
This is not an authoritative set of prescriptions. It’s a starting point
for developing your own set of guidelines. Discard or modify practices
as you see fit.

You’ll need to be familiar with Python to some extent since we won’t
explain basics of the language. But there are helpful references in the
appendix especially for common design patterns. If you are not familiar
with some parts of Python like how modules and packages work, you’ll
need to read up in the `Python Standard Library documentation <https://docs.python.org>`_.

Most of this material is applicable to most Python versions but we
assume a more or less current version like 3.7 or even higher.


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   python_guidelines
   context_dependent_variables
   class_design
   code_review_checklist

Indices and tables
==================

* :ref:`search`
