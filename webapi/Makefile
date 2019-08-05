bin/ lib/:
	virtualenv --no-site-packages .

install: bin/
	bin/python setup.py install
	mkdir log
	/bin/bash install_app.sh

clean:
	sudo rm -rf bin/ lib/ build/ dist/ main.egg-info/ include/ local/ /etc/supervisor/conf.d/webapi-service.conf log/
