"""Bildvorverarbeitung: Dekodieren, Verkleinern, Qualitätsprüfung, Foto-Hash."""
import base64
import io
from collections import deque

import numpy as np
from PIL import Image, ImageFilter, ImageOps

from . import config


def decode(data_url: str) -> Image.Image:
    raw = data_url.split(',', 1)[1] if data_url.startswith('data:') else data_url
    img = Image.open(io.BytesIO(base64.b64decode(raw)))
    return ImageOps.exif_transpose(img).convert('RGB')


def to_data_url(img: Image.Image, max_px=None) -> str:
    img = img.copy()
    img.thumbnail((max_px or config.IMAGE_MAX_PX,) * 2)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=85)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def quality(img: Image.Image):
    """Schnelle Prüfung vor der KI: zu dunkel, zu hell oder unscharf?"""
    g = np.asarray(img.convert('L').resize((320, 320)), dtype=np.float32)
    hell = float(g.mean())
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    schaerfe = float(lap.var())
    hinweis = None
    if hell < 45:
        hinweis = 'Das Bild ist sehr dunkel. Bitte Licht einschalten.'
    elif hell > 235:
        hinweis = 'Das Bild ist überbelichtet.'
    elif schaerfe < 25:
        hinweis = 'Das Bild ist unscharf. Gegenstand ruhig hinlegen und neu scannen.'
    return {'ok': hinweis is None, 'helligkeit': round(hell), 'schaerfe': round(schaerfe), 'hinweis': hinweis}


def _otsu(v):
    hist, edges = np.histogram(v, bins=64)
    w, m = np.cumsum(hist), np.cumsum(hist * edges[:-1])
    wb, mb = w[:-1], m[:-1]
    wf, mf = w[-1] - wb, m[-1] - mb
    between = wb * wf * (mb / np.maximum(wb, 1) - mf / np.maximum(wf, 1)) ** 2
    return float(edges[1:][np.argmax(between)])


def _largest_component(mask):
    """Größte zusammenhängende Fläche (4er-Nachbarschaft) auf dem kleinen Raster."""
    H, W = mask.shape
    seen = np.zeros_like(mask)
    best = []
    for sy, sx in zip(*np.nonzero(mask)):
        if seen[sy, sx]:
            continue
        comp, q = [], deque([(sy, sx)])
        seen[sy, sx] = True
        while q:
            y, x = q.popleft()
            comp.append((y, x))
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    q.append((ny, nx))
        if len(comp) > len(best):
            best = comp
    return best


def find_object(img: Image.Image, size=160):
    """Gegenstand freistellen, ohne KI: Ein stark weichgezeichnetes Bild schätzt den Untergrund.
    Kompakte Gegenstände weichen davon ab, Holzmaserung und großflächige Reflexe kaum.
    Rückgabe (x, y, w, h) als Anteile oder None, wenn nichts Eindeutiges gefunden wurde."""
    small = img.copy()
    small.thumbnail((size, size))
    a = np.asarray(small, np.float32) / 255
    bg = np.asarray(small.filter(ImageFilter.GaussianBlur(max(small.size) / 5)), np.float32) / 255
    diff = np.sqrt(((a - bg) ** 2).sum(2))
    diff = np.asarray(Image.fromarray((diff * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)), np.float32) / 255
    comp = _largest_component(diff > max(_otsu(diff), 0.10))
    H, W = diff.shape
    area = len(comp) / (H * W)
    if not comp or area < 0.004 or area > 0.6:
        return None
    ys, xs = zip(*comp)
    x0, y0 = min(xs) / W, min(ys) / H
    return (x0, y0, (max(xs) + 1) / W - x0, (max(ys) + 1) / H - y0)


def crop(img: Image.Image, box, pad=0.25) -> Image.Image:
    """Quadratischer Ausschnitt um den Gegenstand mit etwas Rand."""
    x, y, w, h = box
    side = max(w * img.width, h * img.height) * (1 + 2 * pad)
    cx, cy = (x + w / 2) * img.width, (y + h / 2) * img.height
    left, top = max(0, cx - side / 2), max(0, cy - side / 2)
    return img.crop((int(left), int(top), int(min(img.width, left + side)), int(min(img.height, top + side))))


def dhash(img: Image.Image, size=8) -> str:
    """Differenz-Hash (64 Bit). Findet dasselbe oder ein sehr ähnliches Foto wieder.
    Ausbaustufe: SigLIP-Bildvektoren, die auch neue Fotos desselben Gegenstands erkennen."""
    g = np.asarray(img.convert('L').resize((size + 1, size)), dtype=np.int16)
    bits = (g[:, 1:] > g[:, :-1]).flatten()
    return ''.join('1' if b else '0' for b in bits)


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))
