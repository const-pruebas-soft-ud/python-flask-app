from behave import given, when, then
from unittest.mock import MagicMock
from bs4 import BeautifulSoup
import re

# Simula table().select().order().execute() devolviendo filas ordenadas por last_visit DESC
def _set_visitors_query_result(mock, rows):
    rows_sorted = sorted(rows, key=lambda r: r["last_visit"], reverse=True)
    table_mock = mock.table.return_value
    select_mock = table_mock.select.return_value
    order_mock  = select_mock.order.return_value
    order_mock.execute.return_value = MagicMock(data=rows_sorted)

@given('que la base de datos contiene visitantes')
@given('que la base de datos contiene visitantes:')
def step_seed_visitors(context):
    rows = []
    if getattr(context, "table", None):
        for r in context.table:
            rows.append({
                "name": r["name"],
                "first_visit": r["first_visit"],
                "last_visit": r["last_visit"],
                "visit_count": int(r["visit_count"]),
            })
    _set_visitors_query_result(context.supabase_mock, rows)

@when('visito la ruta "/visitors"')
def step_visit_visitors(context):
    client = context.app.test_client()
    context.response = client.get("/visitors")
    assert context.response.status_code == 200

@then('veo "Visitantes únicos: 3"')
def step_see_total_unique(context):
    html = context.response.get_data(as_text=True)
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    assert re.search(r"Visitantes\s+únicos:\s*3\b", text), f"No encontré 'Visitantes únicos: 3' en:\n{text}"

@then('veo "Total de visitas: 9"')
def step_see_total_visits(context):
    html = context.response.get_data(as_text=True)
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    assert re.search(r"Total\s+de\s+visitas:\s*9\b", text), f"No encontré 'Total de visitas: 9' en:\n{text}"

# SIN regex: dos decoradores parse, con y sin comentario final
@then('la primera fila de la tabla corresponde a "{nombre}"')
@then('la primera fila de la tabla corresponde a "{nombre}"  # Última visita más reciente')
def step_first_row_is(context, nombre):
    html = context.response.get_data(as_text=True)
    soup = BeautifulSoup(html, "html.parser")
    first_cell = soup.select_one("tbody tr td")
    assert first_cell is not None, "No se encontró la primera celda de la tabla"
    assert first_cell.text.strip() == nombre
