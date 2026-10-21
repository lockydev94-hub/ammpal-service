import sys

def lum(hexc):
    h = hexc.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def aa(r):
    return 'AAA' if r >= 7 else ('AA' if r >= 4.5 else ('AA-large' if r >= 3 else 'FAIL'))

BG_PAGE = '#F5F8FA'
BG_CARD = '#FFFFFF'

pairs = [
    ('ink on page', '#102A43', BG_PAGE),
    ('ink on card', '#102A43', BG_CARD),
    ('body on card', '#334155', BG_CARD),
    ('body on page', '#334155', BG_PAGE),
    ('muted on card', '#64748B', BG_CARD),
    ('muted on page', '#64748B', BG_PAGE),
    ('border on card (non-text)', '#D7E0E8', BG_CARD),
    ('action as text on card', '#087F8C', BG_CARD),
    ('white on action', '#FFFFFF', '#087F8C'),
    ('success on card', '#15803D', BG_CARD),
    ('white on success', '#FFFFFF', '#15803D'),
    ('warning on card', '#B45309', BG_CARD),
    ('white on warning', '#FFFFFF', '#B45309'),
    ('error on card', '#B91C1C', BG_CARD),
    ('white on error', '#FFFFFF', '#B91C1C'),
    ('info on card', '#1D4ED8', BG_CARD),
    ('white on info', '#FFFFFF', '#1D4ED8'),
    ('positive accent on card', '#20A675', BG_CARD),
    ('white on positive accent', '#FFFFFF', '#20A675'),
    ('ink on action', '#102A43', '#087F8C'),
]

for name, fg, bg in pairs:
    r = ratio(fg, bg)
    print('%-32s %-8s on %-8s %5.2f:1  %s' % (name, fg, bg, r, aa(r)))

print()
print('# non-preferred (AA-small needs >=4.5):')
for name, fg, bg in pairs:
    r = ratio(fg, bg)
    if r < 4.5:
        print('  %-32s %5.2f' % (name, r))
