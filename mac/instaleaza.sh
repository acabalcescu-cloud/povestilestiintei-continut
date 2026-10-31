#!/bin/bash
# Instalează pe Mac (launchd):
#   - verificarea știrilor: în fiecare oră, la minutul 47 (mac/verifica.py);
#   - verificarea din ziua meciului: la fiecare 5 minute (mac/meci.py), care pornește Claude
#     la 2 ore după start, apoi din 30 în 30 de minute, până la 23:55.
# Rulare, din folderul depozitului:  bash mac/instaleaza.sh
# Dezinstalare:                       bash mac/instaleaza.sh --sterge
set -e
DEPOZIT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTI="$HOME/Library/LaunchAgents"
PLIST_STIRI="$AGENTI/ro.povestilestiintei.stiri.plist"
PLIST_MECI="$AGENTI/ro.povestilestiintei.meci.plist"

if [ "$1" = "--sterge" ]; then
  for p in "$PLIST_STIRI" "$PLIST_MECI"; do
    launchctl bootout "gui/$(id -u)" "$p" 2>/dev/null || true
    rm -f "$p"
  done
  echo "Verificarile de pe Mac au fost oprite si sterse."
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
mkdir -p .stare-mac "$AGENTI"

CALE="$(dirname "$(command -v claude)"):$(dirname "$(command -v node)"):/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# scrie_plist <fisier> <eticheta> <script> <programare-xml> <jurnal>
scrie_plist() {
  cat > "$1" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$2</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$DEPOZIT/mac/$3</string>
  </array>
  <key>WorkingDirectory</key><string>$DEPOZIT</string>
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>$CALE</string></dict>
  $4
  <key>StandardOutPath</key><string>$DEPOZIT/.stare-mac/$5</string>
  <key>StandardErrorPath</key><string>$DEPOZIT/.stare-mac/$5</string>
</dict>
</plist>
PLIST
}

scrie_plist "$PLIST_STIRI" ro.povestilestiintei.stiri verifica.py \
  '<key>StartCalendarInterval</key><dict><key>Minute</key><integer>47</integer></dict>' launchd.log
scrie_plist "$PLIST_MECI" ro.povestilestiintei.meci meci.py \
  '<key>StartInterval</key><integer>300</integer>' launchd-meci.log

for p in "$PLIST_STIRI" "$PLIST_MECI"; do
  launchctl bootout "gui/$(id -u)" "$p" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$p"
done

echo
echo "Gata."
echo "Stirile se verifica in fiecare ora, la minutul 47."
echo "In zilele cu meci, cronica si video se verifica la 2 ore dupa start, apoi din 30 in 30 de minute, pana la 23:55."
echo "Test stiri (doar lista, fara Claude):  python3 mac/verifica.py --doar-lista"
echo "Programul de azi pentru meci:          python3 mac/meci.py --program"
echo "Jurnal:                                cat .stare-mac/jurnal.log"
