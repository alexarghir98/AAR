#!/usr/bin/env python3
"""gen_apex.py - writes apps/aar_cluster_themes/hud/layouts/apex.json, the Apex theme (AAR's own sport dash). Edit the
numbers here and run it again; don't edit the JSON.

    python3 tools/gen_apex.py

Everything that isn't text is one shader (shared/shaders.js adash): two upright light columns for speed (left) and revs
(right), a car seen from above in the middle with a lead to each tyre's readout, four thin level bars (boost and oil on
the left, coolant and fuel on the right) and two dividers. The text widgets (scale numbers, the speed, the gear and the
drive mode, the tyre readouts, the bar readouts and the bottom row) sit round it. Panel 1920x720; shared/visible.js has
what the hood hides (top corners) and BMW's gear letter window in the bottom row (x 1380..1460), which stays uncovered.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, 'apps', 'aar_cluster_themes')
OUT = os.path.join(APP, 'hud', 'layouts', 'apex.json')
FONTS = os.path.join(APP, 'hud', 'fonts')

W, H = 1920, 720
TOP = 660                      # the shader's height; the bottom row (clock, range, outside) is under it
COL = (118, 34, 150, 600)      # the left column: x, width, top y, bottom y (the right one is its mirror)
TICKS = (8, 8)                 # intervals between labels: speed (SPEED_SCALE's 9 labels), rpm 0..8
RPM_MAX = 8000
LABEL_X = 186                  # scale numbers: left edge on the left (right edge mirrored on the right)
CAR = (960, 362, 124)          # the car: centre x, y, px per unit
WHEEL_Y = 0.62                 # wheel centres, car units from the middle
LEAD = 0.6                     # the leads start this far out (car units) and run 70 px
DIV = (590, 1330, 150, 600)    # dividers: left x, right x, top y, bottom y
HOLE = [600, 120, 720, 480]    # the Waze map window
LEFT_BAR_X, RIGHT_BAR_X, BAR_W = 320, 1400, 200
BAR_Y = (418, 508)             # the upper and lower bar on each side


def cell(font):
    with open(os.path.join(FONTS, font + '.json')) as f:
        return json.load(f)['cellHeight']


def text(id_, x, y, w, font, txt, color='fg', align='center', **kw):
    d = {'id': id_, 'type': 'text', 'z': 5, 'x': int(round(x)), 'y': int(round(y)), 'w': int(w), 'h': cell(font),
         'text': txt, 'font': font, 'color': color, 'align': align}
    d.update(kw)
    return d


ICONS = {'gauge': (30, 28), 'oilcan': (36, 24), 'therm': (24, 30), 'fuel': (24, 28)}


def readout(prefix, x0, bar_y, icon, value, unit):
    """A bar's icon (left), value and unit (right), above the bar from x0 to x0 + BAR_W."""
    iw, ih = ICONS[icon]
    return [
        {'id': prefix + '_icon', 'type': 'icon', 'icon': icon, 'z': 5, 'x': x0, 'y': bar_y - 18 - ih, 'w': iw, 'h': ih,
         'color': 'dim'},
        text(prefix, x0 + BAR_W - 132, bar_y - 46, 84, 'k_val', value, 'fg', 'right'),
        text(prefix + '_u', x0 + BAR_W - 44, bar_y - 43, 50, 'k_unit', unit, 'dim', 'left'),
    ]


