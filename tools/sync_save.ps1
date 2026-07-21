# sync_save.ps1 — Import TFWR save code into the curated repo layout.
# Dry-run by default (reports NEW / CHANGED / OK / UNMAPPED). Use -Apply to copy.
# Compatible with Windows PowerShell 5.1.
param(
    [switch]$Apply,
    [string]$SaveDir = "$env:USERPROFILE\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\pygame"
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$mapJson = Get-Content (Join-Path $PSScriptRoot 'sync_map.json') -Raw -Encoding UTF8 | ConvertFrom-Json

$skip = @($mapJson.skip)
$stats = @{ new = 0; changed = 0; ok = 0; unmapped = 0 }

if (-not (Test-Path $SaveDir)) { Write-Error "Save dir not found: $SaveDir" }

foreach ($f in Get-ChildItem $SaveDir -File) {
    if ($skip -contains $f.Name) { continue }
    $destRel = $mapJson.files.PSObject.Properties[$f.Name].Value
    if (-not $destRel) {
        Write-Host ("UNMAPPED  {0}" -f $f.Name) -ForegroundColor Yellow
        $stats.unmapped++
        continue
    }
    $dest = Join-Path $repo ($destRel -replace '/', '\')
    if (-not (Test-Path $dest)) {
        Write-Host ("NEW       {0} -> {1}" -f $f.Name, $destRel) -ForegroundColor Cyan
        $stats.new++
        if ($Apply) {
            New-Item -ItemType Directory -Force -Path (Split-Path $dest -Parent) | Out-Null
            Copy-Item $f.FullName $dest
        }
    }
    else {
        $srcHash = (Get-FileHash $f.FullName -Algorithm MD5).Hash
        $dstHash = (Get-FileHash $dest -Algorithm MD5).Hash
        if ($srcHash -ne $dstHash) {
            Write-Host ("CHANGED   {0} -> {1}" -f $f.Name, $destRel) -ForegroundColor Magenta
            $stats.changed++
            if ($Apply) { Copy-Item $f.FullName $dest -Force }
        }
        else { $stats.ok++ }
    }
}

Write-Host ""
Write-Host ("OK: {0}  NEW: {1}  CHANGED: {2}  UNMAPPED: {3}" -f $stats.ok, $stats.new, $stats.changed, $stats.unmapped)
if (-not $Apply -and ($stats.new + $stats.changed) -gt 0) {
    Write-Host "Dry-run only. Re-run with -Apply to copy." -ForegroundColor Green
}
if ($stats.unmapped -gt 0) {
    Write-Host "Add unmapped files to tools/sync_map.json (or to its 'skip' list)." -ForegroundColor Yellow
}
