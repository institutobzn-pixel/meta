"""Robô que responde mensagens da Página do Facebook (Messenger) e do
Instagram (Direct) usando o Claude.

Fluxo: Meta envia a mensagem para /webhook -> o Claude gera a resposta ->
a resposta é enviada de volta pela Graph API da Meta.
"""

import hashlib
import hmac
import logging
import os
import threading
from collections import defaultdict, deque

import anthropic
import requests
from flask import Flask, abort, request

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("meta-claude")

# --- Configuração (variáveis de ambiente) -----------------------------------
PAGE_ACCESS_TOKEN = os.environ["PAGE_ACCESS_TOKEN"]
META_VERIFY_TOKEN = os.environ["META_VERIFY_TOKEN"]
META_APP_SECRET = os.environ.get("META_APP_SECRET", "")
GRAPH_VERSION = os.environ.get("GRAPH_API_VERSION", "v23.0")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5")
SYSTEM_PROMPT = os.environ.get(
    "SYSTEM_PROMPT",
    "Você é o assistente virtual do Instituto no Facebook e no Instagram. "
    "Responda sempre em português do Brasil, de forma simpática, clara e curta "
    "(no máximo 3 parágrafos curtos), pois a conversa acontece no chat do celular. "
    "Não use formatação Markdown. Se não souber algo sobre o Instituto, diga que "
    "vai encaminhar a pergunta para a equipe.",
)

MAX_HISTORY = 20          # mensagens guardadas por pessoa (usuário + Claude)
MAX_CHUNK = 1000          # limite de caracteres por mensagem no Instagram

claude = anthropic.Anthropic()  # lê ANTHROPIC_API_KEY
app = Flask(__name__)

# Histórico em memória: some quando o servidor reinicia. Suficiente para começar.
history = defaultdict(lambda: deque(maxlen=MAX_HISTORY))
seen_ids = deque(maxlen=1000)  # a Meta às vezes reenvia o mesmo evento
lock = threading.Lock()


# --- Rotas -------------------------------------------------------------------
@app.get("/")
def health():
    return "ok"


@app.get("/webhook")
def verify():
    """A Meta chama esta rota uma vez, ao salvar o webhook no painel."""
    if (
        request.args.get("hub.mode") == "subscribe"
        and request.args.get("hub.verify_token") == META_VERIFY_TOKEN
    ):
        return request.args.get("hub.challenge", "")
    abort(403)


@app.post("/webhook")
def receive():
    if not valid_signature(request.get_data(), request.headers.get("X-Hub-Signature-256", "")):
        log.warning("Assinatura inválida; evento ignorado")
        abort(403)

    data = request.get_json(silent=True) or {}
    channel = data.get("object")  # "page" (Messenger) ou "instagram"
    if channel not in ("page", "instagram"):
        return "ignorado", 200

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            message = event.get("message") or {}
            text = message.get("text")
            if not text or message.get("is_echo"):
                continue  # ignora fotos/áudios e as mensagens enviadas pela própria Página
            with lock:
                if message.get("mid") in seen_ids:
                    continue
                seen_ids.append(message.get("mid"))
            sender_id = event["sender"]["id"]
            # Responde 200 na hora e processa em segundo plano (a Meta exige resposta rápida).
            threading.Thread(target=handle_message, args=(channel, sender_id, text)).start()

    return "ok", 200


# --- Lógica ------------------------------------------------------------------
def valid_signature(body: bytes, header: str) -> bool:
    if not META_APP_SECRET:
        return True  # sem App Secret configurado, não valida (só para testes)
    expected = "sha256=" + hmac.new(META_APP_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header)


def handle_message(channel: str, sender_id: str, text: str):
    key = f"{channel}:{sender_id}"
    try:
        send_action(sender_id, "typing_on")
        with lock:
            history[key].append({"role": "user", "content": text})
            messages = list(history[key])
        reply = ask_claude(messages)
        with lock:
            history[key].append({"role": "assistant", "content": reply})
        send_text(sender_id, reply)
    except Exception:
        log.exception("Erro ao responder %s", key)
        with lock:
            history.pop(key, None)  # recomeça a conversa limpa se algo deu errado


def ask_claude(messages: list) -> str:
    # O histórico precisa começar com uma mensagem do usuário.
    while messages and messages[0]["role"] != "user":
        messages.pop(0)

    response = claude.beta.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=messages,
        output_config={"effort": "low"},  # chat: respostas rápidas e baratas
        # Se o modelo recusar por segurança, a API tenta outro modelo automaticamente.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        return "Desculpe, não posso ajudar com isso. Posso ajudar com outra coisa?"
    text = "".join(block.text for block in response.content if block.type == "text").strip()
    return text or "Desculpe, não entendi. Pode repetir de outro jeito?"


def graph_post(payload: dict):
    r = requests.post(
        f"https://graph.facebook.com/{GRAPH_VERSION}/me/messages",
        params={"access_token": PAGE_ACCESS_TOKEN},
        json=payload,
        timeout=20,
    )
    if r.status_code >= 400:
        log.error("Erro da Meta (%s): %s", r.status_code, r.text)
    return r


def send_action(recipient_id: str, action: str):
    graph_post({"recipient": {"id": recipient_id}, "sender_action": action})


def send_text(recipient_id: str, text: str):
    for chunk in split_text(text, MAX_CHUNK):
        graph_post({
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {"text": chunk},
        })


def split_text(text: str, size: int):
    """Quebra textos longos em pedaços, de preferência em quebras de linha ou espaços."""
    while len(text) > size:
        cut = text.rfind("\n", 0, size)
        if cut < size // 2:
            cut = text.rfind(" ", 0, size)
        if cut < size // 2:
            cut = size
        yield text[:cut].strip()
        text = text[cut:].strip()
    if text:
        yield text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
