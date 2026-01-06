$env:Path += ";C:\Program Files\Git\cmd"

# Git Configuration
git config --global user.name "tameratta1997"
git config --global user.email "tameratta1997@users.noreply.github.com"
# Credential helper is handled by GH CLI usually, but let's ensure
& "C:\Program Files\GitHub CLI\gh.exe" auth setup-git

# Initialize
if (-not (Test-Path .git)) {
    git init
}

# Add and Commit
git add .
git commit -m "Initial commit of Inventory System"

# Create Repo and Push
# We use 'try' because it might already exist
try {
    & "C:\Program Files\GitHub CLI\gh.exe" repo create tameratta1997/InventorySystem --private --source=. --remote=origin --push
}
catch {
    Write-Host "Repo might already exist, trying to push..."
    git push -u origin main
}
