from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select, update
from starlette import status

from crud.base import CRUDBase, ModelType
from models.user import DBOrder, DBFlower, DBFlowersInOrder
from routers.security import get_password_hash, verify_password
from schema import CreateUserReq, UpdateUserReq, UpdateOrderReq, CreateOrderReq


class CRUDOrder(CRUDBase[DBOrder, CreateOrderReq, UpdateOrderReq]):
    """
    Wrapper to handle Order CRUD operations.
    """

    async def get_by_customer_name(
            self,
            *,
            customer_name: str,
    ) -> DBOrder | None:
        users = await self.session.execute(select(DBOrder).where(DBOrder.customer_name == customer_name))
        return users.scalar_one_or_none()

    async def get_all_orders(self) -> Optional[List[ModelType]]:
        orders = await self.session.execute(select(DBOrder))
        return orders.scalars().all()

    async def get_order(self, order_id: UUID) -> DBOrder:
        order = await self.session.execute(select(DBOrder).where(DBOrder.id == order_id))
        db_order = order.scalar_one()
        return db_order

    async def add_quantity(self, order_id: UUID, quantity: int, price: float, flower: str):
        db_order = await self.session.execute(select(DBOrder).where(DBOrder.id == order_id))
        resp = db_order.scalar_one_or_none()
        # В этом коде мы добавляем к значению ключа flower в словаре resp.flowers значение quantity,
        # если такой ключ уже существует, или создаем ключ со значением quantity, если его нет.
        # Затем мы передаем обновленный словарь resp.flowers в качестве значения поля flowers в функцию update().
        resp.flowers[flower] = resp.flowers.get(flower, 0) + quantity
        order = await self.session.execute(
            update(DBOrder).where(DBOrder.id == order_id).values(quantity=resp.quantity + quantity,
                                                                 total_price=resp.total_price + price,
                                                                 flowers=resp.flowers
                                                                 ))
        await self.session.commit()

    async def get_all_flowers_in_order(self) -> Optional[List[ModelType]]:
        flowers_in_order = await self.session.execute(select(DBFlowersInOrder))
        return flowers_in_order.scalars().all()

    async def check_customer_name_exists(
            self,
            customer_name: str,
    ) -> bool:

        user = await self.get_by_customer_name(customer_name=customer_name)
        if user:
            return True
        else:
            return False

    async def create_order(
            self,
            *,
            obj_in: CreateOrderReq
    ) -> DBOrder:

        db_obj = DBOrder.from_orm(obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def del_order(self, order_id: UUID):
        response = await self.session.execute(
            select(DBOrder).where(DBOrder.id == order_id)
        )
        obj = response.scalar_one_or_none()
        if obj:
            all_flowersinorder = await self.session.execute(
                select(DBFlowersInOrder).where(DBFlowersInOrder.order_id == order_id))
            all_flowersinorder = all_flowersinorder.scalars().all()
            for fl in all_flowersinorder:
                await self.session.delete(fl)
            await self.session.delete(obj)
            await self.session.commit()
        return obj
