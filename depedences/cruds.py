"""
This module contains CRUDs dependencies which create separate database session
for current user and gives access to database operations.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from async_db import get_async_session
from crud.flower import CRUDFlower
from crud.flowers_in_order import CRUDFlowersInOrder
from crud.token import CRUDToken
from crud.order import CRUDOrder
from crud.user import CRUDUser
# from crud.token import CRUDToken
from models.user import DBTokenbl, DBUser, DBOrder, DBFlower, DBFlowersInOrder


async def get_users_crud(
        session: AsyncSession = Depends(get_async_session),
) -> CRUDUser:
    """
    Dependency Injection method to get User CRUD wrapper for current session.

    :param session: active user HTTP session
    :type session: AsyncSession
    :return: User CRUD
    :rtype: CRUDUser
    """
    return CRUDUser(DBUser, session=session)


async def get_token_crud(session: AsyncSession = Depends(get_async_session),
                         ) -> CRUDToken:
    """
        Dependency Injection method to get Token Black List CRUD wrapper for current session.
    """
    return CRUDToken(DBTokenbl, session=session)


async def get_order_crud(session: AsyncSession = Depends(get_async_session)) -> CRUDOrder:
    return CRUDOrder(DBOrder, session=session)


async def get_flower_crud(session: AsyncSession = Depends(get_async_session)) -> CRUDFlower:
    return CRUDFlower(DBFlower, session=session)


async def get_flowers_in_order_crud(session: AsyncSession = Depends(get_async_session)) -> CRUDFlowersInOrder:
    return CRUDFlowersInOrder(DBFlowersInOrder, session=session)
