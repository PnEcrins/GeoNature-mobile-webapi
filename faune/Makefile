bin/ lib/:
	virtualenv --no-site-packages .

install: bin/
	source bin/activate
	python setup.py install

clean:
	rm -rf bin/ lib/ build/ dist/ faune.egg-info/
