# -*- coding: utf-8 -*-
"""Генерация графиков для обзора AI-инструментов для ручных тестировщиков."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import ListedColormap
import numpy as np

os.makedirs("assets", exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": "#0F172A",
    "axes.edgecolor": "#CBD5E1",
    "axes.labelcolor": "#334155",
    "xtick.color": "#475569",
    "ytick.color": "#475569",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

L1, L2, L3, L4 = "#94A3B8", "#0EA5E9", "#6366F1", "#10B981"
LEVEL_COLORS = [L1, L2, L3, L4]

# ----------------------------------------------------------------------------
# 1. Лестница возможностей (4 уровня)
# ----------------------------------------------------------------------------
LEVELS = [
    ("УРОВЕНЬ 1 — ЧАТ", L1,
     ["Промпты и шаблоны", "Кастомные ассистенты", "Генерация текста"]),
    ("УРОВЕНЬ 2 — API", L2,
     ["Боты и скрипты", "Structured output (JSON)", "Импорт в TMS"]),
    ("УРОВЕНЬ 3 — АГЕНТ", L3,
     ["Цикл «шаг → проверка»", "Генерация E2E-тестов", "Self-healing"]),
    ("УРОВЕНЬ 4\nАГЕНТ + MCP", L4,
     ["Jira, браузер, БД, Figma", "Сквозные QA-сценарии", "Интеграции с системами"]),
]
CAPTIONS = ["без единой строчки кода", "пара скриптов / бот",
            "среда агента (IDE/CLI)", "+ MCP-серверы"]

fig, ax = plt.subplots(figsize=(13.4, 7), dpi=170)
W, H, DX, DY = 2.9, 2.35, 3.15, 1.45
for i, (title, color, bullets) in enumerate(LEVELS):
    x, y = i * DX, i * DY
    box = FancyBboxPatch((x, y), W, H,
                         boxstyle="round,pad=0.02,rounding_size=0.12",
                         linewidth=0, facecolor=color, alpha=0.93, zorder=3)
    ax.add_patch(box)
    multiline = "\n" in title
    if multiline:
        ax.text(x + W / 2, y + H - 0.14, title, ha="center", va="top",
                fontsize=12, fontweight="bold", color="white",
                linespacing=1.25, zorder=4)
        b0 = 1.02
    else:
        ax.text(x + W / 2, y + H - 0.30, title, ha="center", va="center",
                fontsize=12, fontweight="bold", color="white", zorder=4)
        b0 = 0.80
    for j, b in enumerate(bullets):
        ax.text(x + 0.17, y + H - b0 - j * 0.44, "• " + b, ha="left",
                va="center", fontsize=10, color="white", zorder=4)
    ax.text(x + W / 2, y - 0.26, CAPTIONS[i], ha="center", va="top",
            fontsize=10, color="#64748B", style="italic")
    if i < 3:
        ax.annotate("", xy=(x + DX - 0.06, y + DY + 0.35),
                    xytext=(x + W + 0.08, y + 0.35),
                    arrowprops=dict(arrowstyle="-|>", lw=2.4, color="#64748B"),
                    zorder=2)
ax.set_xlim(-0.4, 4 * DX + 0.45)
ax.set_ylim(-0.75, 3 * DY + H + 0.4)
ax.axis("off")
ax.set_title("Лестница возможностей: от чата к агенту с MCP",
             fontsize=17, fontweight="bold", pad=16)
plt.savefig("assets/01_levels.png", bbox_inches="tight")
plt.close(fig)

# ----------------------------------------------------------------------------
# 2. Тепловая карта: покрытие задач QA по уровням
# ----------------------------------------------------------------------------
tasks = [
    "Генерация тест-кейсов и чек-листов",
    "Тест-данные (массовая генерация)",
    "Баг-репорты из черновых заметок",
    "BDD / Gherkin сценарии",
    "API-тесты: генерация и прогон",
    "UI / E2E автотесты: генерация",
    "Self-healing автотестов",
    "Триаж падений в CI",
    "Обновление TMS / Jira прогонов",
    "Сверка реализации с макетом",
]
cols = ["Уровень 1\nЧат", "Уровень 2\nAPI", "Уровень 3\nАгент", "Уровень 4\nАгент + MCP"]
# 0 — не реально, 1 — вручную с LLM, 2 — полуавтомат, 3 — автоматизация
M = np.array([
    [2, 3, 3, 3],
    [2, 3, 3, 3],
    [2, 3, 3, 3],
    [2, 3, 3, 3],
    [1, 2, 3, 3],
    [1, 2, 3, 3],
    [0, 1, 3, 3],
    [1, 3, 3, 3],
    [0, 2, 2, 3],
    [1, 2, 2, 3],
])
cmap = ListedColormap(["#F1F5F9", "#E0F2FE", "#7DD3FC", "#34D399"])
fig, ax = plt.subplots(figsize=(12, 7), dpi=170)
ax.imshow(M, cmap=cmap, vmin=0, vmax=3, aspect="auto")
ax.set_xticks(range(4), cols, fontsize=11.5)
ax.set_yticks(range(len(tasks)), tasks, fontsize=11.5)
ax.set_xticks(np.arange(-0.5, 4, 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(tasks), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=2.5)
ax.tick_params(which="minor", length=0)
ax.tick_params(which="major", length=0)
SYM = {0: "—", 1: "±", 2: "◐", 3: "✓"}
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v = M[i, j]
        ax.text(j, i, SYM[v], ha="center", va="center", fontsize=14,
                color="#94A3B8" if v == 0 else ("#0F172A" if v == 3 else "#1E5A7A"),
                fontweight="bold" if v == 3 else "normal")
for s in ax.spines.values():
    s.set_visible(False)
fig.text(0.5, 0.015,
         "—  нереально          ±  вручную с помощью LLM          ◐  полуавтомат          ✓  автоматизация",
         ha="center", fontsize=11.5, color="#334155")
ax.set_title("Покрытие задач QA по уровням доступа к LLM",
             fontsize=16, fontweight="bold", pad=14)
plt.savefig("assets/02_heatmap.png", bbox_inches="tight")
plt.close(fig)

# ----------------------------------------------------------------------------
# 3. Усилия vs ценность
# ----------------------------------------------------------------------------
tools = [
    ("Библиотека промптов",      0.5, 4.0, 1, (0.2, 0.45)),
    ("QA-ассистент на портале",  1.0, 5.5, 1, (0.2, -0.6)),
    ("Бот: тикет → тест-кейсы",  3.0, 6.5, 2, (-0.25, -0.8)),
    ("Импорт тест-кейсов в TMS", 4.0, 7.0, 2, (-0.35, 0.42)),
    ("Триаж падений в CI",       4.5, 7.6, 2, (0.35, 0.35)),
    ("Генератор API-тестов",     6.0, 7.0, 2, (0.3, -0.65)),
    ("Агент: генерация E2E",     7.0, 8.5, 3, (-0.4, 0.4)),
    ("Self-healing агент",      10.0, 9.0, 3, (-0.4, 0.45)),
    ("Playwright MCP-сценарии",  3.0, 9.0, 4, (0.35, 0.3)),
    ("Jira MCP: баг-репорты",    6.5, 8.2, 4, (0.4, -0.4)),
    ("Свой MCP для TMS",        10.0, 7.5, 4, (-0.35, -0.75)),
]
cmap_lvl = {1: L1, 2: L2, 3: L3, 4: L4}
fig, ax = plt.subplots(figsize=(12.5, 7.5), dpi=170)
ax.axvline(5, color="#E2E8F0", lw=1.5, ls="--", zorder=1)
ax.axhline(7, color="#E2E8F0", lw=1.5, ls="--", zorder=1)
qstyle = dict(fontsize=11.5, color="#94A3B8", style="italic", zorder=1)
ax.text(0.4, 9.7, "Быстрые победы", **qstyle)
ax.text(11.2, 9.7, "Стратегические", ha="right", **qstyle)
ax.text(0.4, 3.2, "Разминка", **qstyle)
ax.text(11.2, 3.35, "Позже", ha="right", **qstyle)
for name, x, y, lvl, (dx, dy) in tools:
    ax.scatter(x, y, s=340, color=cmap_lvl[lvl], alpha=0.9, zorder=3,
               edgecolors="white", linewidths=1.8)
    ha = "left" if dx > 0 else "right"
    ax.annotate(name, (x, y), xytext=(x + dx, y + dy), fontsize=10.5,
                ha=ha, va="center", color="#1E293B", zorder=4)
handles = [plt.Line2D([], [], marker="o", ls="", markersize=12,
                      color=c, label=f"Уровень {i + 1}") for i, c in enumerate(LEVEL_COLORS)]
ax.legend(handles=handles, loc="lower right", frameon=True, fontsize=11,
          title="Уровень доступа", title_fontsize=11)
ax.set_xlim(-0.3, 11.5)
ax.set_ylim(3, 10.2)
ax.set_xlabel("Усилия на внедрение, чел.-дни (оценка)", fontsize=12)
ax.set_ylabel("Ценность для команды (экспертная оценка)", fontsize=12)
ax.set_title("Куда браться первым: усилия vs ценность",
             fontsize=16, fontweight="bold", pad=14)
ax.grid(True, color="#F1F5F9", lw=1)
ax.set_axisbelow(True)
plt.savefig("assets/03_effort_value.png", bbox_inches="tight")
plt.close(fig)

# ----------------------------------------------------------------------------
# 4. Дорожная карта на 12 недель
# ----------------------------------------------------------------------------
gantt = [
    ("Библиотека QA-промптов",      1, 2, 1),
    ("QA-ассистент на портале",     1, 2, 1),
    ("Бот «тикет → тест-кейсы»",    2, 4, 2),
    ("Импорт тест-кейсов в TMS",    3, 5, 2),
    ("Триаж падений в CI",          5, 7, 2),
    ("Пилот агента: генерация E2E", 6, 9, 3),
    ("Self-healing автотестов",     8, 10, 3),
    ("Playwright MCP-сценарии",     8, 10, 4),
    ("Jira / TMS MCP-интеграции",  10, 12, 4),
]
fig, ax = plt.subplots(figsize=(12.5, 6), dpi=170)
for i, (name, start, end, lvl) in enumerate(gantt):
    y = len(gantt) - 1 - i
    ax.barh(y, end - start + 1, left=start - 1, height=0.62,
            color=LEVEL_COLORS[lvl - 1], alpha=0.92, zorder=3)
    ax.text(start - 1 + (end - start + 1) / 2, y, f"{lvl}", ha="center",
            va="center", color="white", fontsize=10, fontweight="bold", zorder=4)
ax.set_yticks(range(len(gantt)), [t[0] for t in reversed(gantt)], fontsize=11.5)
ax.set_xticks(range(0, 13))
ax.set_xticklabels([str(w) for w in range(0, 13)], fontsize=10.5)
ax.set_xlim(0, 12)
ax.set_xlabel("Недели", fontsize=12)
ax.grid(axis="x", color="#E2E8F0", lw=1, zorder=0)
ax.set_axisbelow(True)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
handles = [plt.Line2D([], [], marker="s", ls="", markersize=12, color=c,
                      label=f"Уровень {i + 1}") for i, c in enumerate(LEVEL_COLORS)]
ax.legend(handles=handles, loc="upper right", frameon=True, fontsize=10.5,
          bbox_to_anchor=(1.0, 1.06), ncols=4)
ax.set_title("Дорожная карта внедрения на 12 недель (пример)",
             fontsize=16, fontweight="bold", pad=26)
plt.savefig("assets/04_roadmap.png", bbox_inches="tight")
plt.close(fig)

print("Готово:", sorted(os.listdir("assets")))
