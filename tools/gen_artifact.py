#!/usr/bin/env python3
"""gen_artifact.py - writes apps/aar_cluster_themes/hud/layouts/artifact.json, the Artifact theme (after the user's
own mockup "D · Artifact", Nov 2026). Edit the numbers here and run it again; don't edit the JSON.

    python3 tools/gen_artifact.py

The geometry comes from his picture (1774x887): T() maps a point of it to the 1920x720 panel, and the frames were
made a little taller on the mockup (V(): picture y 236..622 to 210..632 for everything tied to them). The right frame
is the left one's mirror. Everything that isn't text is one shader (shared/shaders.js xdash): the glass frames lit
from the bottom up to the speed and the revs, the dark panels, the glints, the base line, the two mini gauges (fuel,
oil), the car with its tyre lines, and the Waze map window, whose edge fades to black while the map shows.

The middle follows the setting "artCenter": the car with each tyre's pressure and temperature, the four readouts
(boost, oil, coolant, fuel), or nothing; while the Waze map shows it gives way to the map (text "showWhen": "!mapUp",
no rebuild). Panel 1920x720; shared/visible.js has what the hood hides (top corners) and BMW's gear letter window in
the bottom row (x 1380..1460), which stays uncovered.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'apps', 'aar_cluster_themes', 'hud', 'layouts', 'artifact.json')
FONTS = os.path.join(ROOT, 'apps', 'aar_cluster_themes', 'hud', 'fonts')

W, H = 1920, 720
TOP = 660
S, X0, Y0 = 1.267, 130, 125            # picture px -> panel px


def V(y):                               # the taller frames
    return 210 + (y - 236) * (632 - 210) / (622 - 236)


def T(x, y, tall=False):
    return ((x - X0) * S, ((V(y) if tall else y) - Y0) * S)


def r(v):
    return round(v, 1)


# the left frame, picture px (outer and inner edge: top, vertex, bottom), taken onto the panel
OUTER = [T(412, 236, True), T(290, 386, True), T(435, 622, True)]
INNER_PIC = [(472, 241), (352, 397), (480, 616)]
FY = [r(p[1]) for p in OUTER]
FO = [r(p[0]) for p in OUTER]


def inner_x(y):
    pts = [T(x, yy, True) for x, yy in INNER_PIC]
    (x0, y0), (x1, y1), (x2, y2) = pts
    if y <= y1:
        return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return x1 + (x2 - x1) * (y - y1) / (y2 - y1)


FI = [r(inner_x(y)) for y in FY]
SCALE = [r(T(0, 610, True)[1]), r(T(0, 243, True)[1])]      # y of the 0 mark and of the top mark
PAN = [*map(r, T(625, 250, True)), *map(r, T(742, 404, True)), *map(r, T(520, 618, True))]
BASE = [r(T(0, 622, True)[1]), r(T(420, 0)[0])]
MINI = [*map(r, T(391, 446, True)), *map(r, T(489, 601, True))]
CAR = (960, r(T(0, 433)[1]), S)
TYRE_X, TYRE_LEN = 878, 108             # the tyre lines: inner end x (left; mirrored), length
WIN = [690, 160, 540, 436]              # the map window, inside BMW's map slot (416,120 1088x480)
COLORS = [[11, 42, 92], [46, 139, 255], [140, 200, 255]]
RPM_MAX = 8000
SPEED_C, GEAR_C = 530, W - 530


_fonts = {}


def font(name):
    if name not in _fonts:
        with open(os.path.join(FONTS, name + '.json')) as f:
            _fonts[name] = json.load(f)
    return _fonts[name]


def width(fnt, s):
    g = font(fnt)['glyphs']
    return sum(g[c]['advance'] for c in s if c in g)


def text(id_, x, base, w, fnt, txt, color='fg', align='center', **kw):
    """a text box whose baseline is at `base` (panel px)"""
    f = font(fnt)
    d = {'id': id_, 'type': 'text', 'z': 5, 'x': int(round(x)), 'y': int(round(base - f['baseline'])), 'w': int(w),
         'h': f['cellHeight'], 'text': txt, 'font': fnt, 'color': color, 'align': align}
    d.update(kw)
    return d


def edge(y):
    """the left frame's outer edge x at panel y"""
    (x0, y0), (x1, y1), (x2, y2) = OUTER
    if y <= y1:
        return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return x1 + (x2 - x1) * (y - y1) / (y2 - y1)


