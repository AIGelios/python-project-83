import pytest
from page_analyzer import app


@pytest.fixture()
def client():
    app.config['TESTING'] = True
    yield app.test_client()


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode()
    assert '<h1 class="display-3">Анализатор страниц</h1>' in html
    assert '<a class="navbar-brand" href="/">Анализатор страниц</a>' in html
    assert '<a class="nav-link" href="/urls">Сайты</a>' in html


def test_urls(client):
    response = client.get('/urls')
    assert response.status_code == 200
    html = response.data.decode()
    assert '<a class="navbar-brand" href="/">Анализатор страниц</a>' in html
    assert '<a class="nav-link" href="/urls">Сайты</a>' in html
    assert '<h1>Сайты</h1>' in html
    assert '<th>ID</th>' in html
    assert '<th>Имя</th>' in html
    assert '<th>Последняя проверка</th>' in html
    assert '<th>Код ответа</th>' in html


def test_404(client):
    response = client.get('/wrong')
    assert response.status_code == 404
    html = response.data.decode()
    assert '<h1>Страница не найдена</h1>' in html
    assert '<p>Здесь нет того, что вы ищете</p>' in html
    assert '<a href="/">Вернуться на главную</a>'
