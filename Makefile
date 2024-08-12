lint:
	PYTHONPATH=. djlint --reformat templates
	PYTHONPATH=. ./venv/bin/python -m black .
	PYTHONPATH=. isort .
	PYTHONPATH=. pylint -v --recursive=y .
