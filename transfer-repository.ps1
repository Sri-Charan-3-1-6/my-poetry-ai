# PowerShell script to transfer repository to new location
# Usage: .\transfer-repository.ps1 "https://github.com/YOUR_USERNAME/YOUR_NEW_REPO_NAME.git"

param(
    [Parameter(Mandatory=$true)]
    [string]$NewRepoUrl
)

Write-Host "🚀 Starting repository transfer..." -ForegroundColor Cyan
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
Write-Host "New repository URL: $NewRepoUrl" -ForegroundColor Gray

# Verify we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Error "❌ This directory is not a Git repository!"
    exit 1
}

# Check current status
Write-Host "`n📋 Current repository status:" -ForegroundColor Yellow
git status --short
git remote -v

# Add new remote
Write-Host "`n🔗 Adding new remote..." -ForegroundColor Yellow
try {
    git remote add new-origin $NewRepoUrl
    Write-Host "✅ New remote added successfully" -ForegroundColor Green
} catch {
    Write-Error "❌ Failed to add new remote: $_"
    exit 1
}

# Push all branches to new repository
Write-Host "`n📤 Pushing main branch to new repository..." -ForegroundColor Yellow
try {
    git push new-origin main
    Write-Host "✅ Main branch pushed successfully" -ForegroundColor Green
} catch {
    Write-Warning "⚠️ Failed to push main branch: $_"
}

# Push all branches
Write-Host "`n📤 Pushing all branches..." -ForegroundColor Yellow
try {
    git push new-origin --all
    Write-Host "✅ All branches pushed successfully" -ForegroundColor Green
} catch {
    Write-Warning "⚠️ Failed to push all branches: $_"
}

# Push all tags
Write-Host "`n📤 Pushing all tags..." -ForegroundColor Yellow
try {
    git push new-origin --tags
    Write-Host "✅ All tags pushed successfully" -ForegroundColor Green
} catch {
    Write-Warning "⚠️ Failed to push tags: $_"
}

# Ask user if they want to switch to new repository as default
$response = Read-Host "`n❓ Do you want to make the new repository your default origin? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "`n🔄 Updating default origin..." -ForegroundColor Yellow
    try {
        git remote remove origin
        git remote rename new-origin origin
        Write-Host "✅ Default origin updated successfully" -ForegroundColor Green
        Write-Host "🎉 Repository transfer completed!" -ForegroundColor Cyan
        Write-Host "Your new repository is now the default origin." -ForegroundColor Green
    } catch {
        Write-Error "❌ Failed to update default origin: $_"
    }
} else {
    Write-Host "`n✅ Repository copied to new location" -ForegroundColor Green
    Write-Host "Both remotes are available:" -ForegroundColor Gray
    git remote -v
    Write-Host "`nTo push future changes to new repo: git push new-origin main" -ForegroundColor Gray
}

Write-Host "`n📊 Final status:" -ForegroundColor Yellow
git remote -v

Write-Host "`n🎉 Transfer process completed!" -ForegroundColor Cyan