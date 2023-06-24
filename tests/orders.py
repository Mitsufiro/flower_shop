import requests

user_data = {
    "email": "user@example.com",
    "password": "string"
}
auth_token = requests.post("http://127.0.0.1:8000/auth/login", json=user_data).json()['access_token']

current_user = requests.get(f"http://127.0.0.1:8000/auth/users/current?authorization={auth_token}").json()

order_id = dict()


def test_create_order():
    data = {
        "flowers": {},
        "customer_name": "string",
        "total_price": 0,
        "customer_email": "user@example.com",
        "quantity": 0
    }
    response = requests.post(f"http://127.0.0.1:8000/orders/create_order?authorization={auth_token}")
    order_id['order_id'] = response.json()['id']
    assert response.status_code == 200
    order = response.json()
    assert order["customer_name"] == data["customer_name"]
    assert order["customer_email"] == data["customer_email"]
    assert order["quantity"] == data["quantity"]
    assert order["total_price"] == data["total_price"]
    assert order["flowers"] == data["flowers"]


def test_get_all_orders():
    response = requests.get(f"http://127.0.0.1:8000/orders/orders?authorization={auth_token}")
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) > 0


def test_get_order():
    response = requests.get(f"http://127.0.0.1:8000/orders/get_order?order_id={order_id['order_id']}&authorization={auth_token}")
    assert response.status_code == 200
    order = response.json()
    assert order["id"] == order_id['order_id']


def test_delete_order():
    response = requests.delete(
        f"http://127.0.0.1:8000/orders/delete_order?order_id={order_id['order_id']}&authorization={auth_token}")
    assert response.status_code == 200
    deleted_order = response.json()
    assert deleted_order["id"] == order_id['order_id']
