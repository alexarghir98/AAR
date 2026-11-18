#!/usr/bin/env python3
"""gen_curved.py - writes apps/cluster_themes/hud/layouts/curved.json, the Curved theme (after BMW's newer
clusters, iDrive 8 / 8.5 Curved Display, Drive layout). Edit the numbers here and run it again; don't edit the JSON.

    python3 tools/gen_curved.py

Everything that isn't text is one shader (shared/shaders.js cdash): two thin bowed scales, speed left and revs right,
a band inside each line that lights from 0 to the value, fuel and oil bars, a curved base line and a road in the
middle while no map shows. The text widgets (scale numbers, the speed, the gear, the drive mode and the bottom row)
sit round it. Panel 1920x720; shared/visible.js has what the hood hides (top corners) and BMW's gear letter window in
the bottom row (x 1380..1460), which stays uncovered.
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'apps', 'cluster_themes', 'hud', 'layouts', 'curved.json')
FONTS = os.path.join(ROOT, 'apps', 'cluster_themes', 'hud', 'fonts')

W, H = 1920, 720
TOP = 660                      # the shader's height; the bottom row (clock, coolant, outside) is under it
ARC = (640, 366, 530, 27.5)    # the left scale's circle: centre x, y, radius, half the sweep in degrees
BAND = 11                      # the lit band inside the line, px
LABEL_IN = BAND + 58          # scale numbers: px inside the line (their centres)
TICKS = (8, 8)                 # intervals between labels: speed (SPEED_SCALE's 9 labels), rpm 0..8
RPM_MAX = 8000
HOLE = [524, 136, 872, 462]    # the Waze map window (as the Sport theme's)
ROAD = (318, 1.25)             # horizon y, px scale
BASE = (618, 18, 214)          # base line: y at its ends, sag in the middle, left end x (right end mirrored)
FUEL_BAR = (334, 433, 150)     # x0, y, width
OIL_BAR = (W - 334 - 150, 433, 150)


def cell(font):
    with open(os.path.join(FONTS, font + '.json')) as f:
        return json.load(f)['cellHeight']


def on_arc(t, inset):
    """Target px of the point t (0 bottom .. 1 top) on the left scale, `inset` px inside its line."""
    cx, cy, r, half = ARC
    phi = math.radians(half) * (1 - 2 * t)
    rr = r - inset
    return cx - rr * math.cos(phi), cy + rr * math.sin(phi)


def text(id_, x, y, w, font, txt, color='fg', align='center', **kw):
    d = {'id': id_, 'type': 'text', 'z': 5, 'x': int(round(x)), 'y': int(round(y)), 'w': int(w), 'h': cell(font),
         'text': txt, 'font': font, 'color': color, 'align': align}
    d.update(kw)
    return d


def main():
    widgets = [{
        'id': 'curved', 'type': 'cdash', 'class': 'content', 'z': 1, 'x': 0, 'y': 0, 'w': W, 'h': TOP,
        'arc': list(ARC), 'band': BAND, 'ticks': list(TICKS), 'rpmMax': RPM_MAX,
        'fuelBar': list(FUEL_BAR), 'oilBar': list(OIL_BAR), 'base': list(BASE), 'road': list(ROAD),
        'hole': HOLE, 'holeWhen': 'mapUp', 'holeInset': 10, 'holeRadius': 28,
    }]
    # the scale numbers, inside each line; the one nearest the needle lights up white
    sh = cell('k_scale')
    for i in range(TICKS[0] + 1):
        x, y = on_arc(i / TICKS[0], LABEL_IN)
        widgets.append(text('spd%d' % i, x - 36, y - sh / 2, 72, 'k_scale', '{{spd:%d}}' % i, 'kscale', near=['speed', i]))
    for i in range(TICKS[1] + 1):
        x, y = on_arc(i / TICKS[1], LABEL_IN)
        widgets.append(text('rpm%d' % i, W - x - 30, y - sh / 2, 60, 'k_scale', str(i), 'kscale', near=['rpm', i]))

    # left: the speed, its unit, fuel; right: the gear, the drive mode, oil
    lx, rx = 380, W - 380
    widgets += [
        text('speed', lx - 140, 246, 280, 'k_speed', '{{speed}}'),
        text('speed_unit', lx - 60, 352, 120, 'k_unit', '{{u:speedLc}}', 'dim'),
        {'id': 'fuel_icon', 'type': 'icon', 'icon': 'fuel', 'z': 5, 'x': FUEL_BAR[0] - 38, 'y': FUEL_BAR[1] - 14,
         'w': 22, 'h': 26, 'color': 'dim'},
        text('range', FUEL_BAR[0], FUEL_BAR[1] + 16, 104, 'k_val', '{{range}}', 'fg', 'right'),
        text('range_u', FUEL_BAR[0] + 110, FUEL_BAR[1] + 18, 44, 'k_unit', '{{u:distLc}}', 'dim', 'left'),
        text('gear', rx - 140, 256, 280, 'k_gear', '{{gear}}', hotWhen='now'),
        text('mode', rx - 140, 356, 280, 'k_label', '{{mode}}', 'klabel'),
        {'id': 'oil_icon', 'type': 'icon', 'icon': 'oilcan', 'z': 5, 'x': OIL_BAR[0] - 46, 'y': OIL_BAR[1] - 12,
         'w': 34, 'h': 22, 'color': 'dim'},
        text('oil', OIL_BAR[0], OIL_BAR[1] + 16, 104, 'k_val', '{{oil}}', 'fg', 'right'),
        text('oil_u', OIL_BAR[0] + 110, OIL_BAR[1] + 18, 40, 'k_unit', '{{u:temp}}', 'dim', 'left'),
        text('badge', 810, 64, 300, 'k_unit', '{{badge}}', 'dim'),
    ]

    # the bottom row: covers BMW's own strip but its gear letter (x 1380..1460), then the clock, coolant and outside
    vh, uh = cell('k_val'), cell('k_unit')
    row = 676
    widgets += [
        {'id': 'strip_cover_l', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 0, 'y': TOP, 'w': 1380, 'h': H - TOP,
         'color': 'bg', 'stripRow': 'l'},
        {'id': 'strip_cover_r', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 1460, 'y': TOP, 'w': W - 1460,
         'h': H - TOP, 'color': 'bg', 'stripRow': 'r'},
        text('strip_time', 150, row, 120, 'k_val', '{{time}}', 'fg', 'right', z=3, stripRow='l'),
        text('strip_ampm', 276, row + 3, 40, 'k_unit', '{{ampmLc}}', 'dim', 'left', z=3, stripRow='l'),
        {'id': 'therm', 'type': 'icon', 'icon': 'therm', 'z': 3, 'x': 880, 'y': row - 1, 'w': 22, 'h': 28,
         'color': 'dim', 'stripRow': 'l'},
        text('strip_coolant', 906, row, 80, 'k_val', '{{coolant}}', 'fg', 'right', z=3, stripRow='l'),
        text('strip_coolant_u', 992, row + 3, 40, 'k_unit', '{{u:temp}}', 'dim', 'left', z=3, stripRow='l'),
        text('strip_out', 1666, row, 90, 'k_val', '{{ambient}}', 'fg', 'right', z=3, stripRow='r'),
        text('strip_out_u', 1762, row + 3, 36, 'k_unit', '{{u:temp}}', 'dim', 'left', z=3, stripRow='r'),
    ]
    assert vh and uh

    layout = {
        'schemaVersion': 2,
        'name': 'Curved',
        'theme': 'curved',
        'mapLive': True,
        '_about': ("After BMW's newer clusters (iDrive 8 / 8.5 Curved Display, Drive layout), generated by "
                   "tools/gen_curved.py (edit that and regenerate): two thin bowed scales, speed left (SPEED_SCALE) and "
                   "revs right (0..8), each with a band that lights from 0 to the needle in the drive mode's colour "
                   "(theme 'curved' modes: blue Comfort, orange-red Sport, red Sport Plus, teal Eco Pro), the speed and "
                   "range inside the left scale, the gear, the drive mode and the oil temperature inside the right one, "
                   "a curved base line and a road to a soft horizon in the middle. While the Waze map shows inside the "
                   "theme ('mapUp') the middle is cut see-through (mapLive: no rebuild). Everything that isn't text is "
                   "one shader (cdash). The bottom row has the clock, coolant and outside temperature, BMW's gear "
                   "letter left uncovered. Widget reference: shared/hud.js header."),
        'widgets': widgets,
    }
    with open(OUT, 'w') as f:
        json.dump(layout, f, indent=2)
        f.write('\n')
    print('wrote %s: %d widgets' % (os.path.relpath(OUT, ROOT), len(widgets)))


if __name__ == '__main__':
    main()
