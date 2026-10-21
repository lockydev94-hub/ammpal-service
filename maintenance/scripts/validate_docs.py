import re, glob, os, sys, collections

files = sorted(glob.glob('Docs/*.md'))

BS = chr(92)
split_pat = re.compile('(?<!' + BS + BS + ')\\|')
sep_row = re.compile(r'^\|[\s:\-|]+\|$')
code_re = re.compile(r'(`+)(?:(?!\1).)*\1')

def cols(line):
    s = line.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'): s = s[:-1]
    return len(split_pat.split(s))

def strip_code(line):
    return code_re.sub(lambda m: 'X' * len(m.group(0)), line)

problems = []
for f in files:
    lines = open(f, encoding='utf-8').read().split('\n')
    i = 0
    while i < len(lines):
        if lines[i].startswith('|'):
            start = i
            tbl = []
            while i < len(lines) and lines[i].startswith('|'):
                tbl.append((i + 1, lines[i]))
                i += 1
            widths = [cols(l) for _, l in tbl]
            if len(set(widths)) > 1:
                seps = [n for n, (_, l) in enumerate(tbl) if sep_row.match(l.strip())]
                ref = widths[seps[0]] if seps else collections.Counter(widths).most_common(1)[0][0]
                for (ln, l), w in zip(tbl, widths):
                    if w != ref:
                        problems.append((f, ln, w, ref, l[:80]))
        else:
            i += 1

print('TABLE COLUMN MISMATCHES:', len(problems))
for p in problems:
    print('  %s:%d cols=%d expected=%d | %s' % p)

bad_fences = [(f, open(f, encoding='utf-8').read().count('```') % 2) for f in files
              if open(f, encoding='utf-8').read().count('```') % 2]
print('UNBALANCED CODE FENCES:', bad_fences or 'none')

link = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
missing = []
anchors = []
for f in files:
    d = os.path.dirname(f)
    txt = open(f, encoding='utf-8').read()
    heads = set(re.findall(r'^#{1,6}\s+(.*)$', txt, re.M))
    for m in link.finditer(txt):
        t = m.group(2).strip()
        if t.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        path, _, frag = t.partition('#')
        if not path:
            continue
        tgt = os.path.normpath(os.path.join(d, path))
        if not os.path.exists(tgt):
            missing.append((f, t))
print('BROKEN LOCAL LINKS:', len(missing))
for x in sorted(set(missing)):
    print('  ', x)

# fence-language check
unknown = collections.Counter()
for f in files:
    for m in re.finditer(r'```(\w*)', open(f, encoding='utf-8').read()):
        unknown[m.group(1)] += 1
print('FENCE LANGUAGES:', dict(unknown))

mermaid = 0
for f in files:
    txt = open(f, encoding='utf-8').read()
    for m in re.finditer(r'```mermaid\n(.*?)```', txt, re.S):
        mermaid += 1
        body = m.group(1)
        first = body.strip().split('\n')[0].strip()
        if not re.match(r'^(graph|flowchart|sequenceDiagram|stateDiagram|classDiagram|erDiagram|gantt|timeline|journey|mindmap|pie|quadrantChart)\b', first):
            print('  MERMAID BAD HEADER', f, repr(first))
        for tok in ['subgraph']:
            pass
        sg = len(re.findall(r'^\s*subgraph\b', body, re.M))
        en = len(re.findall(r'^\s*end\s*$', body, re.M))
        if sg and sg != en:
            print('  MERMAID subgraph/end mismatch', f, sg, en)
print('MERMAID BLOCKS:', mermaid)

sec = re.compile(r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*[\'"]?([A-Za-z0-9_-]{20,})')
hits = []
for f in files:
    for n, l in enumerate(open(f, encoding='utf-8'), 1):
        for m in sec.finditer(l):
            if any(k in l.lower() for k in ['<', 'example', 'placeholder', 'xxx']):
                continue
            hits.append((f, n, m.group(0)[:70]))
print('POSSIBLE SECRETS:', len(hits))
for h in hits[:20]:
    print('  ', h)
