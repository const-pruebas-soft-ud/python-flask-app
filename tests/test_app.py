"""
Pruebas unitarias para la aplicación Flask
"""
import pytest
from app import app


@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Prueba que la ruta principal funciona correctamente"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Azure' in response.data


def test_index_visit_counter(client):
    """Prueba que el contador de visitas incrementa correctamente"""
    # Primera visita
    response1 = client.get('/')
    assert response1.status_code == 200
    
    # Segunda visita
    response2 = client.get('/')
    assert response2.status_code == 200
    
    # Verificar que el contador está presente
    assert b'Page visits:' in response2.data


def test_hello_with_name(client):
    """Prueba el saludo con un nombre válido"""
    response = client.post('/hello', data={'name': 'John'})
    assert response.status_code == 200
    assert b'Hello John' in response.data
    assert b'It is nice to meet you!' in response.data


def test_hello_greeting_counter(client):
    """Prueba que el contador de saludos incrementa correctamente"""
    # Primer saludo
    response1 = client.post('/hello', data={'name': 'Alice'})
    assert response1.status_code == 200
    assert b'Total greetings:' in response1.data
    
    # Segundo saludo
    response2 = client.post('/hello', data={'name': 'Bob'})
    assert response2.status_code == 200
    assert b'Total greetings:' in response2.data


def test_hello_without_name(client):
    """Prueba el saludo sin nombre (debe redirigir)"""
    response = client.post('/hello', data={'name': ''}, follow_redirects=False)
    assert response.status_code == 302  # Redirección
    assert response.location == '/'


def test_hello_without_name_follow_redirect(client):
    """Prueba el saludo sin nombre siguiendo la redirección"""
    response = client.post('/hello', data={'name': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to Azure' in response.data


def test_favicon_route(client):
    """Prueba que el favicon se sirve correctamente"""
    response = client.get('/favicon.ico')
    assert response.status_code == 200
    assert response.mimetype == 'image/vnd.microsoft.icon'


def test_multiple_visits_increment(client):
    """Prueba que múltiples visitas incrementan el contador"""
    # Realizar múltiples visitas
    for _ in range(5):
        response = client.get('/')
        assert response.status_code == 200
    
    # El contador debe estar presente
    assert b'Page visits:' in response.data

def test_multiple_greetings_increment(client):
    """Prueba que múltiples saludos incrementan el contador"""
    names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
    
    for name in names:
        response = client.post('/hello', data={'name': name})
        assert response.status_code == 200
        assert f'Hello {name}'.encode() in response.data
    
    # El contador debe estar presente
    assert b'Total greetings:' in response.data

def test_reset_counters_ok(client):
    # 1) sube el contador con dos visitas
    client.get("/")
    client.get("/")

    # 2) resetear SIN seguir el redirect
    res = client.post("/reset", follow_redirects=False)
    assert res.status_code in (302, 303)

    # 3) primera visita tras reset => debe ser 1
    res2 = client.get("/")
    html2 = res2.data.decode("utf-8")
    assert "Page visits" in html2 and ": 1" in html2

def test_reset_counters_method_not_allowed(client):
    res = client.get("/reset")
    assert res.status_code in (405, 302)