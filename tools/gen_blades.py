#!/usr/bin/env python3
"""gen_blades.py - writes apps/aar_cluster_themes/hud/layouts/lame.json and bumerang.json, AAR's blade themes (the
mockups "B · Lame" and "C · Bumerang", Nov 2026). Edit the numbers here and run it again; don't edit the JSON.

    python3 tools/gen_blades.py

Everything that isn't text is one shader (shared/shaders.js bdash): speed on a blue blade at the left, revs on a red
one at the right, each a solid fill from the bottom up to a white marker, glowing; a see-through dark blue panel in the
middle framing the Waze map (cut see-through while it shows inside the theme, else a road runs there); four readout
bars, two-tone stripes under the speed and the gear, colour pools behind both sides and a base line. Lame's blades
lean straight in towards the top; Bumerang's have one sharp bend pointing out to the screen edge, with stronger colours
and glows and a bluer panel. The text widgets (scale numbers, speed, gear, drive mode, readouts, bottom row) and the
fuel bar under the range sit round it. Panel 1920x720; shared/visible.js has what the hood hides (top corners) and
BMW's gear letter window in the bottom row (x 1380..1460), which stays uncovered.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYOUTS = os.path.join(ROOT, 'apps', 'aar_cluster_themes', 'hud', 'layouts')
FONTS = os.path.join(ROOT, 'apps', 'aar_cluster_themes', 'hud', 'fonts')

W, H = 1920, 720
TOP = 660                      # the shader's height; the bottom row is under it
RPM_MAX = 8000
PANEL = [600, 110, 720, 500]   # the dark blue middle panel
WIN = [624, 134, 672, 452]     # the map window in it (inside BMW's map slot, 416,120 1088x480, where Waze draws)
LX, RX = 465, W - 465          # the centres of the speed and the gear
READ_X, READ_W = 336, 250      # the left readouts: x0 and bar width (the right ones mirrored)
READ_Y = (440, 530)            # their label baselines; the bar 22 px under
STRIPE = [372, 356, 150, 22]   # the left two-tone stripe: x, y, long, short
BASE = [640, 240, 1680]        # the base line: y, x0, x1
FUEL_BAR = (880, 712, 200, 4)  # the fuel bar under the range: x, y, w, h
REDLINE = 7                    # rpm labels from here on are red (the redline setting's default, 7000)

THEMES = {
    'lame': {
        'name': 'Lame',
        'shape': [108, 362, 618, 100],          # yTop, yBend, yBottom, band width (straight: the bend on the line)
        'xo': [176, 136, 96],                   # the left blade's outer edge at the top, the bend, the bottom
        'label_gap': 24,
        'left': [[10, 42, 120], [47, 123, 255], [207, 230, 255]],
        'right': [[74, 6, 12], [232, 38, 47], [255, 201, 201]],
        'look': [1.0, 0.5, 0, 0.26],            # glow, outline alpha, outline in the accent, colour pool alpha
        'panelStyle': [0.22, 0.35, 0, 6],       # fill alpha, border alpha, halo, radius
        'panelColor': [10, 42, 120],
        'zone': [420, 380, 260, 260],
    },
    'bumerang': {
        'name': 'Bumerang',
        'shape': [118, 368, 618, 96],
        'xo': [158, 72, 158],
        'label_gap': 32,
        'left': [[10, 59, 194], [30, 107, 255], [154, 210, 255]],
        'right': [[154, 10, 22], [255, 35, 51], [255, 176, 176]],
        'look': [1.5, 0.85, 1, 0.42],
        'panelStyle': [0.34, 0.75, 0.5, 6],
        'panelColor': [11, 60, 196],
        'zone': [420, 370, 320, 300],
    },
}

SPEED_I = 9                    # SPEED_SCALE's labels
_fonts = {}


def font(name):
    if name not in _fonts:
        with open(os.path.join(FONTS, name + '.json')) as f:
            _fonts[name] = json.load(f)
    return _fonts[name]


def text(id_, x, base, w, fnt, txt, color='fg', align='center', **kw):
    """A text box whose baseline is at `base` (target px)."""
    f = font(fnt)
    d = {'id': id_, 'type': 'text', 'z': 5, 'x': int(round(x)), 'y': int(round(base - f['baseline'])), 'w': int(w),
         'h': f['cellHeight'], 'text': txt, 'font': fnt, 'color': color, 'align': align}
    d.update(kw)
    return d


def xo(cfg, y):
    yT, yM, yB, _ = cfg['shape']
    xT, xM, xB = cfg['xo']
    if y >= yM:
        return xM + (xB - xM) * (y - yM) / (yB - yM)
    return xT + (xM - xT) * (y - yT) / (yM - yT)


def width(fnt, s):
    g = font(fnt)['glyphs']
    return sum(g[c]['advance'] for c in s)


def readout(id_, x0, y, label, value, unit, color, vw=70):
    """A readout: the label at the left, the value right-aligned before its unit, the bar 22 px under (in the shader).
    Text boxes in one sheet must not overlap (a redraw clears its box), so each is as wide as its text needs."""
    return [
        text(id_ + '_l', x0, y, width('k_label_ro', label) + 2, 'k_label_ro', label, 'dim', 'left'),
        text(id_, x0 + READ_W - 44 - vw, y + 2, vw, 'k_val_b', value, 'fg', 'right'),
        text(id_ + '_u', x0 + READ_W - 38, y + 2, 44, 'k_unit', unit, color, 'left'),
    ]


def layout(key):
    cfg = THEMES[key]
    yT, yM, yB, bw = cfg['shape']
    rx0 = W - READ_X - READ_W
    bars = [[READ_X, READ_Y[0] + 22, READ_W], [READ_X, READ_Y[1] + 22, READ_W],
            [rx0, READ_Y[0] + 22, READ_W], [rx0, READ_Y[1] + 22, READ_W]]
    widgets = [{
        'id': key, 'type': 'bdash', 'class': 'content', 'z': 1, 'x': 0, 'y': 0, 'w': W, 'h': TOP,
        'shape': cfg['shape'], 'xo': cfg['xo'], 'rpmMax': RPM_MAX,
        'left': cfg['left'], 'right': cfg['right'], 'look': cfg['look'],
        'panel': PANEL, 'panelStyle': cfg['panelStyle'], 'panelColor': cfg['panelColor'], 'win': WIN,
        'bars': bars, 'stripe': STRIPE, 'zone': cfg['zone'], 'base': BASE,
        'hole': WIN, 'holeWhen': 'mapUp', 'holeInset': 0, 'holeRadius': 12,
    }]

    # the scale numbers along each blade's inner side; the one nearest the value lights up white, the revs red from 7
    span = yB - yT - 8
    for i in range(SPEED_I):
        y = yB - 4 - i / 8 * span
        x = xo(cfg, y) + bw + cfg['label_gap']
        widgets.append(text('spd%d' % i, x, y + 9, 56, 'k_scale_b', '{{spd:%d}}' % i, 'kl', 'left', near=['speed', i]))
    for i in range(9):
        y = yB - 4 - i / 8 * span
        x = W - (xo(cfg, y) + bw + cfg['label_gap'])
        red = i >= REDLINE
        widgets.append(text('rpm%d' % i, x - 56, y + 9, 56, 'k_scale_b', str(i), 'hot' if red else 'kr', 'right',
                            near=['rpm', i], nearColor='hot' if red else 'fg'))

    # left: the speed; right: the gear and the drive mode; the readouts under them
    widgets += [
        text('speed_l', LX - 100, 168, 200, 'k_label_ro', 'VITEZĂ', 'kl'),
        text('speed', LX - 128, 300, 256, 'k_speed_b', '{{speed}}'),
        text('speed_unit', LX - 60, 336, 120, 'k_unit', '{{u:speedLc}}', 'kl'),
        text('gear_l', RX - 100, 168, 200, 'k_label_ro', 'TREAPTĂ', 'kr'),
        text('gear', RX - 110, 300, 220, 'k_gear_b', '{{gear}}', hotWhen='now'),
        text('mode', RX - 150, 336, 300, 'k_mode', '{{mode}}', 'kmode'),
    ]
    widgets += readout('boost', READ_X, READ_Y[0], 'BOOST', '{{boost}}', '{{u:boostLc}}', 'dim', vw=80)
    widgets += readout('oil', READ_X, READ_Y[1], 'ULEI', '{{oil}}', '{{u:temp}}', 'dim')
    widgets += readout('coolant', rx0, READ_Y[0], 'RĂCIRE', '{{coolant}}', '{{u:temp}}', 'dim')
    widgets += readout('fuel', rx0, READ_Y[1], 'COMBUSTIBIL', '{{fuelPct}}', '%', 'dim')

    # the bottom row: covers BMW's own strip but its gear letter (x 1380..1460), then the clock, the range with the
    # fuel bar under it (empty left .. full right, red in the reserve) and the outside temperature
    fx, fy, fw, fh = FUEL_BAR
    widgets += [
        {'id': 'strip_cover_l', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 0, 'y': TOP, 'w': 1380, 'h': H - TOP,
         'color': 'bg', 'stripRow': 'l'},
        {'id': 'strip_cover_r', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 1460, 'y': TOP, 'w': W - 1460,
         'h': H - TOP, 'color': 'bg', 'stripRow': 'r'},
        text('strip_time', 150, 700, 120, 'k_val', '{{time}}', 'fg', 'right', z=3, stripRow='l'),
        text('strip_ampm', 276, 700, 40, 'k_unit', '{{ampmLc}}', 'dim', 'left', z=3, stripRow='l'),
        text('strip_range', fx + 5, 694, 100, 'k_val', '{{range}}', 'fg', 'right', z=3, stripRow='l'),
        text('strip_range_u', fx + 112, 694, 44, 'k_unit', '{{u:distLc}}', 'dim', 'left', z=3, stripRow='l'),
        {'id': 'fuel_bar', 'type': 'meter', 'class': 'content', 'z': 3, 'x': fx, 'y': fy, 'w': fw, 'h': fh,
         'signal': 'fuel', 'min': 0, 'max': 1, 'segments': 100, 'gap': 0, 'colors': ['fg', 'fg', 'fg'],
         'low': [0.15, 'hot'], 'trackColor': 'track', 'stripRow': 'l'},
        text('strip_out', 1666, 700, 90, 'k_val', '{{ambient}}', 'fg', 'right', z=3, stripRow='r'),
        text('strip_out_u', 1762, 700, 36, 'k_unit', '{{u:temp}}', 'dim', 'left', z=3, stripRow='r'),
    ]

    straight = 'leaning straight in towards the top' if cfg['xo'][1] * 2 == cfg['xo'][0] + cfg['xo'][2] else \
        'boomerangs with one sharp bend pointing out to the screen edge'
    return {
        'schemaVersion': 2,
        'name': cfg['name'],
        'theme': key,
        'mapLive': True,
        '_about': ("AAR's own blade theme, generated by tools/gen_blades.py (edit that and regenerate): speed on a blue "
                   "blade at the left (SPEED_SCALE) and revs on a red one at the right (0..8, red from 7), " + straight +
                   ", each a solid fill from the bottom up to a white marker, glowing more in Sport. Speed and gear "
                   "beside them with two-tone stripes, boost / oil / coolant / fuel readouts with bars, a see-through "
                   "dark blue panel in the middle framing the Waze map (cut see-through while it shows inside the "
                   "theme, 'mapUp', mapLive: no rebuild; a road runs there otherwise). Everything that isn't text is "
                   "one shader (bdash). The bottom row has the clock, the range with a fuel bar under it (red in the "
                   "reserve) and the outside temperature, BMW's gear letter left uncovered. Widget reference: "
                   "shared/hud.js header."),
        'widgets': widgets,
    }


def main():
    for key in THEMES:
        out = os.path.join(LAYOUTS, key + '.json')
        d = layout(key)
        with open(out, 'w') as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print('wrote %s: %d widgets' % (os.path.relpath(out, ROOT), len(d['widgets'])))


if __name__ == '__main__':
    main()
