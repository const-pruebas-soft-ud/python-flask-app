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

# Validar que las variables de entorno estén configuradas
if not SUPABASE_URL or not SUPABASE_KEY:  # pragma: no cover
    raise ValueError(
        "Las variables de entorno SUPABASE_URL y SUPABASE_KEY son requeridas. "
        "Por favor, crea un archivo .env basado en .env.example"
    )

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def test_connection():  # pragma: no cover
    """
    Prueba la conexión con Supabase intentando listar las tablas
    """
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
