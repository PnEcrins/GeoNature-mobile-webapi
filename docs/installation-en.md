*Faune Webapi*

Initial documentation to install GeoNature-mobile-webapi (2013). 

=====
SETUP
=====

Requirements
------------

* Ubuntu Server 12.04 Precise Pangolin (http://releases.ubuntu.com/12.04/)

Configuration
--------------  

Copy and extract the source archive.

Copy settings_local.py.sample to settings_local.py and modify informations :

::

        'NAME': 'appli_faune',
        'USER': 'dbuser',    
        'PASSWORD': 'xxxx',   
        'HOST': 'localhost',  
        'PORT': '5432',       

        TOKEN = "666"

        MOBILE_SOFT_PATH = "/full_path_to_mobile_soft_apk_and_version_file/"
        MOBILE_FILE_PATH = "/full_path_to_mbtiles/"

        SYNC_DB_CMD = "/usr/local/bin/talend/ecrins2rezo/ecrins2rezo/ecrins2rezo_run.sh --context_param mes_zp="

You need to fill the correct database connections for the 3 applications, and leave the default empty.

Note for the token: change to correct value (must be the same as the one defiend in the sync app)

Installation
------------

Once the OS is installed (basic installation, with OpenSSH server), with the following packages :

    sudo apt-get install -y python-virtualenv libapache2-mod-wsgi python-dev build-essential

Warning: the package build-essentials has been renamed build-essential in the latest debian versions

Warning Debian 8 : in order to properly compile, 2 other packages need to be installed
    
    sudo apt-get install libpq-dev postgresql-server-dev-9.4


Install the webapi :

::

    cd /path_to_webapi/
    
    make install

BDD
---

Execute the sql/reject_tables.sql on the database.
It will create a new schema synchronomade with 2 reject tables.

Apache vhost
------------

Copy the virtual host example :

::

    sudo cp faune/apache.vhost.sample /etc/apache2/sites-available/faune
    
Warning : starting with apache 2.4 the virtual host file need to have a .conf extension

Edit it and replace /path_to_webapi/faune/ by the correct path.


Activate it and restart apache :

    sudo a2ensite faune
    sudo apache2ctl restart


Web API is now available on http://server/faune/.


=====
USAGE
=====

Export data:

    http://server/faune/export/sqlite
    http://server/faune/export/unity_geojson
    or
    http://server/faune/export/unity_polygons

POST parameter (defined in settings.py) :
    token

Import data:

    http://localhost/faune/import_data

POST parameter:
    token
    data (json data for importing)


Notes:
unity_geojson produces a json file (geojson format) by reading the unities table in the database.
unity_polygons produces a wkt file (geojson format) by reading the unities table in the database. Polygons are simply added to the text file (one polygon per line)


=======
AUTHORS
=======

    * Sylvain Beorchia
    * Mathieu Leplatre

|makinacom|_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com


=======
LICENSE
=======

    * (c) Makina Corpus
