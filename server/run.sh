#!/bin/sh
set -eu
cd /root/car-market-monitor
git pull --ff-only origin main
python3 server/monitor.py
git add data/car-market-history.json
git diff --cached --quiet || git commit -m "Update car market snapshot"
git push origin main
