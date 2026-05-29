# Ynov-Ydays-Forensic
Projet de fin d'année Ydays Ynov campus. Projet Forensic -- BAHLOULI FLORIAN &amp; COMTE SUPREET


ClimIT est une plateforme pédagogique IoT et cybersécurité construite autour d’une entreprise fictive spécialisée dans le suivi de température de bâtiments. Le projet simule une vraie chaîne de collecte de données : des capteurs publient des mesures, celles-ci sont traitées, stockées, exposées via une API, puis affichées dans une interface web.

L’objectif du projet est double :
- montrer une architecture IoT complète de bout en bout ;
- servir de support à des scénarios de cybersécurité, d’investigation et de réponse à incident.

## Aperçu du projet

ClimIT repose sur plusieurs services conteneurisés orchestrés avec Docker Compose, une approche adaptée aux projets multi-services et reproductibles.

### Services principaux

- **Mosquitto** : broker MQTT pour la remontée des mesures. 
- **Node-RED** : traitement des messages entrants et insertion en base. 
- **PostgreSQL** : stockage structuré des clients, sites, capteurs et mesures. 
- **API Flask** : exposition des données de mesures en JSON. 
- **Simulateur Python** : génération automatique de données de capteurs. 
- **Nginx / Front web** : interface de visualisation et futur portail admin/client. 
- **Portainer** : supervision des conteneurs.

## Architecture

```text
Capteur simulé
   ↓
MQTT / Mosquitto
   ↓
Node-RED
   ↓
PostgreSQL
   ↓
API Flask
   ↓
Front web / Nginx
```

Cette architecture permet de visualiser toute la chaîne métier, depuis l’émission d’une mesure jusqu’à son affichage dans un portail web. 

## Cas d’usage

ClimIT peut être utilisé pour :

- apprendre le fonctionnement d’une architecture IoT complète ; 
- manipuler une stack multi-services avec Docker Compose ; 
- créer des dashboards à partir de données réelles ou simulées ;
- construire des scénarios pédagogiques en cybersécurité et forensic. 

## Fonctionnalités actuelles

- Déploiement complet sur VM Debian avec Docker Compose.
- Collecte de mesures de température via MQTT.
- Traitement automatique des messages dans Node-RED. 
- Insertion des données dans PostgreSQL. 
- Consultation des mesures via une API REST Flask. 
- Simulateur de capteur conteneurisé. 
- Serveur web Nginx pour le front, portail web avec authentification. 

## Roadmap

Les prochaines évolutions prévues sont :

- dashboards multi-capteurs et multi-sites ; 
- reverse proxy unifié front + API ;
- scénarios de forensic plus avancés ; 
- centralisation des logs.

## Structure du projet

Exemple de structure attendue :

```text
climit/
├── api/
│   ├── climit_api.py
│   └── requirements.txt
├── mosquitto/
│   ├── mosquitto.conf
│   ├── data/
│   └── log/
├── node-red/
│   └── data/
├── postgres/
│   ├── data/
│   └── initdb/
│       └── 01_schema.sql
├── simulator/
│   └── simulator.py
├── web/
│   └── index.html
└── docker-compose.yml
```

## Pour Ajouter un Portainer si besoin 

---

docker volume create portainer_data

docker run -d \
  -p 8000:8000 -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest

---

## Prérequis

Avant de commencer, il faut disposer de :

- Docker ;
- Docker Compose ;
- une machine Linux ou une VM Debian recommandée pour héberger les conteneurs plus simplement.

## Lancement rapide

1. Cloner le dépôt :

```bash
git clone https://github.com/Sha0Night/Ynov-Ydays-Forensic.git
cd TON-REPO
```

2. Vérifier l’arborescence et les fichiers de configuration.

3. Lancer la stack :

```bash
docker compose up -d
```

4. Vérifier les conteneurs :

```bash
docker compose ps
```

5. Consulter les logs si nécessaire :

```bash
docker compose logs -f
```

## Accès aux services

Une fois la stack lancée, les services sont généralement accessibles sur :

- **Front web** : `http://localhost:8080`
- **API Flask** : `http://localhost:5000/api/measurements?sensor_id=1&limit=5`
- **Node-RED** : `http://localhost:1880`
- **PostgreSQL** : port `5432`
- **Mosquitto** : port `1883`

S'il y a :
- **Portainer** : `http://localhost:9443`

Ces points d’accès correspondent à la stack mise en place et testée au cours du projet.

## Exemple d’utilisation de l’API

Récupérer les 5 dernières mesures du capteur 1 :

```bash
curl "http://localhost:5000/api/measurements?sensor_id=1&limit=5"
```

Exemple de réponse :

```json
[
  {
    "id": 171,
    "measured_at": "2026-05-10T14:18:50+00:00",
    "sensor_id": 1,
    "value_celsius": 24.93
  }
]
```

Ce type de réponse a été validé pendant les tests fonctionnels du projet. 

## Partie cybersécurité

ClimIT n’est pas seulement une plateforme IoT : c’est aussi un support pédagogique pour l’analyse d’incident. 

Exemples de scénarios travaillés :

- vol d’identifiants MQTT ; 
- injection de fausses mesures ; 
- modification de données ; 
- compromission du portail client ; 
- reconstruction du chemin d’attaque ; 

L’idée est de permettre aux étudiants de rejouer une enquête complète, de comprendre l’impact d’une attaque et de proposer des mesures de protection adaptées. 

## Valeur pédagogique

Le projet a été pensé comme une base réutilisable pour des démonstrations, des TP ou des exercices de forensic. Il ne s’agit pas seulement d’un prototype, mais d’un environnement cohérent qui peut évoluer vers une vraie plateforme de formation. 

## Auteurs

Projet conçu dans le cadre des YDAYS 2026.

Créateurs du projet et du scénario :
- **Florian Bahlouli**
- **Supreet Comte** 


## Licence

```
Florian BAHLOULI & Supreet COMTE
Tous droits réservés
```