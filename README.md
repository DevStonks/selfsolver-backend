# SELFSOLVER

Selfsolver project provides a platform for support self-service.

## How to install

Requires `poetry` and `python>=3.8`.

Run `poetry install` to install dependencies.
Copy the `.env.example` to `.env` for development environments.
Use `poetry run flask generate-secret` to generate entropic enough secrets. (see `.env.example`)
Finally, run `poetry run flask run` to run the app.

## How to set up the database

Run `poetry run flask database setup`.
After any changes to the models, you may need to recreate the tables.
Run `poetry run flask database reset`. _THIS WILL DESTROY ALL APP DATA_.

## How to create users

There's no http api for signup (by design).
Run `poetry run flask create-user {COMPANY_ID} {EMAIL} {PASSWORD}` to create a user with those credentials.
E.g. `poetry run flask create-user 1 email@example.com correct-horse-battery-staple`.

## How to deploy to Heroku

Requires [heroku command line][heroku-cli].

```bash
# First, login to heroku.
$ heroku login

# Proceed to create an app
$ heroku create

# Set up a poetry-enabled buildpack
$ heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
$ heroku buildpacks:add heroku/python

# Enable the postgresql addon
$ heroku addons:create heroku-postgresql:hobby-dev

# Set buildpack-specific environment variables
$ heroku config:set POETRY_VERSION=1.0.10
$ heroku config:set DISABLE_POETRY_CREATE_RUNTIME_FILE=1

# Set app-specific environment variables
$ heroku config:set FLASK_APP=selfsolver/app.py
$ heroku config:set JWT_SECRET_KEY=`poetry run flask generate-secret`
$ heroku config:set PASSWORD_PEPPER=`poetry run flask generate-secret`

# Deploy to heroku using git
$ git push heroku main

# Don't forget to setup database once the app is running
$ heroku run flask database setup
```

[heroku-cli]: https://devcenter.heroku.com/articles/heroku-cli#download-and-install
