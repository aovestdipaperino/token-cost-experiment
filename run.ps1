#!/usr/bin/env pwsh
# Runs the same task in English and Italian via Claude Code headless. Requires: claude, jq.
$ErrorActionPreference='Continue'; Set-Location $PSScriptRoot
Remove-Item .runs -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force .runs\en, .runs\it | Out-Null
Copy-Item utils.py .runs\en\; Copy-Item utils.py .runs\it\
Write-Host "== English =="
Push-Location .runs\en
claude -p "Read utils.py and write a clear explanation, about 6 sentences, of what each function does. Respond in English." --output-format json --max-turns 3 | Out-File -Encoding utf8 ..\..\en.json
Pop-Location
Write-Host "== Italian =="
Push-Location .runs\it
claude -p "Leggi utils.py e scrivi una spiegazione chiara, circa 6 frasi, di cosa fa ciascuna funzione. Rispondi in italiano." --output-format json --max-turns 3 | Out-File -Encoding utf8 ..\..\it.json
Pop-Location
$en=(jq '.usage.output_tokens' en.json); $it=(jq '.usage.output_tokens' it.json)
Write-Host "`nEnglish output tokens: $en"; Write-Host "Italian output tokens: $it"
Write-Host ("Delta: +{0:N0}% more tokens in Italian" -f (($it-$en)/$en*100))
