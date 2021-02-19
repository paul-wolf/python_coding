Fish Information Example Class Structure
========================================

Our use case: We are building a web application that retrieves
information from a remote source of data, We'll use the https://fishbase.ropensci.org/
as an example.

All the code should work. It is blackend, passes both mypy and flake8 without errors.

You need at least Python 3.6. 

To install the sample project, clone the repo, go into the directory and run the samples. 

```shell
git clone git@github.com:paul-wolf/python_coding.git
cd python_coding/fish
python -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
```

Run the unrefactored code:

```shell
python original/fishy.py
```

Run the refactored code:

```shell
python refactored/fishery.py
```

The code is intended for reading rather than running. You'll find some hopefully
helpful comments in the source.

As usual, our example does not have most real-world code for exception
handling and many other things. We want to target specific design issues
in a generic way, not figure out how to build a real application. 

