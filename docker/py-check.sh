docker run -it --rm -v $(pwd)/$(dirname "$0")/../py:/code py3-abbey flake8 /code
