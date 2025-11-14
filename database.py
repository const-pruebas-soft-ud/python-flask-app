"""
Configuración y cliente de Supabase
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Crear cliente de Supabase sólo si existen las variables; en entornos de test/CI
# puede que no estén y queremos evitar fallar en la importación.
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        # Si la creación falla (p. ej. clave inválida), dejar supabase en None
        supabase = None
else:
    # No hay configuración; deferir la creación hasta que sea realmente necesaria
    supabase = None


def test_connection():  # pragma: no cover
    """
    Prueba la conexión con Supabase intentando listar las tablas
    """
    if not supabase:  # pragma: no cover
        print("❌ Supabase no configurado en el entorno")
        return False

    try:
        # Intenta hacer una consulta simple a la tabla 'visitors'
        # Si la tabla no existe, esto fallará, lo cual está bien para testing
        response = supabase.table('visitors').select("*").limit(1).execute()
        print("✅ Conexión exitosa con Supabase")
        print(f"📊 Respuesta: {response}")
        return True
    except Exception as e:  # pragma: no cover
        print(f"❌ Error al conectar con Supabase: {str(e)}")
        return False


def get_supabase_client() -> Client:
    """
    Retorna el cliente de Supabase configurado
    """
    return supabase
