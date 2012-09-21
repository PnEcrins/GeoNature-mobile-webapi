bin/ lib/:
	virtualenv --no-site-packages .

install: bin/
	bin/python setup.py install

clean:
	rm -rf bin/ lib/ build/ dist/ faune.egg-info/
