#!/bin/sh
set -eu
cd /root/car-market-monitor
git pull --ff-only origin main
python3 server/monitor.py
git add data/car-market-history.json
git diff --cached --quiet || git commit -m "Update car market snapshot"
git push origin main
mkdir -p /var/www/elitecar-monitor/data
cp car-market.html /var/www/elitecar-monitor/index.html
cp data/car-market-history.json /var/www/elitecar-monitor/data/car-market-history.json
