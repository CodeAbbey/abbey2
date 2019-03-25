# Abbey2

[![Build Status](https://travis-ci.org/CodeAbbey/abbey2.svg?branch=master)](https://travis-ci.org/CodeAbbey/abbey2)
![GitHub contributors](https://img.shields.io/github/contributors/CodeAbbey/abbey2.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/CodeAbbey/abbey2.svg)

New and open-source version of [CodeAbbey](https://www.codeabbey.com) website. At least an
attempt to create one. The goals are:

- to have more manageable code, and in Python rather than PHP (mainly because Python is the
    most popular among CodeAbbey users)
- to allow more than one directions of leaning
- to introduce some new kinds of problems (quizzes and in-browser "games")

**Our new site is already LIVE at [https://openabbey.com](https://rodiongork.pythonanywhere.com/)**

### Information for contributors

**[also at project wiki](https://github.com/CodeAbbey/abbey2/wiki)**

To work with project locally, one needs `Python 3.7` with certain libraries and `MySQL 5.7`.

_This is not strictly necessary for contributing into project, but convenient for working on functional changes and improvements. Small fixes (e.g. design and spelling) could be proposed directly at GitHub._

The **recommended way** to setup this is by using `docker`. It creates small "virtual machines" (called "containers")
with all stuff installed - and you need not spoil your system configuration.

- first run `./docker/build-py3.sh` to create docker image with python and its libraries
- in the same manner run `./docker/build-mysql.sh` to create image with database and schema
- then whenever you need to have test server running, execute in separate console `./docker/mysql.sh` and
    when you see it started (may take several seconds), execute `./docker/py-server.sh`
    to launch application in the test server
- access the application in the browser by `http://localhost:5000` address
- whenever you change files in `py` subfolder, the server will automatically reload them
- however it may sometimes crash if you write erroneous code - then just relaunch `./docker/py-server.sh` (after fixing code)
- pressing `Ctrl-C` (in this docker console) will stop the server
- to stop the database server, use `./docker/mysql-stop.sh
- to check python code use `./docker/py-check.sh`
    and also `./docker/py-test.sh` to run unittests (both need to pass for
    any change to be accepted)

The first steps (building images) need only be done once (unless the image is manually removed later).

Learn a bit more about docker to find out how to use python and mysql consoles in the running containers
