from fastapi import Depends, APIRouter

from crud.order import CRUDOrder
from crud.user import CRUDUser
from depedences.common import RequiredRoles
from depedences.cruds import get_order_crud, get_users_crud
from models.token import TokenData
from models.user import UserRole

from schema import CreateOrderReq

ROUTER = APIRouter(prefix="/orders", tags=["Orders"])

# Получение информации о заказах
@ROUTER.get('/orders')
async def get_all_orders(token: TokenData = Depends(
    RequiredRoles(
        [
            UserRole.admin,
        ]
    )
), order_crud: CRUDOrder = Depends(get_order_crud)):
    return await order_crud.get_all_orders()

# Создание заказа, куда в последствии будут добавляться цветы
@ROUTER.post('/create_order')
async def create_order(
        token: TokenData = Depends(RequiredRoles([UserRole.admin, UserRole.user])),
        order_crud: CRUDOrder = Depends(get_order_crud), user_crud: CRUDUser = Depends(get_users_crud)):
    user = await user_crud.get(id=token.user_id)
    new_order = CreateOrderReq(user_id=token.user_id, customer_name=user.user_name, customer_email=user.email)
    order = await order_crud.create_order(obj_in=new_order)
    return order

# Получение информации  о заказе по id
@ROUTER.get('/get_order')
async def get_order(order_id, token: TokenData = Depends(
    RequiredRoles(
        [
            UserRole.admin,
            UserRole.manager,
            UserRole.user,
        ]
    )
), order_crud: CRUDOrder = Depends(get_order_crud)):
    order = await order_crud.get_order(order_id=order_id)
    print(type(order.flowers))
    return order

# Удаление заказа, вместе с удалением заказа удаляется вся история добавлений цветов к заказу
@ROUTER.delete('/delete_order')
async def delete_order(order_id, token: TokenData = Depends(
    RequiredRoles(
        [
            UserRole.admin,
            UserRole.user,
        ]
    )
), order_crud: CRUDOrder = Depends(get_order_crud)):
    order = await order_crud.del_order(order_id=order_id)
    return order
