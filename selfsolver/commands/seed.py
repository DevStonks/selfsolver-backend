"""Provide commands to seed the database with staging data.

Usage:
$ flask seed
"""
import click
from faker import Faker
from flask.cli import with_appcontext

from selfsolver.models import (
    Brand,
    Company,
    Defect,
    Device,
    Family,
    Location,
    Ticket,
    User,
    db,
)


@click.command("seed")
@click.argument("company_id", type=int, required=False)
@with_appcontext
def seed(company_id=None):
    """Seed the database with staging data."""
    faker = Faker()

    company = Company.query.get(company_id) if company_id else Company()

    if company is None:
        raise click.UsageError(f"No company found with id {company_id}.")

    email, password = faker.email(), faker.password()
    user = User(email=email, password=password, company=company)
    location = Location(label=faker.city(), company=company)
    brand = Brand(name=faker.company())
    family = Family(name=faker.color_name(), brand=brand)
    device = Device(serial=faker.ean(), family=family, location=location)
    ticket = Ticket(device=device)

    defects = [
        Defect(description="O aparelho não liga."),
        Defect(description="O aparelho não conecta à rede."),
        Defect(description="O aparelho exibe uma mensagem de erro."),
    ]

    db.session.add_all([user, location, brand, family, device, ticket] + defects)
    db.session.commit()

    click.echo(
        f'Created user {user} with credentials email={email} password="{password}"'
    )
