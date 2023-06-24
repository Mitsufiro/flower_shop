from fastapi import Depends, APIRouter, HTTPException

from crud.flower import CRUDFlower
from crud.flowers_in_order import CRUDFlowersInOrder
from depedences.common import RequiredRoles
from crud.order import CRUDOrder
from depedences.cruds import get_flowers_in_order_crud, get_flower_crud, get_order_crud
from models.token import TokenData
from models.user import UserRole
from schema import CreateFlsInOrdr

ROUTER = APIRouter(prefix="/flowersinorder", tags=["FlowersInOrder"])


# История добавлений цветов к заказам
@ROUTER.get('/flowersinorder')
async def get_all_flowers_in_order(flowers_in_order_crud: CRUDOrder = Depends(get_flowers_in_order_crud),
                                   token: TokenData = Depends(
                                       RequiredRoles(
                                           [
                                               UserRole.admin,
                                           ]
                                       )
                                   )):
    return await flowers_in_order_crud.get_all_flowers_in_order()


# Добавление цветов к заказу, тут увеличивается цена всего заказа в зависимости от того какие цветы добавлены и сколько
@ROUTER.post('/add_flower_to_order')
async def add_flower_to_order(new_flowers_in_order: CreateFlsInOrdr,
                              flower_crud: CRUDFlower = Depends(get_flower_crud),
                              order_crud: CRUDOrder = Depends(get_order_crud),
                              flowers_in_order_crud: CRUDFlowersInOrder = Depends(get_flowers_in_order_crud),
                              token: TokenData = Depends(
                                  RequiredRoles(
                                      [
                                          UserRole.admin,
                                          UserRole.user,
                                      ]
                                  )
                              ), ):
    flower = await flower_crud.get_flower(flower_id=new_flowers_in_order.flower_id)
    order = await order_crud.get_order(order_id=new_flowers_in_order.order_id)

    await order_crud.add_quantity(order_id=new_flowers_in_order.order_id, quantity=new_flowers_in_order.quantity,
                                  price=flower.price * new_flowers_in_order.quantity, flower=flower.name)
    flowers = await flowers_in_order_crud.add_flowers(obj_in=new_flowers_in_order)
    if not flowers:
        return HTTPException(status_code=404)
    return flowers
