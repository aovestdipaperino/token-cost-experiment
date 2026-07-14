#!/usr/bin/env bash
# Runs the same task in English and Italian via Claude Code headless,
# then prints the output-token counts and the delta. Requires: claude, jq.
set -uo pipefail
cd "$(dirname "$0")"
rm -rf .runs; mkdir -p .runs/en .runs/it
cp utils.py .runs/en/; cp utils.py .runs/it/

echo "== English =="
( cd .runs/en && claude -p "Read utils.py and write a clear explanation, about 6 sentences, of what each function does. Respond in English." --output-format json --max-turns 3 ) > en.json

echo "== Italian =="
( cd .runs/it && claude -p "Leggi utils.py e scrivi una spiegazione chiara, circa 6 frasi, di cosa fa ciascuna funzione. Rispondi in italiano." --output-format json --max-turns 3 ) > it.json

en=$(jq '.usage.output_tokens' en.json); it=$(jq '.usage.output_tokens' it.json)
echo; echo "English output tokens: $en"; echo "Italian output tokens: $it"
awk -v e="$en" -v i="$it" 'BEGIN{printf "Delta: +%.0f%% more tokens in Italian\n",(i-e)/e*100}'
echo "Regenerate the GIF with: python3 make_gif.py"
