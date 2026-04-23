# Plint + OpenClaw Setup Script for Windows
# Run this after installing OpenClaw
# Usage: .\setup-openclaw.ps1

Write-Host "🦞 Plint + OpenClaw Setup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if OpenClaw is installed
$openclawInstalled = Get-Command openclaw -ErrorAction SilentlyContinue
if (-not $openclawInstalled) {
    Write-Host "❌ OpenClaw not found. Installing..." -ForegroundColor Yellow
    Invoke-WebRequest -UseBasicParsing https://openclaw.ai/install.ps1 | Invoke-Expression
    Write-Host "✅ OpenClaw installed!" -ForegroundColor Green
} else {
    Write-Host "✅ OpenClaw already installed" -ForegroundColor Green
}

Write-Host ""

# Create directories
$openclawDir = "$env:USERPROFILE\.openclaw"
$credentialsDir = "$openclawDir\credentials"
$skillsDir = "$openclawDir\skills"
$logsDir = "$openclawDir\logs"

Write-Host "📁 Creating directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $credentialsDir | Out-Null
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
New-Item -ItemType Directory -Force -Path $logsDir | Out-Null
Write-Host "✅ Directories created" -ForegroundColor Green

Write-Host ""

# Copy skills
$plintSkillsDir = "$PSScriptRoot\openclaw-skills"
if (Test-Path $plintSkillsDir) {
    Write-Host "📦 Copying Plint skills..." -ForegroundColor Cyan
    Copy-Item "$plintSkillsDir\*" -Destination $skillsDir -Force
    Write-Host "✅ Skills copied to $skillsDir" -ForegroundColor Green
} else {
    Write-Host "⚠️ Skills directory not found at $plintSkillsDir" -ForegroundColor Yellow
}

Write-Host ""

# Prompt for configuration
Write-Host "⚙️ Configuration Setup" -ForegroundColor Cyan
Write-Host "----------------------" -ForegroundColor Cyan

# OpenRouter API Key
Write-Host ""
Write-Host "1️⃣ OpenRouter API Key" -ForegroundColor Yellow
Write-Host "   Get your free key at: https://openrouter.ai"
$openrouterKey = Read-Host "   Enter your OpenRouter API key (or press Enter to skip)"

# Telegram Bot Token
Write-Host ""
Write-Host "2️⃣ Telegram Bot Token" -ForegroundColor Yellow
Write-Host "   Create a bot with @BotFather on Telegram"
$telegramToken = Read-Host "   Enter your Telegram bot token (or press Enter to skip)"

# Firebase Project ID
Write-Host ""
Write-Host "3️⃣ Firebase Project ID" -ForegroundColor Yellow
$firebaseProject = Read-Host "   Enter your Firebase project ID (or press Enter to skip)"

# Create environment file
Write-Host ""
Write-Host "💾 Saving environment variables..." -ForegroundColor Cyan
$envFile = "$openclawDir\.env"

$envContent = @"
# Plint + OpenClaw Environment Variables
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# OpenRouter (LLM Provider)
OPENROUTER_API_KEY=$openrouterKey

# Telegram Bot
TELEGRAM_BOT_TOKEN=$telegramToken

# Firebase
FIREBASE_PROJECT_ID=$firebaseProject

# Plint Specific
PLINT_STORE_URL=https://your-store.netlify.app
LOW_STOCK_THRESHOLD=5
"@

Set-Content -Path $envFile -Value $envContent
Write-Host "✅ Environment saved to $envFile" -ForegroundColor Green

# Copy config template
Write-Host ""
Write-Host "📋 Setting up configuration..." -ForegroundColor Cyan
$configSource = "$plintSkillsDir\config.yaml"
$configDest = "$openclawDir\config.yaml"

if (Test-Path $configSource) {
    Copy-Item $configSource -Destination $configDest -Force
    Write-Host "✅ Configuration copied" -ForegroundColor Green
} else {
    Write-Host "⚠️ Config template not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Add your Firebase service account key to:" -ForegroundColor White
Write-Host "   $credentialsDir\firebase-key.json" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Edit configuration if needed:" -ForegroundColor White
Write-Host "   $configDest" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start OpenClaw:" -ForegroundColor White
Write-Host "   openclaw start" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Message your Telegram bot to test!" -ForegroundColor White
Write-Host ""
Write-Host "📚 Full guide: OPENCLAW_SETUP_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
