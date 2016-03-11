all:
	pip install -r requirements.txt
	python setup.py install

develop:
	pip install -r requirements-dev.txt
	python setup.py develop

test2:
	python2 /usr/local/bin/nosetests --logging-level=INFO

test3:
	nosetests -v --with-coverage --cover-package=jetpack --logging-level=INFO

clean:
	rm -rf htmlcov/
	rm -rf jetpack.egg-info
	rm -f jetpack/*.pyc
	rm -rf jetpack/__pycache__
