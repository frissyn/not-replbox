# replbox

[![replbox on PyPI](https://img.shields.io/pypi/v/replbox.svg)](https://pypi.python.org/pypi/replbox)
[![License](https://img.shields.io/pypi/l/replbox.svg)](https://pypi.python.org/pypi/replbox)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A synchronous Python client package for loading, reading, and dumping REPL projects from repl.it


**There currently isn't any functionality for writing to REPLs, nor running REPLs in this version, those features will come at a later date. This library is still in alpha and much more is still to come. Version 0.1.0 won't hit until the ability to run a REPL is added. Currently working on learning crosis first lol**


## Usage

You first have to instantiate a `Client` class from `replbox`. Like so:

```python
import replbox

client = replbox.Client()
```

### Load/Create a REPL:

Then you can either load a REPL from a user/team path, or create an anonymous REPL with the client.

```python

repl = client.create(language="python3", title="New Repl")

otherRepl = client.load_from_path("@replbox/dummy-repl")
```

`client.create()` can take a number of keyword arguments but only requires the `language` kwarg, which defaults to `python3`. You get a list of valid languages by running `print(replbox.fetch_langs())`

`client.load_from_path()` takes a single argument: a user/team REPL path. This path is usually follow the format `@<username>/<replname>.` The username is case-insensitive, but the REPL name has to be a compatible slug, so for example, "This is a New Repl" becomes `This-is-a-New-Repl`.

Once you've done that, you now have a REPL!

### Get REPL Info:

You can ouput the REPL object in a pretty way like this:

```python
print(json.dumps(repl.json, indent=2))
```

which will get you a similar output to this:
```json
{
  "id": "dd6f9fcd-c515-4d7f-ae93-0e3b317c85d8",
  "user_id": 4532700,
  "title": "dummy-repl",
  "description": "",
  "is_project": false,
  "is_private": false,
  "time_created": "2020-10-26T20:59:41.312Z",
  "time_updated": "2020-10-26T21:59:42.407Z",
  ...
}
```

NOTE: *All attributes in `repl.json` can be accessed individually, like `repl.id` or `repl.time_created`*


### Read a REPL file:

You can read the contents of a file within a REPL with:
```python
file = repl.read('mock/__init__.py')

print(file)
```

OR

```python
mainFile = repl.read_main()

print(mainFile)
```

The main file of a REPL is usually named `main.<language-extension>`. If a main file can't be found then it will default to the first file in the list `repl.fileNames`.

### Download the REPL:

Using a bit of `os` magic, you can download all the contents of a repl to a folder of your choosing, take a look at this code: 

```python
path = os.getcwd() + "/" + repl.slug + "/"

for file in repl.fileNames:
	repl.ensure_path(path + file)
	print(f"Created directory: {path + file}")

	with open(path + file, 'w+') as fp:
		repl.dump(file, fp)
		print(f"Contents successfully dumped.")
		
	print()
```

This code does a few things:
1. Creates a folder with the REPL name in the same directory as your code.
2. `repl.ensure_path()` Splices the file path and file name, then creates the directory if it doesn't exist already.
3. `repl.dump()` Writes the contents of the REPL file to the local copy.

### Login

You can login with your repl.it SID. Find this value in your cookies after logging into repl.it under `connect.sid` and **keep this supder-duper ultra** secret! It'll look a little something like this:

![image](https://storage.googleapis.com/replit/images/1603811188109_ba966b7bd97966d6947a1bf1a3960ec7.png) 

Then login like so:

```python
import os
import replbox

SID = os.getenv("SID")

client = replbox.Client()
user = client.login(SID)
```

`client.login()` will return a `UserClient()` which is essentially the same as a base client but will make requests to the API on your behalf. So loading a REPL from a path under your username should make `repl.is_owner` equal to `True`.

