# start.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  E-commerce API - Iniciando Entorno" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Activar virtual environment
.\venv\Scripts\Activate.ps1

# Verificaciones
Write-Host "`n✅ Python: $(python --version)" -ForegroundColor Green
Write-Host "✅ Pip: $(pip --version)" -ForegroundColor Green
Write-Host "📁 Proyecto: $(Get-Location)" -ForegroundColor Green

# Verificar paquetes críticos
$required = @('fastapi', 'pytest', 'sqlalchemy', 'pydantic')
Write-Host "`n📦 Verificando paquetes requeridos:" -ForegroundColor Yellow
foreach ($pkg in $required) {
    try {
        $version = python -c "import $pkg; print($pkg.__version__)" 2>$null
        if ($version) {
            Write-Host "  ✅ $pkg" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $pkg (no instalado)" -ForegroundColor Red
        }
    } catch {
        Write-Host "  ❌ $pkg (no instalado)" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  ¡Listo para trabajar! 🚀" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nComandos útiles:" -ForegroundColor Yellow
Write-Host "  - Ejecutar API: uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "  - Ejecutar tests: python -m pytest tests/ -v" -ForegroundColor White
Write-Host "  - Salir del venv: deactivate" -ForegroundColor White
Write-Host ""