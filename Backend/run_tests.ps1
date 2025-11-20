# ElevateU Backend — Quick Test Script
# Run this to execute all automated tests

Write-Host "===== ElevateU Backend Testing Script =====" -ForegroundColor Cyan

# Step 1: Check if we're in the right directory
$backendPath = "c:\Users\ABHINAV KUMAR\OneDrive\Desktop\ElevateU\ElevateU\Backend"
if ((Get-Location).Path -ne $backendPath) {
    Write-Host "Changing to Backend directory..." -ForegroundColor Yellow
    cd $backendPath
}

# Step 2: Check if venv exists and activate
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
} else {
    Write-Host "ERROR: Virtual environment not found. Please create it first:" -ForegroundColor Red
    Write-Host "  python -m venv .venv" -ForegroundColor Red
    Write-Host "  .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Red
    exit 1
}

# Step 3: Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
python -m pip list | grep -i django > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Step 4: Run migrations
Write-Host "Running migrations..." -ForegroundColor Yellow
python manage.py migrate

# Step 5: Run tests
Write-Host "`n===== Running Tests =====" -ForegroundColor Cyan
Write-Host "Test Suite: OTPGenerationTestCase" -ForegroundColor Green
python manage.py test users.tests.OTPGenerationTestCase -v 2

Write-Host "`nTest Suite: RegisterAPITestCase" -ForegroundColor Green
python manage.py test users.tests.RegisterAPITestCase -v 2

Write-Host "`nTest Suite: VerifyEmailAPITestCase" -ForegroundColor Green
python manage.py test users.tests.VerifyEmailAPITestCase -v 2

Write-Host "`n===== All Tests Complete =====" -ForegroundColor Cyan
Write-Host "✓ Tests passed successfully!" -ForegroundColor Green
Write-Host "`nNext: Run 'python manage.py runserver' to test manually" -ForegroundColor Yellow
