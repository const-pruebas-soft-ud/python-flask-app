# 🔧 Fix: SonarCloud Coverage Report

## 🐛 Problema Original:
```
Quality Gate failed
Failed conditions
 0.0% Coverage on New Code (required ≥ 80%)
```

## 🎯 Causa:
SonarCloud no podía encontrar el archivo `coverage.xml` porque:
1. El archivo `sonar-project.properties` no especificaba la ruta del reporte
2. El workflow no descargaba el reporte en la ubicación correcta
3. Faltaba la configuración de `SONAR_HOST_URL`

## ✅ Solución Aplicada:

### 1. Actualizado `sonar-project.properties`:
```properties
# Coverage settings
sonar.python.coverage.reportPaths=coverage.xml

# Test settings
sonar.tests=tests
sonar.test.inclusions=tests/**/*.py

# Exclusions
sonar.exclusions=**/tests/**,**/__pycache__/**,**/htmlcov/**
```

### 2. Actualizado `.github/workflows/main_python-flask-app.yml`:
```yaml
- name: Download Coverage Report
  uses: actions/download-artifact@v4
  with:
    name: coverage-report
    path: .  # ✨ Descarga en el directorio raíz

- name: List files for debugging
  run: |
    echo "Files in current directory:"
    ls -la
    if [ -f coverage.xml ]; then
      echo "✅ coverage.xml found"
    fi

- name: Run SonarQube Scan
  env:
    SONAR_HOST_URL: https://sonarcloud.io  # ✨ Agregado
```

## 📋 Cambios Realizados:

### Archivo: `sonar-project.properties`
- ✅ Descomentadas y configuradas todas las propiedades necesarias
- ✅ Agregado `sonar.python.coverage.reportPaths=coverage.xml`
- ✅ Agregado `sonar.python.version=3.13`
- ✅ Configuradas exclusiones para archivos de test
- ✅ Configurado `sonar.tests=tests`

### Archivo: `.github/workflows/main_python-flask-app.yml`
- ✅ Agregado `path: .` al download del coverage report
- ✅ Agregado step de debugging para verificar archivos
- ✅ Descomentado `SONAR_HOST_URL: https://sonarcloud.io`

## 🚀 Comandos para Actualizar el PR:

```bash
# 1. Ver cambios
git status

# 2. Agregar archivos modificados
git add sonar-project.properties .github/workflows/main_python-flask-app.yml

# 3. Commit
git commit -m "fix: Configurar reporte de cobertura para SonarCloud

- Actualizar sonar-project.properties con ruta de coverage.xml
- Configurar descarga de reporte en directorio raíz
- Agregar SONAR_HOST_URL en workflow
- Agregar step de debugging para verificar archivos
- Configurar exclusiones de tests en SonarCloud"

# 4. Push al PR
git push origin feature/visit-counter
```

## 🔍 Verificación:

Después del push, el workflow debería:
1. ✅ Ejecutar las pruebas y generar `coverage.xml`
2. ✅ Subir el reporte como artefacto
3. ✅ Descargar el reporte en el directorio raíz
4. ✅ Mostrar en logs que `coverage.xml` fue encontrado
5. ✅ SonarCloud debe detectar ~100% de cobertura
6. ✅ Quality Gate debe pasar (≥80% requerido)

## 📊 Resultado Esperado:

```
✅ Quality Gate passed
✅ Coverage on New Code: 100.0% (required ≥ 80%)
✅ All conditions met
```

---

**Nota:** Si aún falla, revisa los logs del step "List files for debugging" para confirmar que `coverage.xml` está presente.
