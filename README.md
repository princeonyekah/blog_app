# Team Software Project Starter Template - Flask

This example shows how to implement a basic app using:

- [Flask](https://flask.palletsprojects.com/en/3.0.x/) 
- [Prisma Client](https://prisma-client-py.readthedocs.io/en/stable/) as the ORM
- A SQLite database file with some initial dummy data which you can find at [`./prisma/dev.db`](./prisma/dev.db)
- [Bootstrap](https://getbootstrap.com/) for basic CSS Styling.
- [Pytest](https://docs.pytest.org/en/7.4.x/) for unit testing
- [pylint](https://pypi.org/project/pylint/) to statically analyze your code and find problems
- [black: The Uncompromising Code Formatter](https://pypi.org/project/black/) to format your code

It is intended to serve as a starting point for your Team Software Project course if you choose to use ExpressJS. It
provides examples for performing basic tasks with different types of endpoints (GET, POST, etc.)

## Getting started

> Note: You may consider using pyenv to create a separate python environment that is configured specifically for this
> app.  Please see the section below with the general steps for getting up and running with pyenv if you want to use
> this path.

### 1. Download example and install dependencies

Clone this repository:

```bash
git clone git@github.com:kiboschool/tsp-flask-starter-template.git

cd tsp-flask-starter-template

```

Setup and activate your virtual environment:

`python3 -m venv .venv`

`source .venv/bin/activate`

Install dependencies:

```bash
pip3 install -r requirements.txt
```

### 2. Create and seed the database

Run the following command to create your SQLite database file. This also creates the `User` and `Post` tables that are
defined in [`prisma/schema.prisma`](./prisma/schema.prisma):

```bash
prisma db push
```

Seed the database by running the `./prisma/seed.py` file

```bash
python3 ./prisma/seed.py
```

### 3. Interacting with the Starter Template

```bash
flask run
```

If you encounter this error:
```
Traceback (most recent call last):
  File "/opt/homebrew/lib/python3.10/site-packages/flask/cli.py", line 219, in locate_app
    __import__(module_name)
  File "/Users/msaudi/kibo/tsp-flask-starter-template/app/__init__.py", line 3, in <module>
    from flask_jwt_extended import JWTManager
ModuleNotFoundError: No module named 'flask_jwt_extended'
```
It means your virtual environment uses a different python version than the one in the environment itself. To fix this, do the following steps:

1. Open this file `.venv/bin/activate` using your favorite text editor
2. Add this line to the end of the file `export PYTHONPATH="./.venv/bin/python3"`
3. Save and close the file
4. Source the file in the terminal using this command `source .venv/bin/activate`
5. Run your flask project `flask run`

### Additional Commands

**pylint configuration is stored in the `.pylintrc` file.**

Check if the formatting matches pylint's rules by running

``` bash
pylint app
```

Format your code with Black using this command:

``` bash
black app
```

Run unit tests with this command:

```bash
pytest tests
```
