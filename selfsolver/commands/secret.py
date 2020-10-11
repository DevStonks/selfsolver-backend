"""Provide a command to generate secrets (for pepper or jwt secret).

Usage:
$ flask generate-secret
"""
import secrets

import click


@click.command("generate-secret")
def generate_secret():
    """Generate secure and entropic secret bytes and print as hexstring."""
    print(secrets.token_hex())
