import pytest
from fastapi import HTTPException, status
from .views import addParticipant
from ..user.schemas import UserSchema
from ...models.models import Group

class MockGroupRepository:
    def get_by_id(self, id):
        if id == 1:
            return Group(id=1, name="Teste", description="Teste", creator_id="320.041.120-18", participants=[])
        return None

    def create(self, group):
        return group

class MockUserRepository:
    def get_by_id(self, userId):
        if userId == "320.041.120-18":
            return UserSchema(cpf="320.041.120-18", username="Teste", email="Teste@test.com", password="123456", role="admin")
        return None

@pytest.fixture
def mock_group_repository():
    return MockGroupRepository()

@pytest.fixture
def mock_user_repository():
    return MockUserRepository()

def test_add_participant_valid(mock_group_repository, mock_user_repository):
    user_id = "320.041.120-18"
    group_id = 1

    response = addParticipant(user_id, group_id, repository=mock_group_repository, userRepository=mock_user_repository)
    assert response != None
    assert response.participants[0].cpf == user_id
    
def test_add_participant_invalid_user(mock_group_repository, mock_user_repository):
    user_id = "12345678901"
    group_id = 1

    with pytest.raises(HTTPException) as exc:
        addParticipant(user_id, group_id, repository=mock_group_repository, userRepository=mock_user_repository)
    
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "Invalid CPF"
    
def test_add_participant_invalid_group(mock_group_repository, mock_user_repository):
    user_id = "320.041.120-18"
    group_id = 2

    with pytest.raises(HTTPException) as exc:
        addParticipant(user_id, group_id, repository=mock_group_repository, userRepository=mock_user_repository)
    
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "Invalid Group ID"