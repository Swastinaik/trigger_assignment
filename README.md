Hello I'm Swasti Santosh Naik,
I've got this project assignment and i have completed all the taks according to the given assignment.
This is the backend API for Service Membership System (like a gym / coaching centre / salon)

## Triggers
The trigger file is kept in sql/triggers.sql where the trigger file is present. 
it contains a function and trigger which will be called for every new record into attendance table,
which will trigger to update the total_check_ins of user to be incremented bt 1.

# Tech Stack:
Language: Python 3.14
Framework: FastAPI
Database: PostgreSQL 16
ORM: SQLModel
Other tools: Docker for PostgreSQL Service.


# Project Setup:

## Method 1: Using Docker setup
First Ensure that the docker is installed in the System if not then below is the link for docker desktop installation
Link: https://docs.docker.com/desktop/setup/install

1. Clone the project using `https://github.com/Swastinaik/trigger_assignment.git`
2. Create virtual Enviornment
  - For Windows : `python -m venv venv`
  - For Mac/Linux: `python3 -m venv venv`
3. Activate Virtual Enviornment
  - move into the folder(common) `cd trigger_assignment`
  - For Windows: `venv/Scripts/activate`
  - For Mac/Linux: `source venv/bin/activate`
4. Install all the dependencies using `pip install -r requirements.txt`
5. Create a .env file in root directory and paste this variable `DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/service_membership`
6. Run the app using command `uvicorn app.main:app --reload`
Next the seeding of data will happen and can test the endpoints.

## Method 2: Using local postgres Setup
First Ensure the Postgres is locally installed on host machine if not then below is the link to install it.
Link: https://www.postgresql.org/download

1. Clone the project using `https://github.com/Swastinaik/trigger_assignment.git`
2. Create virtual Enviornment
  - For Windows : `python -m venv venv`
  - For Mac/Linux: `python3 -m venv venv`
3. Activate Virtual Enviornment
  - move into the folder(common) `cd trigger_assignment`
  - For Windows: `venv/Scripts/activate`
  - For Mac/Linux: `source venv/bin/activate`
4. Install all the dependencies using `pip install -r requirements.txt`
5. Create a .env file in root directory and paste this variable `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/service_membership` and add a variable `ENV=local`
    for local postgres variable.
6. Inside pgAmdin create a db name service_membership using `CREATE DATABASE service_membership;` and test it once.
7. Run the app using command `uvicorn app.main:app --reload`


## These are two approaches for setting up project but docker is recommeneded way for setting it up.




