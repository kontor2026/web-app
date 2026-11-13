"""Claude über die Anthropic-API (offizielles Python-SDK) als Alternative zum lokalen Modell.

Braucht einen API-Schlüssel aus der Claude Console (ANTHROPIC_API_KEY). Ein claude.ai-Abo
(Pro/Max) darf laut Anthropic nicht als Zugang für eigene Produkte verwendet werden."""
import json
import time

import anthropic

from . import config


class ClaudeError(Exception):
    pass


_client = None


def client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(timeout=config.LLM_TIMEOUT, max_retries=2)
    return _client


# Strukturierte Ausgaben bei Claude kennen keine Zahlen-, Längen- und Anzahlgrenzen.
# Diese wandern in die Beschreibung; geprüft wird danach ohnehin in pipeline.py.
_UNSUPPORTED = {'minimum', 'maximum', 'minLength', 'maxLength', 'maxItems', 'multipleOf'}


def claude_schema(s):
    if isinstance(s, list):
        return [claude_schema(x) for x in s]
    if not isinstance(s, dict):
        return s
    out, notes = {}, []
    for k, v in s.items():
        if k in _UNSUPPORTED or (k == 'minItems' and v > 1):
            notes.append(f'{k} {v}')
        else:
            out[k] = claude_schema(v)
    if notes:
        out['description'] = (out.get('description', '') + ' (' + ', '.join(notes) + ')').strip()
    return out


def _image(data_url):
    head, data = data_url.split(',', 1)
    return {'type': 'image', 'source': {'type': 'base64', 'media_type': head[5:].split(';')[0], 'data': data}}


# Erkennung braucht wenig Nachdenken, Steckbrief etwas mehr. Niedrige Stufe = schneller.
EFFORT = {'scan': 'low', 'steckbrief': 'medium', 'projekte': 'low'}


def chat_json(*, model, system, user, schema, name, images=(), max_tokens=2500, temperature=None):
    content = [_image(i) for i in images] + [{'type': 'text', 'text': user}]
    t0 = time.perf_counter()
    try:
        # Streaming verhindert HTTP-Timeouts bei langen Antworten. Bei einer Ablehnung durch die
        # Sicherheitsfilter übernimmt serverseitig ein Ersatzmodell ("fallbacks").
        with client().beta.messages.stream(
            model=config.CLAUDE_MODEL,
            max_tokens=16000,
            system=system,
            messages=[{'role': 'user', 'content': content}],
            output_config={'effort': EFFORT.get(name, 'medium'),
                           'format': {'type': 'json_schema', 'schema': claude_schema(schema)}},
            betas=['server-side-fallback-2026-07-01'],
            fallbacks='default',
        ) as stream:
            msg = stream.get_final_message()
    except anthropic.AuthenticationError as e:
        raise ClaudeError('API-Schlüssel ungültig oder fehlt (ANTHROPIC_API_KEY)') from e
    except anthropic.RateLimitError as e:
        raise ClaudeError('Ratenlimit der Claude-API erreicht, bitte kurz warten') from e
    except anthropic.APIStatusError as e:
        raise ClaudeError(f'Claude-API antwortet {e.status_code}: {e.message}') from e
    except anthropic.APIConnectionError as e:
        raise ClaudeError('Claude-API nicht erreichbar (Internetverbindung?)') from e

    if msg.stop_reason == 'refusal':
        raise ClaudeError('Die Anfrage wurde von Claude abgelehnt')
    if msg.stop_reason == 'max_tokens':
        raise ClaudeError('Antwort abgeschnitten (max_tokens erreicht)')
    text = next((b.text for b in msg.content if b.type == 'text'), '')
    info = {'ms': round((time.perf_counter() - t0) * 1000), 'modell': msg.model,
            'tokens': {'input': msg.usage.input_tokens, 'output': msg.usage.output_tokens}}
    try:
        return json.loads(text), info
    except json.JSONDecodeError as e:
        raise ClaudeError(f'Antwort ist kein gültiges JSON: {e}') from e


def health():
    base = {'modus': 'claude', 'anbieter': 'claude', 'modell': config.CLAUDE_MODEL}
    if not config.ANTHROPIC_API_KEY:
        return {**base, 'ok': False, 'hinweis': 'ANTHROPIC_API_KEY fehlt'}
    try:
        client().with_options(timeout=5.0, max_retries=0).models.retrieve(config.CLAUDE_MODEL)
    except anthropic.AuthenticationError:
        return {**base, 'ok': False, 'hinweis': 'API-Schlüssel ungültig'}
    except anthropic.APIError as e:
        return {**base, 'ok': False, 'hinweis': f'Claude-API nicht erreichbar: {e}'}
    return {**base, 'ok': True, 'hinweis': None}
