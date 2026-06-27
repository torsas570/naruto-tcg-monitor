# NARUTO CARD GAME (Bandai) — investigación y notas del bot

## El lanzamiento

- **Juego:** "NARUTO CARD GAME", de **Bandai Card Games** (la misma división que One Piece
  Card Game, Dragon Ball Super CG Fusion World, Gundam CG, Digimon CG). Primer TCG oficial
  de Naruto en más de una década.
- **Anuncio:** 18 de junio de 2026.
- **Revelación completa + roadmap:** **29 de julio de 2026** (JST) — diseños de cartas,
  tipos de producto y fechas. **Es la fecha clave para afinar el bot** (códigos de set).
- **Debut mundial:** **Gen Con 2026** (30 jul – 2 ago, Indianápolis): primeras sesiones
  tutorial con mazos demo.
- **Lanzamiento global:** **2027**, simultáneo en todo el mundo.
- **Web oficial:** naruto-cardgame.com · cuentas en X/Instagram/Facebook/YouTube.
- **Aval:** Masashi Kishimoto, creador de Naruto.

### Promos de inauguración (Gen Con 2026)
- Carta promocional **CP-001 "Chakra Card"** (versión promo) y **playmats** oficiales.
- Asistentes a los tutoriales: carta promo + mochila + pegatina + ticket de compra de playmat.
- Visitantes del stand: mochila + pegatina (hasta agotar).

## Estrategia del bot

Al ser **Bandai Card Games**, el Naruto CG se distribuirá por los **mismos canales que One
Piece**: las tiendas TCG que ya venden OP serán las que reciban Naruto. Por eso la lista de
tiendas se basa en la del bot de OP (`/op/config.json`) + los feeds de preventa del de
Pokémon.

Como el producto **no existe hasta 2027**, el objetivo ahora es **cazar la primera preventa/
listado**. Cada tienda se vigila por una de estas vías:

1. **Feeds de preventa multi-juego** (Madrid Norte, Pokejotta, SparkLeaf, CardTreasure,
   JapHunter, Factory Cards, Pokezilla) → filtrados por "naruto". Aquí suele aparecer
   primero una línea nueva de Bandai. Van en **HIGH** (cada 5 min).
2. **Colecciones `naruto` "adivinadas"** en tiendas Shopify (por analogía con sus handles
   de One Piece, p. ej. `/collections/naruto-card-game`). Dan **404 hasta que la tienda las
   cree**; el monitor lo trata como warning y **se auto-activan** en cuanto existan.
3. **Búsqueda `?search=naruto`** en tiendas WooCommerce/PrestaShop ES → funciona desde el
   primer día y devuelve vacío hasta que listen producto.

### Prioridad de avisos
- **Sitio HIGH/medium** solo reparte el chequeo entre workflows (HIGH = 5 min, resto = 15 min).
- **Producto** se marca 🚨 **CASE/BOX** y se muestra primero cuando el título contiene
  `case`, `booster box`, `display`, `caja de sobres`, etc. (`high_value_keywords`) — que es
  **lo que más interesa**. Sobres sueltos / starter decks llegan igual, pero sin destacar.

### Filtro de keywords
- `required_keywords`: solo notifica títulos con **"naruto"** (`ナルト`/`うずまき` para imports JP).
- `exclude_keywords`: descarta el **viejo Naruto CCG** (Bandai 2006-2011), el **"Naruto
  Mythos"** (otra empresa, narutotcgmythos.com), **Weiss Schwarz Naruto** y merch
  (figuras/manga/funko) que ensucian la búsqueda.

## TODO tras el reveal del 29-jul-2026
1. Añadir el **código de set** real a `required_keywords` (estilo "OP-01" de One Piece →
   probablemente algo como "NT-01"/"NRT-01") para no depender solo de "naruto".
2. Confirmar **nombres de producto** (¿"Booster Box" / "Booster Display" / "Case"?) y
   ajustar `high_value_keywords` si Bandai usa otra nomenclatura.
3. Cuando las tiendas creen sus colecciones reales, cambiar los handles "adivinados" por los
   correctos (mirar cómo nombran la colección de One Piece en cada una).

## Uso
```bash
python3 setup_telegram.py            # crea/valida bot, detecta chat_id, manda test
                                     # y te imprime los valores para los Secrets
# Probar en local (el token NUNCA va en config.json — se pasa por env):
export TELEGRAM_BOT_TOKEN='...'; export TELEGRAM_CHAT_ID='...'
python3 monitor.py                   # 1 pasada, todas las tiendas
python3 monitor.py --priority high   # solo preventas / cases
python3 monitor.py --loop            # bucle local cada 15 min
```
Despliegue = GitHub Actions (3 workflows: monitor 15 min, monitor-high 5 min, heartbeat
diario). Secrets del repo necesarios: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

> **Primera pasada = baseline silencioso.** No esperes avisos hasta que una tienda liste
> un producto Naruto *nuevo* (la preventa real). Todo el "naruto" que existe hoy es ruido
> y se absorbe sin notificar.
