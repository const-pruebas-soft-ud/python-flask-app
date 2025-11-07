# coding: utf-8
from behave import given, when, then
from app import app

# --- Contexto base ---
@given('que la base de datos contiene visitantes para estadísticas')
def step_impl(context):
    """
    Prepara el cliente Flask para las pruebas de estadísticas.
    No inserta datos reales (la HU3 maneja lista vacía con seguridad).
    """
    context.client = app.test_client()

@given('que no existen visitantes registrados')
def step_impl(context):
    """
    Prepara el cliente Flask para simular base de datos vacía.
    """
    context.client = app.test_client()

# --- Acción ---
@when('visito la ruta "/stats"')
def step_impl(context):
    context.response = context.client.get("/stats")

# --- Utilidad ---
def get_html(context):
    """Convierte el contenido de bytes a string UTF-8."""
    return context.response.data.decode("utf-8")

# --- Verificaciones ---
@then('veo "{texto}"')
def step_impl(context, texto):
    html = get_html(context)
    assert texto in html, f'❌ No se encontró el texto esperado: "{texto}"'

# Alias opcional
@then('debería ver "{texto}"')
def step_impl(context, texto):
    html = get_html(context)
    assert texto in html, f'❌ No se encontró el texto esperado: "{texto}"'
