import pytest
from fastapi import HTTPException, status
from .views import create
from .schemas import UserSchema

class MockUserRepository:
    def create(self, user):
        return True

@pytest.fixture
def mock_user_repository():
    return MockUserRepository()

def test_create_valid_user(mock_user_repository):
    user = UserSchema(cpf="320.041.120-18", password="Abcdefg1", full_name="John Doe", email="email@email.com", username="johndoe", role="user")

    response = create(user, repository=mock_user_repository)
    assert response is True

def test_create_invalid_cpf(mock_user_repository):
    user = UserSchema(cpf="123.456.789-0", password="Abcdefg1", full_name="John Doe", email="email@email.com", username="johndoe", role="user")

    with pytest.raises(HTTPException) as exc:
        create(user, repository=mock_user_repository)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "Invalid CPF"

def test_create_invalid_password(mock_user_repository):

    user = UserSchema(cpf="320.041.120-18", password="abcdefg1", full_name="John Doe", email="email@email.com", username="johndoe", role="user")

    with pytest.raises(HTTPException) as exc:
        create(user, repository=mock_user_repository)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "Invalid password"