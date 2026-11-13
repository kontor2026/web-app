"""Development-only AI proxy: pick the AI once at startup, the backend stays unchanged.

The backend already talks to any OpenAI-compatible server (LLM_PROVIDER=lokal). Point its
LLM_BASE_URL at this proxy, and every request goes to the AI chosen when the proxy starts:

    lokal       pass-through to an OpenAI-compatible server (default: Ollama on localhost:11434)
    claude      Anthropic API, needs ANTHROPIC_API_KEY
    claude-abo  Claude Agent SDK with the Claude Code login of this machine

Switching the AI means restarting only the proxy, not the backend. Not part of the app or the
containers. Usage from the repo root:

    backend/.venv/bin/python tools/ki_proxy.py              # asks which AI to use
    backend/.venv/bin/python tools/ki_proxy.py --ki claude  # no question

Then start the backend with LLM_PROVIDER=lokal and LLM_BASE_URL=http://127.0.0.1:4000/v1.
"""
import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402
import uvicorn  # noqa: E402
from fastapi import FastAPI, Request, Response  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

from backend.app import config  # noqa: E402

CHOICES = {
    'lokal': 'OpenAI-kompatibler Server (Ollama, llama.cpp, vLLM, LM Studio)',
    'claude': 'Anthropic-API mit ANTHROPIC_API_KEY',
    'claude-abo': 'Claude Agent SDK mit der Claude-Code-Anmeldung dieses Rechners',
}
DEFAULT_UPSTREAM = 'http://localhost:11434/v1'


class ProxyError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


def _error(status, message):
    return JSONResponse(status_code=status, content={'error': {'message': message, 'type': 'ki_proxy'}})


def _claude_backend(choice):
    """Return (chat_json, error_type, health) of the backend module that serves this choice."""
    if choice == 'claude':
        from backend.app import llm_claude
        return llm_claude.chat_json, llm_claude.ClaudeError, llm_claude.health
    from backend.app import llm_claude_abo
    return llm_claude_abo.chat_json, llm_claude_abo.ClaudeAboError, llm_claude_abo.health


def to_call_args(body):
    """Translate an OpenAI chat request (as sent by backend/app/llm.py) into chat_json() arguments."""
    system, texts, images = [], [], []
    for message in body.get('messages', []):
        content = message.get('content')
        parts = [{'type': 'text', 'text': content}] if isinstance(content, str) else (content or [])
        for part in parts:
            if part.get('type') == 'text':
                (system if message.get('role') == 'system' else texts).append(part['text'])
            elif part.get('type') == 'image_url' and message.get('role') == 'user':
                url = part['image_url']['url'] if isinstance(part.get('image_url'), dict) else part.get('image_url')
                images.append(url)
    response_format = (body.get('response_format') or {}).get('json_schema') or {}
    if not response_format.get('schema'):
        raise ProxyError(400, 'Der KI-Proxy unterstützt nur Anfragen mit response_format json_schema')
    return {
        'model': body.get('model'),
        'system': '\n\n'.join(system),
        'user': '\n\n'.join(texts),
        'schema': response_format['schema'],
        'name': response_format.get('name', 'antwort'),
        'images': images,
        'max_tokens': body.get('max_tokens', 2500),
    }


def to_openai_response(data, info, requested_model):
    """Wrap a parsed JSON answer as an OpenAI chat completion, as the backend expects it."""
    tokens = info.get('tokens') or {}
    prompt, completion = tokens.get('input') or 0, tokens.get('output') or 0
    return {
        'id': f'chatcmpl-{uuid.uuid4().hex[:16]}',
        'object': 'chat.completion',
        'created': int(time.time()),
        'model': info.get('modell') or requested_model,
        'choices': [{
            'index': 0,
            'message': {'role': 'assistant', 'content': json.dumps(data, ensure_ascii=False)},
            'finish_reason': 'stop',
        }],
        'usage': {'prompt_tokens': prompt, 'completion_tokens': completion, 'total_tokens': prompt + completion},
    }


