# ElevateU Backend — Email OTP Verification Testing Guide

## Quick Start: Local Testing Setup

### 1. Environment Setup (Windows PowerShell)

```powershell
# Navigate to Backend directory
cd "c:\Users\ABHINAV KUMAR\OneDrive\Desktop\ElevateU\ElevateU\Backend"

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
.\\.venv\\Scripts\\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create migrations for CustomUser and EmailVerification models
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser
# Follow prompts: username, email, password

# Run development server
python manage.py runserver
```

**Server will start at:** http://127.0.0.1:8000

---

## Option A: Run Automated Tests

### A1. Run All Tests

```powershell
# From Backend directory (with .venv activated)
python manage.py test users

# Output should show:
# Ran 11 tests in X.XXXs
# OK
```

### A2. Run Specific Test Class

```powershell
# Run only OTP generation tests
python manage.py test users.tests.OTPGenerationTestCase

# Run only registration tests
python manage.py test users.tests.RegisterAPITestCase

# Run only email verification tests
python manage.py test users.tests.VerifyEmailAPITestCase
```

### A3. Run with Verbose Output

```powershell
# Show each test name as it runs
python manage.py test users -v 2

# Even more verbose
python manage.py test users -v 3
```

### A4. Run with Coverage (optional)

```powershell
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run --source='users' manage.py test users

# Generate coverage report
coverage report

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

---

## Option B: Manual API Testing (Recommended for testing locally)

### Setup: Get a REST client

**Option B1: Use curl (Windows PowerShell)**
```powershell
# Test endpoint availability
curl http://127.0.0.1:8000/api/health/
```

**Option B2: Install Postman**
- Download: https://www.postman.com/downloads/
- Import the requests below or create manually

**Option B3: Use VS Code REST Client extension**
- Install: REST Client by Huachao Zheng
- Create `test.http` file and run requests inline

### Test 1: Registration (Create new user + send OTP)

**curl (PowerShell):**
```powershell
$body = @{
    username = "alice"
    email = "alice@bennett.edu.in"
    password = "SecurePass123!"
    password2 = "SecurePass123!"
    field_of_interest = "Computer Science"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/register/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@bennett.edu.in",
    "first_name": "",
    "last_name": "",
    "field_of_interest": "Computer Science",
    "bio": null,
    "campus_verified": false
  },
  "message": "OTP sent to your campus email for verification."
}
```

**Check console output for OTP:**
Look at the Django dev server terminal output — the OTP will be printed:
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: ElevateU Email Verification - OTP
From: noreply@elevateu.bennett.edu.in
To: alice@bennett.edu.in
Date: Wed, 12 Nov 2025 10:30:45 -0000
Message-ID: <...>

Your OTP for email verification: 123456

This OTP is valid for 10 minutes.
```

**Copy the 6-digit OTP (e.g., 123456) for the next test.**

---

### Test 2: Email Verification (Verify OTP + Get JWT tokens)

**curl (PowerShell):**
```powershell
# Replace 123456 with the actual OTP from the console output above
$body = @{
    email = "alice@bennett.edu.in"
    otp_code = "123456"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/verify-email/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@bennett.edu.in",
    "first_name": "",
    "last_name": "",
    "field_of_interest": "Computer Science",
    "bio": null,
    "campus_verified": true
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "Email verified successfully!"
}
```

**Save the `access` token for authenticated requests.**

---

### Test 3: Login (Obtain JWT tokens with username+password)

