############
Écrins Faune
############

L'application Web de visualisation développée par Les Écrins. (Login: admin/admin, 
`<http://dev.ecrins-parcnational.fr/faune/synthese>`_).

Challenges
==========

* Tuiles embarquées sur SD en projection 2154
* Architecture Javascript : Intégration Offline Storage ~ MVC ~ Forms ~ Carto
* Synchro sans connexion Web ? (fichiers avec MTP ? Bluetooth? tethering ?)
* Rotation de la carte JS

.. warning ::

    Ne pas polluer pas le projet avec la synchronisation sans Web. 

Principes
=========

* Tuiles sur support SD
* Téléchargement données Geo/JSON
* Backend en charge de la préparation des données et récupèration des ajouts
* Synchronisation par cable : transfert de fichier(s).

Questions
=========

* Modification des éléments saisis ?
* Suppression des éléments saisis ?
* Consultations de l'historique ?

Technologies
============


Backoffice
----------

Django

    +++ : admin site pas cher
          édition de geometries
          gestion manifest offline (c.f. Gr@ce)
    --- : projet python à déployer


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
          ne gère pas la rotation

OpenLayers

    +++ : client SIG ultra complet
    --- : très lourd
          rotation ?

Modestmaps ?

Proofs-of-concept
=================

Objectif : 

    Cloisonner une problématique, un challenge, dans un exemple simple afin de valider
    les choix technologiques.
    
    Le livrable doit être : un exemple simple qui marche (HTML statique, script, etc.),
    et accompagné éventuellement d'un article de blog.
    
    Le code n'a pas forcément vocation à être réutilisé tel quel.


Offline-storage
---------------

Définir un modèle simple : 

Animal {
  specie: TEXT /* A-Za-z */, 
  size: INT  /* < 400 cm */,
  sexe: ENUM('male', 'female', 'young')
}

Développer un formulaire pour créer/éditer les instances stockées en offline, avec 
de la validation sur les champs (HTML5 regex + validation métier).

Squelette MVC
-------------

Navigation entre écrans (workflows contraints), état des boutons en fonction de l'interaction (machines à état),
rafraichissement bidirectionnel, gestion du routing, et intégration avec offline.

Problèmes implémentés quasi-manuellement dans Gr@ce. Tenter de profiter d'un framework pour :

- Afficher une page A avec un champ de saisie.
- Saisir une valeur ajoute un élement dans une liste.
- Activer le bouton d'ajout que si la liste contient moins de 10 éléments.
- Accéder à la page B en cliquant sur un élement de la liste.
- Empêcher d'accéder à la page B directement.
- La page B contient un formulaire d'édition, en revenant à la page A, le titre de l'objet a
  été raffraichit.


Tuiles en Lambert (2154)
------------------------

Les tuiles (SlippyMap_) s'appliquent à la projection EPSG:3857 et chaque tuile est
orthogonale, et référencée par (zoom, x, y). Stockées dans un fichier MBTiles ou sur
disque "z/x/y.jpg".

Voir comment sont référencées les tuiles d'un WMS-C en EPSG:2154 (bbox?) et trouver 
un moyen simple de les stocker sur disque/sqlite.


Leaflet Lambert (2154)
----------------------

Leaflet supporte les projections, tester son comportement avec 2154 pour la 
saisie de géométries (leaflet version 0.4), la superposition avec des WMS etc.


Support SD
----------

* Tester la lecture sur support SD avec Phonegap
* Tester l'écriture de fichiers JSON sur le support (utile si synchronisation avec MTP)

Resources:

* http://stackoverflow.com/questions/6967696/writing-and-reading-file-in-phonegap


Transferts MTP
--------------

Petite application (Qt?) qui détecte la connection MTP et accède aux fichiers sur la partition.
