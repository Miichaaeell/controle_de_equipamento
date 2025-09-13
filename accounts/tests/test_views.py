import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group


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
    assert "saudacao" in response.context


@pytest.mark.django_db
def test_login_view_get_status_302_dashboard(client, create_user_test):
    url = reverse('login')
    user = create_user_test
    user.user_permissions.add(
        Permission.objects.get(codename='view_controllerstock')
    )
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')


@pytest.mark.django_db
def test_login_view_get_status_302_stock(client, create_user_test):
    url = reverse('login')
    user = create_user_test
    # Adiciona grupo técnico opcionalmente
    tecnico_group = Group.objects.create(name='tecnico')
    user.groups.add(tecnico_group)
    client.force_login(user)
    client.groups = 'tecnico'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_post_status_302(client, create_user_test):
    login_url = reverse("login")
    response = client.post(login_url, {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.wsgi_request.user.username == 'testuser'
    assert response.wsgi_request.user.is_authenticated
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_post_status_302_dashboard(client, create_user_test):
    url = reverse('login')
    user = create_user_test
    user.user_permissions.add(
        Permission.objects.get(codename='view_controllerstock')
    )
    response = client.post(url,{
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 302
    assert response.url == reverse('dashboard')


@pytest.mark.django_db
def test_login_view_post_status_302_stock(client, create_user_test):
    url = reverse('login')
    user = create_user_test
    # Adiciona grupo técnico opcionalmente
    tecnico_group = Group.objects.create(name='tecnico')
    user.groups.add(tecnico_group)
    response = client.post(url,{
        "username": "testuser",
        "password": "testpassword"
    })
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
    assert "saudacao" in response.context


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


@pytest.mark.django_db
def test_detail_account_view_status_404(client, create_user_test):
    url = reverse('detail_account', args=[0])
    client.login(username=create_user_test.username,
                 password='testpassword'
                 )
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_detail_account_view_status_302(client, create_user_test):
    url = reverse('detail_account', args=[create_user_test.id])
    response = client.get(url)
    assert response.status_code == 302


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
            'confirmation_password': 'teste123'
        }
    )
    assert response.wsgi_request.user.username == 'testuser'
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_password_change_diferences_new_password_view(client, create_user_test):
    url = reverse('password_change')
    client.login(
        username=create_user_test.username,
        password='testpassword'
    )
    response = client.post(
        url,
        {
            'old_password': 'testpassword',
            'new_password': 'teste123',
            'confirmation_password': 'mudar123'
        }
    )
    assert response.wsgi_request.user.username == 'testuser'
    assert response.status_code == 200
    assert 'As senhas não são iguais' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_post_passoword_change_diference_old_password_view(client, create_user_test):
    url = reverse('password_change')
    client.login(
        username=create_user_test.username,
        password='testpassword'
    )
    response = client.post(
        url,
        {
            'old_password': 'errorpassword',
            'new_password': 'teste123',
            'confirmation_password': 'teste123'
        }
    )
    assert response.wsgi_request.user.username == 'testuser'
    assert response.status_code == 200
    assert "erro" in response.context
    assert response.context["erro"] == "Senha atual não confere"
    assert 'Senha atual não confere' in response.content.decode('utf-8')
