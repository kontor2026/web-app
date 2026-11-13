"""Einstellungen über Umgebungsvariablen. Standard: Ollama lokal mit Qwen3-VL."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # Projektordner (liefert auch das Frontend aus)
SEED = ROOT / 'backend' / 'seed'
DATA = Path(os.getenv('STATION_DATA', ROOT / 'backend' / 'data'))

# Jeder OpenAI-kompatible Server funktioniert: Ollama, llama.cpp-Server, vLLM, LM Studio, Cloud-API.
LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'http://localhost:11434/v1').rstrip('/')
LLM_API_KEY = os.getenv('LLM_API_KEY', 'lokal')
VISION_MODEL = os.getenv('VISION_MODEL', 'station-vl')  # siehe backend/Modelfile
TEXT_MODEL = os.getenv('TEXT_MODEL', VISION_MODEL)
LLM_MODE = os.getenv('LLM_MODE', 'openai')         # 'openai' oder 'mock' (ohne Modell, nur Foto-Abgleich)

# Anbieter: 'lokal' = OpenAI-kompatibler Server (Ollama im Inferenz-Container), 'claude' = Anthropic-API
# mit API-Schlüssel, 'claude-abo' = Claude Agent SDK mit Abo-Zugang (CLAUDE_CODE_OAUTH_TOKEN).
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'lokal')


def secret(name):
    """Geheimnis aus NAME_FILE (Docker-Secret, Datei mit Rechten 600) oder aus NAME (Umgebung). Nie im Code oder Image."""
    pfad = os.getenv(f'{name}_FILE')
    if pfad and Path(pfad).exists():
        return Path(pfad).read_text(encoding='utf-8').strip()
    return os.getenv(name, '').strip()


ANTHROPIC_API_KEY = secret('ANTHROPIC_API_KEY')
CLAUDE_CODE_OAUTH_TOKEN = secret('CLAUDE_CODE_OAUTH_TOKEN')
CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-opus-5-5')

# Steckbrief und Bauideen schon beim Upload im Hintergrund starten ('auto': nur bei Claude, weil ein
# lokales Modell auf CPU Anfragen ohnehin nacheinander abarbeitet). Werte: auto | an | aus
VORAUSRECHNEN = os.getenv('VORAUSRECHNEN', 'auto')
LLM_TIMEOUT = float(os.getenv('LLM_TIMEOUT', '600'))
LLM_REASONING = os.getenv('LLM_REASONING', 'none')  # 'none' schaltet das Denken ab; leer = Feld weglassen

IMAGE_MAX_PX = int(os.getenv('IMAGE_MAX_PX', '896'))  # kleinere Bilder = weniger Bild-Tokens = schneller
HASH_THRESHOLD = int(os.getenv('HASH_THRESHOLD', '10'))  # Hamming-Abstand für den Foto-Abgleich (0–64)
