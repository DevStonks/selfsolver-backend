"""Test model required columns in a DRY fashion."""
from itertools import chain, product

import pytest
from sqlalchemy.exc import IntegrityError

relationships = {
    "user": ["company"],
    "location": ["company"],
    "family": ["brand"],
}


@pytest.mark.parametrize(
    ("factory", "relationship"),
    chain.from_iterable(
        product([pytest.lazy_fixture(f"{model}_factory")], relations)
        for model, relations in relationships.items()
    ),
)
def test_user_create_with_non_existing_company(db_session, factory, relationship):
    """Test user creation fails with non-existing company."""
    data = factory.stub()
    delattr(data, relationship)
    model_class = factory._meta.get_model_class()
    model = model_class(**data.__dict__, **{f"{relationship}_id": 1337})
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
