Write-Host "========================================"
Write-Host " SignaVision Automated Tests"
Write-Host "========================================"

$ProjectRoot = $PSScriptRoot


# ==========================================================
# FRONTEND TESTS
# ==========================================================

Write-Host ""
Write-Host "Running frontend tests..."
Write-Host ""

Set-Location "$ProjectRoot\frontend"

npm run test:run

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Frontend tests failed." -ForegroundColor Red
    exit 1
}


# ==========================================================
# BACKEND TESTS
# ==========================================================

Write-Host ""
Write-Host "Running backend tests..."
Write-Host ""

Set-Location "$ProjectRoot\backend"

& "$ProjectRoot\venv\Scripts\python.exe" -m pytest tests -v

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Backend tests failed." -ForegroundColor Red
    exit 1
}


# ==========================================================
# SUCCESS
# ==========================================================

Set-Location $ProjectRoot

Write-Host ""
Write-Host "========================================"
Write-Host " ALL TESTS PASSED"
Write-Host "========================================"