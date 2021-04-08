from pytest import  fixture
from app.auth.models.user_model import UserModel
from .user_model_interface import UserModelInterface

@fixture
def interface() -> UserModelInterface:
    return UserModelInterface(
        user_id = 1,
        username = 'bob',
        password = 'bob',
        email = 'bob@gmail.com',
        first_name = 'bob',
        last_name = 'bob'
    )


def test_UserModelInterface_create(interface: UserModelInterface):
    assert  interface

def test_UserModelInterface_works(interface: UserModelInterface):
    user_model = UserModel(**interface)
    assert  user_model