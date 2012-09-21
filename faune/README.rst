*Faune Webapi*

=====
SETUP
=====

Requirements
------------

* Ubuntu Server 12.04 Precise Pangolin (http://releases.ubuntu.com/12.04/)


Installation
------------

Once the OS is installed (basic installation, with OpenSSH server), copy and extract the source archive.

cd /path_to_webapi/faune/
export FAUNE_PROJECT=`pwd`

Set the Virtual env
-------------------

cd $FAUNE_PROJECT
virtualenv --no-site-packages .

Activate virtualenv
-------------------
cd $FAUNE_PROJECT
source $FAUNE_PROJECT/bin/activate

Install django
--------------
cd $FAUNE_PROJECT
# download Django : https://www.djangoproject.com/download/1.4.1/tarball/
tar xzvf Django-1.4.1.tar.gz
rm Django-1.4.1.tar.gz
cd Django-1.4.1
sudo python setup.py install
easy_install psycopg2

Install wepapi
--------------

Copy source code to $FAUNE_PROJECT/faune/

Modify path in $FAUNE_PROJECT/faune/wsgi.py

sys.path.append('/path_to_webapi/faune/')


Configure apache vhost
----------------------

sudo apt-get install libapache2-mod-wsgi

Create a new file :

vi /etc/apache2/sites-available/faune

containing :

    WSGIScriptAlias /faune /path_to_webapi/faune/faune/wsgi.py
    WSGIPythonPath /path_to_webapi/faune/faune/lib/python2.7/site-packages
    <Directory /path_to_webapi/faune/>
        <Files wsgi.py>
            Order deny,allow
            Allow from all
        </Files>
    </Directory>

Replace /path_to_webapi/faune/ by the correct path.

Then, create a link :

    sudo ln -s /etc/apache2/sites-available/faune /etc/apache2/sites-enabled/faune

And restart apache :

    sudo apache2ctl restart


Webapi is now available on http://localhost/faune/.

URLs:
-----

Export data:
http://localhost/faune/export/family
http://localhost/faune/export/taxon
http://localhost/faune/export/taxon_unity
http://localhost/faune/export/criterion
http://localhost/faune/export/unity
http://localhost/faune/export/user

POST parameter: 
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
