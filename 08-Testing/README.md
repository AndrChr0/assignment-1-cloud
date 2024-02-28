# Testing

> NB! This text was drafted and then rewritten, so it may have a slightly messy structure. Apologies in advance.

The goal of this exercise is to install some testing tools, learn a bit about how to test different aspects of our system, and do the necessary setup to achieve these goals.

We will have to make multiple new files with a lot of configuration, but actually, we will mostly just copy them from an existing project.

We will then have to install our local project using `pip`. This technically isn't needed, but it will make using relative imports a lot easier.

Then, we will be able to use the relevant modules to test our project. (Well technically, only the unit testing will require project install.)

## Regarding the files and file hierarchy
Our project structure should look something like this:

```
root
    src
        module_name
            __main__.py
            stuff.py
        py.typed

    tests
        test_main.py
        test_stuff.py

    .github
        workflows
            tests.yml

    pyproject.toml
    requirements.txt
    setup.cfg
    setup.py
    tox.ini
```

The file `py.typed` can be left empty. The python files `*.py` can include whatever we want. The rest of the files should simply be copied from an existing project. (Like this one.)

In these files, we need to update some info. Mainly, update the `requirements.txt` file for our project, and replacing `module_name` (`exercise7` in our case) with the real project name.

Some of these files tell Python/pip how to install our module. Some of these files tell the testing tools (`pytest`, `flake8`, `black`, `mypy` and `tox`) how to run. Some of the files tell GitHub how to run the tests using GitHub actions.

## Installing modules
For this exercise, we need multiple modules. We'll add or copy them to the `requirements.txt` file, and install them from there. Many use a separate file for development modules (usually named `requirements_dev.txt`, but we won't do that this time.)

Install dependencies using

```bash
pip install -r requirements.txt
```

NB! For `pip` and all other modules, you _may_ have to use `python -m pip ...` or `python3 -m pip ...` or `py -m pip ...` and so on. Same with `pytest` and the rest.

## Setting up the module
We want to create an installable and usable module out of our program. (Actually, this may not be entirely necessary, but not a bad thing, so you might as well.) To do this, we will create some setup files and install the `setuptools` package.

To install the module, be in root and run the following command.

```bash
pip install -e .
```

You should now find your module when running `pip list`. (Assuming the `setup.*` files are included in the project properly, and all the folder structures are working and so on. Lots of things can go wrong here.)

## Unit testing
### Basic unit testing
We want to do testing and stuff :D

The function below finds the file type extension of a file name. For example, the file "image.png" should return "png". It does this by splitting the filename on ".", and returns the last element of the resulting list.

```python
def get_file_extension(filename):
    file_ext = filename.split('.')[-1]
    return file_ext
```

Now let's test it!

We can do it in the same code, by running the function with test parameters, and *asserting* we get the expected result. We do this with the keyword `assert`.

```python
assert get_file_extension('image.png') == 'png'
```

This program will crash here, if the statement is not true. You will be told where the error/failed test is.

The syntax of the `assert` statement is as follows:

```python
assert <boolean value>
```

or

```python
assert <boolean value>,  <optional descriptive string>
```

So you could write
```python
assert False 'Test failed because False =/= True'
```

Or maybe more sensibly, using an f-string:

```python
x = False
assert X, f'Test failed, as X =/= True, but is rather {X}. :('
```

### Unit testing using pytest
When writing small programs, I'll often write tests in the same files, right after the function implementation. This is, however, not a good way to structure larger projects. The way is then to split the code into two folders:

* `src` (or something like that)
* `tests`

Well, actually you should do a bunch more, but not the point. Let's use these two folders for now.

In the `src` folder, we create a file called `stuff.py`, with a function `things`.
In the `tests` folder, we create file called `test_stuff.py`, with a function `test_things`. If I'm not mistaken, the function and file has to start with `test_` and the folder must be named `tests` but otherwise these rules aren't absolute.

project
| src
| - stuff.py
| tests
| - test_stuff.py

Let's implement the functions as follows.

File: `src/stuff.py`
```python
def things(x):
    return 3 * x
```

File: `tests/test_stuff.py`
```python
from src.stuff import things
def test_things():
    assert things(2) == 6
    assert things(0) == 0
    assert things(-5) == -15
```

As you may see, the tests are hardcoded truth statements. Make sure to add a sufficient amount of tests to ensure that all edge cases are covered. Or, add edge cases when you find them.

We then use the module pytest (which has to be installed using `pip install pytest` or similar).
When this is installed, we simply run the command `pytest` (or `pytest tests`) in our project directory, and it will run all tests in all files. This should take less than a second.

