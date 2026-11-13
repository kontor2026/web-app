"""Claude über das Claude Agent SDK mit dem Zugang eines Claude-Abos (privater Test).

Anmeldung: lokal die Claude-Code-Anmeldung des Rechners (~/.claude/.credentials.json),
im Container das Token aus `claude setup-token` in CLAUDE_CODE_OAUTH_TOKEN.
Ein gesetzter ANTHROPIC_API_KEY hätte Vorrang und wird in diesem Modus ignoriert."""
import asyncio
import json
import os
import tempfile
import time
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from . import config
from .llm_claude import EFFORT, claude_schema


class ClaudeAboError(Exception):
    pass


# Die Station braucht keine Werkzeuge: alle eingebauten Claude-Code-Werkzeuge abschalten.
# (allowed_tools=[] würde nur die automatische Freigabe leeren, nicht die Werkzeuge entfernen.)
_BUILTIN = ['Bash', 'BashOutput', 'KillShell', 'Read', 'Write', 'Edit', 'MultiEdit', 'NotebookEdit', 'Glob', 'Grep',
            'WebSearch', 'WebFetch', 'Task', 'TodoWrite', 'ExitPlanMode', 'Skill', 'SlashCommand', 'ListMcpResources',
            'ReadMcpResource', 'Monitor', 'AskUserQuestion']
_WORKDIR = Path(tempfile.gettempdir()) / 'station-claude'


def _image(data_url):
    head, data = data_url.split(',', 1)
    return {'type': 'image', 'source': {'type': 'base64', 'media_type': head[5:].split(';')[0], 'data': data}}


async def _run(system, user, schema, name, images):
    content = [{'type': 'text', 'text': user}] + [_image(i) for i in images]

    async def nachricht():
        # Bilder gehen nur im Streaming-Modus: eine einzige Nutzernachricht mit Text und Bildern.
        yield {'type': 'user', 'message': {'role': 'user', 'content': content}}

    _WORKDIR.mkdir(exist_ok=True)
    options = ClaudeAgentOptions(
        model=config.CLAUDE_MODEL,
        system_prompt=system,
        output_format={'type': 'json_schema', 'schema': claude_schema(schema)},
        effort=EFFORT.get(name, 'medium'),
        tools=[],
        disallowed_tools=_BUILTIN,
        setting_sources=[],          # keine CLAUDE.md, Skills oder Einstellungen des Rechners laden
        max_turns=4,                 # Antwort kommt über ein internes StructuredOutput-Werkzeug
        cwd=str(_WORKDIR),
    )
    result = None
    async for msg in query(prompt=nachricht(), options=options):
        if isinstance(msg, ResultMessage):
            result = msg
    return result


def chat_json(*, model, system, user, schema, name, images=(), max_tokens=2500, temperature=None):
    os.environ.pop('ANTHROPIC_API_KEY', None)  # sonst würde der API-Schlüssel statt des Abos genutzt
    t0 = time.perf_counter()
    try:
        res = asyncio.run(asyncio.wait_for(_run(system, user, schema, name, list(images)), config.LLM_TIMEOUT))
    except asyncio.TimeoutError as e:
        raise ClaudeAboError(f'Keine Antwort nach {config.LLM_TIMEOUT:.0f} s') from e
    except Exception as e:  # noqa: BLE001 - das SDK wirft nach Fehlerergebnissen allgemeine Ausnahmen
        raise ClaudeAboError(f'Claude (Abo) fehlgeschlagen: {e}') from e
    if res is None or res.is_error or not res.structured_output:
        grund = (res.errors or [res.subtype]) if res else ['keine Antwort']
        raise ClaudeAboError(f'Claude (Abo) lieferte kein Ergebnis: {"; ".join(map(str, grund))}')
    data = res.structured_output
    if isinstance(data, str):
        data = json.loads(data)
    usage = res.usage or {}
    info = {'ms': round((time.perf_counter() - t0) * 1000), 'modell': config.CLAUDE_MODEL,
            'tokens': {'input': usage.get('input_tokens'), 'output': usage.get('output_tokens')}}
    return data, info


def health():
    base = {'modus': 'claude-abo', 'anbieter': 'claude', 'modell': config.CLAUDE_MODEL}
    token = os.getenv('CLAUDE_CODE_OAUTH_TOKEN')
    lokal = (Path.home() / '.claude' / '.credentials.json').exists()
    if not (token or lokal):
        return {**base, 'ok': False, 'hinweis': 'Kein Abo-Zugang: CLAUDE_CODE_OAUTH_TOKEN setzen (claude setup-token)'}
    return {**base, 'ok': True, 'hinweis': None}
