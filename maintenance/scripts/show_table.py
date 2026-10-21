import re, sys
BS = chr(92)
split_pat = re.compile('(?<!' + BS + BS + ')\\|')

def cols(line):
    s = line.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'): s = s[:-1]
    return len(split_pat.split(s))

f, ln = sys.argv[1], int(sys.argv[2])
lines = open(f, encoding='utf-8').read().split('\n')
start = ln - 1
while start > 0 and lines[start].startswith('|'):
    start -= 1
for i in range(start + 1, min(start + 12, len(lines))):
    if not lines[i].startswith('|'): break
    print('%5d w=%d  %s' % (i + 1, cols(lines[i]), lines[i][:150]))
