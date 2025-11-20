# ElevateU Backend — Manual API Testing Script
# This script runs through all test scenarios using curl/Invoke-WebRequest

$baseUrl = "http://127.0.0.1:8000"
$authBase = "$baseUrl/api/auth"

Write-Host "===== ElevateU API Testing Script =====" -ForegroundColor Cyan
Write-Host "Base URL: $baseUrl" -ForegroundColor Yellow
Write-Host "`nMake sure Django dev server is running: python manage.py runserver`n" -ForegroundColor Yellow

# Helper function to make POST requests
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [hashtable]$Body,
        [int]$ExpectedStatus
    )
    
    Write-Host "TEST: $Name" -ForegroundColor Green
    Write-Host "  URL: $Url" -ForegroundColor Gray
    Write-Host "  Body: $($Body | ConvertTo-Json)" -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri $Url `
            -Method POST `
            -ContentType "application/json" `
            -Body ($Body | ConvertTo-Json) `
            -ErrorAction Stop
        
        Write-Host "  ✓ Status: $($response.StatusCode)" -ForegroundColor Green
        $jsonResponse = $response.Content | ConvertFrom-Json
        Write-Host "  Response: $($jsonResponse | ConvertTo-Json -Depth 2)" -ForegroundColor Cyan
        
        return $jsonResponse
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.Value__
        Write-Host "  ✗ Status: $statusCode" -ForegroundColor Red
        try {
            $errorBody = $_.Exception.Response.Content.ReadAsStream() | StreamReader.ReadToEnd()
            $errorJson = $errorBody | ConvertFrom-Json
            Write-Host "  Error: $($errorJson | ConvertTo-Json)" -ForegroundColor Red
        } catch {
            Write-Host "  Error: $($_)" -ForegroundColor Red
        }
        return $null
    }
}

# Test 1: Registration
Write-Host "`n========== TEST 1: User Registration ==========" -ForegroundColor Cyan
$registerBody = @{
    username = "testuser_$([datetime]::Now.Ticks)"
    email = "test_$([datetime]::Now.Ticks)@bennett.edu.in"
    password = "TestPass123!"
    password2 = "TestPass123!"
    field_of_interest = "Computer Science"
    first_name = "Test"
    last_name = "User"
}

$registerResponse = Test-Endpoint `
    -Name "Register with valid bennett.edu.in email" `
    -Url "$authBase/register/" `
    -Body $registerBody `
    -ExpectedStatus 201

if ($registerResponse) {
    $userEmail = $registerResponse.user.email
    Write-Host "`n  → Registered user: $userEmail" -ForegroundColor Yellow
    Write-Host "  → Check Django console for OTP" -ForegroundColor Yellow
    Write-Host "  → Enter OTP manually in next test" -ForegroundColor Yellow
    
    # Prompt for OTP
    Write-Host "`n" -ForegroundColor Gray
    $otp = Read-Host "  Enter OTP from console (6 digits)"
    
    # Test 2: Email Verification
    Write-Host "`n========== TEST 2: Email Verification ==========" -ForegroundColor Cyan
    $verifyBody = @{
        email = $userEmail
        otp_code = $otp
    }
    
    $verifyResponse = Test-Endpoint `
        -Name "Verify email with OTP" `
        -Url "$authBase/verify-email/" `
        -Body $verifyBody `
        -ExpectedStatus 200
    
    if ($verifyResponse) {
        $accessToken = $verifyResponse.access
        $refreshToken = $verifyResponse.refresh
        Write-Host "`n  → Access Token saved for authenticated requests" -ForegroundColor Yellow
        
        # Test 3: Login
        Write-Host "`n========== TEST 3: Login ==========" -ForegroundColor Cyan
        $loginBody = @{
            username = $registerBody.username
            password = $registerBody.password
        }
        
        $loginResponse = Test-Endpoint `
            -Name "Login with username and password" `
            -Url "$authBase/token/" `
            -Body $loginBody `
            -ExpectedStatus 200
        
        if ($loginResponse) {
            $refreshToken = $loginResponse.refresh
            
            # Test 4: Refresh Token
            Write-Host "`n========== TEST 4: Refresh Token ==========" -ForegroundColor Cyan
            $refreshBody = @{
                refresh = $refreshToken
            }
            
            $refreshResponse = Test-Endpoint `
                -Name "Refresh access token" `
                -Url "$authBase/token/refresh/" `
                -Body $refreshBody `
                -ExpectedStatus 200
        }
    }
}

# Test 5: Invalid Email Domain
Write-Host "`n========== TEST 5: Invalid Email Domain ==========" -ForegroundColor Cyan
$invalidEmailBody = @{
    username = "invalid_user"
    email = "invalid@gmail.com"
    password = "TestPass123!"
    password2 = "TestPass123!"
    field_of_interest = "Sports"
}

Test-Endpoint `
    -Name "Register with non-bennett.edu.in email (should fail)" `
    -Url "$authBase/register/" `
    -Body $invalidEmailBody `
    -ExpectedStatus 400

# Test 6: Mismatched Passwords
Write-Host "`n========== TEST 6: Mismatched Passwords ==========" -ForegroundColor Cyan
$mismatchedBody = @{
    username = "mismatch_user"
    email = "mismatch@bennett.edu.in"
    password = "TestPass123!"
    password2 = "DifferentPass123!"
    field_of_interest = "Music"
}

Test-Endpoint `
    -Name "Register with mismatched passwords (should fail)" `
    -Url "$authBase/register/" `
    -Body $mismatchedBody `
    -ExpectedStatus 400

# Test 7: Wrong OTP
Write-Host "`n========== TEST 7: Wrong OTP ==========" -ForegroundColor Cyan
$wrongOtpBody = @{
    email = "test@bennett.edu.in"
    otp_code = "000000"
}

Test-Endpoint `
    -Name "Verify email with wrong OTP (should fail)" `
    -Url "$authBase/verify-email/" `
    -Body $wrongOtpBody `
    -ExpectedStatus 400

Write-Host "`n===== Testing Complete =====" -ForegroundColor Cyan
Write-Host "✓ All manual tests executed!" -ForegroundColor Green
