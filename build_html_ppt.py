#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 11 月 MBR 的 5 页 HTML PPT。

用法:
    python build_html_ppt.py

输出:
    交付/11月MBR_HTML_PPT.html
"""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "交付"
OUT_FILE = OUT_DIR / "11月MBR_HTML_PPT.html"

# 调色板（经 dataviz validator 校验：蓝 / 橙 / 青三色全配对通过）
C_BLUE = "#2a78d6"
C_ORANGE = "#eb6834"
C_AQUA = "#1baf7a"
C_GRAY = "#898781"
C_INK = "#0b0b0b"
C_INK2 = "#52514e"
C_MUTED = "#898781"
C_GRID = "#e1e0d9"
C_SURFACE = "#fcfcfb"
C_GOOD = "#006300"
C_BAD = "#b3261e"

# ---------------------------------------------------------------------------
# 数据
# ---------------------------------------------------------------------------

MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05",
          "2026-06", "2026-07", "2026-08", "2026-09"]
MONTH_LABELS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月"]

FUNDO_11 = [0.728, 0.718, 0.768, 0.703, 0.725, 0.687, 0.728, 0.687, 0.772]
FUNDO_12 = [0.733, 0.740, 0.728, 0.718, 0.719, 0.696, 0.761, 0.698, 0.778]
FUNDO_DELTA = [0.005, 0.022, -0.040, 0.015, -0.006, 0.010, 0.034, 0.011, 0.005]

NEWCUST_SAMPLES = [3200, 2479, 2787, 4780, 4394, 3881, 4519, 4003, 3636]
NEWCUST_AUC = [0.666, 0.673, 0.629, 0.659, 0.582, 0.669, 0.649, 0.630, 0.698]

WEEKS = ["2026-08-31", "2026-09-07", "2026-09-14", "2026-09-21",
         "2026-09-28", "2026-10-05", "2026-10-12"]
WEEK_NEW = [0.647, 0.611, 0.620, 0.631, 0.635, 0.646, 0.637]
WEEK_OLD = [None, 0.674, 0.650, 0.624, 0.590, 0.631, 0.641]

PROFILE = [
    ("有工资入账的占比", 86.4, 74.0, "{:.1f}%"),
    ("工资中位数（月）", 4508, 3904, "${:,.0f}"),
    ("用过现金贷或工资预支", 68.5, 41.3, "{:.1f}%"),
    ("有未解决扣款失败", 57.7, 32.7, "{:.1f}%"),
    ("还完债后钱不够花", 89.9, 97.2, "{:.1f}%"),
]

# (指标, 新模型, 线上, Δ)
PBARS = [
    ("FPD15 · AUC", 0.785, 0.640, "+0.145"),
    ("FPD7 · AUC", 0.739, 0.636, "+0.103"),
    ("FPD15 · Gini", 0.569, 0.279, "+0.290"),
    ("FPD7 · Gini", 0.478, 0.272, "+0.206"),
    ("FPD15 · KS", 0.464, 0.218, "+0.246"),
    ("FPD7 · KS", 0.384, 0.202, "+0.182"),
]

CMP_ROWS = [
    ("AUC", "0.779", "0.747", "−0.031"),
    ("KS", "0.440", "0.377", "−0.063"),
    ("Top 10% 坏样捕获", "31.4%", "28.8%", "−2.5pp"),
    ("Top 20% 坏样捕获", "54.0%", "48.9%", "−5.1pp"),
    ("Top 30% 坏样捕获", "67.8%", "62.0%", "−5.8pp"),
    ("Brier（越低越好）", "0.0816", "0.0834", "+0.0018"),
]

LANES = [
    ("Fundo · 当期", C_BLUE, [2.5, 11.5, 14.0, 17.0, 19.5, 22.0]),
    ("Fundo · 逾期", C_BLUE, [1.0, 16.0, 21.5]),
    ("Wagego", C_ORANGE, [4.0, 14.0, 22.0]),
]

SIGNALS = [
    {
        "name": "未解决拒付 > 31.9%",
        "sub": "覆盖 5.0% · 坏率 26.6% · 2.6×",
        "x": 5.0, "y": 26.6, "color": C_ORANGE,
        "lx": 97, "ly": 26, "anchor": "start",
    },
    {
        "name": "预支 / 退款类信号",
        "sub": "覆盖 5–10% · 坏率 21.8–24.4%",
        "x": 7.5, "y": 23.1, "xr": (5.0, 10.0), "yr": (21.8, 24.4),
        "color": C_ORANGE, "lx": 149, "ly": 62, "anchor": "start",
    },
    {
        "name": "现金流吃紧",
        "sub": "覆盖 25–30% · 坏率 15.2–17.6%",
        "x": 27.5, "y": 16.4, "xr": (25.0, 30.0), "yr": (15.2, 17.6),
        "color": C_BLUE, "lx": 325, "ly": 102, "anchor": "middle",
    },
    {
        "name": "退款/提款比 ≤ 1.7%",
        "sub": "覆盖 41.1% · 坏率 4.9%",
        "x": 41.1, "y": 4.9, "color": C_AQUA,
        "lx": 478, "ly": 220, "anchor": "end",
    },
    {
        "name": "盈余 > $5,465",
        "sub": "覆盖 19.9% · 坏率 4.4%",
        "x": 19.9, "y": 4.4, "color": C_AQUA,
        "lx": 245, "ly": 226, "anchor": "middle",
    },
]


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------

def esc(value) -> str:
    return html.escape(str(value), quote=True)


def sgn(value: float, digits: int = 3) -> str:
    return f"{value:+.{digits}f}".replace("-", "−")


def mean(values) -> float:
    return sum(values) / len(values)


def svg_text(x, y, text, cls="tick", anchor="start") -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'class="{cls}">{esc(text)}</text>')


def tip(value) -> str:
    return f'data-tip="{esc(value)}"'


def legend(items) -> str:
    cells = []
    for color, label, kind in items:
        cls = "d" if kind == "dot" else ""
        cells.append(f'<span class="k"><i class="{cls}" style="background:{color}"></i>{label}</span>')
    return '<div class="legend">' + "".join(cells) + "</div>"


def card_head(title, side="") -> str:
    side_html = f'<div class="card-k">{side}</div>' if side else ""
    return f'<div class="card-h"><div class="card-t">{title}</div>{side_html}</div>'


def page_head(num, kicker, title, sub) -> str:
    return f'''<header class="s-head">
  <div class="kicker"><b>{num:02d}</b><span class="sep"></span><span>{kicker}</span></div>
  <h1>{title}</h1>
  <p class="sub">{sub}</p>
</header>'''


def page_foot(num) -> str:
    return (f'<footer class="s-foot"><span>11 月 MBR · 模型与策略</span>'
            f'<span class="pg">{num:02d} / 05</span></footer>')


# ---------------------------------------------------------------------------
# 图表
# ---------------------------------------------------------------------------

def fundo_chart() -> str:
    W, H = 528, 224
    ml, mr, mt, mb = 34, 40, 12, 24
    pw, ph = W - ml - mr, H - mt - mb
    ymin, ymax = 0.66, 0.80
    n = len(MONTHS)

    def px(i):
        return ml + pw * i / (n - 1)

    def py(v):
        return mt + (ymax - v) / (ymax - ymin) * ph

    parts = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Fundo 老客模型 1.1 与 1.2 月度 AUC 折线图">']
    for t in (0.68, 0.72, 0.76, 0.80):
        y = py(t)
        parts.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{W - mr}" y2="{y:.1f}" class="grid"/>')
        parts.append(svg_text(ml - 6, y + 3, f"{t:.2f}", "tick", "end"))
    parts.append(f'<line x1="{ml}" y1="{mt + ph}" x2="{W - mr}" y2="{mt + ph}" class="axis"/>')
    for i, label in enumerate(MONTH_LABELS):
        parts.append(svg_text(px(i), H - 6, label, "tick-x", "middle"))

    old_path = "M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(FUNDO_11))
    new_path = "M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(FUNDO_12))
    parts.append(f'<path d="{old_path}" fill="none" stroke="{C_GRAY}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    parts.append(f'<path d="{new_path}" fill="none" stroke="{C_BLUE}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')

    for i, v in enumerate(FUNDO_11):
        text = f"{MONTHS[i]} · 1.1 {v:.3f} · 1.2 {FUNDO_12[i]:.3f} · Δ {sgn(FUNDO_DELTA[i])}"
        parts.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="3.6" fill="{C_GRAY}" stroke="{C_SURFACE}" stroke-width="2" {tip(text)}/>')
    for i, v in enumerate(FUNDO_12):
        text = f"{MONTHS[i]} · 1.2 {v:.3f} · 1.1 {FUNDO_11[i]:.3f} · Δ {sgn(FUNDO_DELTA[i])}"
        parts.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="4" fill="{C_BLUE}" stroke="{C_SURFACE}" stroke-width="2" {tip(text)}/>')

    parts.append(svg_text(px(n - 1) + 8, py(FUNDO_12[-1]) + 3.5, "0.778", "endlabel"))
    parts.append("</svg>")
    return "".join(parts)


def newcust_spark() -> str:
    W, H = 224, 64
    ml, mr, mt, mb = 2, 30, 8, 6
    pw, ph = W - ml - mr, H - mt - mb
    lo = min(NEWCUST_AUC) - 0.008
    hi = max(NEWCUST_AUC) + 0.008
    n = len(NEWCUST_AUC)

    def px(i):
        return ml + pw * i / (n - 1)

    def py(v):
        return mt + (hi - v) / (hi - lo) * ph

    line = "M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(NEWCUST_AUC))
    area = f"{line} L{px(n - 1):.1f},{mt + ph} L{ml:.1f},{mt + ph} Z"
    parts = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="新客模型月度 AUC 迷你趋势">']
    parts.append(f'<path d="{area}" fill="{C_BLUE}" opacity="0.08"/>')
    parts.append(f'<path d="{line}" fill="none" stroke="{C_BLUE}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, v in enumerate(NEWCUST_AUC):
        parts.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="3" fill="{C_BLUE}" stroke="{C_SURFACE}" stroke-width="1.5" {tip(f"{MONTHS[i]} · AUC {v:.3f} · 样本 {NEWCUST_SAMPLES[i]:,}")}/>')
    parts.append(f'<circle cx="{px(n - 1):.1f}" cy="{py(NEWCUST_AUC[-1]):.1f}" r="4" fill="{C_BLUE}" stroke="{C_SURFACE}" stroke-width="2"/>')
    parts.append(svg_text(W - 2, py(NEWCUST_AUC[-1]) + 3, "0.698", "endlabel", "end"))
    parts.append("</svg>")
    return "".join(parts)


def weekly_chart() -> str:
    W, H = 276, 194
    ml, mr, mt, mb = 28, 10, 10, 24
    pw, ph = W - ml - mr, H - mt - mb
    ymin, ymax = 0.57, 0.69
    n = len(WEEKS)

    def px(i):
        return ml + pw * i / (n - 1)

    def py(v):
        return mt + (ymax - v) / (ymax - ymin) * ph

    parts = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Wagego 新老客周度 AUC 折线图">']
    for t in (0.58, 0.62, 0.66):
        y = py(t)
        parts.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{W - mr}" y2="{y:.1f}" class="grid"/>')
        parts.append(svg_text(ml - 5, y + 3, f"{t:.2f}", "tick", "end"))
    parts.append(f'<line x1="{ml}" y1="{mt + ph}" x2="{W - mr}" y2="{mt + ph}" class="axis"/>')
    for i, w in enumerate(WEEKS):
        parts.append(svg_text(px(i), H - 7, w[5:].replace("-", "/"), "tick-x", "middle"))

    old_points = [(px(i), py(v)) for i, v in enumerate(WEEK_OLD) if v is not None]
    old_path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in old_points)
    new_path = "M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(WEEK_NEW))
    parts.append(f'<path d="{old_path}" fill="none" stroke="{C_ORANGE}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    parts.append(f'<path d="{new_path}" fill="none" stroke="{C_BLUE}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')

    for i, v in enumerate(WEEK_OLD):
        if v is None:
            continue
        t = f"{WEEKS[i]} · 老客 {v:.3f} · 新客 {WEEK_NEW[i]:.3f}"
        parts.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="3.6" fill="{C_ORANGE}" stroke="{C_SURFACE}" stroke-width="2" {tip(t)}/>')
    for i, v in enumerate(WEEK_NEW):
        t = f"{WEEKS[i]} · 新客 {v:.3f} · 老客 " + ("—" if WEEK_OLD[i] is None else f"{WEEK_OLD[i]:.3f}")
        parts.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="3.8" fill="{C_BLUE}" stroke="{C_SURFACE}" stroke-width="2" {tip(t)}/>')
    parts.append("</svg>")
    return "".join(parts)


def signal_scatter() -> str:
    W, H = 528, 330
    ml, mr, mt, mb = 34, 16, 16, 36
    pw, ph = W - ml - mr, H - mt - mb
    xmax, ymax = 45.0, 30.0

    def px(v):
        return ml + v / xmax * pw

    def py(v):
        return mt + (ymax - v) / ymax * ph

    parts = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="风险信号：覆盖客户占比与坏率散点图">']
    for t in (0, 10, 20, 30):
        y = py(t)
        parts.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{W - mr}" y2="{y:.1f}" class="grid"/>')
        parts.append(svg_text(ml - 6, y + 3, f"{t}%", "tick", "end"))
    for t in (0, 10, 20, 30, 40):
        parts.append(svg_text(px(t), H - 18, f"{t}%", "tick-x", "middle"))
    parts.append(f'<line x1="{ml}" y1="{mt + ph}" x2="{W - mr}" y2="{mt + ph}" class="axis"/>')
    parts.append(svg_text(W / 2, H - 4, "覆盖客户占比 →", "tick-x", "middle"))

    ref_y = py(10.2)
    parts.append(f'<line x1="{ml}" y1="{ref_y:.1f}" x2="{W - mr}" y2="{ref_y:.1f}" class="ref"/>')
    parts.append(svg_text(W - mr, ref_y - 4, "整体坏率 ≈ 10%", "anno", "end"))

    for s in SIGNALS:
        color = s["color"]
        cx, cy = px(s["x"]), py(s["y"])
        if "xr" in s:
            x0, x1 = px(s["xr"][0]), px(s["xr"][1])
            y0, y1 = py(s["yr"][0]), py(s["yr"][1])
            parts.append(f'<line x1="{x0:.1f}" y1="{cy:.1f}" x2="{x1:.1f}" y2="{cy:.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round" opacity="0.45"/>')
            parts.append(f'<line x1="{cx:.1f}" y1="{y0:.1f}" x2="{cx:.1f}" y2="{y1:.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round" opacity="0.45"/>')
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.2" fill="{color}" stroke="{C_SURFACE}" stroke-width="2" {tip(s["name"] + " · " + s["sub"])}/>')
        parts.append(svg_text(s["lx"], s["ly"], s["name"], "label", s["anchor"]))
        parts.append(svg_text(s["lx"], s["ly"] + 12, s["sub"], "sublabel", s["anchor"]))
    parts.append("</svg>")
    return "".join(parts)


def weekly_range() -> str:
    W, H = 528, 82
    ml, mr, mt, mb = 54, 98, 8, 20
    pw = W - ml - mr
    lo, hi = 0.58, 0.68

    def px(v):
        return ml + (v - lo) / (hi - lo) * pw

    axis_y = H - mb
    lanes = [
        ("新客", WEEK_NEW, C_BLUE, 24),
        ("老客", [v for v in WEEK_OLD if v is not None], C_ORANGE, 46),
    ]
    parts = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="新老客周度 AUC 区间">']
    for t in (0.58, 0.60, 0.62, 0.64, 0.66, 0.68):
        x = px(t)
        parts.append(f'<line x1="{x:.1f}" y1="{mt}" x2="{x:.1f}" y2="{axis_y}" class="grid"/>')
        parts.append(svg_text(x, H - 5, f"{t:.2f}", "tick-x", "middle"))
    parts.append(f'<line x1="{ml}" y1="{axis_y}" x2="{W - mr}" y2="{axis_y}" class="axis"/>')
    ref_x = px(0.63)
    parts.append(f'<line x1="{ref_x:.1f}" y1="{mt}" x2="{ref_x:.1f}" y2="{axis_y}" class="ref"/>')
    parts.append(svg_text(ref_x + 3, mt + 6, "0.63", "anno", "start"))

    for name, values, color, y in lanes:
        lo_v, hi_v = min(values), max(values)
        avg = mean(values)
        parts.append(f'<circle cx="{ml - 54}" cy="{y}" r="3" fill="{color}"/>')
        parts.append(svg_text(ml - 46, y + 3, name, "tick", "start"))
        parts.append(f'<line x1="{px(lo_v):.1f}" y1="{y}" x2="{px(hi_v):.1f}" y2="{y}" stroke="{color}" stroke-width="3.5" stroke-linecap="round" opacity="0.35"/>')
        parts.append(f'<circle cx="{px(avg):.1f}" cy="{y}" r="4.4" fill="{color}" stroke="{C_SURFACE}" stroke-width="2" '
                     f'{tip(f"{name} · 7 周区间 {lo_v:.3f}–{hi_v:.3f} · 均值 {avg:.3f}")}/>')
        parts.append(svg_text(W - 2, y - 1, f"{avg:.3f}", "endlabel", "end"))
        parts.append(svg_text(W - 2, y + 9, f"{lo_v:.3f}–{hi_v:.3f}", "anno", "end"))
    parts.append("</svg>")
    return "".join(parts)


def timeline_chart() -> str:
    W, H = 528, 215
    ml, mr, mt, mb = 122, 12, 14, 24
    pw, ph = W - ml - mr, H - mt - mb
    axis_y = H - 30
    lane_ys = [mt + 20, mt + 70, mt + 120]

    def px(hour):
        return ml + hour / 24 * pw

    parts = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Fundo 与 Wagego 代扣时点分布">']
    for hour in range(0, 25, 4):
        x = px(hour)
        parts.append(f'<line x1="{x:.1f}" y1="{mt}" x2="{x:.1f}" y2="{axis_y}" class="grid"/>')
        label = "24" if hour == 24 else f"{hour:02d}"
        parts.append(svg_text(x, H - 6, label, "tick-x", "middle"))
    parts.append(f'<line x1="{ml}" y1="{axis_y}" x2="{W - mr}" y2="{axis_y}" class="axis"/>')

    for (name, color, hours), y in zip(LANES, lane_ys):
        parts.append(f'<line x1="{ml - 64}" y1="{y - 6}" x2="{ml - 64}" y2="{y + 6}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')
        parts.append(svg_text(ml - 56, y + 3, name, "tick", "start"))
        for hour in hours:
            hh = int(hour)
            mm = int(round((hour - hh) * 60))
            parts.append(f'<circle cx="{px(hour):.1f}" cy="{y}" r="4.2" fill="{color}" stroke="{C_SURFACE}" stroke-width="2" {tip(f"{name} · 悉尼时间 {hh:02d}:{mm:02d}")}/>')
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# 页面片段
# ---------------------------------------------------------------------------

def weekly_table() -> str:
    rows = []
    for i, week in enumerate(WEEKS):
        old = "—" if WEEK_OLD[i] is None else f"{WEEK_OLD[i]:.3f}"
        cls = ' class="mark"' if i == 4 else ""
        rows.append(f'<tr{cls}><td>{week[5:].replace("-", "/")}</td><td>{WEEK_NEW[i]:.3f}</td><td>{old}</td></tr>')
    return ('<table class="tbl weekly"><thead><tr><th>放款周</th><th>新客 AUC</th><th>老客 AUC</th></tr></thead>'
            "<tbody>" + "".join(rows) + "</tbody></table>")


def pbar_rows() -> str:
    rows = []
    for label, new, old, delta in PBARS:
        rows.append(f'''<div class="pbr">
  <div class="pl">{label}</div>
  <div class="pbt">
    <i class="new" style="width:{new * 100:.1f}%" {tip(f"{label} · 新模型 {new:.3f}")}></i>
    <i class="old" style="width:{old * 100:.1f}%" {tip(f"{label} · 线上 {old:.3f}")}></i>
  </div>
  <div class="pbv"><b>{new:.3f}</b><span>{old:.3f}</span></div>
  <div class="pbd up">{delta}</div>
</div>''')
    return "".join(rows)


def profile_rows() -> str:
    rows = []
    for label, wagego, fundo, fmt in PROFILE:
        top = max(wagego, fundo)
        wg = wagego / top * 100
        fd = fundo / top * 100
        rows.append(f'''<div class="prow">
  <div class="plab">{label}</div>
  <div class="pcell"><span class="val">{fmt.format(wagego)}</span><span class="bar"><i style="width:{wg:.1f}%;background:{C_BLUE}"></i></span></div>
  <div class="pcell"><span class="val">{fmt.format(fundo)}</span><span class="bar"><i style="width:{fd:.1f}%;background:{C_ORANGE}"></i></span></div>
</div>''')
    return "".join(rows)


def cmp_table() -> str:
    rows = []
    for name, illion, bscat, delta in CMP_ROWS:
        rows.append(f'<tr><td>{name}</td><td>{illion}</td><td>{bscat}</td><td class="neg">{delta}</td></tr>')
    return ('<table class="tbl cmp"><thead><tr><th>指标</th><th>Illion 分类</th><th>BSCAT 分类</th><th>差异</th></tr></thead>'
            "<tbody>" + "".join(rows) + "</tbody></table>")


# ---------------------------------------------------------------------------
# 五页
# ---------------------------------------------------------------------------

def slide1() -> str:
    return f'''<section class="slide" id="p1" aria-label="第 1 页：模型监控">
{page_head(1, "模型监控 · Fundo / Wagego",
           "模型运行稳定：老客已切换 1.2，Wagego 新客 1.0 即将上线",
           "Fundo 老客 9 月底切换 mltmodel_1.2；新客模型月度 AUC 0.58–0.70；Wagego 线上模型周度 AUC 稳定在 0.63 附近")}
<div class="s-body grid2">
  <div class="col">
    <div class="slab"><i style="background:{C_BLUE}"></i>Fundo · 老客风险主模型</div>
    <div class="card">
      {card_head("1M30 月度 AUC：mltmodel 1.1 vs 1.2",
                 "1.2 自 2025-09 起 OOT<br>模型 Y 标签：3M30+")}
      {legend([(C_BLUE, "mltmodel 1.2", "line"), (C_GRAY, "mltmodel 1.1", "line")])}
      {fundo_chart()}
      <div class="strip">
        <div><span class="ss-l">9 月 AUC</span><span class="ss-v">0.778</span><span class="ss-s up">+0.005</span></div>
        <div><span class="ss-l">1.2 领先月份</span><span class="ss-v">7 / 9</span><span class="ss-s">仅 3 / 5 月落后</span></div>
        <div><span class="ss-l">月均 AUC</span><span class="ss-v">0.730</span><span class="ss-s">1.1 为 0.724</span></div>
      </div>
      <div class="card-note">Y 轴截断 0.66–0.80。3 月 1.2 低于 1.1（−0.040），其余月份多数领先；9 月 0.778 为年内最高。</div>
    </div>
    <div class="card mini">
      <div class="mtext">
        <div class="mhead">新客风险主模型 · 3rdmodel v1.0</div>
        <div class="msub">1M30 月度 AUC · 9 月已表现样本 3,636</div>
        <div class="mstats">
          <div class="mstat"><b>0.698</b><span>9 月 AUC</span></div>
          <div class="mstat"><b>0.582–0.698</b><span>年内区间</span></div>
          <div class="mstat"><b>0.651</b><span>月均</span></div>
        </div>
      </div>
      <div class="spark">{newcust_spark()}</div>
    </div>
  </div>
  <div class="col">
    <div class="slab"><i style="background:{C_ORANGE}"></i>Wagego · 线上模型（新老客共用）</div>
    <div class="card">
      {card_head("FPD15 · 周度 AUC", "仅统计已成熟样本")}
      {legend([(C_BLUE, "新客", "line"), (C_ORANGE, "老客", "line")])}
      <div class="weekly-grid">
        {weekly_table()}
        {weekly_chart()}
      </div>
      <div class="card-note">新客区间 <b>0.611–0.647</b>，老客 <b>0.590–0.674</b>；9/28 周老客 0.590 为本段低点，10/12 已回升至 0.641。</div>
    </div>
    <div class="card judge">
      <div class="big">0.63<small>周度 AUC 中枢</small></div>
      <div class="jtext">7 周内新客均值 <b>0.632</b>、老客 <b>0.635</b>；<br>波动集中在单周，<b>未出现持续漂移</b>。</div>
    </div>
    <div class="card">
      {card_head("7 周区间：新客 / 老客", "点为 7 周均值")}
      {weekly_range()}
    </div>
  </div>
</div>
{page_foot(1)}
</section>'''


def slide2() -> str:
    return f'''<section class="slide" id="p2" aria-label="第 2 页：Wagego 新客 1.0 上线预告">
{page_head(2, "上线预告 · Wagego 新客 1.0",
           "Wagego 新客 1.0：OOT 后 FPD15 AUC 0.785，较线上 +0.145",
           "同一批 OOT 成熟样本上，AUC / Gini / KS 全面抬升；业务侧体现为降损、增长、提效与少误拒")}
<div class="s-body">
  <div class="kpis">
    <div class="kpi"><div class="kpi-l">FPD15 · OOT AUC</div><div class="kpi-v">0.785<span class="d good">+0.145</span></div><div class="kpi-f">线上 0.640 · 成熟 4,000 笔 · 95% CI +0.114 ~ +0.176</div></div>
    <div class="kpi"><div class="kpi-l">FPD7 · OOT AUC</div><div class="kpi-v">0.739<span class="d good">+0.103</span></div><div class="kpi-f">线上 0.636 · 成熟 6,349 笔 · 95% CI +0.082 ~ +0.124</div></div>
    <div class="kpi"><div class="kpi-l">Gini · FPD15</div><div class="kpi-v">0.569<span class="d good">+0.290</span></div><div class="kpi-f">线上 0.279 · Gini = 2×AUC−1</div></div>
    <div class="kpi"><div class="kpi-l">KS · FPD15</div><div class="kpi-v">0.464<span class="d good">+0.246</span></div><div class="kpi-f">线上 0.218 · 排序与拦截能力同步提升</div></div>
  </div>
  <div class="main2">
    <div class="col">
      <div class="slab"><i style="background:{C_BLUE}"></i>业务价值 · 同样的风险标准，更好的结果</div>
      <div class="values">
        <div class="vrow">
          <div class="vtag">降损</div>
          <div class="vbody">
            <div class="vh">通过人群坏率 <span class="from">6.86%</span><span class="arrow">→</span><span class="to">4.43%</span></div>
            <div class="vn">拒绝风险最高 30% 时，每 100 名通过客户少引入 2.4 名坏客户。</div>
          </div>
          <div class="vs"><b>−2.4</b><span>名坏客户 / 百人</span></div>
        </div>
        <div class="vrow">
          <div class="vtag">增长</div>
          <div class="vbody">
            <div class="vh">坏率 ≤8% 时通过率 <span class="from">72.7%</span><span class="arrow">→</span><span class="to">91.7%</span></div>
            <div class="vn">每 100 名申请人多放 19 人，合计多放 175,400 元好客户本金；预算 ≤4% 时 13.1% → 64.6%。</div>
          </div>
          <div class="vs"><b>+19</b><span>人 / 百名申请人</span></div>
        </div>
        <div class="vrow">
          <div class="vtag">提效</div>
          <div class="vbody">
            <div class="vh">第 10 档坏率 <span class="from">27.57%</span><span class="arrow">→</span><span class="to">31.02%</span></div>
            <div class="vn">第 10 档只放 7.8% 本金，却贡献 26.5% 未还本金；第 8–10 档合计 24.4% / 59.1%。</div>
          </div>
          <div class="vs"><b>26.5%</b><span>未还本金来自 D10</span></div>
        </div>
        <div class="vrow">
          <div class="vtag">少误拒</div>
          <div class="vbody">
            <div class="vh">拒绝名单坏率：线上 <span class="from">19.51%</span><span class="arrow">vs</span>新模型 <span class="to">7.02%</span></div>
            <div class="vn">同样 30% 拒绝率，各拒 1,553 人；新模型多拦 194 名坏客户（303 vs 109），同时换回 194 名好客户。</div>
          </div>
          <div class="vs"><b>+194</b><span>好客户被捞回</span></div>
        </div>
      </div>
      <div class="statement"><span class="st-k">一句话</span>同样的风险标准下，新模型<b>少放坏人、多做生意</b>；风险分层更陡，拒绝、额度与催收资源也能更聚焦。</div>
    </div>
    <div class="col">
      <div class="slab"><i style="background:{C_BLUE}"></i>OOT 指标 · 新模型 vs 线上</div>
      <div class="card evid">
        {card_head("区分度与排序能力", "数值越高越好")}
        {legend([(C_BLUE, "新模型", "line"), (C_ORANGE, "线上", "line")])}
        <div class="pbar">{pbar_rows()}</div>
        <div class="lift"><b>最高档 lift（全样本）：</b>FPD15 3.09× vs 2.75×，FPD7 2.70× vs 2.50×。ΔAUC 括号内为 95% 置信区间。</div>
      </div>
    </div>
  </div>
</div>
{page_foot(2)}
</section>'''


def slide3() -> str:
    return f'''<section class="slide" id="p3" aria-label="第 3 页：人群画像">
{page_head(3, "人群画像 · Wagego / Fundo",
           "人群画像：有工资，但现金流薄",
           "Wagego 不是更穷，而是负债更重；两者的共同点是还完债后钱不够花")}
<div class="s-body grid2">
  <div class="col">
    <div class="slab"><i style="background:{C_BLUE}"></i>谁更愿意来 Wagego</div>
    <div class="card profilecard">
      {card_head("五个关键差异", "条形按每行较大值归一")}
      <div class="profile">
        <div class="phead"><span>指标</span><span class="lg"><i style="background:{C_BLUE}"></i>Wagego</span><span class="lg"><i style="background:{C_ORANGE}"></i>Fundo</span></div>
        {profile_rows()}
      </div>
    </div>
    <div class="statrow">
      <div><b>86.4%</b><span>Wagego 有工资入账</span></div>
      <div><b>68.5%</b><span>用过现金贷或工资预支</span></div>
      <div><b>89.9%</b><span>还完债后钱不够花</span></div>
    </div>
    <div class="callout">
      <b>收入更高，负债更重。</b>Wagego 有工资入账比例高 12.4pp、工资中位数高 $604；但预支使用率高 27.2pp、扣款失败率高 25.0pp。Fundo 还完债后不够花的比例更高（97.2%）。<br><b>共同点：</b>绝大多数客户现金流都很薄。
    </div>
  </div>
  <div class="col">
    <div class="slab"><i style="background:{C_ORANGE}"></i>谁更高风险 · 信号覆盖面 vs 坏率</div>
    <div class="card">
      {card_head("拒付、退款与现金流信号", "横轴：覆盖客户占比 · 纵轴：坏率")}
      {legend([(C_ORANGE, "高风险信号", "dot"), (C_BLUE, "现金流吃紧", "dot"), (C_AQUA, "好客户信号", "dot")])}
      {signal_scatter()}
      <div class="card-note">单变量口径，人群有重叠；线段表示覆盖占比与坏率的范围。</div>
    </div>
    <div class="takeaway">
      <span><b>小而集中</b> 拒付/退款类信号覆盖 5–10%，坏率是整体 2 倍以上 → 优先打击。</span>
      <span><b>面广而弱</b> 现金流吃紧覆盖约三成，坏率 15–18% → 常态经营。</span>
      <span><b>好客户</b> 流水干净、有盈余，坏率不到 5% → 清楚画像。</span>
    </div>
  </div>
</div>
{page_foot(3)}
</section>'''


def slide4() -> str:
    return f'''<section class="slide" id="p4" aria-label="第 4 页：Q4 规划 代扣时间点模型">
{page_head(4, "Q4 规划 ① · 代扣策略",
           "代扣最优时间点预测模型：把扣款对准钱到账的那一刻",
           "现状成功率 Fundo 12%、Wagego 17%；下一步用收入时间戳 + 多头应还日提升命中率")}
<div class="s-body">
  <div class="toprow">
    <div class="card">
      {card_head("当前代扣调用时点（悉尼时间）", "每条线为一个代扣窗口")}
      {timeline_chart()}
      <div class="sched">
        <div><span class="dot" style="background:{C_BLUE}"></span><b>Fundo · 当期</b>02:30 · 11:30 · 14:00 · 17:00 · 19:30 · 22:00</div>
        <div><span class="dot" style="background:{C_BLUE};opacity:.55"></span><b>Fundo · 逾期</b>01:00 · 16:00 · 21:30</div>
        <div><span class="dot" style="background:{C_ORANGE}"></span><b>Wagego</b>04:00 · 14:00 · 22:00</div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        {card_head("总体成功率（成功次数 / 调用次数）")}
        <div class="meters">
          <div class="mrow">
            <div class="mlab">Fundo</div>
            <div class="mtrack"><i style="width:12%"></i></div>
            <div class="mval">12%</div>
          </div>
          <div class="mfoot">每 100 次调用仅 12 次扣到，88 次未扣到。</div>
          <div class="mrow">
            <div class="mlab">Wagego</div>
            <div class="mtrack orange"><i style="width:17%"></i></div>
            <div class="mval">17%</div>
          </div>
          <div class="mfoot">每 100 次调用仅 17 次扣到，83 次未扣到。</div>
        </div>
      </div>
      <div class="goal"><b>目标</b>把扣款对准发薪日、先于竞对，抬升当前 12% / 17% 的调用命中率。</div>
      <div class="card focus">
        <div class="focus-t">提升成功率的关键</div>
        <p>在对的时间、向对的人、<b>先于竞对</b>发起扣款。<br>这需要「收入到账时间」和「多头应还日」两张时刻表。</p>
      </div>
    </div>
  </div>
  <div class="card planwide">
    {card_head("技术方案：精准定位收入时点与多头应还日", "Fiskil 时间戳 + BSCAT 分类与还款计划表")}
    <div class="flow">
      <div class="node"><b>收入到账时点</b><span>Fiskil 时间戳</span></div>
      <span class="op">+</span>
      <div class="node"><b>多头应还日</b><span>BSCAT 还款计划表</span></div>
      <span class="op">→</span>
      <div class="node accent"><b>更优代扣时点</b><span>先于竞对扣款</span></div>
    </div>
    <div class="quad">
      <div class="q"><div class="q-tag">现状瓶颈 01</div><div class="q-t">收入与频率识别精度有空间</div><div class="q-n">部分用户存在多份收入或人工收入，当前模型难以准确识别。</div></div>
      <div class="q"><div class="q-tag">现状瓶颈 02</div><div class="q-t">缺乏时间戳</div><div class="q-n">目前仅能判断到日级别；现有数据供应商均无法提供时间戳。</div></div>
      <div class="q blue"><div class="q-tag">BSCAT 能力 01</div><div class="q-t">更精细的收入识别</div><div class="q-n">支持主收入、奖金、零工收入、政府补助等多类型分类。</div></div>
      <div class="q blue"><div class="q-tag">BSCAT 能力 02</div><div class="q-t">多头还款计划表抽取</div><div class="q-n">识别每笔贷款的还款日、状态与频率，在发薪日基础上优化时点；扣款先于竞对。</div></div>
    </div>
    <div class="plan-note"><b>Fiskil Open Banking</b> 是目前唯一可提供时间戳的供应商；该判断与第 5 页的接入评估联动。</div>
  </div>
</div>
{page_foot(4)}
</section>'''


def slide5() -> str:
    return f'''<section class="slide" id="p5" aria-label="第 5 页：Q4 规划 Fiskil 可行性">
{page_head(5, "Q4 规划 ② · 数据成本",
           "Fiskil Open Banking 接入：分类切换 BSCAT，区分度损失有限",
           "调用单价较 Illion 低 2–3 倍；两套评分高度一致，每 100 名坏客户仅少拦截 6 名")}
<div class="s-body spread">
  <div class="top2">
    <div class="col">
      <div class="slab"><i style="background:{C_ORANGE}"></i>为什么是现在</div>
      <div class="tiles">
        <div class="tile"><div class="tile-l">成本</div><div class="tile-v">2–3×</div><div class="tile-n">调用单价低于 Illion，是降低数据成本的核心驱动。</div></div>
        <div class="tile"><div class="tile-l">供给</div><div class="tile-v sm">稀缺</div><div class="tile-n">分类算法可选供应商有限，算法本身价值高、价格昂贵。</div></div>
        <div class="tile"><div class="tile-l">需求</div><div class="tile-v sm">上升</div><div class="tile-n">贷中查询成本已高；开展 refinance 后银行流水查询将进一步增加。</div></div>
        <div class="tile"><div class="tile-l">窗口</div><div class="tile-v sm">关闭</div><div class="tile-n">Illion 已停止 lender 多分类优化服务，且无法提供时间戳。</div></div>
      </div>
      <div class="adapt"><b>适配性：</b>现有 Fiskil 字段已满足 BSCAT 入参要求；等待批量数据接入落库后，回溯历史分类并评估全量效果。</div>
    </div>
    <div class="col">
      <div class="slab"><i style="background:{C_BLUE}"></i>可行性 · 区分度评估</div>
      <div class="card">
        {card_head("同一批 9,503 名客户", "坏样本 950 · FPD15 整体坏率 10.0%")}
        {cmp_table()}
        <div class="card-note">BSCAT：AUC 0.747、KS 0.377、Gini 0.495、PR-AUC 0.241；拒绝最高分 30% 仍可捕获 62.0% 坏客户。</div>
      </div>
    </div>
  </div>
  <div class="cstat">
    <div><b>0.914</b><span>两套评分 Pearson 相关</span></div>
    <div><b>50.8%</b><span>客户落在同一分位</span></div>
    <div><b>82.3%</b><span>分位相差 ≤ 1 档</span></div>
    <div><b>1.81pp</b><span>分位坏率最大绝对差（D6）</span></div>
  </div>
  <div class="pstats">
    <div><b>7.5<span>对 / 10 对</span></b><p>每 10 对好坏客户正确排序；Illion 为 7.8 对。</p></div>
    <div><b>62<span>名 / 100 名</span></b><p>每 100 名坏客户被拦截；Illion 68 名，仅少 6 名。</p></div>
    <div><b>2.98<span>× lift</span></b><p>D10 坏率 29.8%；Illion 31.0%（3.10×）。</p></div>
  </div>
  <div class="conclusion"><b>结论</b>　两套评分高度一致，BSCAT 区分度略有下降但仍具备有效的风险区分能力；在 Wagego 上将分类来源切换至 BSCAT，可在有限损失下实现数据成本下降。</div>
</div>
{page_foot(5)}
</section>'''


# ---------------------------------------------------------------------------
# 样式 / 脚本
# ---------------------------------------------------------------------------

CSS = r"""
:root{
  --page:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,.10);
  --blue:#2a78d6; --blue-soft:#cde2fb; --orange:#eb6834; --orange-soft:rgba(235,104,52,.16);
  --aqua:#1baf7a; --good:#006300; --bad:#b3261e;
  --shadow:0 1px 2px rgba(11,11,11,.04), 0 8px 22px rgba(11,11,11,.045);
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; overflow:hidden; background:#141514; color:var(--ink);
  font-family:system-ui,-apple-system,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  font-size:12.5px; line-height:1.5; -webkit-font-smoothing:antialiased;
}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
.deck{position:fixed;inset:0}
.stage{
  position:absolute; left:50%; top:50%; width:1280px; height:720px;
  transform-origin:center center; background:var(--page); border-radius:10px;
  overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,.45);
}
.slide{
  position:absolute; inset:0; display:none; flex-direction:column;
  padding:42px 54px 34px; background:var(--page); overflow:hidden;
}
.slide.active{display:flex; animation:enter .34s cubic-bezier(.2,.7,.25,1)}
@keyframes enter{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}
.progress{position:absolute;left:0;top:0;height:2px;width:100%;z-index:20;pointer-events:none}
.progress i{display:block;height:100%;width:20%;background:var(--blue);transition:width .35s cubic-bezier(.2,.7,.25,1)}

