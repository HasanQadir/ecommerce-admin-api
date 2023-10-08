# E-Commerce Admin API

This repository contains a FastAPI-based backend API for an e-commerce admin dashboard.

## Prerequisites

- Python 3.9
- PostgreSQL database

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/HasanQadir/ecommerce-admin-api.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd ecommerce-admin-api
    ```

3. **Create a Python 3.9 virtual environment:**

    ```bash
    python3.9 -m venv venv
    ```

4. **Activate the virtual environment:**

    - On Linux/macOS:

        ```bash
        source venv/bin/activate
        ```

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

5. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Database Setup

1. **Create a PostgreSQL database and user:**

   - On Linux/macOS:

      ```bash
      sudo su postgres
      psql
      CREATE DATABASE yourdatabase;
      CREATE USER youruser WITH PASSWORD 'yourpassword';
      GRANT ALL PRIVILEGES ON DATABASE yourdatabase TO youruser;


2. **Update the database connection string:**

    Edit the `alembic.ini` file and set the `sqlalchemy.url` to your PostgreSQL database connection string.

3. **Goto db folder which contain alembic.ini file**

    ```bash
    cd ecommerce_app/db
    ```
   
4. **Run Alembic migrations:**

    ```bash
    alembic upgrade head
    ```

## Seed Database

1. **Update the database connection string in `seed_db.py`:**

    Edit the `seed_db.py` file and set the `SQLALCHEMY_DATABASE_URL` to your PostgreSQL database connection string.

2. **Run the script to populate dummy data:**

    ```bash
    python seed_db.py
    ```

## Run the Application

2. **Run the FastAPI application:**

    ```bash
    uvicorn main:app --reload
    ```

3. **Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) to access the FastAPI Swagger documentation.**

4. **Test the API endpoints using the provided Swagger interface or using my Postman Public API Collection:
https://www.postman.com/hqenterprises/workspace/ecommerce-dashboard-api/collection/2347646-05f2af9e-1d26-4f84-b605-292c21fb0c2e?action=share&creator=2347646.**

## Contributions

Feel free to contribute to this project by submitting issues or pull requests.
