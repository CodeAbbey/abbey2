# Abbey2

**[Live demo at rodiongork.pythonanywhere.com](https://rodiongork.pythonanywhere.com/)**

To create convenient environment, use `docker`:

- first run `docker-build.sh` to create image with suitable version of python and necessary libraries
- then whenever you need to have test server running, execute `docker-py.sh`
- access the app in the browser by `http://localhost:5000` address
- pressing `Ctrl-C` (in the docker console) will stop the server

The first step needs only be done once (unless the image is manually removed later).

These instructions may change (as we'll need more containers for real web-server, database etc)
