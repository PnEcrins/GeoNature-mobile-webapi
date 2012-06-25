############
Écrins Faune
############


Intérêts de l'application mobile :

* appliquer un protocole de saisie qui a pour objectif de remplir les lacunes
  de saisie sur certaines zones. Notamment pour faire la différence entre : il n'y 
  a pas telle espèce dans cette zone, et il n'y a pas eu de relevé dans cette
  zone.

* voir le résultat immédiatement lors de la synchro (dans chaîne papier actuelle, 
  il faut attendre la saisie pendant des semaines)


==========
Ressources
==========

L'application Web de visualisation développée par Les Écrins. (Login: admin/admin, 
`<http://dev.ecrins-parcnational.fr/faune/synthese>`_).

Challenges
==========

* Tuiles embarquées sur SD en projection 2154
* Architecture Javascript : Intégration Offline Storage ~ MVC ~ Workflows ~ Forms ~ Carto
* Synchro MTP + sans fil
* Mise à jour applicative

Principes
=========

* Tuiles sur support SD (éclatées sur disque)

* Téléchargement données (Geo)JSON
  * GeoJSON pour les zones du parcs
  * JSON pour les taxons
  * JSON pour les observateurs
  * JSON pour les taxons et les associations taxons zones
* Chaque donnée est versionnée
* En synchro sans fil, l'application remplit un sqlite local avec les données téléchargées.
* En synchro desktop, l'application créé des sqlite et écrase ceux du mobile 

* Backend en charge de la préparation des données et des ajouts dans la base

Quid de la mise à jour applicative ?

Informations
============

* Environ 1000 taxons
* 300 unités géographiques
* 100 à 300 taxons par unité géographique
* Potentiellement 300x300=100k associations taxon-unité
* Un association taxon-unité = id_tax, id_geo, nombre, couleur, infos


Pour une saisie, on sélectionne les observateurs présents.

Pour chaque contact avec un taxon, on renseigne le dénombrement pour chaque critère.


         Saisie n-------n Observateurs
           1
           |
           n
         Contact 1-------n
           n           Valeur
           |             n----------1
           1
         Taxon                   Critere
           n                        
           |                        
           |                        
           +------1 Groupe

Données
=======

c.f. document `infos_serveur.odt`

Questions
=========

Technologies
============

Backoffice
----------

PHP imposé.

En charge de :
* Préparer les fichiers à utiliser en offline
* Récupérer les saisies et les insérer dans la base

* Serveur public avec https
* Requêtes GET pour obtenir les versions des données
* Requêtes GET pour obtenir les données
* Requêtes POST pour poster les saisies


Mobile
------

HTML5

    +++ : (presque) universel
          local storage
    --- : complexe

Phonegap

    +++ : accès périphériques
    --- : .

JQueryMobile

    +++ : familier
    --- : raffraichissement des widgets suite au changement dans le DOM.


Offline Storage
---------------

* Phonegap-sqlite ? 
* persistence.js ?


MVC Forms
---------

- Modèles métier
- Validation de champs
- Formulaires liés à des instances

* Backbone.js ?
* Ember.js ?
* PureMVC ?


Cartographie
------------

Leaflet

    +++ : léger
          simple à étendre
    --- : une seule projection par carte

OpenLayers

    +++ : client SIG ultra complet
    --- : très lourd

Modestmaps ?

    --- : une seule couche
    +++ : simple

Synchronisation
---------------

* client riche (Qt ?) pour assurer la synchronisation via MTP
    +++ :   permet une synchronisation locale hors connexion
    --- :   développement spécifique par plateforme (Windows dans un premier temps)
            complexe ?
* mise en place d'un cloud pour assurer la synchronisation (voir et étudier http://code.google.com/p/openmobster/)
    +++ :   solution générique et extensible
    --- :   accès à un réseau (wifi) pour assurer la connexion avec le serveur
