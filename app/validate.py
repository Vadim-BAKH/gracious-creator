"""
Валидаторы форм
"""

import re

from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError


class ClientSearchForm(FlaskForm):
    """Форма получения ID клиента"""
    client_id = IntegerField(
        "Введите номер клиента:",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="ID клиента должен быть положительным"),
        ],
    )
    submit = SubmitField("Найти клиента")


class ClientAddForm(FlaskForm):
    """Форма добавления клиента."""

    name = StringField(
        "Введите имя", validators=[DataRequired()]
    )
    surname = StringField(
        "Введите фамилию", validators=[DataRequired()]
    )
    credit_card = StringField(
        "Введите номер кредитной карты"
    )
    car_number = StringField(
        "Введите номер транспортного средства"
    )
    submit = SubmitField("Введите данные клиента")

    def validate_name(self, field):
        """
        Проверяет, что имя содержит только буквы, пробелы и тире.
        """
        if not re.match(r"^[A-Za-zА-Яа-яЁё\s-]+$", field.data):
            raise ValidationError(
                "Поле должно содержать только буквы, пробелы и тире."
            )

    def validate_surname(self, field):
        """
        Проверяет, что фамилия содержит только буквы, пробелы и тире.
        """
        if not re.match(r"^[A-Za-zА-Яа-яЁё\s-]+$", field.data):
            raise ValidationError(
                "Поле должно содержать только буквы, пробелы и тире."
            )


class ParkingAddForm(FlaskForm):
    """Форма добавления парковки."""
    address = StringField(
        "Введите адрес", validators=[DataRequired()]
    )
    opened = BooleanField("Укажите статус парковки")
    count_place = IntegerField(
        "Введите количество парковочных мест:",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Мест должно быть больше 0"),
        ],
    )
    count_available_places = IntegerField(
        "Введите количество свободных парковочных мест:",
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                message="Мест должно быть больше 0.",
            ),
        ],
    )
    submit = SubmitField("Введите данные парковки")

    def validate_count_available_places(self, field):
        """
        Проверяет, что количество свободных
         мест не превышает общее.
        """
        if (self.count_place.data is not None
                and field.data > self.count_place.data):
            raise ValidationError(
                "Количество свободных мест не "
                "может превышать общее количество мест."
            )


class ClientParkingForm(FlaskForm):
    """Форма для работы с данными о парковке клиента."""
    client_id = IntegerField(
        "Введите номер клиента", validators=[DataRequired()]
    )
    parking_id = IntegerField(
        "Введите номер парковки", validators=[DataRequired()]
    )
