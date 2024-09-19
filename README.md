# YouTube Data Pipeline

This project is a data pipeline that retrieves information about specific YouTube channels and their latest videos, then stores them in a PostgreSQL database.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Configuration](#configuration)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Testing the Services](#testing-the-services)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker and Docker Compose
- YouTube API Key (obtained from the Google Developers Console)

## Configuration

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/devvv1337/cloud_project.git
   cd cloud_project
   ```

2. Create a `.env` file at the root of the project and add your YouTube API key and database credentials:
   ```env
   YOUTUBE_API_KEY=your_youtube_api_key
   DB_PASSWORD=123
   DB_USER=postgres
   DB_NAME=postgres
   DB_HOST=localhost
   ```

## Installation

1. Build the Docker images:
   ```bash
   docker-compose build
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

## Usage

The pipeline is configured to run automatically:
- The data retrieval task runs daily at 6:00 PM.
- The data processing task runs daily at 6:30 PM.

You can also run the tasks manually:

1. For data retrieval:
   ```bash
   docker-compose run youtube-data-retrieval python main.py
   ```

2. For data processing:
   ```bash
   docker-compose run youtube-data-processing python main.py
   ```

## Project Structure

- `youtube-data-retrieval/`: YouTube data retrieval service
- `youtube-data-processing/`: Data processing and insertion service into the database
- `local_storage/`: Shared folder for storing temporary CSV files
- `init.sql`: Database initialization script
- `docker-compose.yml`: Docker services configuration
- `celery_config.py`: Celery configuration for task scheduling

## Testing the Services

1. Ensure all services are running:
   ```bash
   docker-compose ps
   ```

2. Check the service logs:
   ```bash
   docker-compose logs youtube-data-retrieval
   docker-compose logs youtube-data-processing
   ```

3. Verify the generated CSV files in the `local_storage/` folder.

4. Connect to the PostgreSQL database to verify the inserted data:
   ```bash
   docker-compose exec db psql -U postgres -d youtube_data
   ```
   Then execute SQL queries, for example:
   ```sql
   SELECT * FROM channel;
   SELECT * FROM video;
   SELECT * FROM import_task;
   ```

## Troubleshooting

- If you encounter file permission issues, ensure that the shared folders have the correct permissions:
  ```bash
  chmod -R 777 local_storage/
  ```

- In case of errors related to the YouTube API, verify that your API key is correct and has not exceeded its usage limits.

- To completely reset the pipeline, you can remove all containers and volumes, then rebuild:
  ```bash
  docker-compose down -v
  docker-compose up -d --build
  ```

For any other questions or issues, feel free to open an issue in the project repository.
