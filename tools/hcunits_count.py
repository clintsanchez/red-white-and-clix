#!/usr/bin/env python3
"""Count Red White & Clix 2026 registrations on HCUnits and append to a log.

Reads only the PUBLIC circuit and event pages (HCUnits has no API; /api/ is
disallowed in its robots.txt). Logs counts, never player names.

    python3 tools/hcunits_count.py
"""
import csv, datetime, html, os, re, urllib.request

BASE = 'https://hcunits.net'
CIRCUIT = '/circuits/red_white_and_clix_2026/'
EVENTS = {'300 Modern': '/events/9151/', 'Team Sealed': '/events/9152/'}
GOAL = 80
LOG = os.path.join(os.path.dirname(__file__), '..', '06-Reports', 'hcunits-registrations.csv')

def text(path):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'Mozilla/5.0 (RWC registration check)'})
    h = urllib.request.urlopen(req, timeout=30).read().decode()
    h = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    return [l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '\n', h)).split('\n') if l.strip()]

def after(lines, label, anchor=None):
    """Return the first integer that follows `label` in the page text.

    `anchor` skips ahead past a heading first: the side menu also has a
    "Players" tab, followed by the event name ("RWC 300 MODERN"), which would
    otherwise be read as 300 players.
    """
    start = lines.index(anchor) if anchor else 0
    for i, l in enumerate(lines[start:], start):
        if l == label:
            for nxt in lines[i + 1:i + 4]:
                m = re.search(r'\d+', nxt)
                if m:
                    return int(m.group())
    raise SystemExit(f'Could not find "{label}" - the page layout may have changed. Check it by hand.')

total = after(text(CIRCUIT + 'players/'), 'Total Players')
modern = after(text(EVENTS['300 Modern']), 'Players', anchor='Registration Type')
teams = after(text(EVENTS['Team Sealed']), 'Parties', anchor='Registration Type')

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
new = not os.path.exists(LOG)
with open(LOG, 'a', newline='') as f:
    w = csv.writer(f)
    if new:
        w.writerow(['checked', 'total_players', '300_modern_players', 'team_sealed_teams'])
    w.writerow([now, total, modern, teams])

print(f'{now}: {total} players registered ({modern} in 300 Modern, {teams} Team Sealed team(s)). '
      f'Goal {GOAL}: {total / GOAL:.0%}.')
