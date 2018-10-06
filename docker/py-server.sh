docker run -it --rm --name py3-abbey-run -v $(pwd)/$(dirname "$0")/../py:/code -p 5000:5000 py3-abbey
