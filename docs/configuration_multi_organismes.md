## Configuration multi-organismes

### Configuration de `settings_local.py`

Copier et renommer le contenu du fichier `settings_local.py.sample` en
`settings_local.py`.

Par défaut, le fichier de paramétrage `settings_local.py` contient les
paramètres suivants ainsi que leurs valeurs par défaut pour la gestion
multi-organismes :

```python
# Fauna meta values
FAUNA_ID_ORGANISM = 2
FAUNA_ID_PROTOCOL = 1
FAUNA_ID_LOT = 1

# Mortality meta values
MORTALITY_ID_ORGANISM = 2
MORTALITY_ID_PROTOCOL = 2
MORTALITY_ID_LOT = 2

# Invertebrate meta values
INVERTEBRATE_ID_ORGANISM = 2
INVERTEBRATE_ID_PROTOCOL = 3
INVERTEBRATE_ID_LOT = 3

# Flora meta values
FLORA_ID_ORGANISM = 2
FLORA_ID_PROTOCOL = 4
FLORA_ID_LOT = 4
```

Le fichier de paramétrage `settings_local.py` contient notamment le paramètre
`MOBILE_FILE_PATH` pour configurer le chemin absolu de base vers les
différents fichiers à synchroniser sur les terminaux mobiles.

Ce paramètre est utilisé par l'URL `data_download/` du module *WebAPI* pour
pouvoir synchroniser n'importe quel fichier à travers l'application de
synchronisation.

C'est ce paramètre qui sera utilisé pour créer autant de sous répertoires qu'il
y a de configuration pour les applications de saisies.

### Exemples

#### Configuration simple

`MOBILE_FILE_PATH` : `/chemin/absolu/vers/le/répertoire/de/base`

Dans ce répertoire, on trouvera :

* `settings.json` : fichier de configuration utilisé par l'application de
synchronisation :

  ```json
  {
    "sync":
    {
      "url": "http://mondomaine.fr/urlsynchro/",
      "token": "mon!token#complexe",
      "timeout": 10000,
	    "status_url": "status/",
      "settings_url": "data_download/",
      "import_url": "import/",
      "app_update":
  		{
  			"version_url": "soft_version/",
  			"download_url": "soft_download/"
  		},
      "exports":
      [
        {
  				"url": "export/sqlite/",
  				"file": "databases/data.db"
  			},
  			{
  				"url": "export/unity_polygons/",
  				"file": "unities.wkt"
  			},
        {
          "url": "data_download/settings_fauna.json/",
          "file": "settings_fauna.json"
        },
        {
          "url": "data_download/settings_mortality.json/",
          "file": "settings_mortality.json"
        },
        {
          "url": "data_download/settings_invertebrate.json/",
          "file": "settings_invertebrate.json"
        },
        {
          "url": "data_download/settings_flora.json/",
          "file": "settings_flora.json"
        },
        {
          "url": "data_download/settings_search.json/",
          "file": "settings_search.json"
        }
      ]
    }
  }
  ```

* `settings_*.json` : fichiers de configuration par application de saisie

L'application de synchronisation utilisera le fichier `settings.json` venant du
module *WebAPI* dans lequel on trouvera les différentes URLs pour synchroniser
les fichiers utilisés pour les applications de saisies, notamment les fichiers
de configuration.

#### Configuration multi-organismes

`MOBILE_FILE_PATH` : `/chemin/absolu/vers/le/répertoire/de/base`

Dans ce répertoire, on trouvera autant de sous-répertoires qu'il y a
d'organismes:

**Organisme #1**

Sous répertoire : `organisme_01` (à nommer comme on le souhaite) :

