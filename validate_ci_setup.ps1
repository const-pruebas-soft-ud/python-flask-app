# Script de validación de configuración para CI/CD
# PowerShell script

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  🔍 Validación de Configuración CI/CD" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$allChecks = $true

# 1. Verificar archivos de configuración
Write-Host "📁 Verificando archivos de configuración..." -ForegroundColor Yellow
Write-Host ""

$configFiles = @(
    "behave.ini",
    "pyproject.toml",
    "requirements.txt",
    ".github\workflows\main_python-flask-app.yml",
    "features\registro_visitantes.feature",
    "features\environment.py",
    "features\steps\registro_visitantes_steps.py"
)

foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file NO ENCONTRADO" -ForegroundColor Red
        $allChecks = $false
    }
}

Write-Host ""

# 2. Verificar dependencias de Python
Write-Host "🐍 Verificando dependencias de Python..." -ForegroundColor Yellow
Write-Host ""

$pythonDeps = @("Flask", "pytest", "pytest-cov", "behave", "supabase", "python-dotenv")
$installedPackages = pip list --format=freeze

foreach ($dep in $pythonDeps) {
    $found = $installedPackages | Select-String -Pattern "^$dep" -Quiet
    if ($found) {
        Write-Host "  ✅ $dep instalado" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $dep NO instalado" -ForegroundColor Red
        $allChecks = $false
    }
}

Write-Host ""

# 3. Verificar variables de entorno
Write-Host "🔐 Verificando variables de entorno..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path .env) {
    Write-Host "  ✅ Archivo .env encontrado" -ForegroundColor Green
    
    $envContent = Get-Content .env
    
    if ($envContent -match "SUPABASE_URL") {
        Write-Host "  ✅ SUPABASE_URL configurado" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  SUPABASE_URL no encontrado en .env" -ForegroundColor Yellow
    }
    
    if ($envContent -match "SUPABASE_KEY") {
        Write-Host "  ✅ SUPABASE_KEY configurado" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  SUPABASE_KEY no encontrado en .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠️  Archivo .env no encontrado (necesario para local)" -ForegroundColor Yellow
}

Write-Host ""

# 4. Verificar estructura de pruebas
Write-Host "🧪 Verificando estructura de pruebas..." -ForegroundColor Yellow
Write-Host ""

$testDirs = @("tests", "features", "features\steps")
foreach ($dir in $testDirs) {
    if (Test-Path $dir) {
        $fileCount = (Get-ChildItem $dir -Filter *.py -ErrorAction SilentlyContinue).Count
        Write-Host "  ✅ $dir ($fileCount archivos .py)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $dir NO ENCONTRADO" -ForegroundColor Red
        $allChecks = $false
    }
}

Write-Host ""

# 5. Verificar sintaxis de Gherkin
Write-Host "📝 Verificando sintaxis de Gherkin..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "features\registro_visitantes.feature") {
    $featureContent = Get-Content "features\registro_visitantes.feature" -Raw
    
    $keywords = @("Característica:", "Escenario:", "Dado", "Cuando", "Entonces")
    foreach ($keyword in $keywords) {
        if ($featureContent -match $keyword) {
            Write-Host "  ✅ Palabra clave '$keyword' encontrada" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  Palabra clave '$keyword' no encontrada" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan

if ($allChecks) {
    Write-Host "  ✅ TODAS LAS VALIDACIONES PASARON" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 El proyecto está listo para CI/CD" -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximos pasos:" -ForegroundColor Yellow
    Write-Host "  1. Ejecutar: .\run_all_tests.ps1" -ForegroundColor White
    Write-Host "  2. Revisar que todas las pruebas pasen" -ForegroundColor White
    Write-Host "  3. git add ." -ForegroundColor White
    Write-Host "  4. git commit -m 'feat: Integrar Behave en GitHub Actions'" -ForegroundColor White
    Write-Host "  5. git push origin feature/registro-visitantes" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "  ❌ ALGUNAS VALIDACIONES FALLARON" -ForegroundColor Red
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Por favor, corrige los problemas antes de continuar" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