**curl (PowerShell):**
```powershell
$body = @{
    username = "alice"
    password = "SecurePass123!"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/token/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### Test 4: Refresh Token

**curl (PowerShell):**
```powershell
# Use the refresh token from test 3
$body = @{
    refresh = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/token/refresh/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## Test Cases: Edge Cases & Error Scenarios

### Test 5: Invalid Email Domain (should reject)

```powershell
$body = @{
    username = "bob"
    email = "bob@gmail.com"
    password = "SecurePass123!"
    password2 = "SecurePass123!"
    field_of_interest = "Sports"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/register/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (400 Bad Request):**
```json
{
  "email": ["Registration allowed only with @bennett.edu.in email addresses"]
}
```

---

### Test 6: Mismatched Passwords (should reject)

```powershell
$body = @{
    username = "charlie"
    email = "charlie@bennett.edu.in"
    password = "SecurePass123!"
    password2 = "DifferentPass123!"
    field_of_interest = "Music"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/register/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (400 Bad Request):**
```json
{
  "password": ["Password fields didn't match."]
}
```

---

### Test 7: Wrong OTP (should reject)

```powershell
# After registering, try with wrong OTP
$body = @{
    email = "alice@bennett.edu.in"
    otp_code = "000000"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/verify-email/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (400 Bad Request):**
```json
{
  "non_field_errors": ["Invalid OTP."]
}
```

---

### Test 8: Expired OTP (should reject after 10 minutes)

**Setup:**
1. Register a new user (save OTP from console)
2. Wait 11 minutes (or manually modify DB to set old timestamp)
3. Try to verify with the old OTP

**Expected Response (400 Bad Request):**
```json
{
  "non_field_errors": ["OTP has expired. Please request a new one."]
}
```

---

### Test 9: Duplicate Email Registration (should reject)

```powershell
# After registering alice, try to register again with same email
$body = @{
    username = "alice2"
    email = "alice@bennett.edu.in"  # Same email
    password = "AnotherPass123!"
    password2 = "AnotherPass123!"
    field_of_interest = "Science"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/register/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (400 Bad Request):**
```json
{
  "email": ["Email already registered."]
}
```

---

### Test 10: Already Verified User (should reject re-verification)

```powershell
# After verifying alice's email, try to verify again with same email
$body = @{
    email = "alice@bennett.edu.in"
    otp_code = "123456"  # Even with correct OTP
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/verify-email/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected Response (400 Bad Request):**
```json
{
  "non_field_errors": ["Email is already verified."]
}
```

---

## Postman Collection (Copy-Paste JSON)

Create a new Postman Collection and import this:

```json
{
  "info": {
    "name": "ElevateU Auth API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "1. Register",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\"username\":\"alice\",\"email\":\"alice@bennett.edu.in\",\"password\":\"SecurePass123!\",\"password2\":\"SecurePass123!\",\"field_of_interest\":\"Computer Science\"}"
        },
        "url": {"raw": "http://127.0.0.1:8000/api/auth/register/", "protocol": "http", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "auth", "register", ""]}
      }
    },
    {
      "name": "2. Verify Email",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\"email\":\"alice@bennett.edu.in\",\"otp_code\":\"PASTE_OTP_HERE\"}"
        },
        "url": {"raw": "http://127.0.0.1:8000/api/auth/verify-email/", "protocol": "http", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "auth", "verify-email", ""]}
      }
    },
    {
      "name": "3. Login",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\"username\":\"alice\",\"password\":\"SecurePass123!\"}"
        },
        "url": {"raw": "http://127.0.0.1:8000/api/auth/token/", "protocol": "http", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "auth", "token", ""]}
      }
    },
    {
      "name": "4. Refresh Token",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\"refresh\":\"PASTE_REFRESH_TOKEN_HERE\"}"
        },
        "url": {"raw": "http://127.0.0.1:8000/api/auth/token/refresh/", "protocol": "http", "host": ["127", "0", "0", "1"], "port": "8000", "path": ["api", "auth", "token", "refresh", ""]}
      }
    }
  ]
}
```

---

## Admin Panel Testing

### Access Admin Interface

1. Start dev server: `python manage.py runserver`
2. Open browser: http://127.0.0.1:8000/admin/
3. Login with superuser credentials created earlier
4. Navigate to **Users** > **Custom Users** or **Users** > **Email Verifications**

### What to check in Admin:

- **CustomUsers:** View registered users, check `campus_verified` status, `field_of_interest`
- **Email Verifications:** View all OTPs, see which are verified, timestamps

---

## Database Inspection (Optional)

### Check records in SQLite (Windows PowerShell)

```powershell
# Install sqlite3 CLI (if not present)
# Already available in most Windows installs

# Connect to database
sqlite3 db.sqlite3

# View users
sqlite> SELECT id, username, email, campus_verified FROM users_customuser;

# View OTPs
sqlite> SELECT user_id, otp_code, created_at, is_verified FROM users_emailverification;

# Exit
sqlite> .exit
```

---

## Checklist: Full Testing Flow

- [ ] Setup venv and install dependencies
- [ ] Run migrations
- [ ] Run automated tests: `python manage.py test users`
- [ ] Start dev server
- [ ] Test Registration (API Test 1)
- [ ] Copy OTP from console output
- [ ] Test Email Verification (API Test 2)
- [ ] Save JWT tokens from response
- [ ] Test Login (API Test 3)
- [ ] Test Refresh Token (API Test 4)
- [ ] Test invalid email domain (API Test 5)
- [ ] Test mismatched passwords (API Test 6)
- [ ] Test wrong OTP (API Test 7)
- [ ] Test duplicate email (API Test 9)
- [ ] Test already-verified user (API Test 10)
- [ ] Check Admin panel
- [ ] Verify database records

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'django'` | Activate venv: `.\\.venv\\Scripts\\Activate.ps1` |
| `Table doesn't exist` | Run migrations: `python manage.py migrate` |
| `OTP not printed to console` | Check dev server terminal (not the request output) |
| `CORS errors in frontend` | Update `CORS_ALLOWED_ORIGINS` in settings.py |
| `Email sending fails` | Check `EMAIL_BACKEND` is set to console backend for dev |
| `Port 8000 already in use` | Run on different port: `python manage.py runserver 8001` |

---

## Next Steps (After Successful Testing)

1. **Merge to develop branch**
   ```powershell
   git checkout develop
   git merge feature/backend-auth
   git push origin develop
   ```

2. **Deploy to staging** (if available)

3. **Add improvements from code review:**
   - Transaction handling for email failures
   - `select_for_update()` for race condition prevention
   - Resend OTP endpoint

4. **Configure real email backend** (SendGrid, AWS SES, etc.)

---

**Happy testing! 🚀**