.s-head{flex:none;padding-bottom:13px;border-bottom:1px solid var(--grid);margin-bottom:15px}
.kicker{display:flex;align-items:center;gap:9px;font-size:8.5px;letter-spacing:.16em;color:var(--muted);text-transform:uppercase}
.kicker::before{content:"";width:16px;height:2px;background:var(--blue);border-radius:1px}
.kicker b{color:var(--ink-2);font-weight:600;letter-spacing:.06em}
.kicker .sep{width:3px;height:3px;border-radius:50%;background:var(--axis)}
h1{margin:7px 0 0;font-size:26px;line-height:1.28;font-weight:600;letter-spacing:-.022em;color:var(--ink)}
.sub{margin:5px 0 0;font-size:11.5px;line-height:1.55;color:var(--ink-2)}
.s-body{flex:1;min-height:0;display:flex;flex-direction:column;gap:10px}
.s-body.spread{justify-content:space-between}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:0}
.col{display:flex;flex-direction:column;gap:10px;min-width:0}
.col:first-child{padding-right:26px}
.col + .col{border-left:1px solid var(--grid);padding-left:26px}
.slab{font-size:8px;letter-spacing:.14em;color:var(--muted);text-transform:uppercase;font-weight:600;display:flex;align-items:center;gap:7px;flex:none;min-height:14px}
.slab i{width:5px;height:5px;border-radius:50%;flex:none}

