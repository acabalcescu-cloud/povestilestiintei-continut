#!/bin/bash
# Instalează verificarea orară a știrilor pe Mac (launchd, în fiecare oră la minutul 47).
# Rulare, din folderul depozitului:  bash mac/instaleaza.sh
# Dezinstalare:                       bash mac/instaleaza.sh --sterge
set -e
DEPOZIT="$(cd "$(dirname "$0")/.." && pwd)"
ETICHETA="ro.povestilestiintei.stiri"
PLIST="$HOME/Library/LaunchAgents/$ETICHETA.plist"

if [ "$1" = "--sterge" ]; then
  launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Verificarea orara a fost oprita si stearsa."
  exit 0
fi

lipsa=0
for p in git python3 node npm curl claude; do
  if ! command -v "$p" >/dev/null 2>&1; then echo "Lipseste: $p"; lipsa=1; fi
done
if [ $lipsa = 1 ]; then
  echo "Instaleaza ce lipseste (vezi mac/README.md), apoi ruleaza din nou."
  exit 1
fi

cd "$DEPOZIT"
echo "Verific accesul la GitHub..."
git fetch -q origin main || { echo "Nu pot accesa depozitul pe GitHub. Vezi mac/README.md, pasul 2."; exit 1; }

echo "Instalez Playwright pentru coperti (o singura data)..."
[ -d node_modules/playwright ] || npm install --no-save --silent playwright
npx --yes playwright install chromium >/dev/null

grep -qx ".stare-mac/" .gitignore 2>/dev/null || echo ".stare-mac/" >> .gitignore
mkdir -p .stare-mac

CALE="$(dirname "$(command -v claude)"):$(dirname "$(command -v node)"):/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$ETICHETA</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$DEPOZIT/mac/verifica.py</string>
  </array>
  <key>WorkingDirectory</key><string>$DEPOZIT</string>
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>$CALE</string></dict>
  <key>StartCalendarInterval</key>
  <dict><key>Minute</key><integer>47</integer></dict>
  <key>StandardOutPath</key><string>$DEPOZIT/.stare-mac/launchd.log</string>
  <key>StandardErrorPath</key><string>$DEPOZIT/.stare-mac/launchd.log</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo
echo "Gata. Verificarea ruleaza in fiecare ora, la minutul 47."
echo "Test acum (doar lista, fara Claude):  python3 mac/verifica.py --doar-lista"
echo "Jurnal:                               cat .stare-mac/jurnal.log"