> Important note here: The relative path depends on project structure as well as how `pytest` looks for files. Try things like: `src.stuff`, `stuff`, and more. Expect this to fail, and you won't be disappointed. :)

### More pytest
We can also add tools like pytest-cov to give us a report on the test coverage, i.e. the percentage/fraction/number of lines we have tested.

For example, say we have a code with 200 lines, and our tests run/access 150 of them. That is a 75% coverage.

There are also a bunch of other bonus modules, like pytest-mock, which is used for mocking (ask me in class what that is). As well as maany configurations for pytest and related modules. We can generate html-reports of the code test coverage, outlining which lines are and are not covered.

## Extra tools
We will also use three additional tools here. Two simple and one much more complex:

* flake8 `style checker`
* mypy `type checker`
* tox `multi environment test runner thing`

We will not go into much detail about how these should be used. A lot of the config will just be copied from an existing project.

### Flake8
Flake8 scans your code, and finds where your code does not follow a set style guide (default is PEP-8). This is about style, not actual functionality. Things like whether or not you include a space around your operators. E.g. `x = 3 + 4` instead of `x   =3+4`.

It is not super important, but very nice when working with others who may have to read your code.

Another tool called `black` exists, and it follows similar styles, but will fix the issues, rather than just tell you where they are. Arguably more useful, but also a bit more dangerous, and will also change your (personal) style without asking.

The internet also says that the module `ruff` is substantially faster, while otherwise being similar to `flake8`. Feel free to try it and update me on which is better.

One of the positive side of using `flake8` (or `ruff`?) is that you have to fix your own mistakes. You will not learn what you do wrong when using `black` to fix your errors.

### Mypy
Mypy goes through your type hinting and such (of which you presumably have little at this point), and tells you if something seems wrong. For example, if you make a function, which accepts two integers and returns a float, mypy can check if it is correct. The function below has type hints.

```python
def divide(a: int, b: int) -> float:
    c: float = a / b
    return c
```

If we call it as follows, we are breaking our promises, and mypy will tell us as much.

```python
divide(3.14, 0.01)
```

The code will work either way, but it does not match the type hinting.

### Tox
Tox allows us to run multiple tests, like pytest, flake8 and mypy, in multiple environments during a test run. E.g. the tests will run in Python 3.6, 3.7, 3.8, 3.9 and 3.10. And all of these sets of tests can also be ran in Linux, Mac and Windows, using GitHub actions. In total 15 different environments. That way, we can have some certainty that our code will work on all different plattforms.

Note: In our situation, this may be less important, as the code does not have to run on all types of plattforms, but it's still a nice skill to know about.

Since tox is doing so much, it is a looot slower than the other tests. Unit testing should usually run in less than a second. Same with style and type checking. Tox will probably use anything from 10 seconds to 10 minutes.

### Run the tests
We can run the tests using the modules directly (or by adding `python -m` or similar in front).

Be in the project root directory and run unit tests using

```bash
pytest
```

This should show us all the ran tests, which failed and succeded, as well as showing us the test coverage.

We can run `flake8`, `black` and/or `mypy` by adding the diretory behind the main command. E.g.

```bash
flake8 src
black src
mypy src
```

Finally, let's run `tox`, to run all the tests in multiple different Python versions. We do this by simply running.

```bash
tox
```

Make a script or a `makefile` to run the first tests. That way you can write something like `make` or `make test` and run the fast tests. Takes 1 second, and you know your program probably works. Do this whenever you update code. Then, when you are ready to push, run a `tox` test. If it passes, push, and GitHub will run a more thorough test. If failed, GitHub will tell you. If passed, you get a green checkmark and everything is wonderful.

### (API) documentation generation
This section is almost certainly not something we will be doing, but I'mma write it anyway. We can automatically generate documentation from our doc-strings using tools like Sphinx or pydoc. Their setup is kinda complicated, so let's not. But for bigger projects, it can be an amazing addition.

And in case that has not been commented on yet, a doc-string is the explanatory string located first in your files, your classes and your functions. If you look at professionals' code, they'll often have those. The automatic documentation generators will generally just take all of those strings, and create a sexy HTML site with them. Make these automatically push to a part of your website, and the documentation will always be up to date. Simply amazing.

### GitHub actions
To add these tests and runs to the GitHub action system, we can simply copy the file + folder structure of the `.github` folder in the project root. This will allow GitHub to run the tests when we push to our remote repo.

As this exercise is not in root, the `.github` folder will be ignored. Therefore, the GitHub actions will not run.

In addition to this, if the repo is public, we can add a little button to say the tests passed. One of those pretty ones all cool and official repos have. :D
