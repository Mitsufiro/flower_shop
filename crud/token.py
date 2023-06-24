from uuid import UUID
from sqlalchemy import select
from crud.base import CRUDBase
from models.user import DBTokenbl
from schema import ExpireTokenReq, TokenSchema


class CRUDToken(CRUDBase[DBTokenbl, TokenSchema, ExpireTokenReq]):
    """
       Wrapper to handle Token CRUD operations.
    """
    async def create_tokenbl(
            self,
            *,
            obj_in: ExpireTokenReq
    ) -> DBTokenbl:
        db_obj = DBTokenbl.from_orm(obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def check_token_in_bl(
            self,
            user_id: UUID,
    ):
        user = await self.session.execute(select(DBTokenbl).where(DBTokenbl.user_id == user_id))

        return user.scalars().all()

    async def del_from_bl(self, user_id: UUID):
        response = await self.session.execute(
            select(DBTokenbl).where(DBTokenbl.user_id == user_id)
        )
        obj = response.scalars().all()
        if obj:
            for i in obj:
                await self.session.delete(i)
                await self.session.commit()
        return obj
