"""Provide schemas to dump selfsolver models to JSON."""
from flask_marshmallow import Marshmallow

from selfsolver.models import Brand, Defect, Device, Family, Location, Solution, Ticket

ma = Marshmallow()


class BrandSchema(ma.SQLAlchemyAutoSchema):
    """Provide schema to dump Brand models to JSON."""

    class Meta:  # noqa: D106
        model = Brand
        include_fk = True


class FamilySchema(ma.SQLAlchemyAutoSchema):
    """Provide schema to dump Family models to JSON."""

    class Meta:  # noqa: D106
        model = Family
        include_fk = True

    brand = ma.Nested(BrandSchema)


class LocationSchema(ma.SQLAlchemyAutoSchema):
    """Provide schema to dump Location models to JSON."""

    class Meta:  # noqa: D106
        model = Location
        include_fk = True


class DeviceSchema(ma.SQLAlchemyAutoSchema):
    """Provide schema to dump Device models to JSON."""

    class Meta:  # noqa: D106
        model = Device
        include_fk = True

    family = ma.Nested(FamilySchema)
    location = ma.Nested(LocationSchema)


class TicketSchema(ma.SQLAlchemyAutoSchema):
    """Provide schema to dump Ticket models to JSON."""

    class Meta:  # noqa: D106
        model = Ticket
        include_fk = True

    device = ma.Nested(DeviceSchema)


class DefectSchema(ma.SQLAlchemyAutoSchema):
    """Provide schema to dump Defect models to JSON."""

    class Meta:  # noqa: D106
        model = Defect
        include_fk = True


class SolutionSchema(ma.SQLAlchemyAutoSchema):
    """Provide schema to dump Solution models to JSON."""

    class Meta:  # noqa: D106
        model = Solution
        include_fk = True