.card{background:var(--surface);border:1px solid var(--ring);border-radius:11px;padding:12px 15px;box-shadow:var(--shadow)}
.card-h{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:4px}
.card-t{font-size:11.5px;font-weight:600;letter-spacing:-.01em}
.card-k{font-size:8px;color:var(--muted);text-align:right;line-height:1.45;max-width:54%}
.card-note{font-size:8.5px;line-height:1.55;color:var(--muted);margin-top:6px}
.card-note b{color:var(--ink-2);font-weight:600}

.chart{display:block;width:100%;height:auto;margin-top:4px}
.chart .grid{stroke:var(--grid);stroke-width:1;shape-rendering:crispEdges}
.chart .axis{stroke:var(--axis);stroke-width:1;shape-rendering:crispEdges}
.chart .ref{stroke:var(--axis);stroke-width:1;stroke-dasharray:3 4}
.chart .tick{fill:var(--muted);font-size:8px;font-variant-numeric:tabular-nums}
.chart .tick-x{fill:var(--muted);font-size:8px}
.chart .endlabel{fill:var(--ink);font-size:10px;font-weight:600}
.chart .anno{fill:var(--muted);font-size:8px}
.chart .label{fill:var(--ink-2);font-size:8.5px;font-weight:600}
.chart .sublabel{fill:var(--muted);font-size:7.6px}
.chart circle{transition:r .12s ease;cursor:default}
.chart circle:hover{r:6}

