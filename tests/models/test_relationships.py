"""Test model for valid relationships in a DRY fashion."""
from itertools import chain, product

import pytest
from sqlalchemy.exc import IntegrityError

relationships = {
    "user": ["company"],
    "location": ["company"],
    "family": ["brand"],
    "device": ["location", "family"],
}


@pytest.mark.parametrize(
    ("factory", "relationship"),
    chain.from_iterable(
        product([pytest.lazy_fixture(f"{model}_factory")], relations)
        for model, relations in relationships.items()
    ),
)
def test_model_create_with_non_existing_relationship(db_session, factory, relationship):
    """Test model creation fails with non-existing company."""
    model_class = factory._meta.get_model_class()
    relationships = [
        rel.key
        for rel in model_class.__mapper__.relationships
        if rel.key != relationship
    ]
    data = factory.build().asdict(exclude_pk=True, include=relationships)
    data[f"{relationship}_id"] = 1337
    model = model_class(**data)
    db_session.add(model)

    with pytest.raises(IntegrityError, match="psycopg2.errors.ForeignKeyViolation"):
        db_session.commit()


@pytest.mark.parametrize(
    ("model", "relationship"),
    chain.from_iterable(
        product([pytest.lazy_fixture(model)], relations)
        for model, relations in relationships.items()
    ),
)
def test_model_update_with_non_existing_relationship(db_session, model, relationship):
    """Test updating model relationship to non-existing relationship."""
    setattr(model, f"{relationship}_id", 1337)
    db_session.add(model)

    with pytest.raises(IntegrityError, match="psycopg2.errors.ForeignKeyViolation"):
        db_session.commit()
