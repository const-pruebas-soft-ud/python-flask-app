"""
Configuración del entorno de pruebas BDD con Behave
"""
import os
import sys
from unittest.mock import patch, MagicMock

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

from app import app


def before_all(context):
    """Se ejecuta una vez antes de todas las pruebas"""
    context.app = app
    context.app.config['TESTING'] = True
    context.client = app.test_client()
    
    # Mock de Supabase para las pruebas
    context.supabase_mock = MagicMock()
    context.supabase_patcher = patch('app.supabase', context.supabase_mock)
    context.supabase_patcher.start()


def before_scenario(context, _scenario):
    """Se ejecuta antes de cada escenario"""
    # Resetear el estado de los mocks
    context.supabase_mock.reset_mock()
    
    # Simular base de datos vacía por defecto
    context.supabase_mock.table().select().eq().execute.return_value = MagicMock(data=[])
    
    # Almacenar datos simulados de la BD
    context.database = {}
    context.visitor_count_before = 0
    context.response = None
    context.visitor_before = None


def after_all(context):
    """Se ejecuta una vez después de todas las pruebas"""
    context.supabase_patcher.stop()