.legend{display:flex;gap:14px;align-items:center;font-size:8.5px;color:var(--ink-2);white-space:nowrap;margin:2px 0 0}
.legend .k{display:inline-flex;align-items:center;gap:5px}
.legend i{width:14px;height:3px;border-radius:2px;display:inline-block}
.legend i.d{width:7px;height:7px;border-radius:50%}

.strip{display:grid;grid-template-columns:repeat(3,1fr);margin-top:7px;border-top:1px solid var(--grid);padding-top:7px}
.strip > div{padding:0 10px;border-left:1px solid var(--grid)}
.strip > div:first-child{padding-left:0;border-left:0}
.ss-l{display:block;font-size:8px;color:var(--muted);letter-spacing:.02em}
.ss-v{font-size:15px;font-weight:600;line-height:1.2;font-variant-numeric:tabular-nums}
.ss-s{font-size:7.5px;color:var(--ink-2);margin-left:4px;white-space:nowrap}
.ss-s.up{color:var(--good)}

.mini{display:flex;align-items:center;gap:18px;padding:11px 15px}
.mini .mtext{flex:1;min-width:0}
.mini .mhead{font-size:10.5px;font-weight:600}
.mini .msub{font-size:8px;color:var(--muted);margin-top:2px}
.mini .mstats{display:flex;gap:18px;margin-top:7px}
.mini .mstat b{display:block;font-size:15px;font-weight:600;line-height:1.1;font-variant-numeric:tabular-nums}
.mini .mstat span{font-size:7.5px;color:var(--muted);white-space:nowrap}
.mini .spark{width:224px;flex:none}

