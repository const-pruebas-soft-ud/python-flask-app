"""
Script para probar la conexión con Supabase
Ejecutar con: python test_supabase_connection.py
"""
from database import test_connection, get_supabase_client

print("=" * 60)
print("🔌 Probando conexión con Supabase...")
print("=" * 60)

# Probar la conexión
if test_connection():
    print("\n✅ ¡Conexión establecida correctamente!")
    
    # Obtener el cliente y mostrar información
    client = get_supabase_client()
    print(f"\n📍 URL de Supabase: {client.supabase_url}")
    print("\n✨ El cliente está listo para usar")
    
else:
    print("\n❌ No se pudo establecer la conexión")
    print("\n📝 Verifica:")
    print("  1. Que el archivo .env existe (copia de .env.example)")
    print("  2. Que SUPABASE_URL y SUPABASE_KEY están configurados")
    print("  3. Que la tabla 'visitors' existe en Supabase")
    print("  4. Que las credenciales son correctas")

print("\n" + "=" * 60)
