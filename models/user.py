import random
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from pydantic import EmailStr
from sqlalchemy import event
from sqlalchemy.databases import postgres
from sqlalchemy.orm import declared_attr
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel
from sqlalchemy.ext.mutable import MutableDict
from models.base import UUIDModel


class UserRole(str, Enum):
    """
    Enum class represents types of users.
    Used to define access level.
    """

    admin = "admin"
    manager = "manager"
    user = "user"


user_role_type = postgres.ENUM(
    "admin",
    "manager",
    "user",
    name=f"user_role",
)


@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):
    """
    Method that generates enum fields for table in database.

    :param metadata:
    :type metadata:
    :param conn:
    :type conn:
    :param kw:
    :type kw:
    :return:
    :rtype:
    """
    user_role_type.create(conn, checkfirst=True)


def generate_segment() -> int:
    """
    :return: random segment for new user
    :rtype: int
    """
    return random.randint(0, 4)


class EditableUserBase(SQLModel):
    """
    Model that represents User fields that can be edited by users.

    :param first_name: first name of user
    :type  first_name: str
    :param last_name: last name of user
    :type  last_name: str
    :param email: user email used as login, should be unique
    :type  email: str
    :param birthdate: user date of birth
    :type birthdate: datetime
    """

    user_name: str | None
    email: EmailStr = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )


class UserBase(EditableUserBase):
    """
    Model that represents User fields that can be edited by admins.

    :param is_active: determines if user is active
    :type  is_active: bool
    :param role: role of user, value is one of :class:`UserRole`
    :type role: str
    :param segment: value used to specify segment of user to test different features
    :type  segment: int
    """

    is_active: bool = Field(default=True)
    role: str = Field(
        sa_column=Column("role", user_role_type, nullable=False),
        default=UserRole.user,
    )


class User(UUIDModel, UserBase):
    """
    Model that represents User fields having additional metadata.
    """

    pass


class DBUser(User, table=True):
    """
    Model that represents User in database.
    Used to create table `user` in database and perform ORM actions.
    Contains relations to other models.

    :param hashed_password: encrypted password that stored in database
    :type hashed_password: str
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return "serviceuser"

    hashed_password: Optional[str] = Field(nullable=False, index=True)
    token: "DBTokenbl" = Relationship(back_populates="user")
    order: "DBOrder" = Relationship(back_populates="user")


class TokenBL(SQLModel):
    token: str = Field(nullable=False, index=True)


class DBTokenbl(UUIDModel, TokenBL, table=True):
    """
    Model that represents Token Black List in database.
    Used to create table tokenbl in database and perform ORM actions.
    Contains relations to other models.

    :param user_id: id of user who created this entry
    :type user_id: UUID
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return "tokenbl"

    # Foreign keys
    user_id: UUID | None = Field(default=None, foreign_key="serviceuser.id")

    # Relations
    user: DBUser = Relationship(back_populates="token")


class EditableFlowerBase(SQLModel):
    name: str
    color: str
    price: float


# Создаем модель для таблицы "Цветы"
class FlowerBase(EditableFlowerBase):
    in_stock: bool


class Flower(UUIDModel, FlowerBase):
    pass


class DBFlower(Flower, table=True):

    @declared_attr
    def __tablename__(cls) -> str:
        return "flower"

    flowersinorder: "DBFlowersInOrder" = Relationship(back_populates="flower")


# Создаем модель для таблицы "Цветы в заказе"
class EditableFlowersInOrder(SQLModel):
    quantity: int


class FlowersInOrderBase(EditableFlowersInOrder):
    flower_id: UUID | None = Field(default=None, foreign_key="flower.id")
    order_id: UUID | None = Field(default=None, foreign_key="order.id")


class FlowersInOrder(UUIDModel, FlowersInOrderBase):
    pass


class DBFlowersInOrder(FlowersInOrder, table=True):

    @declared_attr
    def __tablename__(cls) -> str:
        return "flowersinorder"

    flower: "DBFlower" = Relationship(back_populates="flowersinorder")
    order: "DBOrder" = Relationship(back_populates="flowersinorder")


# Создаем модель для таблицы "Заказы"
class EditableOrder(SQLModel):
    user_id: UUID | None = Field(default=None, foreign_key="serviceuser.id")
    customer_name: str | None = Field(nullable=False)
    customer_email: str | None = Field(nullable=False)
    flowers: MutableDict = Field(
        sa_column=Column("flowers", type_=MutableDict.as_mutable(JSONB)),
        nullable=True, default=dict()
    )
    total_price: float | None = Field(default=0)
    quantity: int | None = Field(default=0)


class OrderBase(EditableOrder):
    pass


class Order(UUIDModel, EditableOrder):
    pass


class DBOrder(Order, table=True):

    @declared_attr
    def __tablename__(cls) -> str:
        return "order"

    user: "DBUser" = Relationship(back_populates="order")
    flowersinorder: "DBFlowersInOrder" = Relationship(back_populates="order")
