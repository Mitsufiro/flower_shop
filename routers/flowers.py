from uuid import UUID

from fastapi import Depends, APIRouter

from crud.flower import CRUDFlower
from crud.order import CRUDOrder
from depedences.cruds import get_flower_crud
from models.token import TokenData
from models.user import UserRole
from schema import CreateFlowerReq
from depedences.common import RequiredRoles

ROUTER = APIRouter(prefix="/flowers", tags=["Flowers"])

# Получение списка цветов в БД
@ROUTER.get('/flowers')
async def get_all_flowers(token: TokenData = Depends(
    RequiredRoles(
        [
            UserRole.admin,
            UserRole.manager,
            UserRole.user,
        ]
    )
), flower_crud: CRUDFlower = Depends(get_flower_crud)):
    return await flower_crud.get_all_flowers()

# Получение информации о цветке в БД по id
@ROUTER.get('/flower')
async def get_flower(flower_id: UUID, flower_crud: CRUDFlower = Depends(get_flower_crud), token: TokenData = Depends(
    RequiredRoles(
        [
            UserRole.admin,
            UserRole.manager,
            UserRole.user,
        ]
    )
), ):
    return await flower_crud.get_flower(flower_id=flower_id)

# Добавление новых цветов в БД
@ROUTER.post('/create_flower')
async def create_flower(new_flower: CreateFlowerReq, flower_crud: CRUDFlower = Depends(get_flower_crud),
                        token: TokenData = Depends(
                            RequiredRoles(
                                [
                                    UserRole.admin,
                                    UserRole.manager,
                                ]
                            )
                        ), ):
    flower = await flower_crud.create_flower(obj_in=new_flower)
    return flower

# Удаление цветка из БД
@ROUTER.delete('/delete_flower')
async def delete_flower(flower_id, flower_crud: CRUDFlower = Depends(get_flower_crud), token: TokenData = Depends(
    RequiredRoles(
        [
            UserRole.admin,
            UserRole.manager,
        ]
    )
)):
    flower = await flower_crud.del_flower(flower_id)
    return flower
