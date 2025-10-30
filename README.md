# 🌐 Python Flask App - Registro de Visitantes

Aplicación web Flask con registro automático de visitantes, integración con Supabase y cobertura completa de pruebas (Unit + BDD).

## ✨ Características

- 🎯 **Contador de Visitas**: Seguimiento global de visitas en sesión
- 👤 **Registro de Visitantes**: Almacenamiento persistente en Supabase
- 📊 **Estadísticas**: Visualización de visitas, fechas y direcciones IP
- 🎨 **Bootstrap 5**: Interfaz responsiva y moderna
- 🧪 **Testing Completo**: 
  - **Unit Tests**: 20 pruebas con pytest (100% coverage)
  - **BDD Tests**: 5 escenarios con Behave/Gherkin (español)
- 🚀 **CI/CD**: GitHub Actions + SonarCloud + Azure App Service

## 🛠️ Tecnologías

- **Backend**: Python 3.13.2 + Flask 3.1.0
- **Base de Datos**: Supabase (PostgreSQL)
- **Testing**: pytest 8.3.3 + Behave 1.2.6
- **CI/CD**: GitHub Actions + SonarCloud
- **Deployment**: Azure App Service
- **Frontend**: Bootstrap 5

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/python-flask-app.git
cd python-flask-app
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env`:
```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_api_key_anon
```

### 5. Ejecutar la aplicación
```bash
python app.py
```

Visitar: http://127.0.0.1:5000

## 🧪 Pruebas

### Pruebas Unitarias (pytest)
```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Ver reporte
start htmlcov/index.html  # Windows
```

### Pruebas BDD (Behave)
```bash
# Ejecutar todos los escenarios
behave features/registro_visitantes.feature

# Con detalles
behave features/ --no-capture

# Escenario específico
behave features/registro_visitantes.feature:9
```

Ver documentación completa: [features/README.md](features/README.md)

## 📊 Estructura del Proyecto

```
python-flask-app/
├── app.py                    # Aplicación Flask principal
├── database.py               # Conexión con Supabase
├── requirements.txt          # Dependencias
├── pyproject.toml           # Configuración de pytest
├── behave.ini               # Configuración de Behave
├── sonar-project.properties # Configuración de SonarCloud
├── templates/
│   ├── index.html           # Página principal
│   └── hello.html           # Página de saludos
├── static/
│   └── bootstrap/           # Bootstrap 5
├── tests/
│   ├── test_app.py          # 20 pruebas unitarias
│   └── README.md
├── features/
│   ├── registro_visitantes.feature  # Escenarios Gherkin
│   ├── environment.py       # Config de Behave
│   ├── steps/
│   │   └── registro_visitantes_steps.py
│   └── README.md
└── .github/
    └── workflows/
        └── main_python-flask-app.yml
```

## 🗄️ Base de Datos (Supabase)

### Tabla: `visitors`
```sql
CREATE TABLE visitors (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  visit_count INTEGER DEFAULT 1,
  first_visit TIMESTAMP DEFAULT NOW(),
  last_visit TIMESTAMP DEFAULT NOW(),
  ip_address VARCHAR(45)
);
```

## 🚀 CI/CD Pipeline

GitHub Actions ejecuta automáticamente:
1. ✅ Instalación de dependencias
2. ✅ Pruebas unitarias con pytest
3. ✅ Generación de cobertura (XML/HTML)
4. ✅ Análisis de SonarCloud
5. ✅ Despliegue a Azure App Service (rama `main`)

Ver: [.github/workflows/main_python-flask-app.yml](.github/workflows/main_python-flask-app.yml)

## 📈 Métricas de Calidad

- ✅ **Cobertura de Código**: 100%
- ✅ **Pruebas Unitarias**: 20/20 pasando
- ✅ **Pruebas BDD**: 5/5 escenarios pasando
- ✅ **SonarCloud**: Configurado y funcionando

## 🔒 Seguridad

- Variables de entorno para credenciales
- `.env` incluido en `.gitignore`
- API keys de Supabase con nivel `anon`
- Validación de entrada de usuario

## 📝 Documentación Adicional

- [DATABASE_SETUP.md](DATABASE_SETUP.md) - Configuración de Supabase
- [HU1_IMPLEMENTATION.md](HU1_IMPLEMENTATION.md) - Historia de Usuario 1
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Resumen técnico
- [FIX_SONARCLOUD.md](FIX_SONARCLOUD.md) - Solución de problemas SonarCloud
- [features/README.md](features/README.md) - Documentación de pruebas BDD

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

**Desarrollado con** ❤️ **usando Flask + Supabase + Azure**
