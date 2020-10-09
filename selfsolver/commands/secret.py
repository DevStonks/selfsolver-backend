import click
import secrets

@click.command('generate-secret')
def generate_secret():
    print(secrets.token_hex())