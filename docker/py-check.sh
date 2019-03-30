docker run -it --rm -v $(pwd)/$(dirname "$0")/../py:/code local-abbey flake8 /code
