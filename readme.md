<div id="badges" align='center'>
    <a>
        <img src="https://img.shields.io/badge/Python-3.10-green?logo=Python">
    </a>
    <a>
        <img src="https://img.shields.io/badge/FastAPI-0.95-green?logo=fastapi&logoColor=black?style=plastic"/>
    </a>
    <a>
        <img src="https://img.shields.io/badge/alembic-1.10-green?logo=alembic&logoColor=black?style=plastic">
    </a>
    <a>
        <img src="https://img.shields.io/badge/postgresql-13-blue?logo=postgresql&logoColor=white">
    </a>
    <a>
        <img src="https://img.shields.io/badge/SQLalchemy-1.4.41-blue?logo=SQLalchemy">
    </a>
    <a>
        <img src="https://img.shields.io/badge/Docker-20.10.16-green?logo=Docker&logoColor=black?style=plastic">
    </a>
</div>

## Клонируем репозиторий:

    git clone https://github.com/Mitsufiro/flower_shop

## Развертывание

`docker-compose up`

## Migrations

При изменении модели данных необходимо создать миграцию

`docker exec app alembic revision --autogenerate -m "New Migration"`

Для применения изменений, необходимо запустить

`docker exec app alembic upgrade head`

Запуск проекта

`docker-compose up`


<img src="screens/user_create.png" width="300" height="200">

* Создание юзера.

<img src="screens/user_create.png" width="300" height="200">

* Вход.

<img src="screens/login.png" width="300" height="200">

* При входе заполняем данные пользователя и просто берем access token, который нам необходим для использования методов.

* Далее в зависиммости от прав юзера можем использовать методы.

* Получение refresh токена.

<img src="screens/refresh.png" width="300" height="200">

* Выход. Токен добавляется в черный список, при входе черный список очищается.

<img src="screens/logout.png" width="300" height="200">

* Получение информации о текущем юзере.

<img src="screens/current_user.png" width="300" height="200">

* Получение списка всех юзеров.

<img src="screens/user_list_info.png" width="300" height="200">

* Получение подробной информации по id юзера.

<img src="screens/get_admin_user_info.png" width="300" height="200">

* Постраничное получение подробной информации всех юзеров.

<img src="screens/get_admin_user_info.png" width="300" height="200">

* Изменение информации по id юзера. Чтобы изменить конкретное поле, то достаточно оставить только его.

<img src="screens/update_user_info.png" width="300" height="200">
## Finally:

* Удаление по id юзера.

<img src="screens/delete_user.png" width="300" height="200">

* Получение информации обо всех цветах в базе данных.

<img src="screens/all_flowers.png" width="300" height="200">
<img src="screens/flowers_indb.png" width="300" height="200">

* Получение конкретного вида цветов по id.

<img src="screens/create_flower.png" width="300" height="200">

* Добавление новых цветов в БД.

<img src="screens/get_admin_user_info.png" width="300" height="200">

* Получение подробной информации по id юзера.

<img src="screens/get_admin_user_info.png" width="300" height="200">

* Удаление цветка из БД.

<img src="screens/delete_flower.png" width="300" height="200">

* Получение всех заказов.

<img src="screens/all_orders.png" width="300" height="200">

* Создание заказа в который в последствии можно будет добавлять цветы.

<img src="screens/create_order.png" width="300" height="200">

* Получение информации о заказе по id заказа.

<img src="screens/get_order.png" width="300" height="200">

* Удаление заказа по его id.

<img src="screens/del_order.png" width="300" height="200">

* Получение информации о добавлении цветов в заказы. Может понадовиться для статистики.

<img src="screens/all_flowersinorder.png" width="300" height="200">

* Добавление цветов в заказ. При добавлении изменяется общая стоимость заказа, если это новый вид цветов, которого не
  было ранее в заказе, то это указывается в описании заказа.

<img src="screens/add_flowers_to_order.png" width="300" height="200">

* Добавляем несколько разных цветов с разным количеством, ранее уже были добавлены Розы, Астры и Лилии в ассортимент
  магазина:
  <img src="screens/roses.png" width="400" height="100">

  <img src="screens/asters.png" width="400" height="100">

  <img src="screens/lily.png" width="400" height="100">

* Смотрим заказ в который мы все добавили:
  <img src="screens/full_order.png" width="300" height="200">

• Реализован ролевой доступ к API-методам в зависимости от уровня прав пользователя.

• Настроена валидация данных.

• Swagger.

• Подготовлен docker-контейнер с сервисами.

• Универсальный CRUD.

• Написаны тесты для эндпоинтов.

• Реализация асинхронных методов.

• Настроено опциональное изменение данных пользователей (Чтобы изменить нужное поле необходимо оставить только его).

• Настроена аутентификация (Доступ к методам производится путем подачи токена со стороны пользователя).


