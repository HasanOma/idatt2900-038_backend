# My Django Application README

This README will guide you through the process of setting up and running the Django application. Please follow the steps below carefully.

## Prerequisites

1. Download and install [Redis](https://redis.io/download).
2. Download and install [PostgreSQL](https://www.postgresql.org/download/).

Ensure that Redis is running on `localhost` with port `6379`, and PostgreSQL is running on `localhost` with port `5432`.

### PostgreSQL Configuration

By default, the application expects the following PostgreSQL configuration:

- Superuser name: `postgres`
- Password: `password`

If you want to use a different configuration, you will need to update `backend/settings.py` and `backend/database.py` accordingly.

### Redis Configuration

No additional configuration is needed for Redis, as it should run on `localhost` with port `6379` by default.

## Installation and Setup

### PostgreSQL Setup

1. Install the PostgreSQL server on your machine by following the official [installation guide](https://www.postgresql.org/download/).

2. Start the PostgreSQL server and create a new database for the application.

3. Configure the `backend/settings.py` and `backend/database.py` files in the Django application with your database information.

### Redis Setup

1. Download and install Redis by following the official [installation guide](https://redis.io/download).

2. Start the Redis server.

## Running the Application

1. Open a terminal and navigate to the `MTP_038_backend` folder.

    ```bash
    cd MTP_038_backend
    ```
   
2. Run the following command to migrate tables into the database.

    ```bash
    python models.py
    ```

3. Start the Django server.
    
    ```bash
    python manage.py runserver
    ```
   
### Run tests
   ```bash
   python manage.py test --verbosity=2
   ```

## Accessing the Websockets

You can access the following Websocket URLs for different data:

- Ship locations: `ws://127.0.0.1:8000/ws/ship_locations/`
- Weather data: `ws://127.0.0.1:8000/ws/weather/`

Multiple clients can join the same instance.

## Troubleshooting

If you encounter any issues during the installation or setup process, please check the application logs or contact the support team for assistance.