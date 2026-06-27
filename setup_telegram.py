#!/usr/bin/env python3
"""
Configuración de Telegram para el bot NARUTO Card Game.

NO escribe el token en config.json (ese archivo se sube a GitHub y filtraría el
secreto). En su lugar: detecta tu CHAT_ID, manda un mensaje de prueba y te imprime
los dos valores listos para meter en GitHub Secrets (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID).

Para probar en local, exporta las variables de entorno que te indica al final.
"""

import sys
import requests


def main():
    print("=" * 56)
    print("  CONFIGURACIÓN DE TELEGRAM — NARUTO CARD GAME BOT 🍥")
    print("=" * 56)
    print()
    print("PASO 1 — Crear el bot en Telegram (si aún no lo tienes):")
    print("  1. Abre Telegram → @BotFather → /newbot")
    print("  2. Nombre: 'Naruto TCG Monitor'")
    print("  3. Username: ej. 'naruto_tcg_monitor_bot'")
    print("  4. Copia el TOKEN que te da BotFather")
    print()
    bot_token = input("Pega aquí tu BOT TOKEN: ").strip()
    if not bot_token or ":" not in bot_token:
        print("❌ Token no válido. Aborto.")
        sys.exit(1)

    # Validar el token
    me = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe", timeout=10).json()
    if not me.get("ok"):
        print(f"❌ El token no funciona: {me}")
        sys.exit(1)
    print(f"✅ Bot detectado: @{me['result'].get('username')}")

    print()
    print("PASO 2 — Obtener tu CHAT ID:")
    print("  1. Busca tu bot en Telegram y envíale cualquier mensaje (ej. 'hola').")
    input("  2. Cuando lo hayas enviado, pulsa Enter aquí...")

    data = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates", timeout=10).json()
    chat_id = ""
    if data.get("result"):
        last = data["result"][-1]["message"]["chat"]
        chat_id = str(last["id"])
        print(f"✅ Chat ID detectado: {chat_id} ({last.get('first_name', '')})")
    else:
        chat_id = input("No se detectó ningún mensaje. Introduce tu Chat ID manualmente: ").strip()

    print("\nEnviando mensaje de prueba...")
    resp = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={
            "chat_id": chat_id,
            "parse_mode": "HTML",
            "text": (
                "✅ <b>Bot NARUTO Card Game configurado!</b> 🍥\n\n"
                "🚨 Avisos HIGH (cada 5 min): preventas/reservas + cases y booster boxes.\n"
                "📦 Avisos MEDIUM (cada 15 min): resto de tiendas.\n\n"
                "Lanzamiento Bandai 2027 — te aviso en cuanto abra la primera preventa."
            ),
        },
        timeout=10,
    )
    print("✅ Mensaje de prueba enviado" if resp.status_code == 200 else f"❌ Error: {resp.text}")

    print()
    print("=" * 56)
    print("  LISTO. Ahora elige dónde corre el bot:")
    print("=" * 56)
    print("\n▶ OPCIÓN A — GitHub Actions (recomendado, 24/7). En el repo:")
    print("    Settings → Secrets and variables → Actions → New repository secret")
    print(f"      TELEGRAM_BOT_TOKEN = {bot_token}")
    print(f"      TELEGRAM_CHAT_ID   = {chat_id}")
    print("    O por terminal con gh (desde la carpeta del repo):")
    print(f"      gh secret set TELEGRAM_BOT_TOKEN --body '{bot_token}'")
    print(f"      gh secret set TELEGRAM_CHAT_ID --body '{chat_id}'")
    print("\n▶ OPCIÓN B — Probar en local ahora mismo:")
    print(f"      export TELEGRAM_BOT_TOKEN='{bot_token}'")
    print(f"      export TELEGRAM_CHAT_ID='{chat_id}'")
    print("      python3 monitor.py --priority high")
    print("\n⚠️  No pegues el token en config.json (ese archivo se sube a GitHub).")
    print("=" * 56)


if __name__ == "__main__":
    main()
