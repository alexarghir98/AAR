'use strict';
/**
 * HUD colour themes. Layouts name colour *roles* ("fg", "dim", "arc", ...) and
 * the active theme fills them in, so every layout works in every theme.
 *
 * HUD rule (Nov 7 2026, from road photos: greys were hard to see even at night): the HUD is a projector, so a dim or
 * see-through colour comes out faint on the glass. Every HUD role is opaque and no lit colour is darker than
 * about 70 % brightness; only "track" (the unlit part of a bar) stays partly see-through, at 96..110 of 255.
 *
 * Colours are [r, g, b, a] 0-255. On the HUD, black is see-through glass, so a
 * theme only ever adds light. Dark blue is the weakest colour on a HUD in sun;
 * M's mid blue is kept brighter than the paint-chip M blue for that reason.
 *
 * bar: the shift bar's three zones. lowColor up to midAt, midColor up to the
 * red zone, highColor from there. midAt: 'shift' = where the shift zone starts
 * (redline - 1500), or a fraction of the bar (M climbs light blue -> blue at 50%).
 */
const THEMES = {
    classic: {
        name: 'Classic',
        fg: [243, 246, 250, 255], dim: [200, 208, 220, 255], track: [243, 246, 250, 96], arc: [243, 246, 250, 255],
        glow: 0.35, stripe: false,
        bar: { low: [243, 246, 250], mid: [255, 154, 60], high: [255, 75, 62], midAt: 'shift' },
        rev: { from: [185, 192, 204], to: [243, 246, 250] },
    },
    m: {
        name: 'M',
        fg: [243, 246, 250, 255], dim: [170, 205, 255, 255], track: [80, 150, 255, 110], arc: [79, 180, 255, 255],
        glow: 0.4, stripe: true,
        bar: { low: [79, 180, 255], mid: [51, 102, 255], high: [232, 38, 45], midAt: 0.5 },
        rev: { from: [51, 102, 255], to: [110, 170, 255] },
    },
    night: {
        name: 'Night',
        fg: [255, 179, 71, 255], dim: [235, 165, 70, 255], track: [255, 179, 71, 96], arc: [255, 179, 71, 255],
        glow: 0.3, stripe: false,
        bar: { low: [255, 179, 71], mid: [255, 179, 71], high: [255, 75, 62], midAt: 'shift' },
        rev: { from: [205, 135, 55], to: [255, 179, 71] },
    },
    // Cluster theme (a layout's own "theme"). The cluster is an LCD, not glass: black is solid black there,
    // and it covers BMW's gauges under it. Extra roles: bg (the screen), panel (box inside), line (box
    // frame), head (box header strip), ink (text on a header), accent (a highlighted header).
    // The car brightens dark tints (Nov 5 2026: a navy backdrop came out light steel blue), so until that curve
    // is measured every large area (bg, panel, well) is pure black in all the cluster themes.
    gt3: {
        name: 'GT3',
        fg: [244, 244, 244, 255], dim: [150, 154, 160, 255], track: [255, 255, 255, 26], arc: [244, 244, 244, 255],
        glow: 0, stripe: false,
        bar: { low: [57, 222, 72], mid: [255, 196, 0], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [57, 222, 72], to: [57, 222, 72] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [205, 208, 214, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [255, 196, 0, 255], well: [0, 0, 0, 255], wellLine: [70, 74, 80, 255],
    },
    // Sport (layout sport.json): BMW's Live Cockpit Sport view, blue speed and red revs round the map.
    // Extra roles: sblue / spink (the speed and rpm scale numbers), sred (the rpm caption).
    sportdash: {
        name: 'Sport',
        fg: [244, 247, 252, 255], dim: [150, 170, 205, 255], track: [70, 80, 100, 255], arc: [60, 215, 255, 255],
        glow: 0, stripe: false,
        bar: { low: [60, 215, 255], mid: [60, 215, 255], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [224, 26, 56], to: [224, 26, 56] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [60, 215, 255, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [60, 215, 255, 255], well: [0, 0, 0, 255], faint: [96, 110, 135, 255],
        sblue: [120, 170, 245, 255], spink: [236, 140, 140, 255], sred: [235, 60, 70, 255],
    },
    // Curved (layout curved.json): after BMW's newer clusters (iDrive 8 / 8.5 Curved Display, Drive layout). White
    // figures on black, the scales' accent by drive mode ("modes", read by hud.js for the cdash shader): BMW blue in
    // Comfort, orange-red in Sport, red in Sport Plus, teal in Eco Pro. Extra roles: kscale (scale numbers), klabel.
    curved: {
        name: 'Curved',
        fg: [244, 246, 250, 255], dim: [150, 158, 172, 255], track: [70, 76, 88, 255], arc: [79, 160, 255, 255],
        glow: 0, stripe: false,
        bar: { low: [79, 160, 255], mid: [79, 160, 255], high: [255, 44, 38], midAt: 'shift' },
        rev: { from: [79, 160, 255], to: [79, 160, 255] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [200, 206, 216, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [79, 160, 255, 255], well: [0, 0, 0, 255], faint: [96, 104, 118, 255],
        kscale: [205, 210, 220, 255], klabel: [150, 158, 172, 255],
        modes: {
            comfort: { acc: [79, 160, 255], acc2: [14, 48, 140] },
            sport: { acc: [255, 92, 36], acc2: [120, 20, 10] },
            sportplus: { acc: [255, 38, 44], acc2: [110, 8, 16] },
            eco: { acc: [40, 220, 190], acc2: [6, 80, 74] },
        },
    },
    // Apex (layout apex.json): AAR's own sport dash, white figures on black, the columns, wheels and bars in the drive
    // mode's accent ("modes", read by hud.js for the adash shader). Extra roles: kscale (scale numbers), klabel.
    apex: {
        name: 'Apex',
        fg: [244, 246, 250, 255], dim: [150, 158, 172, 255], track: [70, 76, 88, 255], arc: [79, 160, 255, 255],
        glow: 0, stripe: false,
        bar: { low: [79, 160, 255], mid: [79, 160, 255], high: [255, 44, 38], midAt: 'shift' },
        rev: { from: [79, 160, 255], to: [79, 160, 255] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [200, 206, 216, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [79, 160, 255, 255], well: [0, 0, 0, 255], faint: [96, 104, 118, 255],
        kscale: [205, 210, 220, 255], klabel: [150, 158, 172, 255],
        modes: {
            comfort: { acc: [64, 150, 255], acc2: [10, 40, 130] },
            sport: { acc: [255, 70, 40], acc2: [110, 14, 8] },
            sportplus: { acc: [255, 30, 60], acc2: [100, 6, 20] },
            eco: { acc: [40, 220, 190], acc2: [6, 80, 74] },
        },
    },
    // Artifact (layout artifact.json, after the user's own mockup): white figures on black, blue glass; the frames,
    // panels and car take their colours from the layout (shaders.js xdash). Extra roles: kl (the speed numbers),
    // kr (the rev numbers from 6 up), kmode (the drive mode).
    artifact: {
        name: 'Artifact',
        fg: [242, 245, 250, 255], dim: [154, 166, 184, 255], track: [58, 65, 76, 255], arc: [46, 139, 255, 255],
        glow: 0, stripe: false,
        bar: { low: [46, 139, 255], mid: [46, 139, 255], high: [255, 42, 58], midAt: 'shift' },
        rev: { from: [255, 42, 58], to: [255, 42, 58] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [200, 206, 216, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [63, 180, 255, 255], well: [0, 0, 0, 255], faint: [96, 104, 118, 255],
        hot: [255, 42, 58, 255],
        kl: [242, 245, 250, 255], kr: [243, 214, 220, 255], kmode: [242, 245, 250, 255], cyan: [63, 180, 255, 255],
    },
    // Lame and Bumerang (layouts lame.json, bumerang.json): AAR's blue and red blade dashes. White figures on black;
    // the blades, panel, bars and stripes take their colours from the layout (shaders.js bdash). Extra roles: kl / kr
    // (the left and right scale numbers and captions), kmode (the drive mode under the gear).
    lame: {
        name: 'Lame',
        fg: [244, 246, 250, 255], dim: [138, 147, 166, 255], track: [70, 76, 88, 255], arc: [47, 123, 255, 255],
        glow: 0, stripe: false,
        bar: { low: [47, 123, 255], mid: [47, 123, 255], high: [232, 38, 47], midAt: 'shift' },
        rev: { from: [232, 38, 47], to: [232, 38, 47] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [200, 206, 216, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [47, 123, 255, 255], well: [0, 0, 0, 255], faint: [96, 104, 118, 255],
        hot: [255, 42, 42, 255],
        kl: [143, 194, 255, 255], kr: [255, 140, 140, 255], kmode: [255, 90, 90, 255],
    },
    bumerang: {
        name: 'Bumerang',
        fg: [244, 246, 250, 255], dim: [138, 147, 166, 255], track: [70, 76, 88, 255], arc: [30, 107, 255, 255],
        glow: 0, stripe: false,
        bar: { low: [30, 107, 255], mid: [30, 107, 255], high: [255, 35, 51], midAt: 'shift' },
        rev: { from: [255, 35, 51], to: [255, 35, 51] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [200, 206, 216, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [30, 107, 255, 255], well: [0, 0, 0, 255], faint: [96, 104, 118, 255],
        hot: [255, 42, 42, 255],
        kl: [154, 210, 255, 255], kr: [255, 176, 176, 255], kmode: [255, 35, 51, 255],
    },
    // M cluster look (layout m.json, after design/photos/ref-m8-cluster.png): black, white numbers with a chrome
    // fade, M red needles and setup bars. Extra roles: redTrack, chrome (bottom of a chrome fade), grey / grey2
    // (the dim gear number's fade), faint.
    mdash: {
        name: 'M',
        fg: [238, 241, 246, 255], dim: [132, 140, 152, 255], track: [104, 110, 120, 255], arc: [226, 36, 44, 255],
        glow: 0, stripe: false,
        bar: { low: [226, 36, 44], mid: [226, 36, 44], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [226, 36, 44], to: [226, 36, 44] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [196, 202, 212, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [226, 36, 44, 255], well: [0, 0, 0, 255], redTrack: [90, 16, 20, 255],
        chrome: [182, 188, 198, 255], grey: [160, 166, 176, 255], grey2: [104, 110, 122, 255], faint: [96, 104, 118, 255],
    },
    // Vector (layout vector.json, design/gen_vector.py): black with grey bracket lines, white numbers, coloured rings.
    vector: {
        name: 'Vector',
        fg: [238, 241, 246, 255], dim: [140, 148, 160, 255], track: [40, 43, 50, 255], arc: [238, 241, 246, 255],
        glow: 0, stripe: false,
        bar: { low: [238, 241, 246], mid: [238, 241, 246], high: [242, 31, 36], midAt: 'shift' },
        rev: { from: [242, 31, 36], to: [242, 31, 36] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [128, 135, 148, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [242, 31, 36, 255], well: [0, 0, 0, 255], faint: [96, 104, 118, 255],
    },
    // Minimal (layout minimal.json): white on black, nothing but the speed, the gear and a fuel line.
    minimal: {
        name: 'Minimal',
        fg: [240, 243, 248, 255], dim: [128, 134, 146, 255], track: [44, 48, 56, 255], arc: [240, 243, 248, 255],
        glow: 0, stripe: false,
        bar: { low: [240, 243, 248], mid: [240, 243, 248], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [240, 243, 248], to: [240, 243, 248] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [70, 74, 82, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [240, 243, 248, 255], well: [0, 0, 0, 255],
    },
    // Track (layout track.json): the race-dash frame of GT3 with amber headers, tyres and temps round a big gear.
    track: {
        name: 'Track',
        fg: [244, 244, 244, 255], dim: [150, 154, 160, 255], track: [255, 255, 255, 30], arc: [244, 244, 244, 255],
        glow: 0, stripe: false,
        bar: { low: [57, 222, 72], mid: [255, 196, 0], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [57, 222, 72], to: [57, 222, 72] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [205, 208, 214, 255], head: [255, 176, 0, 255],
        ink: [12, 12, 14, 255], accent: [226, 228, 232, 255], well: [0, 0, 0, 255],
    },
    // Drag (layout drag.json): a full-width shift bar, the 0-60 timer, green for go.
    drag: {
        name: 'Drag',
        fg: [244, 246, 250, 255], dim: [140, 148, 160, 255], track: [255, 255, 255, 30], arc: [80, 230, 110, 255],
        glow: 0, stripe: false,
        bar: { low: [80, 230, 110], mid: [255, 205, 0], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [80, 230, 110], to: [80, 230, 110] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [190, 196, 206, 255], head: [226, 228, 232, 255],
        ink: [12, 12, 14, 255], accent: [80, 230, 110, 255], well: [0, 0, 0, 255], go: [80, 230, 110, 255],
    },
    // Rally (layout rally.json): a sweeping rev arc over a huge gear, a G-meter, rally yellow.
    rally: {
        name: 'Rally',
        fg: [246, 246, 246, 255], dim: [160, 164, 170, 255], track: [255, 255, 255, 34], arc: [255, 210, 0, 255],
        glow: 0, stripe: false,
        bar: { low: [246, 246, 246], mid: [255, 210, 0], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [246, 246, 246], to: [255, 210, 0] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [205, 208, 214, 255], head: [255, 210, 0, 255],
        ink: [12, 12, 14, 255], accent: [255, 210, 0, 255], well: [0, 0, 0, 255],
    },
    // Retro (layouts retro80s.json, HUD retro.json): an 80s digital dash, amber seven-segment digits over their
    // unlit 8s, green-amber-red bar graphs. Kept bright enough for the HUD rule above.
    retro: {
        name: 'Retro',
        fg: [255, 178, 36, 255], dim: [226, 156, 40, 255], track: [255, 170, 40, 100], arc: [80, 255, 120, 255],
        glow: 0, stripe: false,
        bar: { low: [80, 255, 120], mid: [255, 178, 36], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [80, 255, 120], to: [255, 178, 36] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [255, 178, 36, 255], head: [80, 255, 120, 255],
        ink: [12, 12, 14, 255], accent: [80, 255, 120, 255], well: [0, 0, 0, 255],
        green: [80, 255, 120, 255], ghost: [255, 170, 40, 40],
    },
    // Cruise (layouts cruise.json): calm and quiet for the highway, soft white and a cool teal, no reds until needed.
    cruise: {
        name: 'Cruise',
        fg: [228, 234, 242, 255], dim: [176, 188, 204, 255], track: [255, 255, 255, 100], arc: [120, 212, 222, 255],
        glow: 0, stripe: false,
        bar: { low: [120, 212, 222], mid: [228, 234, 242], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [120, 212, 222], to: [120, 212, 222] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [96, 110, 126, 255], head: [120, 212, 222, 255],
        ink: [12, 12, 14, 255], accent: [120, 212, 222, 255], well: [0, 0, 0, 255],
    },
    // Dyno (layout dyno.json, Nov 8 2026): readout tiles in BMW M's colours: near-black tiles with an M light-blue
    // strip, bars light blue -> dark blue -> red (bar1, bar2, hot), a tile goes M red (warn) over its warning limit
    dyno: {
        name: 'Dyno',
        fg: [242, 245, 250, 255], dim: [150, 164, 184, 255], track: [255, 255, 255, 28], arc: [0, 150, 224, 255],
        glow: 0, stripe: false,
        bar: { low: [0, 150, 224], mid: [40, 92, 200], high: [226, 39, 46], midAt: 'shift' },
        rev: { from: [0, 150, 224], to: [0, 150, 224] },
        bg: [0, 0, 0, 255], panel: [14, 17, 23, 255], line: [46, 56, 72, 255], head: [0, 150, 224, 255],
        ink: [12, 12, 14, 255], accent: [0, 150, 224, 255], well: [0, 0, 0, 255],
        bar1: [0, 150, 224, 255], bar2: [40, 92, 200, 255], warn: [226, 39, 46, 255],
    },
    // Ribbon (layout ribbon.json, Nov 13 2026): calm and premium. One ribbon of light under the hood line fills with the
    // revs (cool white, warming to amber, red at the top), a huge thin speed, thin side columns. Extra roles: gear (the
    // gear number), ribbon (the line's gradient), greeting (the {{holiday}} text). holidays: true = the holiday
    // editions below (ribbon_<key>, shared/holidays.js) replace it while the "holiday" setting picks one.
    ribbon: {
        name: 'Ribbon',
        fg: [244, 241, 234, 255], dim: [107, 122, 140, 255], track: [29, 39, 51, 255], arc: [201, 180, 138, 255],
        glow: 0, stripe: false,
        bar: { low: [159, 211, 255], mid: [255, 196, 107], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [159, 211, 255], to: [255, 196, 107] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [107, 122, 140, 255], head: [201, 180, 138, 255],
        ink: [12, 12, 14, 255], accent: [201, 180, 138, 255], well: [0, 0, 0, 255], gear: [233, 215, 173, 255],
        ribbon: { stops: [[159, 211, 255], [255, 255, 255], [255, 196, 107], [255, 90, 60], [255, 42, 42]], at: [0.55, 0.8, 0.93, 1] },
        holidays: true,
        deco: 0,
        greeting: '',
    },
    ribbon_xmas: {
        name: 'Ribbon · Christmas',
        fg: [246, 241, 230, 255], dim: [127, 154, 136, 255], track: [29, 39, 51, 255], arc: [232, 194, 90, 255],
        glow: 0, stripe: false,
        bar: { low: [255, 58, 58], mid: [255, 211, 107], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [255, 58, 58], to: [255, 211, 107] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [127, 154, 136, 255], head: [232, 194, 90, 255],
        ink: [12, 12, 14, 255], accent: [232, 194, 90, 255], well: [0, 0, 0, 255], gear: [232, 194, 90, 255],
        ribbon: { stops: [[255, 58, 58], [47, 220, 106], [255, 211, 107], [79, 163, 255], [255, 26, 26]], at: [0.5, 0.8, 0.86, 1] },
        bulbs: true,
        wire: [31, 58, 42],
        deco: 1,
        decoColors: [[255, 255, 255], [255, 255, 255], [255, 255, 255]],
        greeting: 'MERRY CHRISTMAS',
    },
    ribbon_thanks: {
        name: 'Ribbon · Thanksgiving',
        fg: [251, 238, 221, 255], dim: [160, 138, 112, 255], track: [29, 39, 51, 255], arc: [224, 135, 58, 255],
        glow: 0, stripe: false,
        bar: { low: [201, 162, 74], mid: [255, 154, 60], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [201, 162, 74], to: [255, 154, 60] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [160, 138, 112, 255], head: [224, 135, 58, 255],
        ink: [12, 12, 14, 255], accent: [224, 135, 58, 255], well: [0, 0, 0, 255], gear: [224, 135, 58, 255],
        ribbon: { stops: [[201, 162, 74], [255, 217, 160], [255, 154, 60], [224, 69, 31], [255, 42, 26]], at: [0.5, 0.8, 0.93, 1] },
        deco: 5,
        decoColors: [[224, 135, 58], [201, 80, 42], [217, 164, 65]],
        greeting: 'HAPPY THANKSGIVING',
    },
    ribbon_newyear: {
        name: 'Ribbon · New Year',
        fg: [255, 248, 232, 255], dim: [154, 146, 126, 255], track: [29, 39, 51, 255], arc: [242, 207, 114, 255],
        glow: 0, stripe: false,
        bar: { low: [185, 162, 106], mid: [255, 210, 74], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [185, 162, 106], to: [255, 210, 74] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [154, 146, 126, 255], head: [242, 207, 114, 255],
        ink: [12, 12, 14, 255], accent: [242, 207, 114, 255], well: [0, 0, 0, 255], gear: [242, 207, 114, 255],
        ribbon: { stops: [[185, 162, 106], [255, 244, 214], [255, 210, 74], [255, 106, 58], [255, 42, 42]], at: [0.5, 0.8, 0.93, 1] },
        deco: 4,
        decoColors: [[242, 207, 114], [255, 255, 255], [217, 176, 74]],
        greeting: 'HAPPY NEW YEAR',
    },
    ribbon_july4: {
        name: 'Ribbon · Fourth of July',
        fg: [244, 246, 255, 255], dim: [125, 140, 171, 255], track: [29, 39, 51, 255], arc: [255, 75, 75, 255],
        glow: 0, stripe: false,
        bar: { low: [58, 107, 255], mid: [255, 128, 128], high: [255, 42, 42], midAt: 'shift' },
        rev: { from: [58, 107, 255], to: [255, 128, 128] },
        bg: [0, 0, 0, 255], panel: [0, 0, 0, 255], line: [125, 140, 171, 255], head: [255, 75, 75, 255],
        ink: [12, 12, 14, 255], accent: [255, 75, 75, 255], well: [0, 0, 0, 255], gear: [255, 75, 75, 255],
        ribbon: { stops: [[58, 107, 255], [255, 255, 255], [255, 128, 128], [255, 51, 51], [255, 26, 26]], at: [0.5, 0.8, 0.93, 1] },
        deco: 3,
        decoColors: [[255, 75, 75], [111, 149, 255], [255, 255, 255]],
        greeting: 'FOURTH OF JULY',
    },
};
// every theme: the shift-point red, used by "hot" (the gear and SHIFT at the shift point, the rev bar past it)
Object.keys(THEMES).forEach((k) => { THEMES[k].hot = [255, 42, 42, 255]; });

// Redline layout (after cauliflowermossgrape's Redline app): rev bar segments ramp rev.from -> rev.to up to
// the shift point; the shift lights run green -> yellow -> red in every theme; grade badges by verdict.
const LIGHTS = { green: [47, 210, 122], yellow: [255, 194, 26], red: [255, 42, 42], blue: [40, 110, 255] };
const VERDICT = {
    'SPOT ON': [47, 210, 122, 255], EARLY: [255, 194, 26, 255], LATE: [255, 138, 26, 255],
    LIMITER: [255, 42, 42, 255], 'COLD REV': [61, 139, 255, 255], COLD: [61, 139, 255, 255],
};

// The M tricolour stripe: light blue, dark blue, red (brightened for the HUD).
const M_STRIPE = [[79, 180, 255, 255], [47, 91, 216, 255], [232, 38, 45, 255]];

/** A colour from a role name ("fg") or a literal [r,g,b,a]. */
function color(theme, c) {
    if (Array.isArray(c)) return c;
    return theme[c] || theme.fg;
}

module.exports = { THEMES, M_STRIPE, LIGHTS, VERDICT, color };
