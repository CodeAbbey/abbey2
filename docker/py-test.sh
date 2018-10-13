docker run -it --rm -v $(pwd)/$(dirname "$0")/../py:/code -w /code py3-abbey python -m unittest