* `settings.json` : fichier de configuration utilisé par l'application de
synchronisation

  ```json
  {
    "sync":
    {
      "url": "http://mondomaine.fr/urlsynchro/",
      "token": "mon!token#complexe",
      "timeout": 10000,
	    "status_url": "status/",
      "settings_url": "data_download/organisme_01",
      "import_url": "import/",
      "app_update":
  		{
  			"version_url": "soft_version/",
  			"download_url": "soft_download/"
  		},
      "exports":
      [
        {
  				"url": "export/sqlite/",
  				"file": "databases/data.db"
  			},
  			{
  				"url": "export/unity_polygons/",
  				"file": "unities.wkt"
  			},
        {
          "url": "data_download/organisme_01/settings_fauna.json/",
          "file": "settings_fauna.json"
        },
        {
          "url": "data_download/organisme_01/settings_mortality.json/",
          "file": "settings_mortality.json"
        },
        {
          "url": "data_download/organisme_01/settings_invertebrate.json/",
          "file": "settings_invertebrate.json"
        },
        {
          "url": "data_download/organisme_01/settings_flora.json/",
          "file": "settings_flora.json"
        },
        {
          "url": "data_download/organisme_01/settings_search.json/",
          "file": "settings_search.json"
        }
      ]
    }
  }
  ```

* `settings_*.json` : fichiers de configuration par application de saisie

  ```json
  {
    "qualification": {
      "organism": 2,
      "protocol": 1,
      "lot": 1
    }
  }
  ```

**Organisme #2**

Sous répertoire : `organisme_02` (à nommer comme on le souhaite) :

* `settings.json` : fichier de configuration utilisé par l'application de
synchronisation

  ```json
  {
    "sync":
    {
      "url": "http://mondomaine.fr/urlsynchro/",
      "token": "mon!token#complexe",
      "timeout": 10000,
	    "status_url": "status/",
      "settings_url": "data_download/organisme_02",
      "import_url": "import/",
      "app_update":
  		{
  			"version_url": "soft_version/",
  			"download_url": "soft_download/"
  		},
      "exports":
      [
        {
  				"url": "export/sqlite/",
  				"file": "databases/data.db"
  			},
  			{
  				"url": "export/unity_polygons/",
  				"file": "unities.wkt"
  			},
        {
          "url": "data_download/organisme_02/settings_fauna.json/",
          "file": "settings_fauna.json"
        },
        {
          "url": "data_download/organisme_02/settings_mortality.json/",
          "file": "settings_mortality.json"
        },
        {
          "url": "data_download/organisme_02/settings_invertebrate.json/",
          "file": "settings_invertebrate.json"
        },
        {
          "url": "data_download/organisme_02/settings_flora.json/",
          "file": "settings_flora.json"
        },
        {
          "url": "data_download/organisme_02/settings_search.json/",
          "file": "settings_search.json"
        }
      ]
    }
  }
  ```

* `settings_*.json` : fichiers de configuration par application de saisie

  ```json
  {
    "qualification": {
      "organism": 3,
      "protocol": 1,
      "lot": 4
    }
  }
  ```

### Principe de fonctionnement

Une fois le module *WebAPI* et l'application de synchronisation correctement
paramétrés, l'application de synchronisation va mettre à jour les fichiers de
configuration des différentes applications de saisie qui contiendra le
paramétrage pour la gestion multi-organismes.
Lorsqu'une saisie est terminée et prête à être synchronisée (soit directement
via le terminal ou via l'application de synchronisation), celle-ci est
complétée automatiquement pour y inclure la configuration correspondant à
l'organisme issue du fichier de paramétrage. Par exemple :

```json
{
  "qualification": {
    "organism": 3,
    "protocol": 1,
    "lot": 4
  }
}
```

Lors de la synchronisation, les données de saisie contient donc à la fois la
saisie en elle même mais aussi la configuration concernant l'organisme en
question à utiliser par le module WebAPI. Si cette configuration n'est pas
présente, le module WebAPI utilise sa configuration par défaut issue de
`settings_local.py`.

**Note :** Il faut lancer au moins une première fois la synchronisation via
l'application de synchronisation pour que le paramétrage concernant l'organisme
soit bien présent coté application de saisie.
