# SELFSOLVER

Selfsolver project provides a platform for support self-service.

## How to install

Requires `poetry` and `python>=3.8`.

Run `poetry install` to install dependencies.
Copy the `.env.example` to `.env` for development environments.
Use `poetry run generate-secret` to generate entropic enough secrets. (see `.env.example`)
Finally, run `poetry run flask run` to run the app.

## How to set up the database

Run `poetry run flask database setup`.
After any changes to the models, you may need to recreate the tables.
Run `poetry run flask database reset`. *THIS WILL DESTROY ALL APP DATA*.

## How to create users

There's no http api for signup (by design).
Run `poetry run flask create-user {EMAIL} {PASSWORD}` to create a user with those credentials.
E.g. `poetry run flask create-user email@example.com correct-horse-battery-staple`.