def create_app(choice, upstream=DEFAULT_UPSTREAM):
    """Build the proxy for one fixed choice. Sync handlers run in a worker thread each."""
    app = FastAPI(title=f'KI-Proxy ({choice})', docs_url=None, redoc_url=None)
    upstream = upstream.rstrip('/')

    if choice == 'lokal':
        def forward(method, path, request_headers, body=None):
            headers = {k: v for k, v in request_headers.items() if k.lower() in ('authorization', 'content-type')}
            try:
                with httpx.Client(timeout=config.LLM_TIMEOUT) as client:
                    r = client.request(method, f'{upstream}{path}', content=body, headers=headers)
            except httpx.HTTPError as e:
                return _error(502, f'Modellserver hinter dem KI-Proxy nicht erreichbar ({upstream}): {e}')
            return Response(content=r.content, status_code=r.status_code,
                            media_type=r.headers.get('content-type', 'application/json'))

        @app.get('/v1/models')
        def models(request: Request):
            return forward('GET', '/models', request.headers)

        @app.post('/v1/chat/completions')
        def chat_completions(body: dict, request: Request):
            return forward('POST', '/chat/completions', request.headers, json.dumps(body).encode())

        return app

    chat_json, error_type, _ = _claude_backend(choice)

    @app.get('/v1/models')
    def models():
        # The backend only checks that its configured model name is listed.
        ids = sorted({config.VISION_MODEL, config.TEXT_MODEL})
        return {'object': 'list', 'data': [{'id': i, 'object': 'model', 'owned_by': f'ki-proxy:{choice}'} for i in ids]}

    @app.post('/v1/chat/completions')
    def chat_completions(body: dict):
        try:
            args = to_call_args(body)
            data, info = chat_json(**args)
        except ProxyError as e:
            return _error(e.status, str(e))
        except error_type as e:
            return _error(502, str(e))
        return to_openai_response(data, info, body.get('model'))

    return app


def ask_choice():
    print('Welche KI soll der Proxy nutzen?')
    keys = list(CHOICES)
    for i, key in enumerate(keys, 1):
        print(f'  {i}) {key:<11} {CHOICES[key]}')
    while True:
        answer = input('Auswahl [1]: ').strip() or '1'
        if answer in keys:
            return answer
        if answer.isdigit() and 1 <= int(answer) <= len(keys):
            return keys[int(answer) - 1]
        print(f'Bitte 1 bis {len(keys)} oder einen Namen eingeben.')


def status_line(choice, upstream):
    if choice == 'lokal':
        try:
            r = httpx.get(f'{upstream.rstrip("/")}/models', timeout=3)
            ids = [m['id'] for m in r.json().get('data', [])]
            return f'bereit, Modelle: {", ".join(ids) or "keine"}'
        except Exception as e:  # noqa: BLE001 - any failure means "not ready yet", the proxy still starts
            return f'Modellserver {upstream} noch nicht erreichbar ({e.__class__.__name__})'
    health = _claude_backend(choice)[2]()
    return 'bereit' if health.get('ok') else f'Hinweis: {health.get("hinweis")}'


def main():
    parser = argparse.ArgumentParser(description='KI-Proxy für die Entwicklung: KI einmal beim Start wählen.')
    parser.add_argument('--ki', choices=list(CHOICES), default=os.getenv('KI_PROXY_KI'),
                        help='welche KI (ohne Angabe wird gefragt)')
    parser.add_argument('--upstream', default=os.getenv('KI_PROXY_UPSTREAM', DEFAULT_UPSTREAM),
                        help=f'Modellserver für "lokal" (Standard: {DEFAULT_UPSTREAM})')
    parser.add_argument('--host', default='127.0.0.1', help='Adresse (Standard: nur dieser Rechner)')
    parser.add_argument('--port', type=int, default=4000)
    args = parser.parse_args()

    choice = args.ki
    if not choice:
        if not sys.stdin.isatty():
            parser.error('keine KI gewählt: --ki lokal|claude|claude-abo angeben')
        choice = ask_choice()

    model = args.upstream if choice == 'lokal' else config.CLAUDE_MODEL
    address = f'http://{args.host}:{args.port}/v1'
    print()
    print('KI-Proxy für die Entwicklung')
    print(f'  KI:       {choice} ({CHOICES[choice]})')
    print(f'  Ziel:     {model}')
    print(f'  Status:   {status_line(choice, args.upstream)}')
    print(f'  Adresse:  {address}')
    print()
    print('Backend damit starten (KI im Backend bleibt "lokal", der Proxy entscheidet):')
    print(f'  LLM_PROVIDER=lokal LLM_BASE_URL={address} python -m uvicorn backend.app.main:app --port 8000')
    print(flush=True)

    uvicorn.run(create_app(choice, args.upstream), host=args.host, port=args.port, log_level='warning')


if __name__ == '__main__':
    main()
