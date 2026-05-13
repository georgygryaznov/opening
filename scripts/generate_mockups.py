#!/usr/bin/env python3
"""
Генератор PNG-макетов для 7 отчётов первой очереди.
Сохраняет файлы в brd/mockups/
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ─── Настройки ───────────────────────────────────────────────────────────────

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "brd", "mockups")
os.makedirs(OUT_DIR, exist_ok=True)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_BG = (245, 245, 245)
GRAY_LINE = (200, 200, 200)
GRAY_TEXT = (100, 100, 100)
DARK_BG = (45, 55, 72)
HEADER_BG = (55, 65, 85)
GREEN = (76, 175, 80)
YELLOW = (255, 193, 7)
RED = (244, 67, 54)
BLUE = (33, 150, 243)
LIGHT_BLUE = (227, 242, 253)
LIGHT_GREEN = (232, 245, 233)
LIGHT_YELLOW = (255, 248, 225)
LIGHT_RED = (255, 235, 238)
ORANGE = (255, 152, 0)

# Шрифты
try:
    FONT_TITLE = ImageFont.truetype("arial.ttf", 18)
    FONT_HEADER = ImageFont.truetype("arial.ttf", 13)
    FONT_NORMAL = ImageFont.truetype("arial.ttf", 11)
    FONT_SMALL = ImageFont.truetype("arial.ttf", 9)
    FONT_BOLD = ImageFont.truetype("arialbd.ttf", 11)
except:
    FONT_TITLE = ImageFont.load_default()
    FONT_HEADER = ImageFont.load_default()
    FONT_NORMAL = ImageFont.load_default()
    FONT_SMALL = ImageFont.load_default()
    FONT_BOLD = ImageFont.load_default()


def draw_table(draw, x, y, col_widths, headers, rows, header_bg=HEADER_BG):
    """Рисует таблицу с заголовками и строками."""
    row_h = 22
    total_w = sum(col_widths)
    
    # Заголовок
    cx = x
    for i, h in enumerate(headers):
        draw.rectangle([cx, y, cx + col_widths[i], y + row_h], fill=header_bg)
        draw.text((cx + 4, y + 4), h, fill=WHITE, font=FONT_BOLD)
        cx += col_widths[i]
    
    # Строки
    for ri, row in enumerate(rows):
        cy = y + row_h + ri * row_h
        bg = GRAY_BG if ri % 2 == 0 else WHITE
        draw.rectangle([x, cy, x + total_w, cy + row_h], fill=bg)
        cx = x
        for ci, val in enumerate(row):
            color = BLACK
            # Цветовая индикация для числовых значений
            if isinstance(val, str) and val.startswith("🟢"):
                color = GREEN
            elif isinstance(val, str) and val.startswith("🟡"):
                color = ORANGE
            elif isinstance(val, str) and val.startswith("🔴"):
                color = RED
            draw.text((cx + 4, cy + 3), str(val), fill=color, font=FONT_NORMAL)
            cx += col_widths[ci]
        # Линия
        draw.line([x, cy + row_h, x + total_w, cy + row_h], fill=GRAY_LINE, width=1)


def draw_card(draw, x, y, w, h, title, value, color_indicator):
    """Рисует KPI-карточку."""
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=GRAY_LINE, width=1)
    draw.text((x + 8, y + 6), title, fill=GRAY_TEXT, font=FONT_SMALL)
    draw.text((x + 8, y + 22), value, fill=BLACK, font=FONT_BOLD)
    # Цветовой индикатор
    ci = {"green": GREEN, "yellow": YELLOW, "red": RED}.get(color_indicator, GRAY_LINE)
    draw.rectangle([x + w - 16, y + 6, x + w - 6, y + 16], fill=ci)


def draw_bar_chart(draw, x, y, w, h, data, colors):
    """Рисует простую столбчатую диаграмму."""
    if not data:
        return
    max_val = max(data)
    bar_w = (w - 20) // len(data)
    for i, val in enumerate(data):
        bar_h = int((val / max_val) * (h - 30))
        draw.rectangle(
            [x + 10 + i * bar_w, y + h - 10 - bar_h, x + 10 + i * bar_w + bar_w - 2, y + h - 10],
            fill=colors[i] if i < len(colors) else BLUE
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 1. ОПиУ (P&L)
# ═══════════════════════════════════════════════════════════════════════════════
def render_opiu():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), GRAY_BG)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 15), "Отчёт 1.1 — ОПиУ (P&L)", fill=BLACK, font=FONT_TITLE)
    draw.text((20, 40), "Отчёт о прибылях и убытках | Май 2026", fill=GRAY_TEXT, font=FONT_NORMAL)
    
    headers = ["Юрлицо", "Выручка", "Себестоимость", "Вал. прибыль", "Вал. маржа %", "EBITDA", "Чистая прибыль"]
    col_w = [140, 100, 100, 100, 80, 100, 100]
    rows = [
        ["Открытие", "1 500 000", "900 000", "600 000", "🟢 40%", "350 000", "250 000"],
        ["Открытие Тюмень", "800 000", "500 000", "300 000", "🟢 37.5%", "180 000", "120 000"],
        ["Открытие Пермь", "600 000", "420 000", "180 000", "🟡 30%", "90 000", "50 000"],
        ["ИП Зиновьев", "300 000", "210 000", "90 000", "🟡 30%", "40 000", "20 000"],
        ["ИП Семенов", "200 000", "160 000", "40 000", "🔴 20%", "10 000", "-5 000"],
        ["ИП Ушакова", "100 000", "75 000", "25 000", "🔴 25%", "5 000", "0"],
        ["", "", "", "", "", "", ""],
        ["ИТОГО по ГК", "3 500 000", "2 265 000", "1 235 000", "🟢 35.3%", "675 000", "435 000"],
    ]
    draw_table(draw, 20, 65, col_w, headers, rows)
    
    # Легенда
    draw.text((20, 320), "Цветовая индикация:", fill=GRAY_TEXT, font=FONT_SMALL)
    draw.text((20, 335), "🟢 Валовая маржа > 25%", fill=GREEN, font=FONT_SMALL)
    draw.text((180, 335), "🟡 Валовая маржа 15-25%", fill=ORANGE, font=FONT_SMALL)
    draw.text((360, 335), "🔴 Валовая маржа < 15%", fill=RED, font=FONT_SMALL)
    
    draw.text((20, 360), "Drill-down: клик на выручку → регионы → клиенты → заказы", fill=GRAY_TEXT, font=FONT_SMALL)
    draw.text((20, 380), "Сравнение: тек. месяц / прошлый месяц / аналог. период прошлого года / % изменений", fill=GRAY_TEXT, font=FONT_SMALL)
    
    img.save(os.path.join(OUT_DIR, "01_opiu.png"))
    print("[OK] 01_opiu.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. ОДДС (Cash Flow)
# ═══════════════════════════════════════════════════════════════════════════════
def render_odds():
    W, H = 800, 550
    img = Image.new("RGB", (W, H), GRAY_BG)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 15), "Отчёт 1.2 — ОДДС (Cash Flow)", fill=BLACK, font=FONT_TITLE)
    draw.text((20, 40), "Отчёт о движении денежных средств | Май 2026 | ГК «Открытие»", fill=GRAY_TEXT, font=FONT_NORMAL)
    
    headers = ["Поток", "План", "Факт", "Отклонение", "Откл. %"]
    col_w = [200, 120, 120, 120, 100]
    rows = [
        ["Операционный приток", "3 200 000", "3 500 000", "+300 000", "🟢 +9.4%"],
        ["Операционный отток", "-2 500 000", "-2 800 000", "-300 000", "🔴 -12.0%"],
        ["Чистый операционный поток", "700 000", "700 000", "0", "🟢 0%"],
        ["Инвестиционный приток", "0", "50 000", "+50 000", "—"],
        ["Инвестиционный отток", "-200 000", "-150 000", "+50 000", "🟢 +25%"],
        ["Чистый инвестиционный поток", "-200 000", "-100 000", "+100 000", "🟢 +50%"],
        ["Финансовый приток", "500 000", "500 000", "0", "🟢 0%"],
        ["Финансовый отток", "-300 000", "-300 000", "0", "🟢 0%"],
        ["Чистый финансовый поток", "200 000", "200 000", "0", "🟢 0%"],
        ["", "", "", "", ""],
        ["ЧИСТЫЙ ДЕНЕЖНЫЙ ПОТОК", "700 000", "800 000", "+100 000", "🟢 +14.3%"],
    ]
    draw_table(draw, 20, 65, col_w, headers, rows, header_bg=(55, 65, 85))
    
    # График
    draw.text((20, 340), "Динамика Cash Flow по месяцам:", fill=BLACK, font=FONT_HEADER)
    chart_data = [600, 750, 700, 800, 650, 800]
    chart_colors = [BLUE, GREEN, YELLOW, GREEN, ORANGE, GREEN]
    draw_bar_chart(draw, 20, 365, 500, 120, chart_data, chart_colors)
    months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн"]
    for i, m in enumerate(months):
        draw.text((30 + i * 80, 475), m, fill=GRAY_TEXT, font=FONT_SMALL)
    
    draw.text((20, 510), "⚠ Критическое предупреждение: прибыль ≠ деньги. Компания может быть прибыльной по ОПиУ и иметь кассовый разрыв.", fill=RED, font=FONT_SMALL)
    
    img.save(os.path.join(OUT_DIR, "02_odds.png"))
    print("[OK] 02_odds.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. Управленческий баланс
# ═══════════════════════════════════════════════════════════════════════════════
def render_balance():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), GRAY_BG)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 15), "Отчёт 1.3 — Управленческий баланс", fill=BLACK, font=FONT_TITLE)
    draw.text((20, 40), "Срез на 31.05.2026 | ГК «Открытие»", fill=GRAY_TEXT, font=FONT_NORMAL)
    
    headers = ["Статья", "Открытие", "Тюмень", "Пермь", "ИП", "ИТОГО"]
    col_w = [200, 100, 100, 100, 100, 100]
    rows = [
        ["АКТИВЫ", "", "", "", "", ""],
        ["  Остаток ДС", "2 500 000", "800 000", "400 000", "300 000", "4 000 000"],
        ["  Товарные запасы", "5 000 000", "2 000 000", "1 500 000", "500 000", "9 000 000"],
        ["  Дебиторская задолженность", "3 000 000", "1 200 000", "800 000", "400 000", "5 400 000"],
        ["  Основные средства", "8 000 000", "3 000 000", "2 000 000", "1 000 000", "14 000 000"],
        ["  Активы, всего", "18 500 000", "7 000 000", "4 700 000", "2 200 000", "32 400 000"],
        ["ПАССИВЫ", "", "", "", "", ""],
        ["  Кредиторская задолженность", "2 000 000", "1 000 000", "600 000", "300 000", "3 900 000"],
        ["  Заёмные средства", "5 000 000", "2 000 000", "1 500 000", "500 000", "9 000 000"],
        ["  Пассивы, всего", "7 000 000", "3 000 000", "2 100 000", "800 000", "12 900 000"],
        ["", "", "", "", "", ""],
        ["СОБСТВЕННЫЙ КАПИТАЛ", "11 500 000", "4 000 000", "2 600 000", "1 400 000", "19 500 000"],
    ]
    draw_table(draw, 20, 65, col_w, headers, rows)
    
    # CCC
    draw.text((20, 360), "Cash Conversion Cycle (CCC):", fill=BLACK, font=FONT_HEADER)
    draw.text((20, 385), "Оборачиваемость запасов: 35 дн. + DSO: 28 дн. – DPO: 22 дн. = CCC: 🟡 41 дн.", fill=BLACK, font=FONT_NORMAL)
    draw.text((20, 410), "Цветовая индикация: CCC < 30 дн. — зелёный, 30-60 дн. — жёлтый, > 60 дн. — красный", fill=GRAY_TEXT, font=FONT_SMALL)
    
    img.save(os.path.join(OUT_DIR, "03_balance.png"))
    print("[OK] 03_balance.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. Дебиторская задолженность
# ═══════════════════════════════════════════════════════════════════════════════
def render_debitor():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), GRAY_BG)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 15), "Отчёт 1.4 — Дебиторская задолженность", fill=BLACK, font=FONT_TITLE)
    draw.text((20, 40), "Срез на 31.05.2026 | ГК «Открытие»", fill=GRAY_TEXT, font=FONT_NORMAL)
    
    headers = ["Контрагент", "Юрлицо", "Сумма долга", "Дней просрочки", "0-7 дн.", "8-15 дн.", "16-30 дн.", ">30 дн."]
    col_w = [130, 100, 100, 80, 70, 70, 70, 70]
    rows = [
        ["ООО СтройМаркет", "Открытие", "1 200 000", "5", "1 200 000", "0", "0", "0"],
        ["ИП Петров", "Открытие", "800 000", "12", "0", "800 000", "0", "0"],
        ["ООО РемСтрой", "Тюмень", "500 000", "🔴 35", "0", "0", "0", "500 000"],
        ["ООО Снабженец", "Пермь", "300 000", "3", "300 000", "0", "0", "0"],
        ["ИП Сидоров", "Открытие", "200 000", "🔴 45", "0", "0", "0", "200 000"],
        ["ООО СтройКом", "Тюмень", "150 000", "8", "0", "150 000", "0", "0"],
        ["", "", "", "", "", "", "", ""],
        ["ИТОГО", "", "3 150 000", "", "1 500 000", "950 000", "0", "700 000"],
    ]
    draw_table(draw, 20, 65, col_w, headers, rows)
    
    draw.text((20, 320), "DSO (средний срок оплаты): 🟡 28 дней", fill=BLACK, font=FONT_NORMAL)
    draw.text((20, 345), "Доля просрочки > 30 дней: 22% (700 000 / 3 150 000) — требуется контроль", fill=RED, font=FONT_SMALL)
    draw.text((20, 370), "Drill-down: клик на контрагента → детализация по документам реализации", fill=GRAY_TEXT, font=FONT_SMALL)
    
    img.save(os.path.join(OUT_DIR, "04_debitor.png"))
    print("[OK] 04_debitor.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. Платёжный календарь
# ═══════════════════════════════════════════════════════════════════════════════
def render_payments():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), GRAY_BG)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 15), "Отчёт 1.5 — Платёжный календарь", fill=BLACK, font=FONT_TITLE)
    draw.text((20, 40), "Прогноз выплат на июнь 2026 | ГК «Открытие»", fill=GRAY_TEXT, font=FONT_NORMAL)
    
    headers = ["Дата", "Тип платежа", "Юрлицо", "Сумма", "Назначение"]
    col_w = [80, 150, 120, 100, 250]
    rows = [
        ["01.06", "Налоги", "Открытие", "450 000", "НДС + налог на прибыль"],
        ["05.06", "Аренда", "Открытие", "200 000", "Аренда офиса и склада"],
        ["10.06", "ФОТ", "Все", "1 500 000", "Зарплата за май"],
        ["15.06", "Кредит", "Открытие", "300 000", "Платеж по кредиту"],
        ["20.06", "Закуп товара", "Открытие", "800 000", "Оплата поставщикам"],
        ["25.06", "Лизинг", "Тюмень", "150 000", "Лизинговый платёж"],
        ["28.06", "Налоги", "Пермь", "120 000", "НДС"],
        ["", "", "", "", ""],
        ["ИТОГО", "", "", "3 520 000", ""],
    ]
    draw_table(draw, 20, 65, col_w, headers, rows)
    
    # Прогноз
    draw.text((20, 320), "Прогноз остатка ДС:", fill=BLACK, font=FONT_HEADER)
    draw.text((20, 345), "Текущий остаток: 4 000 000 руб.", fill=BLACK, font=FONT_NORMAL)
    draw.text((20, 365), "Прогноз на 2 недели: 2 800 000 руб.  🟢", fill=GREEN, font=FONT_NORMAL)
    draw.text((20, 385), "Прогноз на 4 недели: 480 000 руб.  🟡 (риск кассового разрыва)", fill=ORANGE, font=FONT_NORMAL)
    
    draw.text((20, 420), "Цветовая индикация: остаток < 0 — красный (кассовый разрыв)", fill=GRAY_TEXT, font=FONT_SMALL)
    
    img.save(os.path.join(OUT_DIR, "05_payments.png"))
    print("[OK] 05_payments.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. План-фактный анализ
# ═══════════════════════════════════════════════════════════════════════════════
def render_planfact():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), GRAY_BG)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 15), "Отчёт 1.6 — План-фактный анализ", fill=BLACK, font=FONT_TITLE)
    draw.text((20, 40), "Май 2026 | ГК «Открытие»", fill=GRAY_TEXT, font=FONT_NORMAL)
    
    headers = ["Показатель", "План", "Факт", "Отклонение", "Откл. %", "Причина"]
    col_w = [180, 100, 100, 100, 70, 150]
    rows = [
        ["Выручка", "3 200 000", "3 500 000", "+300 000", "🟢 +9.4%", "Рост продаж в Тюмени"],
        ["Валовая маржа", "35%", "35.3%", "+0.3%", "🟢 +0.9%", "—"],
        ["EBITDA", "600 000", "675 000", "+75 000", "🟢 +12.5%", "Снижение коммерческих расходов"],
        ["Расходы на логистику", "400 000", "450 000", "-50 000", "🔴 -12.5%", "Рост цен на топливо"],
        ["Коммерческие расходы", "350 000", "320 000", "+30 000", "🟢 +8.6%", "Экономия на маркетинге"],
        ["Чистая прибыль", "380 000", "435 000", "+55 000", "🟢 +14.5%", "—"],
    ]
    draw_table(draw, 20, 65, col_w, headers, rows)
    
    draw.text((20, 320), "Правила:", fill=BLACK, font=FONT_HEADER)
    draw.text((20, 345), "• Отклонение > 10% — обязательный разбор с руководителем подразделения", fill=BLACK, font=FONT_NORMAL)
    draw.text((20, 365), "• Поле «Причина отклонения» обязательно для заполнения при отклонении > 10%", fill=BLACK, font=FONT_NORMAL)
    draw.text((20, 385), "• Прогноз выручки до конца месяца на основе run rate", fill=BLACK, font=FONT_NORMAL)
    draw.text((20, 410), "Цветовая индикация: 🟢 < 5%  🟡 5-10%  🔴 > 10%", fill=GRAY_TEXT, font=FONT_SMALL)
    
    img.save(os.path.join(OUT_DIR, "06_planfact.png"))
    print("[OK] 06_planfact.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. Сводный Dashboard
# ═══════════════════════════════════════════════════════════════════════════════
def render_dashboard():
    W, H = 900, 650
    img = Image.new("RGB", (W, H), GRAY_BG)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 15), "Отчёт 1.7 — Сводный Dashboard", fill=BLACK, font=FONT_TITLE)
    draw.text((20, 40), "ГК «Открытие» | Май 2026 | Обновление: ежедневно", fill=GRAY_TEXT, font=FONT_NORMAL)
    
    # Верхняя строка — KPI карточки
    cards = [
        ("Выручка (план/факт)", "3.5M / 3.2M", "green"),
        ("Валовая прибыль %", "35.3%", "green"),
        ("Чистая прибыль", "435 000", "green"),
        ("Остаток ДС", "4.0M", "green"),
        ("Cash Flow (нед.)", "+180 000", "green"),
        ("Средний чек", "12 500", "yellow"),
        ("Кол-во заказов", "280", "yellow"),
        ("Оборач. склада", "41 дн.", "yellow"),
    ]
    card_w = 100
    card_h = 55
    gap = 10
    start_x = 20
    for i, (title, val, ci) in enumerate(cards):
        x = start_x + i * (card_w + gap)
        draw_card(draw, x, 65, card_w, card_h, title, val, ci)
    
    # Средний блок — графики
    draw.text((20, 140), "Графики:", fill=BLACK, font=FONT_HEADER)
    
    # График 1: Выручка и прибыль
    draw.text((20, 165), "Выручка и прибыль", fill=GRAY_TEXT, font=FONT_SMALL)
    draw.rectangle([20, 180, 280, 280], fill=WHITE, outline=GRAY_LINE)
    chart_data = [2500, 2800, 3100, 2900, 3500, 3200]
    chart_colors = [BLUE, GREEN, BLUE, YELLOW, GREEN, BLUE]
    draw_bar_chart(draw, 25, 185, 250, 90, chart_data, chart_colors)
    draw.text((30, 270), "Янв  Фев  Мар  Апр  Май  Июн(план)", fill=GRAY_TEXT, font=FONT_SMALL)
    
    # График 2: Cash Flow
    draw.text((310, 165), "Cash Flow", fill=GRAY_TEXT, font=FONT_SMALL)
    draw.rectangle([310, 180, 570, 280], fill=WHITE, outline=GRAY_LINE)
    cf_data = [500, 650, 600, 700, 800, 750]
    cf_colors = [GREEN, GREEN, YELLOW, GREEN, GREEN, GREEN]
    draw_bar_chart(draw, 315, 185, 250, 90, cf_data, cf_colors)
    draw.text((325, 270), "Янв  Фев  Мар  Апр  Май  Июн(план)", fill=GRAY_TEXT, font=FONT_SMALL)
    
    # График 3: Unit-экономика
    draw.text((600, 165), "Unit-экономика", fill=GRAY_TEXT, font=FONT_SMALL)
    draw.rectangle([600, 180, 860, 280], fill=WHITE, outline=GRAY_LINE)
    ue_data = [3500, 2265, 450, 320]
    ue_colors = [BLUE, RED, ORANGE, YELLOW]
    draw_bar_chart(draw, 605, 185, 250, 90, ue_data, ue_colors)
    draw.text((610, 270), "Выр.  Себ.  Лог.  Марк.", fill=GRAY_TEXT, font=FONT_SMALL)
    
    # Нижний блок — таблицы
    draw.text((20, 300), "Управленческие таблицы:", fill=BLACK, font=FONT_HEADER)
    
    # Таблица: Регионы
    headers = ["Регион", "Выручка", "Маржа", "Логистика", "Прибыль"]
    col_w = [100, 80, 80, 80, 80]
    rows = [
        ["Москва", "1 500 000", "40%", "150 000", "450 000"],
        ["Тюмень", "800 000", "37%", "120 000", "180 000"],
        ["Пермь", "600 000", "30%", "100 000", "90 000"],
        ["Екатеринбург", "400 000", "28%", "80 000", "30 000"],
    ]
    draw_table(draw, 20, 325, col_w, headers, rows)
    
    # Таблица: ABC-анализ
    headers2 = ["Категория", "Доля в выручке", "Доля в ассортименте"]
    col_w2 = [100, 120, 130]
    rows2 = [
        ["A (топ-20%)", "80%", "20%"],
        ["B (средние)", "15%", "30%"],
        ["C (остальные)", "5%", "50%"],
    ]
    draw_table(draw, 20, 445, col_w2, headers2, rows2)
    
    # Таблица: Логистика
    headers3 = ["Регион", "Стоимость доставки", "% опозданий"]
    col_w3 = [100, 130, 100]
    rows3 = [
        ["Москва", "150 000", "5%"],
        ["Тюмень", "120 000", "8%"],
        ["Пермь", "100 000", "12%"],
        ["Екатеринбург", "80 000", "15%"],
    ]
    draw_table(draw, 450, 325, col_w3, headers3, rows3)
    
    draw.text((20, 540), "Drill-down: клик на выручку → регионы → клиенты → заказы", fill=GRAY_TEXT, font=FONT_SMALL)
    draw.text((20, 560), "Прогноз выручки до конца месяца: 3 800 000 руб. | Прогноз Cash Flow на 2-4 нед.: 480 000 руб.", fill=GRAY_TEXT, font=FONT_SMALL)
    
    img.save(os.path.join(OUT_DIR, "07_dashboard.png"))
    print("[OK] 07_dashboard.png")


# ═══════════════════════════════════════════════════════════════════════════════
# Запуск
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Генерация макетов отчётов...")
    render_opiu()
    render_odds()
    render_balance()
    render_debitor()
    render_payments()
    render_planfact()
    render_dashboard()
    print(f"\nГотово! Файлы сохранены в: {OUT_DIR}")
