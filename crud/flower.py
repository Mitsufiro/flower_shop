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
from models.user import DBFlower
from schema import CreateUserReq, UpdateUserReq, UpdateOrderReq, CreateOrderReq, CreateFlowerReq, UpdateFlowerReq


class CRUDFlower(CRUDBase[DBFlower, CreateFlowerReq, UpdateFlowerReq]):
    """
    Wrapper to handle Flower CRUD operations.
    """

    async def get_by_name(
            self,
            *,
            name: str,
    ) -> DBFlower | None:

        flower = await self.session.execute(select(DBFlower).where(DBFlower.name == name))
        return flower.scalar_one_or_none()

    async def get_all_flowers(self) -> Optional[List[ModelType]]:
        flowers = await self.session.execute(select(DBFlower))
        return flowers.scalars().all()

    async def check_flower_name_exists(
            self,
            name: str,
    ) -> bool:

        user = await self.get_by_name(name=name)
        if user:
            return True
        else:
            return False

    async def get_flower(self, flower_id) -> DBFlower:
        flower = await self.session.execute(select(DBFlower).where(DBFlower.id == flower_id))
        return flower.scalar_one_or_none()

    async def create_flower(
            self,
            *,
            obj_in: CreateFlowerReq
            # role: UserRole | None = UserRole.user,
    ) -> DBFlower:

        db_obj = DBFlower.from_orm(obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def del_flower(self, flower_id: UUID):
        response = await self.session.execute(
            select(DBFlower).where(DBFlower.id == flower_id)
        )
        obj = response.scalar_one_or_none()
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
        return obj
