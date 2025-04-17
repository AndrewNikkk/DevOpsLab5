from fastapi.testclient import TestClient

from src.main import app
from src.fake_db.database import db

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    },
    {
        'id': 3,
        'name': 'Vladimir Vladimirov',
        'email': 'v.v.vladimirov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'non_existent_email'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
    

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    response = client.post("/api/v1/user", json=users[2])
    assert response.status_code == 201
    assert isinstance(response.json(), int)
    
    user_in_db = db.get_user_by_email(users[2]["email"])
    assert user_in_db is not None
    assert user_in_db["name"] == users[2]["name"]
    assert user_in_db["email"] == users[2]["email"]

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    response = client.post("/api/v1/user", json=users[1])
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    response = client.delete("/api/v1/user", params={'email': users[2]['email']})
    assert response.status_code == 204
    assert db.get_user_by_email(users[2]['email']) is None
    