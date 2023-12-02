.PHONY: test

test:
	export PYTHONPATH=$$PYTHONPATH:$(PWD); \
    python -m unittest discover . '*.py'
