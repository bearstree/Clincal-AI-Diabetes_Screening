$ErrorActionPreference = "Stop"

$baseUrl = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles"
$target = Join-Path $PSScriptRoot "../data/raw/nhanes_2017_2020"
$manifest = Join-Path $target "manifest.sha256"

New-Item -ItemType Directory -Force -Path $target | Out-Null

Get-Content $manifest | Where-Object { $_.Trim() } | ForEach-Object {
    $expected, $name = $_ -split "\s+", 2
    $path = Join-Path $target $name
    if (-not (Test-Path $path)) {
        Invoke-WebRequest -Uri "$baseUrl/$name" -OutFile $path
    }
    $actual = (Get-FileHash -Algorithm SHA256 $path).Hash.ToLower()
    if ($actual -ne $expected) {
        throw "Checksum mismatch: $name"
    }
    Write-Host "verified $name"
}

