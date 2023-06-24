# тесты для регистрации, аутентификации, редактирования пользователей
import requests

localhost = 'http://127.0.0.1:8000'

auth = dict()


def test_create_user():
    user_data = {
        "user_name": "testuser",
        "email": "test@example.com",
        "is_active": True,
        "role": "admin",
        "password": "testpass",
    }
    response = requests.post(f"{localhost}/auth/create", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["user_name"] == user_data["user_name"]
    assert created_user["role"] == user_data["role"]


def test_create_duplicate_user():
    user_data = {
        "user_name": "testuser",
        "email": "test@example.com",
        "is_active": True,
        "role": "admin",
        "password": "testpass",
    }
    response = requests.post(f"{localhost}/auth/create", json=user_data)
    assert response.status_code == 409


def test_login_by_email():
    login_data = {
        "email": "test@example.com",
        "password": "testpass",
    }
    response = requests.post(f"{localhost}/auth/login", json=login_data)
    assert response.status_code == 200
    tokens = response.json()
    auth['access_token'] = tokens['access_token']
    auth['refresh_token'] = tokens['refresh_token']
    assert "access_token" in tokens
    assert "refresh_token" in tokens


def test_login_with_invalid_credentials():
    login_data = {
        "email": "jane.doe@example.com",
        "password": "wrongpassword"
    }
    response = requests.post(f"{localhost}/auth/login", json=login_data)
    assert response.status_code == 401


def test_refresh_token():
    refresh_data = {"token": auth['refresh_token']}
    response = requests.post(f"{localhost}/auth/auth/refresh?authorization={auth['access_token']}",
                             json=refresh_data)
    assert response.status_code == 200
    new_tokens = response.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens


def test_logout():
    response = requests.post(f"{localhost}/auth/logout?authorization={auth['access_token']}")
    assert response.status_code == 200


def test_get_current_user():
    login_data = {
        "email": "test@example.com",
        "password": "testpass"
    }
    login = requests.post(f"{localhost}/auth/login", json=login_data).json()
    auth['access_token'] = login['access_token']
    response = requests.get(f"{localhost}/auth/users/current?authorization={auth['access_token']}")
    assert response.status_code == 200
    current_user = response.json()
    assert current_user["email"] == login_data["email"]


def test_get_all_users():
    response = requests.get(f"{localhost}/auth/get_all_users?authorization={auth['access_token']}")
    assert response.status_code == 200
    all_users = response.json()
    assert isinstance(all_users, list)


user_id = dict()


def test_get_user_list():
    response = requests.get(f"{localhost}/auth/private/users?authorization={auth['access_token']}&page=1&size=50")
    assert response.status_code == 200
    user_list = response.json()
    items = user_list['items']
    for user in items:
        if user["user_name"] == "testuser":
            user_id['id'] = user['id']
    assert isinstance(user_list, dict)
    assert "items" in user_list


def test_get_user_by_id():
    response = requests.get(
        f"{localhost}/auth/private/users/{user_id['id']}?user_id={user_id['id']}&authorization={auth['access_token']}")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == user_id['id']


def test_get_user():
    email = "test@example.com"
    response = requests.get(f"{localhost}/auth/get_user?email={email}")
    assert response.status_code == 200
    is_active = response.json()
    assert is_active is True


def test_edit_user_by_id():
    update_data = {
        'user_name': "NewFullName",
        'email': "testtest@example.com",
        'is_active': True,
        'role': "manager",
    }
    response = requests.put(f"{localhost}/auth/update/{user_id['id']}?authorization={auth['access_token']}",
                            json=update_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["email"] == update_data['email']
    assert updated_user["is_active"] == update_data['is_active']
    assert updated_user["role"] == update_data['role']


#
#
def test_edit_current_user():
    update_data = {
        "user_name": "testtesttest",
        "email": "usertesttesttest@example.com"
    }
    response = requests.put(f"{localhost}/auth/update_current_user?authorization={auth['access_token']}",
                            json=update_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["email"] == update_data['email']
    assert updated_user["user_name"] == update_data['user_name']


def test_delete_user():
    response = requests.delete(
        f"{localhost}/auth/private/user/delete?user_id={user_id['id']}&authorization={auth['access_token']}")
    assert response.status_code == 200
