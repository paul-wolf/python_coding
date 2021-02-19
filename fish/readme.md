Fish Information Example Class Structure
========================================

My use case: We are building a web application that retrieves
information from a remote source of data, We'll use the https://fishbase.ropensci.org/
as an example, all the code should work. 

You need at least Python 3.6. 

To install the sample project: 

```shell
cd fish
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

As usual, our example does not have most real-world code for exception
handling and many other things. We want to target specific design issues
in a generic way, not figure out how to build a real application. 

The example: we want a class that gets data from the remote site. We
assume a javascript web client. Since the web client is already
rendering a view, we want to notify that view via web sockets when we
have our data ready.

   {
      "ComName": "\tPez pipa culebra",
      "SpecCode": 2481,
      "Language": "Arabic",
      ...
   }
