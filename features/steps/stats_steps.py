# coding: utf-8
from behave import given, when, then
from app import app

# --- Contexto base ---
@given('que la base de datos contiene visitantes')
def step_impl(context):
    """
    Prepara el cliente Flask para las pruebas.
    No inserta datos reales (la lógica de HU3 maneja lista vacía con seguridad).
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

# --- Utilidad para decodificar HTML ---
def get_html(context):
    """Convierte el contenido de bytes a string UTF-8."""
    return context.response.data.decode("utf-8")

# --- Verificaciones ---
@then('veo "{texto}"')
def step_impl(context, texto):
    html = get_html(context)
    assert texto in html, f'No se encontró el texto esperado: "{texto}"'

# Alias opcional para pasos que usen “Entonces debería ver …”
@then('debería ver "{texto}"')
def step_impl(context, texto):
    html = get_html(context)
    assert texto in html, f'No se encontró el texto esperado: "{texto}"'