def main():
    x0, cw, y_top, y_bot = COL
    span = y_bot - y_top - 12
    widgets = [{
        'id': 'apex', 'type': 'adash', 'class': 'content', 'z': 1, 'x': 0, 'y': 0, 'w': W, 'h': TOP,
        'col': list(COL), 'ticks': list(TICKS), 'rpmMax': RPM_MAX,
        'bars': [[LEFT_BAR_X, BAR_Y[0], BAR_W], [LEFT_BAR_X, BAR_Y[1], BAR_W],
                 [RIGHT_BAR_X, BAR_Y[0], BAR_W], [RIGHT_BAR_X, BAR_Y[1], BAR_W]],
        'car': list(CAR), 'div': list(DIV),
        'hole': HOLE, 'holeWhen': 'mapUp', 'holeInset': 10, 'holeRadius': 24,
    }]

    # the scale numbers beside each column's marks; the one nearest the marker lights up white
    sh = cell('k_scale')
    for i in range(TICKS[0] + 1):
        y = y_bot - 6 - span * i / TICKS[0]
        widgets.append(text('spd%d' % i, LABEL_X, y - sh / 2, 70, 'k_scale', '{{spd:%d}}' % i, 'kscale', 'left',
                            near=['speed', i]))
    for i in range(TICKS[1] + 1):
        y = y_bot - 6 - span * i / TICKS[1]
        widgets.append(text('rpm%d' % i, W - LABEL_X - 70, y - sh / 2, 70, 'k_scale', str(i), 'kscale', 'right',
                            near=['rpm', i]))
    widgets += [
        text('speed_cap', LABEL_X, y_top - 40, 90, 'k_unit', '{{u:speedLc}}', 'dim', 'left'),
        text('rpm_cap', W - LABEL_X - 90, y_top - 40, 90, 'k_unit', 'x1000', 'dim', 'right'),
    ]

    # left: the speed and its unit, boost and oil; right: the gear and the drive mode, coolant and fuel
    widgets += [
        text('speed', 280, 160, 280, 'k_speed', '{{speed}}'),
        text('speed_unit', 380, 262, 100, 'k_unit', '{{u:speedLc}}', 'dim'),
        text('gear', W - 560, 168, 280, 'k_gear', '{{gear}}', hotWhen='now'),
        text('mode', W - 560, 264, 280, 'k_label', '{{mode}}', 'klabel'),
    ]
    widgets += readout('boost', LEFT_BAR_X, BAR_Y[0], 'gauge', '{{boost}}', '{{u:boost}}')
    widgets += readout('oil', LEFT_BAR_X, BAR_Y[1], 'oilcan', '{{oil}}', '{{u:temp}}')
    widgets += readout('coolant', RIGHT_BAR_X, BAR_Y[0], 'therm', '{{coolant}}', '{{u:temp}}')
    widgets += readout('fuel', RIGHT_BAR_X, BAR_Y[1], 'fuel', '{{fuelPct}}', '%')

    # the tyres: pressure and temperature at the end of each lead (hidden while the map takes the middle)
    cx, cy, s = CAR
    lead_end = LEAD * s + 70
    for corner, sx, sy in (('FL', -1, -1), ('FR', 1, -1), ('RL', -1, 1), ('RR', 1, 1)):
        wy = cy + sy * WHEEL_Y * s
        if sx < 0:
            xr = cx - lead_end - 8                       # right edge of the left readouts
            widgets += [
                text('t%s_p' % corner, xr - 118, wy - 31, 74, 'k_val', '{{tyreP:%s}}' % corner, 'fg', 'right', toggle='!mapUp'),
                text('t%s_pu' % corner, xr - 40, wy - 28, 40, 'k_unit', '{{u:pressure}}', 'dim', 'left', toggle='!mapUp'),
                text('t%s_t' % corner, xr - 110, wy + 4, 110, 'k_unit', '{{tyreT:%s}}{{u:temp}}' % corner, 'dim', 'right',
                     toggle='!mapUp'),
            ]
        else:
            xl = cx + lead_end + 8                       # left edge of the right readouts
            widgets += [
                text('t%s_p' % corner, xl, wy - 31, 54, 'k_val', '{{tyreP:%s}}' % corner, 'fg', 'left', toggle='!mapUp'),
                text('t%s_pu' % corner, xl + 58, wy - 28, 40, 'k_unit', '{{u:pressure}}', 'dim', 'left', toggle='!mapUp'),
                text('t%s_t' % corner, xl, wy + 4, 110, 'k_unit', '{{tyreT:%s}}{{u:temp}}' % corner, 'dim', 'left',
                     toggle='!mapUp'),
            ]
    widgets.append(text('badge', 810, 64, 300, 'k_unit', '{{badge}}', 'dim'))

    # the bottom row: covers BMW's own strip but its gear letter (x 1380..1460), then the clock, range and outside
    row = 676
    widgets += [
        {'id': 'strip_cover_l', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 0, 'y': TOP, 'w': 1380, 'h': H - TOP,
         'color': 'bg', 'stripRow': 'l'},
        {'id': 'strip_cover_r', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 1460, 'y': TOP, 'w': W - 1460,
         'h': H - TOP, 'color': 'bg', 'stripRow': 'r'},
        text('strip_time', 150, row, 120, 'k_val', '{{time}}', 'fg', 'right', z=3, stripRow='l'),
        text('strip_ampm', 276, row + 3, 40, 'k_unit', '{{ampmLc}}', 'dim', 'left', z=3, stripRow='l'),
        text('strip_range', 874, row, 110, 'k_val', '{{range}}', 'fg', 'right', z=3, stripRow='l'),
        text('strip_range_u', 990, row + 3, 40, 'k_unit', '{{u:distLc}}', 'dim', 'left', z=3, stripRow='l'),
        text('strip_out', 1666, row, 90, 'k_val', '{{ambient}}', 'fg', 'right', z=3, stripRow='r'),
        text('strip_out_u', 1762, row + 3, 36, 'k_unit', '{{u:temp}}', 'dim', 'left', z=3, stripRow='r'),
    ]

    layout = {
        'schemaVersion': 2,
        'name': 'Apex',
        'theme': 'apex',
        '_about': ("AAR's own sport dash, generated by tools/gen_apex.py (edit that and regenerate): speed (SPEED_SCALE) and "
                   "revs (0..8) as two upright light columns at the far left and right, lit in LED steps in the drive "
                   "mode's colour (theme 'apex' modes), the speed and gear in big figures inside them, boost and oil on "
                   "the left, coolant and fuel on the right, and a car seen from above in the middle with each tyre's "
                   "pressure and temperature (a wheel turns amber under 1.9 bar). While the Waze map shows inside the theme "
                   "('mapUp') the middle is cut see-through and the tyre readouts step aside. Everything that isn't text "
                   "is one shader (adash). The bottom row has the clock, range and outside temperature, BMW's gear letter "
                   "left uncovered. Widget reference: shared/hud.js header."),
        'widgets': widgets,
    }
    with open(OUT, 'w') as f:
        json.dump(layout, f, indent=2)
        f.write('\n')
    print('wrote %s: %d widgets' % (os.path.relpath(OUT, ROOT), len(widgets)))


if __name__ == '__main__':
    main()
