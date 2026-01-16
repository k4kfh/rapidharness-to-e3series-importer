"""Set development version based on git commit hash."""

# Get the short hash of the current commit
$commitHash = git rev-parse --short HEAD

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to get git commit hash. Make sure you're in a git repository."
    exit 1
}

$devVersion = "dev-$commitHash"
$versionFile = "src/__version__.py"

# Update the version file
$content = @"
"""Version information for the From-To List Converter."""

__version__ = "$devVersion"
"@

Set-Content -Path $versionFile -Value $content -Encoding UTF8
Write-Host "Development version set to: $devVersion" -ForegroundColor Green
