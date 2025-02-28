"""Определение моделей SQLAlchemy"""

import math
from datetime import datetime
from typing import Any, List, Optional, Tuple
from zoneinfo import ZoneInfo

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError

from log import logger

tax: Optional[int] = 100

db = SQLAlchemy()


class Client(db.Model):
    """Класс базы данных клиентов"""
    __tablename__ = "client"
    __table_args__ = (db.UniqueConstraint(
        "name", "surname", name="unique_name"),
    )

    id: db.Mapped[int] = db.mapped_column(
        db.Sequence("client_id"), primary_key=True
    )
    name: db.Mapped[str] = db.mapped_column(
        db.String(50), nullable=False
    )
    surname: db.Mapped[str] = db.mapped_column(db.String(50), nullable=False)
    credit_card: db.Mapped[str] = db.mapped_column(
        db.String(50), nullable=True
    )
    car_number: db.Mapped[str] = db.mapped_column(db.String(10), nullable=True)

    def __repr__(self) -> str:
        return f"Client: {self.name!r}"

    @classmethod
    def add_or_update_client(
            cls, data_client: dict
    ) -> List[Tuple[int, str, str]]:
        """Метод добавления/обновления клиента"""
        mandatory_fields = ("name", "surname")
        missing_fields = [
            field
            for field in mandatory_fields
            if field not in data_client
            or data_client[field] is None
        ]
        if missing_fields:
            raise ValueError(
                f"Отсутствуют обязательные поля:"
                f" {', '.join(missing_fields)}"
            )

        client = (
            insert(cls)
            .values(
                name=data_client.get("name"),
                surname=data_client.get("surname"),
                credit_card=data_client.get("credit_card"),
                car_number=data_client.get("car_number"),
            )
            .on_conflict_do_update(
                index_elements=["name", "surname"],
                set_={
                    "credit_card": data_client.get("credit_card"),
                    "car_number": data_client.get("car_number"),
                },
            )
            .returning(
                cls.id,
                cls.name,
                cls.surname,
                cls.credit_card,
                cls.car_number
            )
        )
        try:
            result = db.session.execute(client)
            db.session.commit()
            return result.fetchall()

        except InvalidRequestError as ire:
            db.session.rollback()
            raise InvalidRequestError("Связь с сессией прервана") from ire

        except SQLAlchemyError as sae:
            db.session.rollback()
            raise SQLAlchemyError("Ошибка базы данных") from sae
        except ValueError as val:
            db.session.rollback()
            raise val from val

    @classmethod
    def select_clients(cls) -> List["Client"]:
        """Метод показывает всех клиентов"""
        clients = select(cls)
        try:
            result = db.session.execute(clients)
            clients_list = result.scalars().all()
            if not clients_list:
                raise ValueError(
                    "Отсутствуют клиенты для паркинга"
                )
            return clients_list
        except InvalidRequestError as ire:
            raise InvalidRequestError("Связь с сессией прервана") from ire
        except SQLAlchemyError as sae:
            raise SQLAlchemyError("Ошибка базы данных") from sae
        except ValueError as val:
            raise val from val

    @classmethod
    def select_client_by_id(
            cls, idc: int
    ) -> "Client":
        """Метод найти клиента по ID"""
        try:
            client = select(cls).where(cls.id == idc)
            result = db.session.execute(client)
            client_in_list = result.scalar_one_or_none()
            if client_in_list is None:
                raise ValueError(
                    f"Клиент под номером {idc} отсутствует в базе клиентов."
                )
            logger.info(f"Have found a client under number {idc}")
            return client_in_list
        except InvalidRequestError as ire:
            db.session.rollback()
            raise InvalidRequestError("Связь с сессией прервана") from ire
        except ValueError as val:
            raise val from val
        except SQLAlchemyError as sae:
            raise SQLAlchemyError("Ошибка базы данных") from sae

    @classmethod
    def check_car_number_and_credit_card(cls, idc: int) -> bool:
        """Метод проверки полей кредитки и номера машины"""
        client_data = select(cls).where(cls.id == idc)
        try:
            client = (
                db.session
                .execute(client_data)
                .scalar_one_or_none()
            )
            if client:
                if (
                    client.credit_card
                    and client.credit_card.strip()
                    and client.car_number
                    and client.car_number.strip()
                ):
                    logger.info(
                        f"Client number {idc} is ready for payment"
                    )
                    return True

                logger.info(
                    f"Client number {idc} is not ready for payment"
                )
                raise ValueError(
                    f"Клиент номер {idc} не готов к оплате:"
                    f" обновите данные кредитной карты и номера ТС."
                )

            logger.info(f"Client number {idc} not found")
            raise ValueError(f"Клиент с номером {idc} не найден.")

        except InvalidRequestError as ire:
            db.session.rollback()
            raise InvalidRequestError("Связь с сессией прервана") from ire
        except ValueError as val:
            raise val from val
        except SQLAlchemyError as sae:
            logger.error(sae)
            raise SQLAlchemyError("Ошибка базы данных") from sae


