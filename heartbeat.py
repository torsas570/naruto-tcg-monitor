#!/usr/bin/env python3
"""Heartbeat diario — manda a Telegram resumen del estado del bot."""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE = Path(__file__).parent
CONFIG = json.load(open(BASE / "config.json"))
STATE_PATH = BASE / "state.json"

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN") or CONFIG["telegram_bot_token"]
chat_id = os.environ.get("TELEGRAM_CHAT_ID") or CONFIG["telegram_chat_id"]

state = json.load(open(STATE_PATH)) if STATE_PATH.exists() else {}

n_sites_cfg = len([s for s in CONFIG["sites"] if "url" in s])
RESERVED = ("__health__", "__health_meta__")
health = state.get("__health__", {})
sites_state = {k: v for k, v in state.items() if k not in RESERVED and isinstance(v, dict)}

n_sites_tracked = len(sites_state)
total_products = sum(len(v) for v in sites_state.values())
oos = sum(
    1
    for site in sites_state.values() if isinstance(site, dict)
    for p in site.values() if isinstance(p, dict) and not p.get("in_stock", True)
)
in_stock = total_products - oos

# Resumen de salud: el monitor solo interrumpe en el momento si algo es grave;
# el repaso tranquilo de "qué llevo roto" va una vez al día, aquí.
caidas = sorted(n for n, h in health.items() if h.get("fails", 0) >= 3)


def _lista(nombres, limite=8):
    resto = len(nombres) - limite
    return " · ".join(nombres[:limite]) + (f" y {resto} más" if resto > 0 else "")


salud = (f"\n⚠️ <b>Sin responder ({len(caidas)})</b>: {_lista(caidas)}"
         if caidas else "\n💚 Todas las tiendas responden")

msg = (
    f"💓 <b>Heartbeat NARUTO Card Game</b> 🍥\n"
    f"📅 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    f"✅ Bot vivo y funcionando\n"
    f"🏪 Tiendas configuradas: {n_sites_cfg}\n"
    f"📊 Tiendas con producto Naruto: {n_sites_tracked}\n"
    f"📦 Productos Naruto tracked: {total_products}\n"
    f"  • En stock: {in_stock}\n"
    f"  • Agotados: {oos}\n\n"
    f"{salud}\n"
    f"ℹ️ Lanzamiento Bandai en 2027 (reveal 29-jul-2026). Hasta entonces 0 productos es lo normal.\n"
    f"Si esto no te llega cada noche → el bot está caído. Revisa GitHub Actions."
)

resp = requests.post(
    f"https://api.telegram.org/bot{bot_token}/sendMessage",
    json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"},
    timeout=15,
)
if resp.status_code != 200:
    print(f"Error: {resp.text}")
    sys.exit(1)
print("Heartbeat enviado")
