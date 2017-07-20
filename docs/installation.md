
INSTALLATION DE L'APPLICATION
=============================

Cette procédure décrit l'installation de l'application GeoNature-mobile-webapi couplée à l'utilisation de l'application web GeoNature : [https://github.com/PnEcrins/GeoNature](https://github.com/PnEcrins/GeoNature), des applications mobiles Android : [https://github.com/PnEcrins/GeoNature-mobile](https://github.com/PnEcrins/GeoNature-mobile) et de l'utilitaire de synchronisation desktop : [https://github.com/PnEcrins/GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync).

Par Xavier Arbez (PnMercantour)

Pré-requis
=========
* Pré-tuilage des fonds raster au format .mbtiles : [``tuilage_raster_mbtiles.pdf``](https://github.com/PnEcrins/GeoNature-mobile/blob/master/docs/tuilage_raster_mbtiles-2017-01.pdf)

* Environnement serveur : 

Voir le chapitre sur l'installation du serveur de l'application web GeoNature ([http://geonature.readthedocs.org/fr/latest/server.html](http://geonature.readthedocs.org/fr/latest/server.html))

* Disposer d'un utilisateur linux nommé par exemple ``synthese``. Dans ce guide, le répertoire de cet utilisateur est dans ``/home/synthese``

* Se loguer sur le serveur avec l'utilisateur ``synthese`` ou tout autre utilisateur linux faisant partie du groupe www-data.

* Installer les paquets suivants :
  
        sudo apt-get install -y python-virtualenv libapache2-mod-wsgi python-dev build-essential
        
    Attention sur Debian 8, 2 autres paquets sont nécessaires pour compiler correctement :   
    
        sudo apt-get install libpq-dev postgresql-server-dev-9.4

    Sur debian 9 un autre paquet est nécessaire pour compiler correctement :

        sudo apt-get install libgeos-dev


Installation
------------
		
* Récupérer le zip de l’application sur le Github du projet (`X.Y.Z à remplacer par le numéro de version souhaitée` [https://github.com/PnEcrins/GeoNature-mobile-webapi/releases](https://github.com/PnEcrins/GeoNature-mobile-webapi/releases)), dézippez le dans le répertoire de l'utilisateur linux du serveur puis copiez le dans le répertoire de l’utilisateur linux :
  
        cd /home/synthese
        wget https://github.com/PnEcrins/GeoNature-mobile-webapi/archive/X.Y.Z.zip
        unzip X.Y.Z.zip
        mv GeoNature-mobile-webapi-X.Y.Z/ synchronomade/

* Copier et renommer le contenu du fichier settings_local.py.sample en ``settings_local.py``

        cd synchronomade
        cp webapi/faune/settings_local.py.sample webapi/faune/settings_local.py
		
* Adapter le contenu du fichier ``settings_local.py`` à votre contexte en modifiant les informations :
[https://github.com/PnEcrins/GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync)

        'NAME': 'db_name',
        'USER': 'db_user',    
        'PASSWORD': 'xxxx',   
        'HOST': 'localhost',  
        'PORT': '5432',       

        TOKEN = "666"

        MOBILE_SOFT_PATH = "/full_path_to_mobile_soft_apk_and_version_file/"
        MOBILE_FILE_PATH = "/full_path_to_synchronized_files/"

        SYNC_DB_CMD = ""

Vous devez renseigner correctement la connection à la base de données pour les 3 applications (and leave the default empty).

Pour le Token : Renseigner une valeur (devra être identique à celle qui sera renseignée dans le fichier de server.conf  de l'application desktop de synchronisation : https://github.com/PnEcrins/GeoNature-mobile-sync)

Les valeurs de ``MOBILE_SOFT_PATH`` et ``MOBILE_FILE_PATH`` doivent être renseignés selon les chemins défini dans les étapes suivantes :

* Créer les répertoires ``apk`` et ``datas`` puis récupérer les fichiers d'installation (apk) et de settintgs (json) des applications depuis le Github de GeoNature-mobile : https://github.com/PnEcrins/GeoNature-mobile
  (`X.Y.Z à remplacer par le numéro de version souhaitée <https://github.com/PnEcrins/GeoNature-mobile/releases>)
  
        cd synchronomade/webapi
        mkdir apk
        cd apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/apk/fauna-release-1.1.0.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/apk/flora-release-1.1.0.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/apk/invertebrate-release-1.1.0.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/apk/mortality-release-1.1.0.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/apk/search-release-1.1.0.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/apk/version.json
        cd ..
        mkdir datas
        cd datas
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/internal%20memory/settings_fauna.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/internal%20memory/settings_flora.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/internal%20memory/settings_invertebrate.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/internal%20memory/settings_mortality.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/vX.Y.Z/internal%20memory/settings_search.json
        cd ..

* Modifier les fichiers de configuration .json copiés dans /synchronomade/webapi/datas pour chacune des applications en adaptant les paramètres des objets ``"sync"`` et ``"map"`` à votre contexte.


* Installer la webapi :
  
   		make install

	
Adaptation de la BDD
---
Exécuter le script sql/reject_tables.sql sur votre BDD GeoNature (``geonaturedb``) avec l'utilisateur ``geonatuser``.
* Executer le script SQL suivant :
     
		export PGPASSWORD=monpassachanger; sudo psql -h geonatdbhost -U geonatuser -d geonaturedb -f sql/reject_tables.sql

		
Configuration d'Apache vhost
------------

Copier l'exemple de virtual-host Apache

    sudo cp faune/apache.vhost.sample /etc/apache2/sites-available/synchronomade.conf
    
ATTENTION : Depuis la version 2.4 d'Apache, le fichier du virtual-host doit avoir une extension ``.conf`` ainsi que la clause ``Require all granted``

Editer-le en adaptant les chemins à votre contexte et avec les paramètres suivants :

	WSGIScriptAlias /synchronomade /home/synthese/synchronomade/webapi/faune/wsgi.py
	WSGIPythonPath /home/synthese/synchronomade/webapi/lib/python2.7/site-packages
	<Directory /home/synthese/synchronomade/webapi/faune/>
		<Files wsgi.py>
			Order allow,deny
			Allow from all
			Require all granted
		</Files>
	</Directory>

Activer-le et redémarrer Apache :

    sudo a2ensite synchronomade
    sudo apache2ctl restart


la Web API est maintenant disponible sur ``http://server/synchronomade/``.

=================================================
INSTALLER L'UTILITAIRE DESKTOP DE SYNCHRONISATION
=================================================

Prérequis
=========
* Système d'exploitation Windows uniquement en x32 ou x64.
* Installer Java dans la version adapter à votre système (En x64 : Java soit être installé en x32 ET en x64)


* Installer les drivers USB des teminaux sur les ordinateurs concernés.

*  Télécharger et installer l'utilitaire de synchronisation : [https://github.com/PnEcrins/GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync) en suivant la documentation dédiée : [GeoNature-mobile-sync/docs/install_conf_sync.odt](GeoNature-mobile-sync/docs/install_conf_sync.odt)


=================================================
DEPLOYER ET CONFIGURER SUR LE(S) MOBILE(S)
=================================================

Prérequis
=========
* Disposer d'un terminal mobile sous Android (4.X ou 5.X).
* Disposer de plus de 100 Mo d'espace de stockage sur la mémoire physique du terminal mobile.
* Disposer d'une carte mémoire SD avec au moins 6go d'espace disponible.
* Activer le mode développeur et le debogage USB :

	    Paramètres -> A propos du téléphone : cliquer 6 ou 7 fois sur le numéro de build pour activer le mode développeur
    	Paramètres -> Options pour les développeurs : Activer le debogage USB	
	
* Connecter le terminal à l'ordinateur en tant que périphérique multimédia (MTP).
* Lancer la synchronistation à l'aide de l'utilitaire desktop installé précedemment.

ATTENTION sur Android 5 : Il est nécessaire de redémarer le terminal pour que le contenu de la mémoire soit rafraîchi afin de voir le dossier ``com.makina.ecrins`` dans l'explorateur de fichier de l'ordinateur.

* Une fois l'installation terminée se rendre dans la mémoire de la carte SD de l'appareil puis dans : ``Android/data`` et creer un nouveau répertoire ``com.makina.ecrins``
* Ajouter dans ce dernier un nouveau dossier ``databases`` 
* Y copier depuis l'ordinateur les 3 fichiers .mbtiles nécessaire au fonctionnement des applications (les rasters : scan, ortho et unities).

ATTENTION sur Android 5 : Sur Android 4 le dossier ``com.makina.ecrins`` est installé aussi sur la mémoire interne de l'appareil. Il faut donc le créer à nouveau sur la carte SD comme expliqué ci-dessus.
Sur Android 5, la méthode de virtualisation de la mémoire ayant changée, il est possible que le dossier soit déjà crée sur la carte SD. Dans ce cas il faut y ajouter le répertoire 'databases' et les .mbtiles directement dans ce dernier.

Lancer les applications pour vérifier leur bon fonctionnement et le bon chargement des fonds rasters dans la carte.


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
