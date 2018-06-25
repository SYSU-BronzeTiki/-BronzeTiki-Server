# BronzeTiki-Server

using the python backend framework flask

# Programming Language

- development environment: python3.6
- test environment: python3.6
- production environment: python3.6

# Database

- database: mysql5.7

## Web Framework

- flask version: 1.0.2
- - ``pip install Flask==1.0.2``

- MySQL-python middleware: a driver
- MySQL-Client: a Python 3 compatible fork of MySQL-python
- ``https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient``

# ORM

ORM: Object Relationship Mapping(对象关系映射)

- Make it as easy as manipulating object to operate on the database.
- A data table is abstracted to a class and one column of data is an object.
- SQLAlchemy: flask-sqlalchemy
- install: ``pip install flask-sqlalchemy``

# Time

- Use ntp to check the time
- - ``sudo apt-get install ntp``
- - ``/etc/init.d/ntp start``
