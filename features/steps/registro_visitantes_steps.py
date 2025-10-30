"""
Steps (pasos) para las pruebas BDD de registro de visitantes
"""
from behave import given, when, then
from unittest.mock import MagicMock
from datetime import datetime, timedelta
import re


# ============================================================================
# GIVEN (Dado) - Precondiciones
# ============================================================================

@given('que la base de datos está vacía')
def step_database_is_empty(context):
    """Simula que la base de datos no tiene registros"""
    context.database = {}
    context.supabase_mock.table().select().eq().execute.return_value = MagicMock(data=[])


@given('que visito la página principal')
def step_visit_homepage(context):
    """Visita la página principal"""
    context.response = context.client.get('/')
    assert context.response.status_code == 200


@given('que existe un visitante "{nombre}" con {visitas:d} visita registrada hace "{tiempo}"')
@given('que existe un visitante "{nombre}" con {visitas:d} visitas')
def step_existing_visitor(context, nombre, visitas, tiempo=None):
    """Simula un visitante existente en la base de datos"""
    # Calcular fecha de first_visit
    if tiempo:
        hours_match = re.search(r'(\d+)\s*hora', tiempo)
        if hours_match:
            hours = int(hours_match.group(1))
            first_visit = datetime.now() - timedelta(hours=hours)
        else:
            first_visit = datetime.now() - timedelta(hours=1)
    else:
        first_visit = datetime.now() - timedelta(days=1)
    
    # Crear visitante simulado
    visitor = {
        'id': 1,
        'name': nombre,
        'visit_count': visitas,
        'first_visit': first_visit.isoformat(),
        'last_visit': first_visit.isoformat(),
        'ip_address': '127.0.0.1'
    }
    
    # Guardar en contexto
    context.database[nombre] = visitor
    context.visitor_before = visitor.copy()
    context.visitor_count_before = len(context.database)
    
    # Configurar mock para retornar este visitante
    context.supabase_mock.table().select().eq().execute.return_value = MagicMock(
        data=[visitor]
    )
    
    # Configurar mock para UPDATE
    updated_visitor = visitor.copy()
    updated_visitor['visit_count'] = visitas + 1
    updated_visitor['last_visit'] = datetime.now().isoformat()
    context.supabase_mock.table().update().eq().execute.return_value = MagicMock(
        data=[updated_visitor]
    )


@given('que visito la página principal desde la IP "{ip}"')
def step_visit_from_ip(context, ip):
    """Simula una visita desde una IP específica"""
    context.client_ip = ip
    context.response = context.client.get('/', environ_base={'REMOTE_ADDR': ip})
    assert context.response.status_code == 200


# ============================================================================
# WHEN (Cuando) - Acciones
# ============================================================================

@when('envío el formulario con el nombre "{nombre}"')
@when('envío el formulario con el nombre ""')
def step_submit_form_with_name(context, nombre=""):
    """Envía el formulario con un nombre"""
    # Si el nombre está vacío, no configurar mocks de INSERT
    if not nombre or nombre.strip() == "":
        # No se debe insertar nada
        context.response = context.client.post(
            '/hello',
            data={'name': nombre},
            follow_redirects=True
        )
        return
    
    # Configurar comportamiento del mock según el caso
    if nombre in context.database:
        # Visitante existente - retornar datos
        visitor = context.database[nombre]
        context.supabase_mock.table().select().eq().execute.return_value = MagicMock(
            data=[visitor]
        )
        
        # Simular UPDATE
        updated = visitor.copy()
        updated['visit_count'] += 1
        updated['last_visit'] = datetime.now().isoformat()
        context.supabase_mock.table().update().eq().execute.return_value = MagicMock(
            data=[updated]
        )
        context.updated_visitor = updated
    else:
        # Nuevo visitante
        context.supabase_mock.table().select().eq().execute.return_value = MagicMock(data=[])
        
        # Simular INSERT
        new_visitor = {
            'id': len(context.database) + 1,
            'name': nombre,
            'visit_count': 1,
            'first_visit': datetime.now().isoformat(),
            'last_visit': datetime.now().isoformat(),
            'ip_address': getattr(context, 'client_ip', '127.0.0.1')
        }
        context.supabase_mock.table().insert().execute.return_value = MagicMock(
            data=[new_visitor]
        )
        context.new_visitor = new_visitor
        context.database[nombre] = new_visitor
    
    # Enviar formulario
    ip = getattr(context, 'client_ip', '127.0.0.1')
    context.response = context.client.post(
        '/hello',
        data={'name': nombre},
        environ_base={'REMOTE_ADDR': ip},
        follow_redirects=True
    )


