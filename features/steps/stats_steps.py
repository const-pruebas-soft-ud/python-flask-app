# coding: utf-8
from behave import given, when, then
from app import app
from database import get_supabase_client
from datetime import datetime

# Obtener cliente de supabase para insertar/limpiar datos durante las pruebas
supabase = get_supabase_client()

# --- Contexto base ---
@given('que la base de datos contiene visitantes para estadísticas:')
def step_impl(context):
    """
    Si el step recibe una tabla (context.table), limpia la tabla 'visitors'
    y inserta las filas proporcionadas por el feature.
    """
    context.client = app.test_client()

    # Si feature provee una tabla, usarla para poblar la BD de prueba
    if hasattr(context, "table") and len(context.table.rows) > 0:
        try:
            # Intentar limpiar la tabla (borrar todos los registros)
            # Nota: la API de supabase python requiere un filtro para delete(); usamos neq('id', 0)
            # que típicamente borra todo (siempre revisar en entorno real).
            supabase.table('visitors').delete().neq('id', 0).execute()
        except Exception:
            # Si no puede borrar (tabla no existe / permisos), continuar e intentar insertar
            pass

        rows = []
        for row in context.table:
            rows.append({
                'name': row['name'],
                'first_visit': row['first_visit'],
                'last_visit': row['last_visit'],
                'visit_count': int(row['visit_count']),
                'ip_address': row.get('ip_address', '127.0.0.1')
            })

        try:
            supabase.table('visitors').insert(rows).execute()
        except Exception as e:
            # Mostrar en logs si falla (CI mostrará esto)
            print("❌ Error insertando registros de prueba en Supabase:", e)

@given('que no existen visitantes registrados')
def step_impl(context):
    """
    Limpia la tabla 'visitors' para simular que no hay datos.
    """
    context.client = app.test_client()
    try:
        supabase.table('visitors').delete().neq('id', 0).execute()
    except Exception:
        # si falla la limpieza (ej. tabla no existe), no abortamos el test
        pass

# --- Acción ---
@when('visito la ruta "/stats"')
def step_impl(context):
    context.response = context.client.get("/stats")

# --- Utilidad ---
def get_html(context):
    """Convierte bytes a string UTF-8."""
    return context.response.data.decode("utf-8")

# --- Verificaciones ---
@then('veo "{texto}"')
def step_impl(context, texto):
    html = get_html(context)
    assert texto in html, f'❌ No se encontró el texto esperado: "{texto}"\nHTML:\n{html}'

@then('debería ver "{texto}"')
def step_impl(context, texto):
    html = get_html(context)
    assert texto in html, f'❌ No se encontró el texto esperado: "{texto}"\nHTML:\n{html}'
