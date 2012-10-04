

*Faune recette*

========
Sprint 2
========

#15 Définir l'observateur par défaut dans les settings de l'application
-----------------------------------------------------------------------

Lancer l'application mobile, et aller dans les paramètres (depuis le menu Android)
Cliquer sur "Ajouter un observateur" ou "Observateur par défaut" pour sélectionner un observateur
La vue listant les observateurs s'affiche par ordre alphabétique avec la barre de recherche en haut
Sélectionner un observateur depuis la liste
La sélection d'un observateur entraîne la désélection de l'observateur sélectionné préalablement
Cliquer sur bouton "Valider" pour quitter la vue des observateurs
La vue des paramètres se met à jour et indique l'observateur sélectionné comme observateur par défaut

#22 Afficher / masquer les unités sur la carte
----------------------------------------------

Lancer l'application et commencer la saisie en cliquant sur le bouton "Input"
Sélectionner au moins un observateur pour passer à la vue suivante (carte)
La vue carte s'affiche et présente une barre d'action comportant un bouton permettant d'afficher ou non les unités géographiques
Cliquer sur ce bouton pour afficher les unités géographiques
Le bouton devient inactif le temps de charger les unités géographiques et de les afficher sur la carte
Cliquer une nouvelle fois sur ce bouton pour masquer les unités géographiques

#24 [Carto] Le fond : relief >scan250>scan100>scan25.... est déterminé automatiquement en fonction du niveau de zoom
--------------------------------------------------------------------------------------------------------------------

Lancer l'application sur le mobile et aller sur la cartographie. Zoomer sur la carte jusqu'à provoquer le basculement sur
un autre fond de plan. Dézoomer, et constater que la carte revient sur le fond de plan précédent.

#25 [Carto] Forcer le fond ortho ou scan manuellement
-----------------------------------------------------

Le passage d'un fond à l'autre est automatique entre les niveaux de zoom mais pour les derniers niveaux de zoom, il est possible de forcer l'ortho.
Lancer l'application sur le mobile et aller sur la cartograhie. Zoomer sur la carte jusqu'à provoquer le basculement sur un autre fond de plan. 
Changer alors manuellement le fond de plan et constater que le changement s'affectue bien.

#50 Affichage des unités géographiques par défaut
-------------------------------------------------

Lancer l'application mobile, et aller dans les paramètres (depuis le menu Android)
Cocher "Afficher les unités géographiques"
Quitter les paramètres via le bouton "Back" du terminal
Commencer la saisie en cliquant sur le bouton "Input"
Sélectionner au moins un observateur pour passer à la vue suivante (carte)
La vue carte s'affiche en présentant aussi les unités géographiques
Quitter la saisie en cliquant sur le bouton "Annuler" et confirmer ce choix
Retourner dans les paramètres et désactiver "Afficher les unités géographiques"
Commencer la saisie en cliquant sur le bouton "Input"
Sélectionner au moins un observateur pour passer à la vue suivante (carte)
La vue carte s'affiche sans présenter les unités géographiques

#54 Breadcrumbs saisie
----------------------

Lancer l'application et commencer la saisie en cliquant sur le bouton "Input"
En haut de chaque vue, on peut voir l'affichage des puces indiquant sur quelle page on se trouve
En cliquant sur les boutons "Suivant" ou "Précédent" pour changer de page, l'affichage des puces se met à jour en mettant en surveillance la puce correspondant à la page courante

#59 mise en place de la recherche dans la liste des observateurs
----------------------------------------------------------------

Lancer l'application et commencer la saisie en cliquant sur le bouton "Input"
Cliquer sur l'observateur par défaut ou sur le libellé "Select an observer"
La vue listant les observateurs s'affiche par ordre alphabétique avec la barre de recherche en haut
Cliquer sur le champ de recherche, le clavier virtuel apparaît pour la saisie
Commencer à faire une recherche en tapant au moins trois caractères
L'application offre une suggestion de recherche à partir du troisième caractère saisi et liste au maximum cinq propositions en bas de la barre de recherche
Cliquer sur une des proposition
Le champ de recherche est automatiquement renseigné par la proposition sélectionnée, la liste des suggestions disparaît et la liste des observateurs se met à jour en tenant compte de la recherche effectuée
Cliquer sur le bouton ayant une croix comme icône situé à droite du champ de recherche
La barre de recherche disparaît et on retrouve la barre d'icônes. La liste des observateurs se remet à jour en supprimant la recherche effectuée préalablement
Commencer une nouvelle recherche en tapant au moins trois caractères puis cliquer directement sur le bouton de recherche du clavier virtuel
La liste des suggestions disparaît et la liste des observateurs se met à jour en tenant compte de la recherche effectuée

