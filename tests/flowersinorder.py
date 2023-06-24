import uuid

import requests

user_data = {
    "email": "user@example.com",
    "password": "string"
}
auth_token = requests.post("http://127.0.0.1:8000/auth/login", json=user_data).json()['access_token']

flower_data = {
    "name": "Rose",
    "color": "red",
    "price": 5.99,
    "in_stock": True
}
create_response = requests.post(f"http://127.0.0.1:8000/flowers/create_flower?authorization={auth_token}",
                                json=flower_data)
created_flower = create_response.json()
create_order_response = requests.post(f"http://127.0.0.1:8000/orders/create_order?authorization={auth_token}")
created_order = create_order_response.json()


def test_get_all_flowers_in_order():
    response = requests.get(f"http://127.0.0.1:8000/flowersinorder/flowersinorder?authorization={auth_token}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_flower_to_order():
    flowers_in_order_data = {
        'quantity': 3,
        'flower_id': created_flower["id"],
        'order_id': created_order["id"]
    }
    add_flower_response = requests.post(
        f"http://127.0.0.1:8000/flowersinorder/add_flower_to_order?authorization={auth_token}",
        json=flowers_in_order_data)
    assert add_flower_response.status_code == 200
    added_flowers = add_flower_response.json()
    del_order = requests.delete(
        f"http://127.0.0.1:8000/orders/delete_order?order_id={created_order['id']}&authorization={auth_token}")
    del_flowers = requests.delete(
        f"http://127.0.0.1:8000/flowers/delete_flower?flower_id={created_flower['id']}&authorization={auth_token}")
    assert isinstance(uuid.UUID(added_flowers["id"]), uuid.UUID)
    assert added_flowers["flower_id"] == created_flower["id"]
    assert added_flowers["order_id"] == created_order["id"]
    assert added_flowers["quantity"] == 3


