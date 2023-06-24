import requests

user_data = {
    "email": "user@example.com",
    "password": "string"
}
auth_token = requests.post("http://127.0.0.1:8000/auth/login", json=user_data).json()['access_token']
flower_id = []


def test_create_flower():
    flower_data = {
        "name": "Rose",
        "color": "red",
        "price": 10.0,
        "in_stock": True
    }
    response = requests.post(f"http://127.0.0.1:8000/flowers/create_flower?authorization={auth_token}",
                             json=flower_data)
    assert response.status_code == 200
    response_data = response.json()
    flower_id.append(response_data.get("id"))
    print(flower_id[0])
    assert response_data.get("name") == "Rose"
    assert response_data.get("color") == "red"
    assert response_data.get("price") == 10.0
    assert response_data.get("in_stock") is True


def test_get_all_flowers():
    response = requests.get(f"http://127.0.0.1:8000/flowers/flowers?authorization={auth_token}")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)


def test_get_flower():
    get_response = requests.get(
        f"http://127.0.0.1:8000/flowers/flower?flower_id={flower_id[0]}&authorization={auth_token}")
    assert get_response.status_code == 200
    get_response_data = get_response.json()
    assert get_response_data.get("name") == "Rose"
    assert get_response_data.get("color") == "red"
    assert get_response_data.get("price") == 10.0
    assert get_response_data.get("in_stock") is True


def test_delete_flower():
    del_response = requests.delete(
        f"http://127.0.0.1:8000/flowers/delete_flower?flower_id={flower_id[0]}&authorization={auth_token}")
    assert del_response.status_code == 200
    del_response_data = del_response.json()
    assert del_response_data.get("name") == "Rose"
    assert del_response_data.get("color") == "red"
    assert del_response_data.get("price") == 10.0
    assert del_response_data.get("in_stock") is True
