"""
Pruebas unitarias para la aplicación Flask
"""
import pytest
from unittest.mock import patch, MagicMock
import os

# Evitar error de importación cuando no hay .env en entorno de CI/local
os.environ.setdefault('SUPABASE_URL', 'http://example')
os.environ.setdefault('SUPABASE_KEY', 'dummy')

from app import app, register_visitor
from datetime import datetime


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
    assert b'Total de saludos en esta sesi' in response1.data  # Actualizado el texto
    
    # Segundo saludo
    response2 = client.post('/hello', data={'name': 'Bob'})
    assert response2.status_code == 200
    assert b'Total de saludos en esta sesi' in response2.data  # Actualizado el texto


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
    assert b'Total de saludos en esta sesi' in response.data  # Actualizado el texto


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
    """Prueba que solo POST está permitido en /reset"""
    response = client.get("/reset")
    assert response.status_code == 405  # Method Not Allowed


# ============================================================================
# PRUEBAS DE REGISTRO DE VISITANTES (HU1)
# ============================================================================

@patch('app.supabase')
def test_register_visitor_new_user(mock_supabase):
    """Prueba el registro de un nuevo visitante"""
    # Configurar mock para simular que el visitante no existe
    mock_supabase.table().select().eq().execute.return_value = MagicMock(data=[])
    
    # Configurar mock para la inserción
    mock_insert_response = MagicMock()
    mock_insert_response.data = [{
        'id': 1,
        'name': 'Test User',
        'visit_count': 1,
        'first_visit': datetime.now().isoformat(),
        'last_visit': datetime.now().isoformat(),
        'ip_address': '127.0.0.1'
    }]
    mock_supabase.table().insert().execute.return_value = mock_insert_response
    
    # Ejecutar la función
    result = register_visitor('Test User', '127.0.0.1')
    
    # Verificaciones
    assert result is not None
    assert result['name'] == 'Test User'
    assert result['visit_count'] == 1
    assert result['ip_address'] == '127.0.0.1'


@patch('app.supabase')
def test_register_visitor_existing_user(mock_supabase):
    """Prueba la actualización de un visitante existente"""
    # Configurar mock para simular que el visitante existe
    existing_visitor = {
        'id': 1,
        'name': 'Existing User',
        'visit_count': 5,
        'first_visit': '2025-10-25T10:00:00',
        'last_visit': '2025-10-29T10:00:00',
        'ip_address': '127.0.0.1'
    }
    mock_supabase.table().select().eq().execute.return_value = MagicMock(
        data=[existing_visitor]
    )
    
    # Configurar mock para la actualización
    updated_visitor = existing_visitor.copy()
    updated_visitor['visit_count'] = 6
    updated_visitor['last_visit'] = datetime.now().isoformat()
    mock_supabase.table().update().eq().execute.return_value = MagicMock(
        data=[updated_visitor]
    )
    
    # Ejecutar la función
    result = register_visitor('Existing User', '127.0.0.1')
    
    # Verificaciones
    assert result is not None
    assert result['name'] == 'Existing User'
    assert result['visit_count'] == 6


@patch('app.supabase')
def test_register_visitor_without_ip(mock_supabase):
    """Prueba el registro sin dirección IP"""
    # Configurar mock
    mock_supabase.table().select().eq().execute.return_value = MagicMock(data=[])
    mock_insert_response = MagicMock()
    mock_insert_response.data = [{
        'id': 1,
        'name': 'No IP User',
        'visit_count': 1,
        'ip_address': None
    }]
    mock_supabase.table().insert().execute.return_value = mock_insert_response
    
    # Ejecutar sin IP
    result = register_visitor('No IP User', None)
    
    # Verificaciones
    assert result is not None
    assert result['name'] == 'No IP User'
    assert result['ip_address'] is None


@patch('app.supabase')
def test_hello_registers_visitor(mock_supabase, client):
    """Prueba que la ruta /hello registra al visitante en la BD"""
    # Configurar mock para nuevo visitante
    mock_supabase.table().select().eq().execute.return_value = MagicMock(data=[])
    mock_insert_response = MagicMock()
    mock_insert_response.data = [{
        'id': 1,
        'name': 'John Doe',
        'visit_count': 1,
        'first_visit': datetime.now().isoformat(),
        'last_visit': datetime.now().isoformat(),
        'ip_address': '127.0.0.1'
    }]
    mock_supabase.table().insert().execute.return_value = mock_insert_response
    
    # Hacer request
    response = client.post('/hello', data={'name': 'John Doe'})
    
    # Verificaciones
    assert response.status_code == 200
    assert b'John Doe' in response.data
    assert b'Informaci' in response.data  # "Información de Visita"


