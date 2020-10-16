publish:
	rm dist/*.tar.gz || true
	python setup.py sdist
	twine upload dist/*