class Parking(db.Model):
    """Класс базы данных парковок"""
    __tablename__ = "parking"
    __table_args__ = (
        db.UniqueConstraint(
            "address", name="unique_address"
        ),
    )

    id: db.Mapped[int] = db.mapped_column(
        db.Sequence("parking_id"), primary_key=True
    )
    address: db.Mapped[str] = db.mapped_column(db.String(100), nullable=False)
    opened: db.Mapped[bool] = db.mapped_column(db.BOOLEAN, default=False)
    count_place: db.Mapped[int] = db.mapped_column(db.Integer, nullable=False)
    count_available_places: db.Mapped[int] = db.mapped_column(
        db.Integer, nullable=False
    )

    @classmethod
    def insert_or_update_parking(
            cls, data_parking: dict
    ) -> List[tuple[int, str]]:
        """Метод добавления/обновления парковки"""
        mandatory_fields = (
            "address",
            "opened",
            "count_place",
            "count_available_places",
        )
        missing_fields = [
            field
            for field in mandatory_fields
            if field not in data_parking
            or data_parking[field] is None
        ]
        if missing_fields:
            raise ValueError(
                f"Отсутствуют обязательные поля:"
                f" {', '.join(missing_fields)}"
            )
        parking = (
            insert(cls)
            .values(
                address=data_parking.get("address"),
                opened=data_parking.get("opened"),
                count_place=data_parking.get("count_place"),
                count_available_places=data_parking.get(
                    "count_available_places"
                ),
            )
            .on_conflict_do_update(
                index_elements=["address"],
                set_={
                    "opened": data_parking.get("opened"),
                    "count_place": data_parking.get("count_place"),
                    "count_available_places": data_parking.get(
                        "count_available_places"
                    ),
                },
            )
            .returning(
                cls.id,
                cls.address,
                cls.opened,
                cls.count_place,
                cls.count_available_places,
            )
        )
        try:
            result = db.session.execute(parking)
            db.session.commit()
            return result.fetchall()

        except InvalidRequestError as ire:
            db.session.rollback()
            raise InvalidRequestError("Связь с сессией прервана") from ire

        except ValueError as val:
            db.session.rollback()
            raise val from val

        except SQLAlchemyError as sae:
            db.session.rollback()
            raise SQLAlchemyError("Ошибка базы данных") from sae

    @classmethod
    def select_all_parking(cls) -> List["Parking"]:
        """Метод получения базы парковок"""
        parking_query = select(cls)
        try:
            all_parking = (db.session
                           .execute(parking_query)
                           .scalars().all())
            if not all_parking:
                raise ValueError(
                    "В базе данных нет доступных парковок"
                )
            return all_parking

        except InvalidRequestError as ire:
            raise InvalidRequestError("Связь с сессией прервана") from ire
        except ValueError as val:
            raise val from val
        except SQLAlchemyError as sae:
            raise SQLAlchemyError("Ошибка базы данных") from sae

    @classmethod
    def select_parking_by_id(cls, idp: int) -> "Parking":
        """Метод получить парковку по ID"""
        try:
            parking = select(cls).where(cls.id == idp)
            result = db.session.execute(parking)
            parking_in_list = result.scalar_one_or_none()
            if parking_in_list is None:
                raise ValueError(
                    f"Паркинг под номером {idp}"
                    f" отсутствует в базе парковок."
                )
            logger.info(
                f"Have found a parking under number {idp}"
            )
            return parking_in_list

        except InvalidRequestError as ire:

            raise InvalidRequestError("Связь с сессией прервана") from ire
        except ValueError as val:
            raise val from val
        except SQLAlchemyError as sae:
            raise SQLAlchemyError("Ошибка базы данных") from sae

    @classmethod
    def test_update_parking_enter(cls, idp: int) -> bool:
        """Метод проверки и обновления свободных мест"""

        try:
            data_parking_query = (
                select(cls)
                .where(
                    cls.id == idp, cls.opened.is_(True)
                )
            )
            result = (db.session
                      .execute(data_parking_query)
                      .scalar_one_or_none())
            if result:
                logger.info(
                    f"Parking parking number {idp} is allowed"
                )
                if result.count_available_places >= 2:
                    result.count_available_places -= 1

                elif result.count_available_places == 1:
                    result.count_available_places -= 1
                    result.opened = False
                    logger.info(
                        f"There are no more places"
                        f" in the parking lot of {idp}"
                    )
                db.session.commit()
                return True

            logger.info(
                f"There are no places "
                f"in the parking lot of {idp}"
            )
            db.session.rollback()
            raise ValueError(
                f"Нет мест на парковке номер {idp}"
            )

        except InvalidRequestError as ire:
            db.session.rollback()
            raise InvalidRequestError("Связь с сессией прервана") from ire

        except ValueError as val:
            db.session.rollback()
            raise val from val

        except SQLAlchemyError as sql:
            db.session.rollback()
            raise SQLAlchemyError(f"Ошибка базы данных: {sql}") from sql

    @classmethod
    def test_update_parking_out(cls, idp: int) -> bool:
        """Метод обновления мест пр выезде"""
        parking_query = select(cls).where(cls.id == idp)
        try:
            result = (db.session
                      .execute(parking_query)
                      .scalar_one_or_none())
            if result.count_available_places == 0:
                result.count_available_places += 1
                result.opened = True
            else:
                result.count_available_places += 1
            db.session.commit()
            return True

        except InvalidRequestError as ire:
            db.session.rollback()
            raise InvalidRequestError("Связь с сессией прервана") from ire

        except SQLAlchemyError as sql:
            db.session.rollback()
            raise SQLAlchemyError(f"Ошибка базы данных: {sql}") from sql