def main():
    widgets = [{
        'id': 'artifact', 'type': 'xdash', 'class': 'content', 'z': 1, 'x': 0, 'y': 0, 'w': W, 'h': TOP,
        'fy': FY, 'fo': FO, 'fi': FI, 'scale': SCALE, 'rpmMax': RPM_MAX, 'colors': COLORS, 'pan': PAN,
        'base': BASE, 'mini': MINI, 'car': list(CAR), 'carWhen': 'artCenter=tyres',
        'tyre': [TYRE_X, r(T(0, 366)[1]), r(T(0, 522)[1]), TYRE_LEN], 'glow': 1,
        'hole': WIN, 'holeWhen': 'mapUp', 'holeInset': 0, 'holeRadius': 40, 'holeFeather': 70,
    }]

    # left and right are listed apart (one text sheet a side): the scale numbers outside each frame, the one nearest
    # the value lit up, the revs from 6 in pink; the speed, and the gear with the drive mode, in big italic figures
    left, right = [], []
    y0, y8 = SCALE
    for i in range(9):
        y = y0 - i * (y0 - y8) / 8
        ex = edge(y)
        left.append(text('spd%d' % i, ex - 28 - 80, y + 11, 80, 'x_scl', '{{spd:%d}}' % i, 'dim', 'right',
                         near=['speed', i], nearColor='fg'))
        right.append(text('rpm%d' % i, W - ex + 30, y + 13, 50, 'x_sclr', str(i), 'kr' if i >= 6 else 'dim', 'left',
                          near=['rpm', i], nearColor='hot' if i >= 7 else 'fg'))
    right.append(text('rpm_unit', W - 500, r(T(0, 222, True)[1]) + 8, 160, 'k_unit', '1/min x 1000', 'dim'))
    left += [
        text('speed', SPEED_C - 150, r(T(0, 437)[1]), 300, 'x_big', '{{speed}}'),
        text('speed_unit', SPEED_C - 60, r(T(0, 460)[1]), 120, 'k_unit', '{{u:speedLc}}', 'fg'),
    ]
    right += [
        text('gear', GEAR_C - 110, r(T(0, 428)[1]), 220, 'x_gear', '{{gear}}', hotWhen='now'),
        text('mode', GEAR_C - 140, r(T(0, 460)[1]) + 2, 260, 'x_mode', '{{mode}}', 'kmode'),
    ]

    # the mini gauges' labels: fuel on the left (full, half, empty), oil on the right (150, 100, 50 C)
    for (px, py), lab_l, lab_r, k in (((420, 462), '1', '{{temp:150}}', 'hi'), ((470, 530), '1/2', '{{temp:100}}', 'mid'),
                                      ((507, 598), '0', '{{temp:50}}', 'lo')):
        x, y = T(px, py, True)
        x += 18                         # clear of the slanted segments
        left.append(text('fuel_' + k, x - 23, y, 46, 'x_mini', lab_l, 'fg'))
        right.append(text('oil_' + k, W - x - 23, y, 46, 'x_mini', lab_r, 'fg'))
    fx, fy = T(487, 552, True)
    fx += 20
    left.append({'id': 'fuel_icon', 'type': 'icon', 'icon': 'fuel', 'z': 5, 'x': int(fx - 11), 'y': int(fy - 15), 'w': 22, 'h': 26, 'color': 'fg'})
    right.append({'id': 'oil_icon', 'type': 'icon', 'icon': 'oilcan', 'z': 5, 'x': int(W - fx - 17), 'y': int(fy - 11), 'w': 34, 'h': 22, 'color': 'fg'})
    widgets += left + right

    # the middle, "artCenter": the tyres round the car ...
    rows = ((r(T(0, 357)[1]), r(T(0, 390)[1]), 'FL', 'FR'), (r(T(0, 513)[1]), r(T(0, 546)[1]), 'RL', 'RR'))
    tw = lambda f, s: width(f, s) + 2
    for pb, tb, cl, cr in rows:
        # left: right-aligned at the line's inner end; right: left-aligned at its mirror
        xl, xr = TYRE_X, W - TYRE_X
        uw = tw('x_tunit', 'psi')
        widgets += [
            text('t%s_p' % cl, xl - uw - 6 - 70, pb, 70, 'x_tyre', '{{tyreP:%s}}' % cl, 'fg', 'right', toggle='artCenter=tyres', showWhen='!mapUp'),
            text('t%s_u' % cl, xl - uw, pb, uw, 'x_tunit', '{{u:pressure}}', 'fg', 'right', toggle='artCenter=tyres', showWhen='!mapUp'),
            text('t%s_t' % cl, xl - 34 - 60, tb, 60, 'x_ttemp', '{{tyreT:%s}}' % cl, 'fg', 'right', toggle='artCenter=tyres', showWhen='!mapUp'),
            text('t%s_tu' % cl, xl - 30, tb, 30, 'x_tunit', '{{u:temp}}', 'fg', 'right', toggle='artCenter=tyres', showWhen='!mapUp'),
            text('t%s_p' % cr, xr, pb, 56, 'x_tyre', '{{tyreP:%s}}' % cr, 'fg', 'left', toggle='artCenter=tyres', showWhen='!mapUp'),
            text('t%s_u' % cr, xr + 60, pb, uw, 'x_tunit', '{{u:pressure}}', 'fg', 'left', toggle='artCenter=tyres', showWhen='!mapUp'),
            text('t%s_t' % cr, xr, tb, 46, 'x_ttemp', '{{tyreT:%s}}' % cr, 'fg', 'right', toggle='artCenter=tyres', showWhen='!mapUp'),
            text('t%s_tu' % cr, xr + 48, tb, 30, 'x_tunit', '{{u:temp}}', 'fg', 'left', toggle='artCenter=tyres', showWhen='!mapUp'),
        ]
    # ... or the four readouts: a label over each value with its unit
    vals = (('boost', 'BOOST', '{{boost}}', '{{u:boostLc}}', 0, 0), ('oil', 'ULEI', '{{oil}}', '{{u:temp}}', 0, 1),
            ('coolant', 'RĂCIRE', '{{coolant}}', '{{u:temp}}', 1, 0), ('fuel', 'COMBUSTIBIL', '{{fuelPct}}', '%', 1, 1))
    for id_, lab, val, unit, col, row in vals:
        base = (330, 500)[row]
        if col == 0:
            x1 = 900
            widgets += [
                text('v_%s_l' % id_, x1 - 200, base - 44, 200, 'k_label_ro', lab, 'dim', 'right', toggle='artCenter=values', showWhen='!mapUp'),
                text('v_%s' % id_, x1 - 46 - 100, base, 100, 'x_row', val, 'fg', 'right', toggle='artCenter=values', showWhen='!mapUp'),
                text('v_%s_u' % id_, x1 - 42, base, 42, 'x_rowu', unit, 'dim', 'left', toggle='artCenter=values', showWhen='!mapUp'),
            ]
        else:
            x1 = W - 900 + 160
            widgets += [
                text('v_%s_l' % id_, x1 - 200, base - 44, 200, 'k_label_ro', lab, 'dim', 'right', toggle='artCenter=values', showWhen='!mapUp'),
                text('v_%s' % id_, x1 - 46 - 100, base, 100, 'x_row', val, 'fg', 'right', toggle='artCenter=values', showWhen='!mapUp'),
                text('v_%s_u' % id_, x1 - 42, base, 42, 'x_rowu', unit, 'dim', 'left', toggle='artCenter=values', showWhen='!mapUp'),
            ]

    # the bottom row: covers BMW's own strip but its gear letter (x 1380..1460): the range with the fuel icon, the clock,
    # the drive mode before BMW's gear letter, the outside temperature, the coolant
    row = 700
    widgets += [
        {'id': 'strip_cover_l', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 0, 'y': TOP, 'w': 1380, 'h': H - TOP,
         'color': 'bg', 'stripRow': 'l'},
        {'id': 'strip_cover_r', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 1460, 'y': TOP, 'w': W - 1460,
         'h': H - TOP, 'color': 'bg', 'stripRow': 'r'},
        {'id': 'row_fuel', 'type': 'icon', 'icon': 'fuel', 'z': 3, 'x': 164, 'y': row - 26, 'w': 22, 'h': 26, 'color': 'fg', 'stripRow': 'l'},
        text('row_range', 200, row, 90, 'x_row', '{{range}}', 'fg', 'right', z=3, stripRow='l'),
        text('row_range_u', 296, row, 40, 'x_rowu', '{{u:distLc}}', 'fg', 'left', z=3, stripRow='l'),
        text('row_time', 356, row, 120, 'x_row', '{{time}}', 'fg', 'center', z=3, stripRow='l'),
        text('row_mode', 1060, row, 310, 'x_rowm', '{{mode}}', 'fg', 'right', z=3, stripRow='l'),
        text('row_out', 1478, row, 100, 'x_row', '{{ambient}}', 'fg', 'right', z=3, stripRow='r'),
        text('row_out_u', 1582, row, 36, 'x_rowu', '{{u:temp}}', 'fg', 'left', z=3, stripRow='r'),
        {'id': 'row_therm', 'type': 'icon', 'icon': 'therm', 'z': 3, 'x': 1648, 'y': row - 28, 'w': 22, 'h': 28, 'color': 'cyan', 'stripRow': 'r'},
        text('row_cool', 1674, row, 76, 'x_row', '{{coolant}}', 'cyan', 'right', z=3, stripRow='r'),
        text('row_cool_u', 1754, row, 36, 'x_rowu', '{{u:temp}}', 'cyan', 'left', z=3, stripRow='r'),
    ]

    layout = {
        'schemaVersion': 2,
        'name': 'Artifact',
        'theme': 'artifact',
        'mapLive': True,
        '_about': ("After the user's own mockup (D · Artifact), generated by tools/gen_artifact.py (edit that and "
                   "regenerate): speed on a glass chevron frame at the left (SPEED_SCALE) and revs on its mirror at the "
                   "right (0..8, red from the redline), each lit brighter from the bottom up to a white marker; the speed "
                   "and the gear in big italic figures, a slanted fuel gauge (left) and oil gauge (right) inside the "
                   "frames, and in the middle (setting artCenter) a car seen from above with each tyre's pressure and "
                   "temperature, the four readouts, or nothing. While the Waze map shows inside the theme ('mapUp') the "
                   "middle is cut see-through with its edges fading to black (mapLive: no rebuild). Everything that isn't "
                   "text is one shader (xdash). The bottom row has the range, the clock, the drive mode, the outside "
                   "and coolant temperatures, BMW's gear letter left uncovered. Widget reference: shared/hud.js header."),
        'widgets': widgets,
    }
    with open(OUT, 'w') as f:
        json.dump(layout, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print('wrote %s: %d widgets' % (os.path.relpath(OUT, ROOT), len(widgets)))


if __name__ == '__main__':
    main()