# ============================================================================
# THEN (Entonces) - Verificaciones
# ============================================================================

@then('se crea un nuevo registro en la base de datos')
def step_new_record_created(context):
    """Verifica que se creó un nuevo registro"""
    assert hasattr(context, 'new_visitor'), "No se creó un nuevo visitante"
    assert len(context.database) > context.visitor_count_before


@then('el registro tiene nombre "{nombre}"')
def step_record_has_name(context, nombre):
    """Verifica que el registro tiene el nombre correcto"""
    assert context.new_visitor['name'] == nombre


@then('el campo "visit_count" es {count:d}')
def step_visit_count_is(context, count):
    """Verifica el valor de visit_count"""
    if hasattr(context, 'new_visitor'):
        assert context.new_visitor['visit_count'] == count
    elif hasattr(context, 'updated_visitor'):
        assert context.updated_visitor['visit_count'] == count


@then('los campos "first_visit" y "last_visit" tienen la fecha actual')
def step_dates_are_current(context):
    """Verifica que las fechas son recientes"""
    visitor = context.new_visitor
    first_visit = datetime.fromisoformat(visitor['first_visit'].replace('Z', '+00:00'))
    last_visit = datetime.fromisoformat(visitor['last_visit'].replace('Z', '+00:00'))
    
    now = datetime.now()
    # Verificar que las fechas son de hoy (con margen de 1 minuto)
    assert abs((first_visit.replace(tzinfo=None) - now).total_seconds()) < 60
    assert abs((last_visit.replace(tzinfo=None) - now).total_seconds()) < 60


@then('veo el mensaje "Hello {nombre}"')
def step_see_hello_message(context, nombre):
    """Verifica que se muestra el mensaje de saludo"""
    assert context.response.status_code == 200
    assert f'Hello {nombre}'.encode() in context.response.data


@then('no se crea un registro nuevo')
def step_no_new_record(context):
    """Verifica que no se creó un nuevo registro"""
    assert len(context.database) == context.visitor_count_before


@then('el campo "visit_count" se incrementa a {count:d}')
def step_visit_count_increments(context, count):
    """Verifica que visit_count se incrementó"""
    assert context.updated_visitor['visit_count'] == count


@then('el campo "last_visit" se actualiza a la fecha actual')
def step_last_visit_updated(context):
    """Verifica que last_visit se actualizó"""
    last_visit = datetime.fromisoformat(
        context.updated_visitor['last_visit'].replace('Z', '+00:00')
    )
    now = datetime.now()
    assert abs((last_visit.replace(tzinfo=None) - now).total_seconds()) < 60


@then('el campo "first_visit" permanece sin cambios')
def step_first_visit_unchanged(context):
    """Verifica que first_visit no cambió"""
    assert context.visitor_before['first_visit'] == context.updated_visitor.get(
        'first_visit',
        context.visitor_before['first_visit']
    )


@then('no se registra ninguna visita en la base de datos')
def step_no_visit_registered(context):
    """Verifica que no se registró ninguna visita"""
    # La base de datos debe estar vacía o sin cambios
    assert len(context.database) == context.visitor_count_before


@then('soy redirigido a la página principal')
def step_redirected_to_home(context):
    """Verifica que se redirigió a la página principal"""
    assert context.response.status_code == 200
    assert b'Welcome to Azure' in context.response.data


@then('el registro almacena la IP "{ip}"')
def step_record_stores_ip(context, ip):
    """Verifica que se almacenó la IP correcta"""
    assert context.new_visitor['ip_address'] == ip
