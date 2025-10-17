# Pruebas Unitarias - Python Flask App

Este documento describe las pruebas unitarias implementadas para la aplicación Flask.

## 🧪 Pruebas Implementadas

El archivo `tests/test_app.py` contiene las siguientes pruebas:

### 1. **Pruebas de Rutas Básicas**
- ✅ `test_index_route`: Verifica que la página principal carga correctamente
- ✅ `test_favicon_route`: Verifica que el favicon se sirve correctamente

### 2. **Pruebas del Contador de Visitas**
- ✅ `test_index_visit_counter`: Verifica que el contador de visitas incrementa
- ✅ `test_multiple_visits_increment`: Verifica múltiples visitas

### 3. **Pruebas de Funcionalidad de Saludo**
- ✅ `test_hello_with_name`: Verifica que el saludo funciona con un nombre
- ✅ `test_hello_without_name`: Verifica la redirección sin nombre
- ✅ `test_hello_without_name_follow_redirect`: Verifica el comportamiento de redirección
- ✅ `test_hello_greeting_counter`: Verifica que el contador de saludos incrementa
- ✅ `test_multiple_greetings_increment`: Verifica múltiples saludos

## 🚀 Ejecutar las Pruebas Localmente

### Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar Todas las Pruebas
```bash
pytest tests/
```

### Ejecutar con Cobertura
```bash
pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### Ver Reporte de Cobertura
Después de ejecutar las pruebas con cobertura, abre:
```bash
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

## 📊 Cobertura de Código

Las pruebas están configuradas para generar reportes de cobertura en tres formatos:
- **Terminal**: Muestra un resumen en la consola
- **XML**: Para integración con SonarQube (`coverage.xml`)
- **HTML**: Para visualización detallada (`htmlcov/`)

## 🔄 Integración con GitHub Actions

Las pruebas se ejecutan automáticamente en GitHub Actions:

1. **Build and Test**: Ejecuta pytest con cobertura
2. **SonarQube**: Analiza el código y la cobertura
3. **Deploy**: Solo se ejecuta si las pruebas pasan

## 📝 Agregar Nuevas Pruebas

Para agregar nuevas pruebas:

1. Crea una función en `tests/test_app.py` con el prefijo `test_`
2. Usa el fixture `client` para simular peticiones HTTP
3. Ejecuta las pruebas localmente antes de hacer commit

Ejemplo:
```python
def test_nueva_funcionalidad(client):
    """Descripción de la prueba"""
    response = client.get('/nueva-ruta')
    assert response.status_code == 200
    assert b'Contenido esperado' in response.data
```

## 🛠️ Comandos Útiles

```bash
# Ejecutar una prueba específica
pytest tests/test_app.py::test_index_route

# Ejecutar con modo verbose
pytest tests/ -v

# Ejecutar y mostrar print statements
pytest tests/ -s

# Ejecutar y detener en el primer error
pytest tests/ -x

# Ver qué pruebas se ejecutarán sin ejecutarlas
pytest tests/ --collect-only
```

## 📦 Dependencias de Pruebas

- `pytest==8.3.3`: Framework de pruebas
- `pytest-cov==6.0.0`: Plugin de cobertura para pytest

## 🎯 Objetivos de Cobertura

Se recomienda mantener una cobertura de código de al menos:
- **80%** para código general
- **90%** para funciones críticas de negocio
