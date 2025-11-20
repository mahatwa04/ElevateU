@echo off
REM Create Pull Request - ElevateU Cloud Deployment
REM This script helps create a PR from feature/backend-posts to main

echo.
echo ============================================
echo ElevateU Pull Request Creator
echo ============================================
echo.
echo PR Title: feat: Cloud Deployment Setup - Render Backend, Vercel Frontend, E2E Tests, Performance Optimization
echo.
echo Base Branch: main
echo Compare Branch: feature/backend-posts
echo.
echo PR Description:
echo - Cloud Deployment Configuration (Render + Vercel)
echo - End-to-End Testing Suite (30+ tests)
echo - Database Optimization (6 strategic indexes)
echo - Performance Optimization (Caching + CDN)
echo - Production Settings (Security hardened)
echo - Comprehensive Documentation
echo.
echo ============================================
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found in PATH
    echo Please install Git from: https://git-scm.com/download/win
    exit /b 1
)

REM Check current directory
if not exist ".git" (
    echo ERROR: Not in a git repository
    echo Please run this from the ElevateU project root
    exit /b 1
)

REM Verify branch exists
git rev-parse --verify feature/backend-posts >nul 2>&1
if errorlevel 1 (
    echo ERROR: feature/backend-posts branch not found
    exit /b 1
)

echo ============================================
echo Creating Pull Request...
echo ============================================
echo.

REM Try using GitHub CLI if available
where gh >nul 2>&1
if %errorlevel% equ 0 (
    echo Attempting to create PR using GitHub CLI...
    gh pr create ^
        --title "feat: Cloud Deployment Setup - Render Backend, Vercel Frontend, E2E Tests, Performance Optimization" ^
        --body "## Overview^nThis PR completes the final phase of ElevateU project deployment.^n^n### Features Added^n- Cloud Deployment Configuration (Render + Vercel)^n- End-to-End Testing Suite (30+ tests)^n- Database Optimization (indexes)^n- Performance Optimization (Caching + CDN)^n- Production Settings^n- Documentation^n^n### Checklist^n- [x] Render configuration^n- [x] Vercel configuration^n- [x] E2E tests^n- [x] Database optimization^n- [x] Documentation^n^n**Status:** Ready for production deployment" ^
        --base main ^
        --head feature/backend-posts
    
    if %errorlevel% equ 0 (
        echo.
        echo SUCCESS: Pull request created!
        echo.
        echo Next steps:
        echo 1. Visit: https://github.com/mahatwa04/ElevateU/pulls
        echo 2. Review the pull request
        echo 3. Merge when ready
        echo.
        exit /b 0
    )
)

echo.
echo GitHub CLI not found. Please create PR manually:
echo.
echo 1. Visit: https://github.com/mahatwa04/ElevateU
echo 2. Click "Pull Requests" tab
echo 3. Click "New pull request" button
echo 4. Set:
echo    - Base: main
echo    - Compare: feature/backend-posts
echo 5. Click "Create pull request"
echo 6. Add description from PR_TEMPLATE.md
echo.
echo For detailed instructions, see: PR_TEMPLATE.md
echo.

pause
