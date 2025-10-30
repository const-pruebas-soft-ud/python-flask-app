# Script para ejecutar todas las pruebas localmente (similar a GitHub Actions)
# PowerShell script

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  🧪 Ejecutando Suite Completa de Pruebas" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el entorno virtual
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Activando entorno virtual..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
}

# 1. PRUEBAS UNITARIAS CON PYTEST
Write-Host "================================================" -ForegroundColor Green
Write-Host "  1️⃣  PRUEBAS UNITARIAS (pytest)" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

pytest tests/ --verbose --junit-xml=test-results.xml --cov=. --cov-report=xml --cov-report=html --cov-report=term

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Las pruebas unitarias FALLARON" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Pruebas unitarias PASARON" -ForegroundColor Green
Write-Host ""

# 2. PRUEBAS BDD CON BEHAVE
Write-Host "================================================" -ForegroundColor Green
Write-Host "  2️⃣  PRUEBAS BDD (Behave/Gherkin)" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

behave features/ --format=pretty --format=json --outfile=behave-results.json --format=html --outfile=behave-report.html --junit --junit-directory=behave-junit

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Las pruebas BDD FALLARON" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Pruebas BDD PASARON" -ForegroundColor Green
Write-Host ""

# RESUMEN FINAL
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  ✅ TODAS LAS PRUEBAS COMPLETADAS" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Reportes generados:" -ForegroundColor Yellow
Write-Host "  - Coverage HTML:    htmlcov\index.html" -ForegroundColor White
Write-Host "  - Coverage XML:     coverage.xml" -ForegroundColor White
Write-Host "  - Pytest JUnit:     test-results.xml" -ForegroundColor White
Write-Host "  - Behave HTML:      behave-report.html" -ForegroundColor White
Write-Host "  - Behave JSON:      behave-results.json" -ForegroundColor White
Write-Host "  - Behave JUnit:     behave-junit\" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Listo para commit y push!" -ForegroundColor Green
Write-Host ""
