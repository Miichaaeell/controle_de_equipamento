from pytest import mark
from accounts.models import CustomUser


@mark.django_db
def test_custom_user_str():
    user = CustomUser(username='testuser')
    assert str(user) == 'testuser'
