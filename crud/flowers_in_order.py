"""
Module that contains User CRUD subclass. Contains custom logic to handle
user retrieval, creation and authentication.
"""
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from starlette import status

from crud.base import CRUDBase, ModelType
from models.user import DBOrder, DBFlower, DBFlowersInOrder
from routers.security import get_password_hash, verify_password
from schema import CreateUserReq, UpdateUserReq, UpdateOrderReq, CreateOrderReq, CreateFlsInOrdr


class CRUDFlowersInOrder(CRUDBase[DBFlowersInOrder, CreateFlsInOrdr, UpdateOrderReq]):
    """
    Wrapper to handle User CRUD operations.
    """

    async def get_by_order_id(
            self,
            *,
            order_id: UUID,
    ) -> DBFlowersInOrder | None:
        """
        Method to get user by email.

        :param email: user email
        :type email: str
        :return: user object
        :rtype: DBUser
        """
        flower_orders = await self.session.execute(
            select(DBFlowersInOrder).where(DBFlowersInOrder.order_id == order_id))
        return flower_orders.scalar_one_or_none()

    async def get_all_orders(self) -> Optional[List[ModelType]]:
        flower_orders = await self.session.execute(select(DBFlowersInOrder))
        return flower_orders.scalars().all()

    async def get_all_flowers_in_order(self) -> Optional[List[ModelType]]:
        flowers_in_order = await self.session.execute(select(DBFlowersInOrder))
        return flowers_in_order.scalars().all()

    # async def check_flowers_in_order_exists(
    #         self,
    #         customer_name: str,
    # ) -> bool:
    #
    #     user = await self.get_by_order_id(customer_name=customer_name)
    #     if user:
    #         return True
    #     else:
    #         return False

    async def add_flowers(
            self,
            obj_in: CreateFlsInOrdr
    ) -> DBFlowersInOrder:

        db_obj = DBFlowersInOrder.from_orm(obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def del_flowers(self, flowers_id: UUID):
        response = await self.session.execute(
            select(DBFlowersInOrder).where(DBFlowersInOrder.id == flowers_id)
        )
        obj = response.scalar_one_or_none()
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
        return obj