.weekly-grid{display:grid;grid-template-columns:232px 1fr;gap:12px;align-items:start;margin-top:4px}
.tbl{width:100%;border-collapse:collapse;font-size:9px;font-variant-numeric:tabular-nums}
.tbl th{font-weight:500;color:var(--muted);font-size:7.5px;letter-spacing:.02em;text-align:right;padding:0 0 4px;border-bottom:1px solid var(--grid);white-space:nowrap}
.tbl td{padding:4.5px 0;border-bottom:1px solid var(--grid);text-align:right;color:var(--ink-2)}
.tbl tr:last-child td{border-bottom:0}
.tbl td:first-child,.tbl th:first-child{text-align:left;color:var(--ink)}
.tbl tr.mark td{background:rgba(179,38,30,.05);font-weight:600;color:var(--ink)}
.tbl.weekly td{padding:4.7px 0}

.judge{display:flex;align-items:center;gap:18px}
.judge .big{font-size:40px;font-weight:600;letter-spacing:-.035em;line-height:1;min-width:104px}
.judge .big small{font-size:8.5px;color:var(--muted);display:block;letter-spacing:.02em;font-weight:500;margin-top:5px}
.judge .jtext{font-size:9px;line-height:1.65;color:var(--ink-2);border-left:1px solid var(--grid);padding-left:16px}
.judge .jtext b{color:var(--ink)}

