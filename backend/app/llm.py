"""Client für OpenAI-kompatible Modellserver mit erzwungenem JSON-Schema.

Das Schema wird als response_format übergeben. Ollama, llama.cpp und vLLM wandeln es in eine
Grammatik um: Das Modell kann dann nur noch gültiges JSON in genau dieser Form erzeugen."""
import json
import re
import time

import httpx

from . import config


class LLMError(Exception):
    pass


def _strip(text: str) -> str:
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.S).strip()
    text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text).strip()
    return text


def chat_json(modus=None, **kw):
    """Ein KI-Aufruf mit erzwungenem JSON-Schema. Rückgabe (daten, info) mit Dauer und Token-Zahlen.
    modus: 'souveraen' (lokal) oder 'cloud' (Claude) aus der Oberfläche, None = LLM_PROVIDER."""
    anbieter = config.provider(modus)
    if anbieter == 'claude':
        from . import llm_claude
        try:
            return llm_claude.chat_json(**kw)
        except llm_claude.ClaudeError as e:
            raise LLMError(str(e)) from e
    if anbieter == 'claude-abo':
        from . import llm_claude_abo
        try:
            return llm_claude_abo.chat_json(**kw)
        except llm_claude_abo.ClaudeAboError as e:
            raise LLMError(str(e)) from e
    return _chat_openai(**kw)


def _chat_openai(*, model, system, user, schema, name, images=(), max_tokens=2500, temperature=0.2):
    content = [{'type': 'text', 'text': user}]
    content += [{'type': 'image_url', 'image_url': {'url': img}} for img in images]
    payload = {
        'model': model,
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': content}],
        'temperature': temperature,
        'max_tokens': max_tokens,
        'response_format': {'type': 'json_schema', 'json_schema': {'name': name, 'schema': schema, 'strict': True}},
    }
    if config.LLM_REASONING:
        # Denkmodelle (z. B. Qwen3-VL) würden sonst erst lange "nachdenken": auf CPU Faktor 5–10 langsamer.
        payload['reasoning_effort'] = config.LLM_REASONING
    t0 = time.perf_counter()
    try:
        with httpx.Client(timeout=config.LLM_TIMEOUT) as c:
            r = c.post(f'{config.LLM_BASE_URL}/chat/completions', json=payload,
                       headers={'Authorization': f'Bearer {config.LLM_API_KEY}'})
    except httpx.HTTPError as e:
        raise LLMError(f'Modellserver nicht erreichbar ({config.LLM_BASE_URL}): {e}') from e
    if r.status_code != 200:
        raise LLMError(f'Modellserver antwortet {r.status_code}: {r.text[:300]}')
    body = r.json()
    msg = body['choices'][0]['message']
    # Ollama legt die Antwort bei abgeschaltetem Denken teils in "reasoning" statt "content".
    text = _strip(msg.get('content') or msg.get('reasoning') or msg.get('reasoning_content') or '')
    if body['choices'][0].get('finish_reason') == 'length':
        raise LLMError(f'Antwort abgeschnitten (max_tokens={max_tokens} erreicht)')
    info = {'ms': round((time.perf_counter() - t0) * 1000), 'modell': model, 'tokens': body.get('usage', {})}
    try:
        return json.loads(text), info
    except json.JSONDecodeError as e:
        raise LLMError(f'Antwort ist kein gültiges JSON: {e}; Anfang: {text[:200]}') from e


def health():
    """Stand beider Modi für den Umschalter in der Oberfläche, plus der Standardmodus vorne."""
    if config.LLM_MODE == 'mock':          # Abschaltschalter hat Vorrang vor dem Anbieter
        return {'ok': True, 'modus': 'mock', 'modell': None, 'hinweis': 'KI abgeschaltet: nur Kategorien und Foto-Abgleich'}
    modi = {m: _health(config.provider(m)) for m in ('souveraen', 'cloud')}
    return {**modi[config.STANDARD_MODUS], 'standard': config.STANDARD_MODUS, 'modi': modi}


def _health(anbieter):
    if anbieter == 'claude':
        from . import llm_claude
        return llm_claude.health()
    if anbieter == 'claude-abo':
        from . import llm_claude_abo
        return llm_claude_abo.health()
    try:
        r = httpx.get(f'{config.LLM_BASE_URL}/models', timeout=3,
                      headers={'Authorization': f'Bearer {config.LLM_API_KEY}'})
        ids = [m['id'] for m in r.json().get('data', [])]
    except Exception as e:  # noqa: BLE001 - jede Störung heißt "nicht bereit"
        return {'ok': False, 'modus': 'openai', 'modell': config.VISION_MODEL, 'hinweis': f'Modellserver nicht erreichbar: {e}'}
    ok = config.VISION_MODEL in ids or f'{config.VISION_MODEL}:latest' in ids
    return {'ok': ok, 'modus': 'openai', 'anbieter': 'lokal', 'modell': config.VISION_MODEL,
            'hinweis': None if ok else f'Modell {config.VISION_MODEL} nicht geladen. Verfügbar: {", ".join(ids) or "keine"}'}
