"""Test model required columns in a DRY fashion."""
from itertools import chain, product

import pytest
from sqlalchemy.exc import IntegrityError

required_columns = {
    "user": ["company", "email"],
    "location": ["company", "label"],
    "brand": ["name"],
    "family": ["brand", "name"],
}


@pytest.mark.parametrize(
    ("factory", "column"),
    chain.from_iterable(
        product([pytest.lazy_fixture(f"{model}_factory")], columns)
        for model, columns in required_columns.items()
    ),
)
def test_model_create_without_required(db_session, factory, column):
    """Test model creation fails without required parameters."""
    model = factory.build(**{column: None})
    db_session.add(model)
    with pytest.raises(IntegrityError, match="psycopg2.errors.NotNullViolation"):
        db_session.commit()


@pytest.mark.parametrize(
    ("model", "column"),
    chain.from_iterable(
        product([pytest.lazy_fixture(model)], columns)
        for model, columns in required_columns.items()
    ),
)
def test_model_update_remove_required(db_session, model, column):
    """Test model update."""
    setattr(model, column, None)
    db_session.add(model)

    with pytest.raises(IntegrityError, match="psycopg2.errors.NotNullViolation"):
        db_session.commit()
