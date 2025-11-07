from behave import given, when, then
from app import app

@given('que existen visitantes registrados')
def step_impl(context):
    context.client = app.test_client()
    # Podrías insertar registros falsos en Supabase aquí si lo deseas
    # o asumir que ya existen por ejecución previa

@given('que no existen visitantes registrados')
def step_impl(context):
    context.client = app.test_client()
    # En un entorno real, podrías limpiar la tabla "visitors"

@when('visito la ruta "/stats"')
def step_impl(context):
    context.response = context.client.get('/stats')

@then('debería ver "Estadísticas Generales"')
def step_impl(context):
    assert b'Estadísticas Generales' in context.response.data

@then('debería ver "Top 10 Visitantes"')
def step_impl(context):
    assert b'Top 10 Visitantes' in context.response.data

@then('debería ver "No hay datos de visitantes"')
def step_impl(context):
    assert b'No hay datos de visitantes' in context.response.data
