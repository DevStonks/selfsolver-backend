"""Create and configure selfsolver flask application.

Configure the app, initialize all extensions (sqlalchemy and jwt) and register
selfsolver blueprints and commands.
"""
from selfsolver.app_factory import create_app
from selfsolver.config import BaseConfiguration

app = create_app(BaseConfiguration())