#70 Module de recherche dans la vue des taxons
----------------------------------------------

Lancer l'application et commencer la saisie en cliquant sur le bouton "Input"
Sélectionner au moins un observateur pour passer à la vue suivante (carte)
Passer à la vue suivante pour arriver à la liste des taxons
Par défaut l'application affiche les dix premiers taxons par ordre alphabétique
Cliquer sur le bouton ayant une loupe comme icône
La barre de recherche apparaît par dessus la barre d'icônes
Cliquer sur le champ de recherche, le clavier virtuel apparaît pour la saisie
Commencer à faire une recherche en tapant au moins trois caractères
L'application offre une suggestion de recherche à partir du troisième caractère saisi et liste au maximum cinq propositions en bas de la barre de recherche
Cliquer sur une des proposition
Le champ de recherche est automatiquement renseigné par la proposition sélectionnée, la liste des suggestions disparaît et la liste des taxons se met à jour en tenant compte de la recherche effectuée
Cliquer sur le bouton ayant une croix comme icône situé à droite du champ de recherche
La barre de recherche disparaît et on retrouve la barre d'icônes. La liste des taxons se remet à jour en supprimant la recherche effectuée préalablement
Cliquer de nouveau sur le bouton ayant une loupe comme icône
Commencer à faire une recherche en tapant au moins trois caractères puis cliquer directement sur le bouton de recherche du clavier virtuel
La liste des suggestions disparaît et la liste des taxons se met à jour en tenant compte de la recherche effectuée

#73 Api leaflet/titanium
------------------------
Lancer l'application et constater que la cartographie répond bien aux actions de l'utilisateur.

#74 [Carto] Gros boutons de zoom
--------------------------------

Lancer l'application sur le mobile et aller sur la cartographie. Constater que les boutons de zoom sont suffisament grands pour une utilisation fluide.

#75 WebApi
----------

Lancer l'application de synchro et constater que l'application mobile et la base de données se synchronise bien.
Pour tester manuellement la webapi, les URL à utiliser sont les suivantes :
 * http://server/export/taxon/
 * http://server/export/family/
 * http://server/export/unity/
 * http://server/export/taxon_unity/
 * http://server/export/criterion/
 * http://server/export/user/
 * http://server/export/classes/
 * http://server/export/unity_geojson/
 * http://server/export/sqlite/

A noter que ces URL doivent être appelée en passant un paramètre POST (token).
Pour l'import :
 * http://server/import/
 A noter que cette URL doit être appelée en passant 2 paramètres POST (token, et data au format json)

#76 Sélection de un ou plusieurs observateurs lors de la saisie
---------------------------------------------------------------

Lancer l'application et commencer la saisie en cliquant sur le bouton "Input"
La première vue affiche l'observateur par défaut tel que défini dans les paramètres de l'application
Cliquer sur l'observateur par défaut pour afficher la liste des observateurs disponibles
La liste des observateurs s'affiche avec l'observateur par défaut déjà sélectionné
La sélection d'un autre observateur n'entraîne pas la désélection de l'observateur sélectionné préalablement
Le bouton "Valider" se met à jour en indiquant le nombre d'observateur sélectionnés en tout
Cliquer sur le bouton "Valider" pour terminer la sélection et revenir à la vue précédente
La première vue de la saisie se met à jour en listant les observateurs sélectionnés pour cette saisie

#95 Génération de la base de données SQLite de l'application mobile
-------------------------------------------------------------------

Lancer l'application de synchro (en mode export de données). Vérifier que le fichier data.db est bien généré, et compatible avec l'application mobile.
Pour tester de manière manuelle l'export du fichier sqlite, appeler un navigateur et appeler l'url suivante :

 * http://server/export/sqlite/

 (A noter qu'un paramètre POST token doit être fourni)
 Constatez que la réponse est bien un fichier à télécharger de type sqlite.




