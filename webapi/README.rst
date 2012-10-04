*Faune Webapi*

=====
SETUP
=====

Requirements
------------

* Ubuntu Server 12.04 Precise Pangolin (http://releases.ubuntu.com/12.04/)

Configuration
--------------  

Copy and extract the source archive.

Copy settings_local.py.sample to settings_local.py and modify informations in settings.py

::

        'NAME': 'appli_faune',
        'USER': 'dbuser',    
        'PASSWORD': 'xxxx',   
        'HOST': 'localhost',  
        'PORT': '5432',       

        TOKEN = "666"


Installation
------------

Once the OS is installed (basic installation, with OpenSSH server), with the following packages :

    sudo apt-get install -y python-virtualenv libapache2-mod-wsgi python-dev build-essentials

Install the webapi :

::

    cd /path_to_webapi/faune/
    
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

POST parameter (defined in settings.py) :
    token

Import data:

    http://localhost/faune/import_data

POST parameter:
    token
    data (json data for importing)



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
