test:
    find . -name "*.py" | grep -v __init__ | xargs -n1 pytest --quiet --quiet
