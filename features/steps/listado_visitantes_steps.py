from behave import given, when, then
from unittest.mock import MagicMock
from bs4 import BeautifulSoup

# Helper para armar la cadena de mocks: table().select().order().execute()
def _set_visitors_query_result(mock, rows):
    table_mock = mock.table.return_value
    select_mock = table_mock.select.return_value
    order_mock = select_mock.order.return_value
    order_mock.execute.return_value = MagicMock(data=rows)

@given('que la base de datos contiene visitantes:')
def step_seed_visitors(context):
    # Convertir DataTable de Gherkin a lista de dicts
    rows = []
    for r in context.table:
        rows.append({
            "name": r["name"],
            "first_visit": r["first_visit"],
            "last_visit": r["last_visit"],
            "visit_count": int(r["visit_count"]),
        })
    # Configurar el mock de Supabase para la consulta del listado
    _set_visitors_query_result(context.supabase_mock, rows)

@when('visito la ruta "/visitors"')
def step_visit_visitors(context):
    client = context.app.test_client()
    context.response = client.get("/visitors")
    assert context.response.status_code == 200

@then('veo "Visitantes únicos: 3"')
def step_see_total_unique(context):
    assert "Visitantes únicos: 3" in context.response.get_data(as_text=True)

@then('veo "Total de visitas: 9"')
def step_see_total_visits(context):
    assert "Total de visitas: 9" in context.response.get_data(as_text=True)

@then('la primera fila de la tabla corresponde a "Carla Ríos"')
def step_first_row_is_carla(context):
    html = context.response.get_data(as_text=True)
    soup = BeautifulSoup(html, "html.parser")
    first_row = soup.select_one("tbody tr td")
    assert first_row is not None
    assert first_row.text.strip() == "Carla Ríos"