.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;flex:none}
.kpi{background:var(--surface);border:1px solid var(--ring);border-radius:10px;padding:9px 13px 10px;box-shadow:var(--shadow)}
.kpi-l{font-size:8px;color:var(--muted);letter-spacing:.02em}
.kpi-v{font-size:27px;font-weight:600;line-height:1.15;letter-spacing:-.028em;margin-top:1px}
.kpi-v .d{font-size:11px;font-weight:600;margin-left:5px;letter-spacing:0;font-variant-numeric:tabular-nums}
.d.good{color:var(--good)}
.kpi-f{font-size:7.5px;color:var(--muted);margin-top:2px;line-height:1.35}
.main2{display:grid;grid-template-columns:1fr 1fr;gap:0;flex:1;min-height:0}
.main2 .col:first-child{padding-right:26px}
.main2 .col + .col{border-left:1px solid var(--grid);padding-left:26px}

.values{flex:1;display:grid;grid-auto-rows:1fr;gap:8px}
.vrow{display:grid;grid-template-columns:40px 1fr 86px;gap:11px;align-items:center;background:var(--surface);border:1px solid var(--ring);border-radius:10px;padding:9px 12px;box-shadow:var(--shadow)}
.vtag{font-size:8.5px;font-weight:600;color:var(--ink);background:#eef2f8;border-radius:6px;padding:4px 0;text-align:center;letter-spacing:.05em}
.vh{font-size:11.5px;font-weight:600;line-height:1.35;letter-spacing:-.005em}
.vh .from{color:var(--muted);font-weight:500}
.vh .to{color:var(--blue);font-weight:600}
.vh .arrow{color:var(--axis);font-weight:400;padding:0 4px}
.vn{font-size:8.5px;color:var(--ink-2);line-height:1.5;margin-top:2px}
.vs{text-align:right;border-left:1px solid var(--grid);padding-left:9px}
.vs b{display:block;font-size:16px;font-weight:600;line-height:1.15;font-variant-numeric:tabular-nums}
.vs span{font-size:7px;color:var(--muted);line-height:1.3;display:block;margin-top:1px}
.statement{background:#eef3fc;border-left:3px solid var(--blue);border-radius:8px;padding:10px 13px;font-size:9px;line-height:1.6;color:var(--ink-2);flex:none}
.statement b{color:var(--ink)}
.st-k{font-size:7px;letter-spacing:.14em;color:var(--muted);display:block;margin-bottom:2px}
.evid{display:flex;flex-direction:column;height:100%}
.pbar{display:flex;flex-direction:column;justify-content:space-evenly;margin-top:6px;flex:1}
.pbr{display:grid;grid-template-columns:82px 1fr 88px 42px;gap:9px;align-items:center}
.pbr .pl{font-size:8px;color:var(--ink-2);white-space:nowrap}
.pbt{display:flex;flex-direction:column;gap:2px}
.pbt i{display:block;height:6px;border-radius:0 3px 3px 0;min-width:1px}
.pbt i.new{background:var(--blue)}
.pbt i.old{background:var(--orange)}
.pbv{font-size:8.5px;font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
.pbv b{font-weight:600;color:var(--ink)}
.pbv span{color:var(--muted);margin-left:4px}
.pbd{font-size:8.5px;text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.pbd.up{color:var(--good)}
.lift{border-top:1px solid var(--grid);margin-top:8px;padding-top:7px;font-size:8px;line-height:1.55;color:var(--ink-2)}
.lift b{color:var(--ink)}

.profilecard{flex:1;display:flex;flex-direction:column;min-height:0}
.profile{display:flex;flex-direction:column;flex:1;min-height:0}
.phead{display:grid;grid-template-columns:166px 1fr 1fr;gap:10px;align-items:center;padding-bottom:5px;border-bottom:1px solid var(--grid);font-size:7.5px;color:var(--muted);flex:none}
.phead .lg{display:flex;align-items:center;gap:5px}
.phead .lg i{width:7px;height:7px;border-radius:50%;display:inline-block}
.prow{display:grid;grid-template-columns:166px 1fr 1fr;gap:10px;align-items:center;padding:6px 0;border-bottom:1px solid var(--grid);flex:1}
.prow:last-child{border-bottom:0}
.plab{font-size:9px;color:var(--ink)}
.pcell{display:flex;align-items:center;gap:6px;min-width:0}
.pcell .val{width:44px;text-align:right;font-size:8.5px;font-variant-numeric:tabular-nums;flex:none}
.pcell .bar{height:7px;flex:1;background:var(--grid);border-radius:3px;position:relative;overflow:hidden}
.pcell .bar i{position:absolute;left:0;top:0;bottom:0;border-radius:3px;display:block}
.statrow{display:grid;grid-template-columns:repeat(3,1fr);background:var(--surface);border:1px solid var(--ring);border-radius:10px;box-shadow:var(--shadow);overflow:hidden;flex:none}
.statrow > div{padding:9px 13px;border-left:1px solid var(--grid)}
.statrow > div:first-child{border-left:0}
.statrow b{display:block;font-size:21px;font-weight:600;line-height:1.15;letter-spacing:-.02em}
.statrow span{font-size:7.5px;color:var(--muted);display:block;margin-top:2px}
.callout{background:#f2f0ea;border-radius:10px;padding:9px 13px;font-size:9px;line-height:1.65;color:var(--ink-2)}
.callout b{color:var(--ink)}

.takeaway{display:flex;flex-direction:column;gap:6px;background:var(--surface);border:1px solid var(--ring);border-radius:10px;padding:11px 12px;font-size:8.5px;line-height:1.5;color:var(--ink-2);margin-top:auto}
.takeaway b{color:var(--ink);font-weight:600;margin-right:5px}

.sched{display:flex;flex-direction:column;gap:4px;margin-top:4px;font-size:8px;color:var(--ink-2)}
.sched b{color:var(--ink);font-weight:600;margin-right:7px}
.sched .dot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:6px;vertical-align:1px}
.meters{display:flex;flex-direction:column;gap:3px;margin-top:3px}
.mrow{display:grid;grid-template-columns:52px 1fr 44px;gap:10px;align-items:center;margin-top:4px}
.mlab{font-size:9px;font-weight:600}
.mtrack{height:10px;border-radius:5px;background:var(--blue-soft);overflow:hidden}
.mtrack i{display:block;height:100%;border-radius:5px;background:var(--blue)}
.mtrack.orange{background:var(--orange-soft)}
.mtrack.orange i{background:var(--orange)}
.mval{font-size:16px;font-weight:600;text-align:right;font-variant-numeric:tabular-nums}
.mfoot{font-size:7.5px;color:var(--muted);margin-left:62px}
.goal{background:#eef3fc;border-left:3px solid var(--blue);border-radius:8px;padding:9px 13px;font-size:9px;line-height:1.55;color:var(--ink-2);flex:none}
.goal b{color:var(--ink);margin-right:6px}

.toprow{display:grid;grid-template-columns:1fr 1fr;gap:0;flex:none}
.toprow > .card{margin-right:26px}
.toprow > .col{border-left:1px solid var(--grid);padding-left:26px;gap:9px}
.focus{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;background:#eef3fc;border-color:rgba(42,120,214,.18)}
.focus-t{font-size:7.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--blue);font-weight:600}
.focus p{margin:3px 0 0;font-size:9.5px;line-height:1.6;color:var(--ink-2)}
.focus p b{color:var(--ink)}
.flow{display:flex;align-items:center;gap:7px;margin:2px 0 12px}
.node{flex:1;border:1px solid var(--ring);background:#f7f6f2;border-radius:8px;padding:9px 8px;text-align:center}
.node b{display:block;font-size:9px;font-weight:600}
.node span{display:block;font-size:7px;color:var(--muted);margin-top:1px}
.node.accent{background:#eef3fc;border-color:rgba(42,120,214,.28)}
.flow .op{color:var(--axis);font-size:13px;flex:none;line-height:1}
.quad{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}
.q{background:#f7f6f2;border:1px solid var(--ring);border-radius:8px;padding:11px 12px}
.q.blue{background:#f2f6fc;border-color:rgba(42,120,214,.18)}
.q-tag{font-size:6.5px;letter-spacing:.1em;color:var(--muted);text-transform:uppercase;font-weight:600}
.q.blue .q-tag{color:var(--blue)}
.q-t{font-size:9.5px;font-weight:600;margin-top:2px}
.q-n{font-size:8px;line-height:1.5;color:var(--ink-2);margin-top:2px}
.plan-note{margin-top:9px;border-top:1px solid var(--grid);padding-top:10px;font-size:8px;line-height:1.55;color:var(--ink-2)}
.plan-note b{color:var(--ink)}

.top2{display:grid;grid-template-columns:1fr 1.12fr;gap:0}
.top2 .col:first-child{padding-right:24px}
.top2 .col + .col{border-left:1px solid var(--grid);padding-left:24px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--grid);border:1px solid var(--ring);border-radius:11px;overflow:hidden;box-shadow:var(--shadow)}
.tile{background:var(--surface);padding:15px 14px}
.tile-l{font-size:7.5px;letter-spacing:.1em;color:var(--muted)}
.tile-v{font-size:22px;font-weight:600;line-height:1.2;letter-spacing:-.025em;margin-top:1px}
.tile-v.sm{font-size:17px}
.tile-n{font-size:8px;color:var(--ink-2);line-height:1.5;margin-top:2px}
.adapt{font-size:8px;line-height:1.55;color:var(--ink-2);background:#f2f0ea;border-radius:8px;padding:8px 11px}
.adapt b{color:var(--ink)}

.tbl.cmp{font-size:9.5px}
.tbl.cmp td{padding:8px 0}
.tbl.cmp td.neg{color:var(--bad);font-weight:600}
.cstat{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--ring);border-radius:10px;background:var(--surface);overflow:hidden;flex:none;box-shadow:var(--shadow)}
.cstat > div{padding:9px 13px;border-left:1px solid var(--grid)}
.cstat > div:first-child{border-left:0}
.cstat b{display:block;font-size:16px;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.2}
.cstat span{font-size:7.5px;color:var(--muted)}
.pstats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;flex:none}
.pstats > div{background:var(--surface);border:1px solid var(--ring);border-radius:10px;padding:12px 14px;box-shadow:var(--shadow)}
.pstats b{display:block;font-size:24px;font-weight:600;line-height:1.1;letter-spacing:-.025em;font-variant-numeric:tabular-nums}
.pstats b span{font-size:9px;color:var(--muted);font-weight:500;letter-spacing:0;margin-left:4px}
.pstats p{margin:3px 0 0;font-size:8.5px;line-height:1.5;color:var(--ink-2)}
.conclusion{background:#eef3fc;border-left:3px solid var(--blue);border-radius:8px;padding:11px 14px;font-size:9.5px;line-height:1.55;color:var(--ink-2);flex:none}
.conclusion b{color:var(--ink)}
.s-foot{position:absolute;left:54px;right:54px;bottom:15px;display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:8px;letter-spacing:.06em}
.s-foot .pg{font-variant-numeric:tabular-nums;color:var(--ink-2);font-weight:600;letter-spacing:.1em}

.hud{position:fixed;left:50%;bottom:13px;transform:translateX(-50%);display:flex;align-items:center;gap:2px;background:rgba(20,21,20,.78);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:4px 7px;color:#f0efec;z-index:40;opacity:.55;transition:opacity .2s;backdrop-filter:blur(10px)}
.hud:hover,.hud:focus-within{opacity:1}
.hud button{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;color:inherit;transition:background .15s}
.hud button:hover{background:rgba(255,255,255,.14)}
.hud .count{font-size:9px;font-variant-numeric:tabular-nums;padding:0 8px;letter-spacing:.1em;color:#c3c2b7}
.hud .sep{width:1px;height:13px;background:rgba(255,255,255,.2);margin:0 4px}
.hud svg{width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.tip{position:fixed;left:0;top:0;z-index:60;pointer-events:none;background:#161817;color:#f0efec;font-size:9.5px;line-height:1.5;padding:5px 9px;border-radius:7px;box-shadow:0 8px 24px rgba(0,0,0,.3);opacity:0;transform:translate(-50%,-130%);transition:opacity .12s;white-space:nowrap;max-width:90vw}
.tip.on{opacity:1}

@media (prefers-reduced-motion:reduce){.slide.active{animation:none}.progress i{transition:none}}
@media print{
  @page{size:13.333in 7.5in;margin:0}
  html,body{height:auto;overflow:visible;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .deck{position:static}
  .stage{position:static;left:auto;top:auto;transform:none!important;width:1280px;height:auto;border-radius:0;box-shadow:none;overflow:visible}
  .slide{position:relative;display:flex!important;width:1280px;height:720px;break-inside:avoid;break-after:page;border-radius:0;animation:none}
  .slide:last-child{break-after:auto}
  .progress,.hud,.tip{display:none!important}
}
"""

JS = r"""
(function(){
  const slides = Array.from(document.querySelectorAll('.slide'));
  const stage = document.getElementById('stage');
  const tip = document.getElementById('tip');
  const bar = document.getElementById('bar');
  const count = document.getElementById('count');
  let cur = 0;

  function fit(){
    const s = Math.min(innerWidth / 1280, innerHeight / 720);
    stage.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
  }

  function hideTip(){ tip.classList.remove('on'); }

  function go(n, updateHash){
    n = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((s, i) => s.classList.toggle('active', i === n));
    cur = n;
    count.textContent = (n + 1) + ' / ' + slides.length;
    bar.style.width = ((n + 1) / slides.length * 100) + '%';
    if (updateHash !== false) history.replaceState(null, '', '#p' + (n + 1));
    hideTip();
  }

  addEventListener('resize', fit);

  addEventListener('keydown', function(e){
    const k = e.key;
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ' || k === 'Enter') {
      e.preventDefault(); go(cur + 1);
    } else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp' || k === 'Backspace') {
      e.preventDefault(); go(cur - 1);
    } else if (k === 'Home') { e.preventDefault(); go(0); }
    else if (k === 'End') { e.preventDefault(); go(slides.length - 1); }
    else if (k === 'f' || k === 'F') { toggleFullscreen(); }
  });

  document.querySelectorAll('[data-nav]').forEach(function(b){
    b.addEventListener('click', function(){
      go(cur + (b.getAttribute('data-nav') === 'next' ? 1 : -1));
    });
  });

  function toggleFullscreen(){
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
    } else {
      document.exitFullscreen && document.exitFullscreen();
    }
  }
  document.getElementById('fs').addEventListener('click', toggleFullscreen);
  document.getElementById('print').addEventListener('click', function(){ window.print(); });

  let tx = 0, ty = 0;
  addEventListener('touchstart', function(e){ tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, {passive:true});
  addEventListener('touchend', function(e){
    const dx = e.changedTouches[0].clientX - tx;
    const dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 52 && Math.abs(dx) > Math.abs(dy)) go(cur + (dx < 0 ? 1 : -1));
  }, {passive:true});

  function placeTip(e){
    const pad = 12;
    tip.style.left = e.clientX + 'px';
    tip.style.top = (e.clientY - 8) + 'px';
    const r = tip.getBoundingClientRect();
    if (r.left < pad) tip.style.left = (pad + r.width / 2) + 'px';
    if (r.right > innerWidth - pad) tip.style.left = (innerWidth - pad - r.width / 2) + 'px';
  }

  document.querySelectorAll('[data-tip]').forEach(function(el){
    el.addEventListener('mouseenter', function(e){
      tip.textContent = el.getAttribute('data-tip');
      tip.classList.add('on');
      placeTip(e);
    });
    el.addEventListener('mousemove', placeTip);
    el.addEventListener('mouseleave', hideTip);
  });

  addEventListener('hashchange', function(){
    const n = parseInt(location.hash.replace('#p', ''), 10);
    if (!isNaN(n)) go(n - 1, false);
  });

  fit();
  const initial = parseInt(location.hash.replace('#p', ''), 10);
  go(isNaN(initial) ? 0 : initial - 1, false);
})();
"""


# ---------------------------------------------------------------------------
# 组装
# ---------------------------------------------------------------------------

def build() -> str:
    slides = "\n".join([slide1(), slide2(), slide3(), slide4(), slide5()])
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>11 月 MBR · 模型与策略</title>
<style>{CSS}</style>
</head>
<body>
<div class="deck">
  <div class="stage" id="stage">
    <div class="progress"><i id="bar"></i></div>
    {slides}
  </div>
</div>

<div class="hud" role="group" aria-label="幻灯片控制">
  <button data-nav="prev" title="上一页（←）" aria-label="上一页">
    <svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg>
  </button>
  <span class="count" id="count">1 / 5</span>
  <button data-nav="next" title="下一页（→）" aria-label="下一页">
    <svg viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg>
  </button>
  <span class="sep"></span>
  <button id="fs" title="全屏（F）" aria-label="全屏">
    <svg viewBox="0 0 16 16"><path d="M6 2H2v4M10 2h4v4M6 14H2v-4M10 14h4v-4"/></svg>
  </button>
  <button id="print" title="打印 / 导出 PDF" aria-label="打印">
    <svg viewBox="0 0 16 16"><path d="M5 6V2h6v4M5 12H3V7h10v5h-2M5 10h6v4H5z"/></svg>
  </button>
</div>

<div class="tip" id="tip"></div>
<script>{JS}</script>
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    HTML = build()
    OUT_FILE.write_text(HTML, encoding="utf-8")
    print(f"已生成: {OUT_FILE}")


if __name__ == "__main__":
    main()