class ClientParking(db.Model):
    """Класс базы данных клиент-паркинга"""
    __tablename__ = "client_parking"
    __table_args__ = (
        db.UniqueConstraint(
            "client_id", "parking_id",
            name="unique_client_parking"
        ),
    )

    id: db.Mapped[int] = db.mapped_column(
        db.Sequence("client_parking_id"), primary_key=True
    )
    client_id: db.Mapped[int] = db.mapped_column(
        db.ForeignKey("client.id"), nullable=False
    )
    parking_id: db.Mapped[int] = db.mapped_column(
        db.ForeignKey("parking.id"), nullable=False
    )
    time_in: db.Mapped[datetime] = db.mapped_column(
        db.TIMESTAMP(timezone=True), nullable=True
    )
    time_out: db.Mapped[datetime] = db.mapped_column(
        db.TIMESTAMP(timezone=True), nullable=True
    )

    client: db.Mapped[Client] = db.relationship(
        backref=db.backref(
            "clients_parking", cascade="all, delete-orphan", lazy="select"
        )
    )
    parking: db.Mapped[Parking] = db.relationship(
        backref=db.backref(
            "clients_parking", cascade="all, delete-orphan", lazy="select"
        )
    )

    def __repr__(self) -> str:
        return (f" Client - Parking:"
                f" {self.client_id!r}"
                f" - {self.parking_id!r}")

    @classmethod
    def select_all_client_parking(cls) -> list["ClientParking"]:
        """Метод показывает базу клиент-паркинга"""
        client_parking_query = select(cls)
        try:
            client_parking = (db.session
                              .execute(client_parking_query)
                              .scalars().all())
            if not client_parking:
                raise ValueError(
                    "В системе нет сведений о парковках"
                )
            return client_parking

        except InvalidRequestError as ire:
            raise InvalidRequestError("Связь с сессией прервана") from ire
        except ValueError as val:
            raise val from val
        except SQLAlchemyError as sae:
            raise SQLAlchemyError("Ошибка базы данных") from sae

    @classmethod
    def search_client_in_parking_enter(cls, idc: int) -> bool:
        """Метод находит клиента на парковке"""
        try:
            client_query = select(cls).where(
                cls.client_id == idc,
                cls.time_in.is_not(None),
                cls.time_out.is_(None)
            )
            client = (db.session
                      .execute(client_query)
                      .scalar_one_or_none())
            if client:
                logger.info(
                    f"The client under number {idc}"
                    f" is already parked in parking number"
                    f" {client.parking_id}"
                )
                raise ValueError(
                    f"Клиент номер {idc}"
                    f" уже припаркован на парковке"
                    f" номер {client.parking_id}"
                )

            logger.info(
                f"Client number {idc}"
                f" is not parked anywhere."
            )
            return True

        except InvalidRequestError as ire:
            raise InvalidRequestError("Связь с сессией прервана") from ire
        except ValueError as val:
            raise val from val
        except SQLAlchemyError as sae:
            raise SQLAlchemyError("Ошибка базы данных") from sae

    @classmethod
    def search_client_in_parking_out(cls, idc: int, idp: int) -> bool:
        """Метод ищет клиента для выезда"""
        try:
            client_query = select(cls).where(
                cls.client_id == idc,
                cls.parking_id == idp,
                cls.time_out.is_(None)
            )
            client = (db.session
                      .execute(client_query)
                      .scalar_one_or_none())
            if client:
                logger.info(
                    f"Client number {idc} parked"
                    f" in parking number {idp}."
                )
                return True

            raise ValueError(
                f"Клиент номер {idc}"
                f" не припаркован на парковке номер {idp}"
            )

        except InvalidRequestError as ire:
            raise InvalidRequestError("Связь с сессией прервана") from ire
        except ValueError as val:
            raise val from val
        except SQLAlchemyError as sae:
            raise SQLAlchemyError("Ошибка базы данных") from sae

    @classmethod
    def insert_or_update_client_parking(
        cls, idc: int, idp: int
    ) -> List[tuple[int, int, datetime]]:
        """Метод добавляет/обновляет базу паркингов"""
        moscow_time =\
            datetime.now(ZoneInfo("Europe/Moscow"))

        client_parking_query = (
            insert(cls)
            .values(
                client_id=idc,
                parking_id=idp,
                time_in=moscow_time,
                time_out=None,
            )
            .on_conflict_do_update(
                index_elements=["client_id", "parking_id"],
                set_={"time_in": moscow_time, "time_out": None},
            )
            .returning(
                cls.client_id, cls.parking_id, cls.time_in
            )
        )

        try:
            result = (db.session
                      .execute(client_parking_query))

            db.session.commit()
            return result.fetchall()

        except InvalidRequestError as ire:
            db.session.rollback()
            raise InvalidRequestError("Связь с сессией прервана") from ire

        except SQLAlchemyError as sae:
            logger.error(sae)
            db.session.rollback()
            raise SQLAlchemyError("Ошибка базы данных") from sae

    @classmethod
    def update_time_out_client_parking(
        cls, idc: int, idp: int
    ) -> list[tuple[Any, Any, datetime, int, int]]:
        """Метод фиксирует время выезда из парковки"""
        moscow_time =\
            datetime.now(ZoneInfo("Europe/Moscow"))
        client_parking_query = select(cls).where(
            cls.client_id == idc,
            cls.parking_id == idp
        )
        try:
            result = (db.session
                      .execute(client_parking_query)
                      .scalar_one_or_none())

            result.time_out = moscow_time

            time_difference =\
                result.time_out - result.time_in
            ceil_hours = math.ceil(
                time_difference.total_seconds() / 3600
            )
            check = ceil_hours * tax
            db.session.commit()
            return [
                (
                    result.client_id,
                    result.parking_id,
                    result.time_out,
                    ceil_hours,
                    check,
                ),
            ]

        except InvalidRequestError as ire:
            db.session.rollback()
            raise InvalidRequestError("Связь с сессией прервана") from ire

        except SQLAlchemyError as sae:
            logger.error(sae)
            db.session.rollback()
            raise SQLAlchemyError("Ошибка базы данных") from sae
