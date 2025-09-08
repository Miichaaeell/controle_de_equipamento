import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.fixture
def create_user_test():
    User = get_user_model()
    username = "testuser"
    password = "testpassword"
    user = User.objects.create_user(username=username, password=password)
    return user


# testes views de login
def test_login_view_status_200(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_status_302(client, create_user_test):
    login_url = reverse("login")
    response = client.post(login_url, {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.wsgi_request.user.username == 'testuser'
    assert response.wsgi_request.user.is_authenticated
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_fail_view_status_200(client):
    login_url = reverse("login")
    response = client.post(login_url, {
        "username": "wronguser",
        "password": "wrongpassword"
    })
    assert response.status_code == 200
    assert b'Usu\xc3\xa1rio ou Senha inv\xc3\xa1lidos' in response.content


# testes views de logout
@pytest.mark.django_db
def test_logout_view(client, create_user_test):
    url = reverse('logout')
    client.login(username=create_user_test.username,
                 password='testpassword'
                 )
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login')


# testes de view de detalhe da conta
@pytest.mark.django_db
def test_detail_account_view_status_200(client, create_user_test):
    url = reverse('detail_account', args=[create_user_test.id])
    client.login(username=create_user_test.username,
                 password='testpassword'
                 )
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_account_view_status_302(client, create_user_test):
    url = reverse('detail_account', args=[create_user_test.id])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == f"{reverse('login')}?next={url}"


# testes de view de alteração de senha
@pytest.mark.django_db
def test_get_password_change_view_status_200(client, create_user_test):
    url = reverse('password_change')
    client.login(username=create_user_test.username,
                 password='testpassword'
                 )
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_password_change_view_status_302(client, create_user_test):
    url = reverse('password_change')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_password_change_view(client, create_user_test):
    url = reverse('password_change')
    client.login(username=create_user_test.username,
                 password='testpassword'
                 )
    response = client.post(
        url,
        {
            'old_password': 'testpassword',
            'new_password': 'teste123',
            'confirmation_passowrd': 'teste123'
        }
    )
    assert response.wsgi_request.user.username == 'testuser'
    assert response.status_code == 302
