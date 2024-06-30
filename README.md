# YouTube Data Pipeline

Ce projet est un pipeline de données qui récupère des informations sur des chaînes YouTube spécifiques et leurs dernières vidéos, puis les stocke dans une base de données PostgreSQL.

## Table des matières

1. [Prérequis](#prérequis)
2. [Configuration](#configuration)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Structure du projet](#structure-du-projet)
6. [Tester les services](#tester-les-services)
7. [Dépannage](#dépannage)

## Prérequis

- Docker et Docker Compose
- Clé API YouTube (obtenue depuis la Google Developers Console)

## Configuration

1. Clonez ce dépôt sur votre machine locale :
   ```
   git clone <url-du-repo>
   cd <nom-du-repo>
   ```

2. Créez un fichier `.env` à la racine du projet et ajoutez votre clé API YouTube :
   ```
   YOUTUBE_API_KEY=votre_clé_api_youtube
   ```

## Installation

1. Construisez les images Docker :
   ```
   docker-compose build
   ```

2. Lancez les services :
   ```
   docker-compose up -d
   ```

## Utilisation

Le pipeline est configuré pour s'exécuter automatiquement :
- La tâche de récupération des données s'exécute tous les jours à 18h00.
- La tâche de traitement des données s'exécute tous les jours à 18h30.

Vous pouvez également exécuter les tâches manuellement :

1. Pour la récupération des données :
   ```
   docker-compose run youtube-data-retrieval python main.py
   ```

2. Pour le traitement des données :
   ```
   docker-compose run youtube-data-processing python main.py
   ```

## Structure du projet

- `youtube-data-retrieval/`: Service de récupération des données YouTube
- `youtube-data-processing/`: Service de traitement et d'insertion des données dans la base de données
- `local_storage/`: Dossier partagé pour stocker les fichiers CSV temporaires
- `init.sql`: Script d'initialisation de la base de données
- `docker-compose.yml`: Configuration des services Docker
- `celery_config.py`: Configuration de Celery pour la planification des tâches

## Tester les services

1. Vérifiez que tous les services sont en cours d'exécution :
   ```
   docker-compose ps
   ```

2. Consultez les logs des services :
   ```
   docker-compose logs youtube-data-retrieval
   docker-compose logs youtube-data-processing
   ```

3. Vérifiez les fichiers CSV générés dans le dossier `local_storage/`.

4. Connectez-vous à la base de données PostgreSQL pour vérifier les données insérées :
   ```
   docker-compose exec db psql -U postgres -d youtube_data
   ```
   Puis exécutez des requêtes SQL, par exemple :
   ```sql
   SELECT * FROM channel;
   SELECT * FROM video;
   SELECT * FROM import_task;
   ```

## Dépannage

- Si vous rencontrez des problèmes avec les permissions des fichiers, assurez-vous que les dossiers partagés ont les bonnes permissions :
  ```
  chmod -R 777 local_storage/
  ```

- En cas d'erreur liée à l'API YouTube, vérifiez que votre clé API est correcte et n'a pas atteint ses limites d'utilisation.

- Pour réinitialiser complètement le pipeline, vous pouvez supprimer tous les conteneurs et volumes, puis reconstruire :
  ```
  docker-compose down -v
  docker-compose up -d --build
  ```

Pour toute autre question ou problème, n'hésitez pas à ouvrir une issue dans le dépôt du projet.