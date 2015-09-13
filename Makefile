all:
	python setup.py install

develop:
	python setup.py develop

test:
	py.test -v --cov=jetpack --cov-report=html tests

clean:
	rm -rf htmlcov/
	rm -rf jetpack.egg-info
	rm -f jetpack/*.pyc
	rm -rf jetpack/__pycache__
