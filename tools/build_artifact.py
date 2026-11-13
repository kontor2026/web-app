"""Baut aus dem Projekt eine einzelne Artefakt-Seite: CSS und JS inline, anime.js per CDN, Fotos verkleinert."""
import re, sys, pathlib
from PIL import Image

src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
(out / 'assets/samples').mkdir(parents=True, exist_ok=True)

def strip(code):
    code = re.sub(r"^import .*?;\s*$", "", code, flags=re.M)
    code = re.sub(r"^export (const|function|class) ", r"\1 ", code, flags=re.M)
    return code

parts = [strip((src / 'js/data/catalog.js').read_text(encoding='utf-8')),
         strip((src / 'js/data/inventory.js').read_text(encoding='utf-8'))]
for name in ['smartphone', 'laptop', 'netzteil', 'flasche']:
    body = (src / f'js/data/objects/{name}.js').read_text(encoding='utf-8').replace('export default {', 'return {')
    parts.append(f"const {name} = (() => {{\n{body}\n}})();")
parts.append(strip((src / 'js/data/objects/index.js').read_text(encoding='utf-8')))
parts.append(strip((src / 'js/iso.js').read_text(encoding='utf-8')))
parts.append(strip((src / 'js/main.js').read_text(encoding='utf-8')))
js = "const { animate, stagger, svg } = anime;\n" + "\n\n".join(parts)

css = (src / 'css/app.css').read_text(encoding='utf-8')
html = (src / 'index.html').read_text(encoding='utf-8')
body = html[html.index('<body>') + 6: html.index('<script type="module"')]

page = f"""<title>Kreislauf-Station</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{css}
</style>
{body}
<script src="https://cdn.jsdelivr.net/npm/animejs@4.5.0/dist/bundles/anime.umd.min.js"></script>
<script>
{js}
</script>
"""
(out / 'kreislauf-station.html').write_text(page, encoding='utf-8')

for p in (src / 'assets/samples').glob('*.jpg'):
    im = Image.open(p); im.thumbnail((1100, 1100))
    im.save(out / 'assets/samples' / p.name, quality=80, optimize=True)
print('ok', len(page))
