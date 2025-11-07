# coding: utf-8
from behave import when, then
from app import app

@when('visito la ruta "/stats"')
def step_impl(context):
    context.client = app.test_client()
    context.response = context.client.get("/stats")

@then('veo "{texto}"')
def step_impl(context, texto):
    html = context.response.data.decode("utf-8")
    assert texto in html, f'❌ No se encontró el texto esperado: "{texto}"\nHTML:\n{html}'
