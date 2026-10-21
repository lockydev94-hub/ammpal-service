from PIL import Image
import glob, collections, os

for p in sorted(glob.glob('visualize-image-of-project/*.png')):
    im = Image.open(p).convert('RGB')
    w, h = im.size
    small = im.resize((80, max(1, int(80 * h / w))))
    cnt = collections.Counter(small.getdata())
    total = sum(cnt.values())
    print(os.path.basename(p), '%dx%d' % (w, h), '%.2f MB' % (os.path.getsize(p) / 1048576))
    for (r, g, b), n in cnt.most_common(7):
        print('    #%02X%02X%02X  %5.1f%%' % (r, g, b, 100.0 * n / total))
