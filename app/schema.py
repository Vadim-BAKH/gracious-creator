"""
Схемы для сериализации
"""

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .models import Client, Parking


class ClientSchema(SQLAlchemyAutoSchema):
    """Схема Marshmallow для модели Client."""
    class Meta:
        """Настройки схемы."""
        model = Client
        load_instance = True


class ParkingSchema(SQLAlchemyAutoSchema):
    """Схема Marshmallow для модели Parking."""
    class Meta:
        """Настройки схемы."""
        model = Parking
        load_instance = True


class ClientParkingSchema(Schema):
    """Схема Marshmallow для модели Client_Parking."""
    client_id = fields.Int()
    parking_id = fields.Int()
    time_in = fields.DateTime()
    time_out = fields.DateTime()
