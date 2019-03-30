docker run -it --rm -v $(pwd)/$(dirname "$0")/../py:/code -w /code -e PYTHONDONTWRITEBYTECODE=1 local-abbey python -m unittest
