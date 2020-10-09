import secrets

import click


@click.command("generate-secret")
def generate_secret():
    print(secrets.token_hex())