@patch('app.supabase')
def test_hello_shows_visit_count(mock_supabase, client):
    """Prueba que se muestra el número de visitas correcto"""
    # Simular visitante con 3 visitas previas
    existing_visitor = {
        'id': 1,
        'name': 'Repeat Visitor',
        'visit_count': 3,
        'first_visit': '2025-10-25T10:00:00',
        'last_visit': '2025-10-29T10:00:00',
        'ip_address': '127.0.0.1'
    }
    mock_supabase.table().select().eq().execute.return_value = MagicMock(
        data=[existing_visitor]
    )
    
    # Configurar actualización a 4 visitas
    updated = existing_visitor.copy()
    updated['visit_count'] = 4
    mock_supabase.table().update().eq().execute.return_value = MagicMock(
        data=[updated]
    )
    
    # Hacer request
    response = client.post('/hello', data={'name': 'Repeat Visitor'})
    
    # Verificaciones
    assert response.status_code == 200
    assert b'Repeat Visitor' in response.data
    # Verificar que muestra el número de visitas
    html = response.data.decode('utf-8')
    assert '4' in html  # El contador debe mostrar 4


@patch('app.supabase')
def test_hello_shows_first_visit_message(mock_supabase, client):
    """Prueba que se muestra mensaje de primera visita"""
    # Configurar mock para nuevo visitante
    mock_supabase.table().select().eq().execute.return_value = MagicMock(data=[])
    mock_insert_response = MagicMock()
    mock_insert_response.data = [{
        'id': 1,
        'name': 'First Timer',
        'visit_count': 1,
        'first_visit': datetime.now().isoformat(),
        'last_visit': datetime.now().isoformat(),
        'ip_address': '127.0.0.1'
    }]
    mock_supabase.table().insert().execute.return_value = mock_insert_response
    
    # Hacer request
    response = client.post('/hello', data={'name': 'First Timer'})
    
    # Verificaciones
    assert response.status_code == 200
    assert b'primera visita' in response.data


@patch('app.supabase')
def test_hello_shows_return_visit_message(mock_supabase, client):
    """Prueba que se muestra mensaje de visita de retorno"""
    # Simular visitante que regresa
    existing_visitor = {
        'id': 1,
        'name': 'Return Visitor',
        'visit_count': 2,
        'first_visit': '2025-10-25T10:00:00',
        'last_visit': '2025-10-29T10:00:00',
        'ip_address': '127.0.0.1'
    }
    mock_supabase.table().select().eq().execute.return_value = MagicMock(
        data=[existing_visitor]
    )
    
    updated = existing_visitor.copy()
    updated['visit_count'] = 3
    mock_supabase.table().update().eq().execute.return_value = MagicMock(
        data=[updated]
    )
    
    # Hacer request
    response = client.post('/hello', data={'name': 'Return Visitor'})
    
    # Verificaciones
    assert response.status_code == 200
    assert b'Bienvenido de nuevo' in response.data
    html = response.data.decode('utf-8')
    assert 'visita #3' in html


@patch('app.supabase')
def test_hello_captures_ip_address(mock_supabase, client):
    """Prueba que se captura la dirección IP del visitante"""
    # Configurar mock
    mock_supabase.table().select().eq().execute.return_value = MagicMock(data=[])
    
    captured_data = {}
    
    def capture_insert(data):
        nonlocal captured_data
        captured_data.update(data)
        mock_response = MagicMock()
        mock_response.data = [{
            'id': 1,
            'name': data['name'],
            'visit_count': 1,
            'first_visit': data.get('first_visit'),
            'last_visit': data.get('last_visit'),
            'ip_address': data.get('ip_address')
        }]
        mock_execute = MagicMock()
        mock_execute.execute.return_value = mock_response
        return mock_execute
    
    mock_supabase.table().insert.side_effect = capture_insert
    
    # Hacer request
    response = client.post('/hello', data={'name': 'IP Test User'})
    
    # Verificaciones
    assert response.status_code == 200
    # En tests, la IP suele ser 127.0.0.1
    assert 'ip_address' in captured_data
    assert captured_data['ip_address'] is not None


@patch('app.supabase')
def test_register_visitor_database_error(mock_supabase):
    """Prueba el manejo de errores de base de datos"""
    # Simular un error de base de datos
    mock_supabase.table().select().eq().execute.side_effect = Exception("Database error")
    
    # Ejecutar la función
    result = register_visitor('Error User', '127.0.0.1')
    
    # Debe retornar None o dict vacío en caso de error
    assert result is None or result == {}


@patch('app.supabase')
def test_list_visitors_shows_rows(mock_supabase, client):
    """Prueba que la ruta /visitors muestra filas cuando hay datos"""
    rows = [{
        'name': 'Alice',
        'visit_count': 2,
        'first_visit': '2025-10-29T10:00:00',
        'last_visit': '2025-10-29T12:00:00'
    }]
    mock_resp = MagicMock()
    mock_resp.data = rows
    mock_supabase.table().select().order().execute.return_value = mock_resp

    response = client.get('/visitors')
    assert response.status_code == 200
    assert b'Alice' in response.data
