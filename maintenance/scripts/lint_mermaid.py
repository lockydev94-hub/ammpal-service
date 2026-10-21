import re, glob

ARROWS = ['-->', '---', '-.->', '-.-', '<-->']
NL = chr(10)


def strip_quoted(line):
    out, inq = [], False
    for ch in line:
        if ch == '"':
            inq = not inq
            out.append('"')
        elif not inq:
            out.append(ch)
    return ''.join(out)


def check(line_no, body):
    errs = []
    lines = body.split(NL)
    kind = lines[0].strip().split()[0] if lines and lines[0].strip() else ''
    if kind not in ('graph', 'flowchart'):
        return errs, kind
    sg = 0
    for k, raw in enumerate(lines):
        ln = line_no + k + 1
        l = raw.strip()
        if not l or l.startswith('%%'):
            continue
        if re.match(r'^(class |classDef |style |linkStyle )', l):
            continue
        if l == 'end':
            sg -= 1
            if sg < 0:
                errs.append((ln, 'end without subgraph'))
            continue
        if re.match(r'^subgraph\b', l):
            sg += 1
            continue
        if re.match(r'^(flowchart|graph)\s+(TD|TB|LR|RL|BT)$', l):
            continue
        if raw.count('"') % 2:
            errs.append((ln, 'unbalanced double quote: ' + l[:70]))
            continue
        u = strip_quoted(l)
        for a, b in [('[', ']'), ('{', '}'), ('(', ')')]:
            if u.count(a) != u.count(b):
                errs.append((ln, 'unbalanced %s%s: %s' % (a, b, l[:70])))
        if ';' in u:
            errs.append((ln, 'stray semicolon: ' + l[:70]))
        if '`' in u:
            errs.append((ln, 'backtick in flowchart label: ' + l[:70]))
        if not any(a in u for a in ARROWS) and '[' not in u and '{' not in u:
            errs.append((ln, 'no arrow and no node definition: ' + l[:70]))
        if re.search(r'\|\s*$', u):
            errs.append((ln, 'edge label pipe left open: ' + l[:70]))
    if sg != 0:
        errs.append((line_no, 'subgraph/end imbalance (%d)' % sg))
    return errs, kind


total = bad = 0
kinds = {}
for f in sorted(glob.glob('Docs/*.md')):
    txt = open(f, encoding='utf-8').read()
    for m in re.finditer(r'```mermaid' + NL + r'(.*?)```', txt, re.S):
        total += 1
        line = txt[:m.start()].count(NL) + 2
        errs, kind = check(line, m.group(1))
        kinds[kind] = kinds.get(kind, 0) + 1
        if errs:
            bad += 1
            print('BLOCK', f, 'line', line, '(' + kind + ')')
            for e in errs:
                print('   line %d: %s' % e)
print('kinds:', kinds)
print('checked %d mermaid blocks, %d with issues' % (total, bad))
