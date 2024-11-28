# Parcours à la carte

---

# Table des matières

- [À propos](#à-propos)
- [Pré-requis](#pré-requis)
- [Application web](#application-web)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [Analyse statistique : pondération du réseau piéton](#analyse-statistique--pondération-du-réseau-piéton)


# 🚀 Démarrage rapide

copier le fichier **.env.example** et le renommer en **.env** à la racine du projet. 
```bash
cp .env.example .env
```

télécharger les data de opendata lyon
```bash
cd score_calculation_it/input_data
pip i geopandas owslib
python fetch_data.py
# Selectionner l'option WEB_ONLY
```

télécharger le réseau final pré-calculé
```bash
mkdir -p score_calculation_it/output_data/network/graph
cd score_calculation_it/output_data/network/graph
wget https://endpoint-minio.projets.erasme.org/fichiers-publics/data_sortons_au_frais/final_network_P0_01O5At0_01Ar10C0_01E5Ca.gpkg
```

lancer le backend et le frontend
```bash
docker-compose up
```

Le frontend est accessible à l'adresse [http://localhost:3000](http://localhost:3000)
Le backend est accessible à l'adresse [http://localhost:3002](http://localhost:3002)



# À propos

Le projet Sortons au frais est un projet mené par Erasme (laboratoire d'innovation de la Métropole de Lyon), le service Données Métropolitaines et le service Géomatique de la Métropole de Lyon. Ce projet a été réalisé en partenariat avec les services Géomatiques d'une quinzaine de communes de la métropole de Lyon dans le cadre de la [DatAgora](https://datagora.erasme.org/). 
L'objectif est d'apporter une solution d'adaptation à la canicule en proposant une application avec 3 fonctionnalitées principales : 

- Proposer des itinéraires piétons permettant de se déplacer "au frais", en minimisant la chaleur le long du trajet
- Trouver les lieux "frais" autour de chez soi
- Afficher des éléments utiles en cas de canicule (fontaines, parcs, toilettes etc.)

La totalité du code et de l'analyse statistique a été réalisée dans le cadre d'un stage de master 2 par [Yannis BARBA](https://www.linkedin.com/in/yannis-barba-90b9391bb/) et a donné lieu à un rapport de stage expliquant la démarche suivie pour déterminer la pondération du réseau piéton.
La partie statistique est présente dans le backend de l'application web mais le détail de l'arborescence des scripts est expliqué dans la partie [**Analyse statistique**](#analyse-statistique--pondération-du-réseau-piéton).

Toutes les informations du projet se trouvent sur la page [https://datagora.erasme.org/projets/sortons-au-frais/](https://datagora.erasme.org/projets/sortons-au-frais/)

# Pré-requis et Installation

Le projet a été développé dans un environnement conda, si l'application n'est pas exécutée via les images dockers, il est préférable de créer un environnement conda. Les versions utilisées dans le cadre de ce projet sont les suivantes : 

- **conda** : 23.1.0
- **docker** :  23.0.2
- **docker-compose** : 1.29.2

Une fois le projet téléchargé via github, 
- se placer à la racine du projet et créer un fichier **.env** avec la variable d'environnement
```txt
REACT_APP_URL_SERVER=http://localhost:3002
**REACT_APP_PORT_SERVER**=3002
```
- se placer à la racine du dossier backend et créer un fichier **.env** avec la variable d'environnement : 
```txt
PORT=3000
```
- se placer à la racine du dossier frontend et créer un fichier **.env** avec ces variables d'env : 
```txt
REACT_APP_URL_SERVER=http://172.17.0.2:3002
REACT_APP_PORT_SERVER=3002
```
- télécharger le [réseau final](https://endpoint-minio.projets.erasme.org/fichiers-publics/data_sortons_au_frais/final_network_P0_01O5At0_01Ar10C0_01E5Ca.gpkg) et le placer à cet endroit : *backend/score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca.gpkg* 

- télécharger les données nécessaires au fonctionnement de l'application web en suivant les instructions de la partie [Données utilisables via l'application Web](#données-utilisables-via-lapplication-web) et en choisissant l'option "WEB_ONLY".

## Exécution via Docker

Si besoin,les images docker du frontend et du backend sont disponibles à aux adresses suivantes : 
- backend : https://hub.docker.com/repository/docker/yannisbarba/itineraires_fraicheur_backend/general
- frontend : https://hub.docker.com/repository/docker/yannisbarba/itineraires_fraicheur_frontend/general

Celles-ci peuvent être build en exécutant le fichier **docker-compose.yml**. 
Dans un premier temps, build le backend avec la commande :

```bash
docker-compose build backend
```
 
Vérifier l'adresse sur laquelle le serveur s'exécute (*Running on <adresse-serveur> *), puis modifier si besoin le fichier .env à la racine du frontend et mettre les variales d'environnement suivantes : 

```txt
REACT_APP_URL_SERVER=<adresse-serveur>
REACT_APP_PORT_SERVER=3002
```

lancer alors le build du frontend via 
```bash
docker-compose build frontend
```
lancer l'application via
```bash
docker-compose run
```
se rendre à l'addresse

```txt
http://localhost:3000/
```

## Exécution via conda (conseillé pour le développement)

### Création de l'environnement conda

Une fois conda installé (via anaconda par exemple), se placer à la racine du projet et créer un environnement conda pour le projet via la commande suivante : 

```bash
conda create --name <nom-env>
```
Suivre les indications de créations de l'environnement puis une fois à la racine du projet, activer l'environnement conda : 

```bash
conda activate <nom-env>
```

Puis installer toutes les dépendances avec 

```bash
pip install -r requirements.txt
```

## Exécution du backend
**Se placer à la racine du dossier backend**

Créer un fichier **.env** avec la variable suivante :

```txt
PORT=3000
```

Avant de lancer le backend il est nécessaire de télécharger certaines données nécessaires au bon fonctionnement de l'application, suivre les indications de la partie [Données utilisables via l'application Web](#données-utilisables-via-lapplication-web).

Afin de lancer le backend, se positionner à la racine du dossier backend et exécuter la commande suivante : 

```bash
python app.py
```

## Exécution du frontend
**Se placer à la racine du dossier frontend**
Créer un fichier **.env** avec les variables suivantes: 

```txt
REACT_APP_URL_SERVER=http://localhost:3002
REACT_APP_PORT_SERVER=3002
```

Avant de lancer l'exécution du frontend, il est nécessaire d'installer les dépendances npm via la commande : 

```bash
npm install
```

Afin de lancer le frontend, exécuter la commande suivante : 

```bash
npm start
```



# Application web

## Backend


Toutes les variables globales (les chemins des fichiers, les paramètres spécifiques etc.) sont stockées dans le fichier **global_variable.py** à la racine du dossier backend. Il n'y a pas de base de données pour ce projet car il n'y en avait pas le besoin. Les quelques informations nécessaires au bon fonctionnement du frontend (chemin des layers, chemin des icons etc.) sont également stockés directement dans un dictionnaire python dans le fichier **global_variable.py**.

### LES DONNÉES 
L'ensemble des données utiles pour l'application web (et pour le calcul de score) sont stockées dans le dossier *score_calculation_it/input_data*

On peut distinguer deux types de données : 

- Les [données](#requête-wfs) directement issues d'une requête WFS à l'api de datagrandlyon
- Les données de plus grosse taille et nécessitant des calculs spécifiques

#### Données utilisables via l'application Web

Les données du bruit sont à télécharger sur le site CRAIG via le lien suivant : "https://depot.atmo-aura.fr/orhane/orhane_2023_multibruit.zip", puis il faut mettre le fichier bruit.gpkg dans le dossier bruit (itineraires_multicriteres-dev/backend/score_calculation_it/input_data/bruit/).

Les données issues d'une requête WFS à datagrandlyon peuvent être téléchargées directement en exécutant le script **fetch_data.py** situé dans le dossier *score_calculation_it/input_data/*. Il est possible de télécharger une donnée en particulier ou toutes les données d'un coup.  Afin de lancer le téléchargement, exécuter le script dans un terminal **en se plaçant au niveau du script** puis lancer la commande suivante : 

```bash
python fetch_data.py
```
Puis se laisser guider par les indications dans le terminal.

À chaque fois qu'une donnée est téléchargée, un dossier se créé avec la donnée sous format geojson (pour l'affichage sur la web app) et sous format gpkg (pour l'ensemble des calculs). 

### L'API
Le script python principal du backend est le fichier **app.py** qui constitue le *endpoint* du backend permettant d'exécuter les différentes requêtes utilisateur. Avant le lancement de l'application, vérifier que le chemin du graph est celui souhaité dans le fichier **global_variable.py**.

Il y a seulement deux routes:
- requête des layers
- requête pour le calcul d'itinéraire

Les endpoints se servent de fonction présentes dans le dossier *models* avec un fichier correspondant à chaque route.
Les données distribuées pour l'application web sont celles stockées dans le dossier *score_calculation_it/input_data/* (cf [partie](#les-données))


## Frontend
Le frontend est conçu en React et react-leaflet pour ce qui est de la cartographie. Il est conçu pour être une unique page intégrable dans un site web. 
Le dossier src contient l'ensemble des scripts avec des composants et un context (permettant la circulation des variables entre les différents composants).

NB : le fetch des données *Lieux frais ouverts au public* se fait via une URL temporaire suite à changement de conception côté datagrandlyon. Si modification d'URL il y a, ce changement s'effectue dans le fichier **mainContext.js** Ligne 141.

# Pondération du réseau piéton et analyse statistique

## Pre-processing
Afin de pouvoir réaliser le calcul de la pondération, il est nécessaire de faire un pre-processing. Si les données sont amenées à être mise à jour, chaque script peut être exécutable pour relancer les calculs spécifiques à chaque donnée. En sortie de chaque script on obtient un sous-réseau enregistré dans un fichier **edges_nom_données.gpkg** qui nous permet d'avoir le taux de recouvrement ou la présence d'une donnée sur chaque segments. Ce sont tous ces fichiers qui sont ensuite utilisés pour les calculs de score. Ces sous-réseaux suffisent pour le [calcul de score](#pondération-du-graph-calcul-du-score).

Tous ces sous-réseaux sont directements disponibles dans le dossier à cette [adresse](https://minio.projets.erasme.org/browser/fichiers-publics/ZGF0YV9zb3J0b25zX2F1X2ZyYWlzL2VkZ2VzLw==). Placer chaque réseau à l'emplacement suivant : *./score_calculation_it/output_data/network/edges/*.

Ils correpondent à une version des données de l'été 2023. Toutefois, si l'on souhaite recalculer une ou toutes les données, suivre les instructions pour chaque données.

### Le réseau de la métropole
Cette donnée est indispensable pour la suite (à télécharger en premier lieu donc). Afin de la mettre à jour, exécuter le fichier 
**fetch_network.py** à partir de *./score_calculation_it/input_data/* et se laisser guider par les instructions du terminal.

```bash
python fetch_network.py
```

## Itinéraire pollen
Le graphe pollen est calculé via différentes données d'arbres ainsi que les données des parcs. 

### Arbres

Les calculs nécessaire pour ce graphe peuvent être exécuté via le fichier **arbres_preprocessing.py** et en se laissant guider par les instructions du terminal.

```bash
python arbres_preprocessing.py
```

### Parcs

Les calculs nécessaire pour ce graphe peuvent être exécuté via le fichier **parcs_preprocessing.py** et en se laissant guider par les instructions du terminal.

```bash
python parcs_preprocessing.py
```

## Itinéraire bruit

Les calculs nécessaire pour ce graphe peuvent être exécuté via le fichier **bruit_preprocessing.py** et en se laissant guider par les instructions du terminal.

```bash
python bruit_preprocessing.py
```

## Itinéraire touristique

Les calculs nécessaire pour ce graphe peuvent être exécuté via le fichier **tourisme_preprocessing.py** et en se laissant guider par les instructions du terminal.

```bash
python tourisme_preprocessing.py
```

## Itinéraire frais

### Parcs et Jardins pour l'itinéraire frais
Les parcs ont un traitement un peu différents des autres POI, par conséquent, les calculs nécessaire pour le calculateur d'itinéraire peuvent être exécuté via le fichier **parcs_jardins_preprocessing.py** et en se laissant guider par les instructions du terminal.

```bash
python parcs_jardins_preprocessing.py
```

### Eaux

Les cours d'eau ont un traitement un peu différents des autres POI, par conséquent, les calculs nécessaire pour le calculateur d'itinéraire peuvent être exécuté via le fichier **eaux_preprocessing.py** et en se laissant guider par les instructions du terminal.

```bash
python eaux_preprocessing.py
```

### La végétation
La donnée de végétation stratifiée la donnée la plus volumineuse. Il est possible de la recalculer de A à Z en partant de la donnée brute présente à [cette addresse](https://data.grandlyon.com/portail/fr/jeux-de-donnees/vegetation-stratifiee-2018-metropole-lyon/telechargements). Afin de pouvoir l'utiliser dans le cadre de ce projet, des calculs ont été réalisés avec Qgis.
- Réduire la résolution du raster (de 1m à 5m). 
- Vectoriser le raster
- réduire le nombre de classes (de 5 à 3). Les nouvelles classes sont : 
    - arbres (>1.5m)
    - arbustes (<1.5m)
    - prairies (anciennement herbacées)
Les temps de calculs sont relativement longs et demandent une RAM assez importante (> 16G).
Sauvegarder le résultat sous format Geopackage (gpkg). 

Sinon, la donnée déjà calculée est présente à [cette adresse](https://endpoint-minio.projets.erasme.org/fichiers-publics/data_sortons_au_frais/raw_veget_strat.gpkg)
Une fois téléchargée, la donné de végétation doit être sauvegardée ici : *"./score_calculation_it/input_data/vegetation/raw_veget_strat.gpkg"*
Cette donnée étant encore trop volumineuse pour être manipulée aisément dans le cadre du projet, elle a été "clippé" avec la version bufferisée du réseau OSM. Le calcul étant long (24h !) avec une configuration standard, la version déjà calculée en date du 03.07.23 est présente [ici](https://endpoint-minio.projets.erasme.org/fichiers-publics/data_sortons_au_frais/clipped_veget_12.gpkg).
Pour mettre à jour cette donnée, exécuter le script **vegetation_preprocessing.py**. en se plaçant ici *./score_calculation_it/* et se laisser guider par les indications du terminal.

```bash
python vegetation_preprocessing.py
```

### La température

La donnée de température est également une donnée demandant des pré-calculs spécifiques. Le tutoriel pour recalculer cette donnée est disponible [ici](https://endpoint-minio.projets.erasme.org/fichiers-publics/data_sortons_au_frais/Mise_a_jour_donnees_temp_surface.pdf).
La donnée déjà calculée est disponible à [cette adresse](https://endpoint-minio.projets.erasme.org/fichiers-publics/data_sortons_au_frais/temperature_surface.gpkg). Une fois téléchargée, elle doit être sauvegardée ici : *"./score_calculation_it/input_data/temperature/temperature_surface.gpkg"*.
Pour relancer le calcul de la température moyenne par segment, exécuter le script **temperature_preprocessing.py**en se plaçant ici *./score_calculation_it/* et suivre les indications du terminal.

```bash
python temperature_preprocessing.py
```
### L'ombre des bâtiments
La donnée bâtiments est une donnée requêtable en WFS en suivant les instructions de la partie [requete WFS](#requête-wfs). Cependant, c'est la donnée d'ombre calculée à partir de la hauteur des bâtiments qui est utilisée dans le calculateur d'itinéraires. Tous les résultats des calculs intermédiaires pour les ombres sont disponibles [ici](https://minio.projets.erasme.org/browser/fichiers-publics/ZGF0YV9zb3J0b25zX2F1X2ZyYWlzL29tYnJlcy8=), ils sont à placer dans le dossier *score_calculation_it/output_data/ombres/*
Le calcul est exécutable en se plaçant ici : *./score_calculation_it/* et en exécutant le fichier **ombre_preprocessing.py** et en se laissant guider par le terminal. 

```bash
python ombre_preprocessing.py
```
Tel que le script est conçu aujourd'hui, il n'est utile de mettre à jour la donnée que si la donnée des bâtiments ou le réseau piéton est mise à jour. Le script n'est pas conçu pour choisir l'horaire et la date à laquelle faire le calcul. Cependant, ce script peut être assez facilement généralisé. 

## Pondération des graph (calcul du score)
La pondération de chaque graph ne peut se faire que si l'ensemble des sous-réseaux associés existent (et ont été mis à jour au besoin). La pondération de chaque graph est à renseigner directement au début des fichiers **score_calculation[_...].py** en suivant l'exemple *final_params* puis peuvent être exécutés via les commandes suivantes : 

```bash
python score_calculation.py
```

```bash
python score_calculation_pollen.py
```

```bash
python score_calculation_bruit.py
```

```bash
python score_calculation_tourisme.py
```


## Les POIs
Actuellement les points d'interêts (POI) ne sont pas pris en compte dans la pondération du graphe, cependant, il existe un fichier **poi_preprocessing.py** permettant de calculer la présence de POI sur les segments. Les résultats pourraient être utilisés dans le cadre d'une amélioration du calculateur d'itinéraire. 
Afin de lancer les calculs, se placer ici : *./score_calculation_it/* puis exécuter le fichier et se laisser guider par les instructions du temrinal. 

```bash
python poi_preprocessing.py
```
