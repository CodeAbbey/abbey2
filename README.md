# Abbey2

[![Build Status](https://travis-ci.org/CodeAbbey/abbey2.svg?branch=master)](https://travis-ci.org/CodeAbbey/abbey2)
![GitHub contributors](https://img.shields.io/github/contributors/CodeAbbey/abbey2.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/CodeAbbey/abbey2.svg)

New and open-source version of [CodeAbbey](https://www.codeabbey.com) website - another place to learn
programming with programming problems. The aims of having new site are:

- to have more manageable code, and in Python rather than PHP (mainly because Python is the
    most popular among CodeAbbey users)
- to allow more than one directions of learning (e.g. specializations)
- to introduce some new kinds of problems (quizzes and in-browser "games")

**Our new site is already LIVE at [https://openabbey.com](https://openabbey.com)**

---

### Information for contributors

I recommend this even for those who do not want to contribute anything. It is good experience - attempting to
launch the developer's version of site at your desktop and play a bit with it.

**Project uses `Python 3.7` with some libraries for website engine and `MySQL 5.7` (or higher) as a database.**

There are roughly 2 ways of setting this up locally:

1. Either install proper version of Python and MySQL manually.
2. **Recommended way** - to use `docker` to automatically setup environment in container.
3. Also small changes (e.g. orthography) could be done without running environment, of course.

Using `docker` is recomended not only because it is much simple, but also because in this way you do not
modify your system Python or anything. It automatically creates small "virtual machine" according to description
in the supplied `Dockerfile` - and when you don't need it anymore, you simply delete the image.

Here are the steps:
- clone (or download as `zip`) the project folder and enter it
- [install docker](https://docs.docker.com/install/) specific to your OS
- run `./docker/build-local-server.sh` to create docker image with python, its libraries and mysql
- if you use windows, either try to rename and modify this file to `.bat` version, or use `git bash` which
    is usually installed with `git` (and you probably use one to clone the project).
- now image is ready and whenever you need to launch test server, execute in separate console
    `./docker/local-server.sh`
- access the application in the browser by `http://localhost:5000` address
- whenever you change files in `py` subfolder, the server will automatically reload them
- pressing `Ctrl-C` (in this docker console) will stop and remove the server container
- to check python code use `./docker/py-check.sh`
    and also `./docker/py-test.sh` to run unittests (both need to pass for
    any change to be accepted on github)

I advice not to be hesitant to learn a bit more about docker - it is far not as hard as one may think.
