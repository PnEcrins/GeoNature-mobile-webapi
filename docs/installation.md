
INSTALLATION DE L'APPLICATION
=============================

Cette procédure décrit l'installation de l'application GeoNature-mobile-webapi couplée à l'utilisation de l'application web GeoNature : [https://github.com/PnEcrins/GeoNature](https://github.com/PnEcrins/GeoNature), des applications mobiles Android : [https://github.com/PnEcrins/GeoNature-mobile](https://github.com/PnEcrins/GeoNature-mobile) et de l'utilitaire de synchronisation desktop : [https://github.com/PnEcrins/GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync).


Pré-requis
=========

Environnement serveur
---------------------

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
============

* Récupérer le zip de l’application [sur le Github du projet](https://github.com/PnEcrins/GeoNature-mobile-webapi/releases)
    *X.Y.Z à remplacer par le numéro de version souhaitée
* Dézipper l'archive dans le répertoire ``/home`` de l'utilisateur linux et le renommer :

        cd /home/synthese
        wget https://github.com/PnEcrins/GeoNature-mobile-webapi/archive/X.Y.Z.zip
        unzip X.Y.Z.zip
        mv GeoNature-mobile-webapi-X.Y.Z/ synchronomade/
        rm X.Y.Z.zip

* Copier et renommer le contenu du fichier ``settings_local.py.sample`` en ``settings_local.py``

        cd synchronomade/webapi
        cp main/settings_local.py.sample main/settings_local.py

* Créer les répertoires ``apk`` et ``datas`` puis récupérer les fichiers d'installation (apk) et de settintgs (json) des applications depuis le Github de [GeoNature-mobile](https://github.com/PnEcrins/GeoNature-mobile). X.Y.Z à remplacer par le numéro de version souhaitée https://github.com/PnEcrins/GeoNature-mobile/releases)

        mkdir apk
        cd apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/apk/fauna-release-X.Y.Z.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/apk/flora-release-X.Y.Z.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/apk/invertebrate-release-X.Y.Z.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/apk/mortality-release-X.Y.Z.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/apk/search-release-X.Y.Z.apk
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/apk/version.json
        cd ..
        mkdir datas
        cd datas
        wget https://github.com/PnEcrins/GeoNature-mobile-sync/raw/master/docs/install/settings.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/internal_memory/Android/data/com.makina.ecrins/settings_fauna.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/internal_memory/Android/data/com.makina.ecrins/settings_flora.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/internal_memory/Android/data/com.makina.ecrins/settings_invertebrate.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/internal_memory/Android/data/com.makina.ecrins/settings_mortality.json
        wget https://github.com/PnEcrins/GeoNature-mobile/raw/master/docs/install/internal_memory/Android/data/com.makina.ecrins/settings_search.json
        cd ..

* Modifier les fichiers de configuration .json des applications Android copiés dans ``synchronomade/webapi/datas`` en adaptant les paramètres des objets ``sync``, ``qualification`` et ``map`` à votre contexte. [Voir la documentation](/docs/install/installation.rst); 

Ces fichiers sont les fichiers de configuration des applications Android que l'application [GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync), si elle est utilisée, pourra mettre à jour sur les terminaux Android lors de la synchronisation. Si le fichier présent sur le serveur (webapi) est plus récent que le fichier présent sur le terminal Android, celui du terminal est remplacé par celui du serveur; Ce mécanisme permet de s'assurer que la configuration des applications est toujours à jour et permmet de centraliser les modifications à opérer sur les terminaux à partir de la webapi. Il suffit donc de mettre à jour les fichiers de configuration sur la webapi pour mettre à jour tous les terminaux qui s'y connecteront par le biais de [GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync). Si vous n'utilisez pas [GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync) mais que vous synchronisez directement depuis les applications, cette mise à jour ne peut opérer ; elle devra être faite manuellement sur chacun des terminaux Android.

De la même manière, si une mise à jour des applications doit être réalisée, l'application [GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync) compare la version des applications installées sur le terminal avec le contenu du fichier apk/version.json. Si les applications GeoNature-mobile doivent être mise à jour sur le terminal Android, [GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync) s'en occupera. Pour cela vous devez replacer les fichiers .apk dans le répertoire ``synchronomade/webapi/apk`` ainsi que le fichier version.json.

* Modifier le fichier ``synchronomade/webapi/datas/settings.json``. Ce fichier est le fichier de configuration de l'application [GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync). Il permet de déclarer l'url et le token de la webapi ainsi que les opérations de synchronisation que [GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync) doit réaliser.
Ce fichier est un exemple de configuration à adapter à votre contexte.
Si votre contexte est multi-organismes, [voir la documentation](/home/gil/synchronomade/docs/configuration_multi_organismes.md)

* Adapter le contenu du fichier ``synchronomade/webapi/main/settings_local.py`` à votre contexte en modifiant les informations :

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

Pour le Token : Renseigner une valeur qui devra être identique dans le fichier de ``server.json`` de l'application [GeoNature-mobile-sync](https://github.com/PnEcrins/GeoNature-mobile-sync) ainsi que dans le fichier ``synchronomade/webapi/datas/settings.json``

Les valeurs de ``MOBILE_SOFT_PATH`` et ``MOBILE_FILE_PATH`` doivent être renseignés selon les chemins défini dans les étapes précédentes :


* Installer la webapi :

		cd /home/synthese/synchronomade/webapi
   		make install


Adaptation de la BDD
--------------------
Examiner la base de données GeoNature; Vous devez avoir un schéma ``synchronomade`` comportant 4 tables ``erreurs_xxx``. Ces tables ont vocation à recevoir les saisies des applications Android tombées en erreur lors de la synchronisation.
Si ce n'est pas le cas, exécuter le script sql/reject_tables.sql sur votre BDD GeoNature (``geonaturedb``) avec l'utilisateur ``geonatuser``.
* Executer le script SQL suivant :

		export PGPASSWORD=monpassachanger; sudo psql -h geonatdbhost -U geonatuser -d geonaturedb -f sql/reject_tables.sql


Configuration Apache
--------------------

Copier l'exemple de virtual-host Apache

    sudo cp main/apache.vhost.sample /etc/apache2/sites-available/synchronomade.conf

ATTENTION : Depuis la version 2.4 d'Apache, le fichier du virtual-host doit avoir une extension ``.conf`` ainsi que la clause ``Require all granted``

Editer-le en adaptant les chemins à votre contexte et avec les paramètres suivants :

	WSGIScriptAlias /synchronomade /home/synthese/synchronomade/webapi/main/wsgi.py
	WSGIPythonPath /home/synthese/synchronomade/webapi/lib/python2.7/site-packages
	<Directory /home/synthese/synchronomade/webapi/main/>
		<Files wsgi.py>
			Order allow,deny
			Allow from all
			Require all granted
		</Files>
	</Directory>

Activer-le et redémarrer Apache :

    sudo a2ensite synchronomade
    sudo apache2ctl restart


la Web API est maintenant disponible sur ``http://server/synchronomade/``. Elle est utilisable directement depuis les applications Android [GeoNature-mobile](https://github.com/PnEcrins/GeoNature-mobile) pour synchroniser les observations saisies. Pour cela, vous devez fournir l'url et le token de la webapi dans les fichiers de ces applications. [voir la partie "Mémoire interne du terminal de la documentation](https://github.com/PnEcrins/GeoNature-mobile/blob/develop/docs/install/installation.rst)



USAGE DEVELOPPEUR
-----------------

Export data:

    http://server/synchronomade/export/sqlite
    http://server/synchronomade/export/unity_geojson
    or
    http://server/synchronomade/export/unity_polygons

POST parameter (defined in settings.py) :
    token

Import data:

    http://localhost/synchronomade/import_data

POST parameter:
    token
    data (json data for importing)


Notes:
unity_geojson produces a json file (geojson format) by reading the unities table in the database.
unity_polygons produces a wkt file (geojson format) by reading the unities table in the database. Polygons are simply added to the text file (one polygon per line)
