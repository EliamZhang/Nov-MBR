import csv
import glob
import math
import sys
from collections import Counter, OrderedDict

sys.stdout.reconfigure(encoding="utf-8")

INPUT_PATTERN = "samples_sample_with_feature_all_y_fpd15_ovd_特征分箱结果.csv"
OUTPUT_HTML = "用户画像分析.html"
OUTPUT_CSV = "用户画像_变量统计.csv"
MIN_BIN_N = 30

GLOSS = {
    "bank_txn_dishonour_lender_unresolved_ratio_3gp_56d": "借贷机构未解决拒付占比（56天，3期）",
    "bank_txn_worthiness_refund_or_reversal_to_drawdown_ratio_28d": "退款/冲正 ÷ 提款金额（28天）",
    "bank_txn_worthiness_refund_or_reversal_to_drawdown_ratio_182d": "退款/冲正 ÷ 提款金额（182天）",
    "bank_txn_dishonour_cash_wage_advance_unresolved_ratio_3gp_28d": "工资预支未解决拒付占比（28天）",
    "bank_txn_lender_disburse_advance_amount_max_l28d": "借贷机构预支最大金额（近28天）",
    "bank_txn_dishonour_cash_wage_advance_unresolved_ratio_3gp_168d": "工资预支未解决拒付占比（168天）",
    "bank_txn_category_dishonours_amt_14d": "拒付金额（近14天）",
    "bank_txn_worthiness_refund_or_reversal_cnt_56d": "退款/冲正笔数（56天）",
    "bank_txn_dishonour_lender_unresolved_ratio_3gp_7d": "借贷机构未解决拒付占比（7天）",
    "bank_txn_worthiness_refund_or_reversal_to_drawdown_ratio_7d": "退款/冲正 ÷ 提款金额（7天）",
    "bank_txn_surplus_liabilitydrawdown_sum_28d": "盈余 − 负债提款合计（28天）",
    "bank_txn_surplus_liabilitydrawdown_mean_28d": "盈余 − 负债提款均值（28天）",
    "bank_txn_surplus_liabilitydrawdown_std_28d": "盈余 − 负债提款标准差（28天）",
    "bank_txn_surplus_liabilitydrawdown_max_56d": "盈余 − 负债提款最大值（56天）",
    "bank_txn_surplus_liabilityrepayment_std_28d": "盈余 − 负债还款标准差（28天）",
    "bank_txn_surplus_liabilityrepayment_cv_28d": "盈余 − 负债还款变异系数（28天）",
    "bank_txn_category_non_sacc_loans_share_28d": "非 SACC 贷款交易占比（28天）",
    "bank_txn_category_non_sacc_loans_amt_56d": "非 SACC 贷款金额（56天）",
    "bank_txn_lender_disburse_advance_amount_max": "借贷机构预支最大金额（全期）",
    "bank_txn_lender_disburse_amount_max_l14d": "借贷机构放款最大金额（近14天）",
    "bank_txn_lender_disburse_amount_avg_l84d": "借贷机构放款平均金额（近84天）",
    "bank_txn_dishonour_lender_unresolved_cnt_3gp_14d": "借贷机构未解决拒付笔数（14天）",
    "bank_txn_lender_disburse_advance_amount_avg_l182d": "借贷机构预支平均金额（近182天）",
    "bank_txn_worthiness_net_income_after_expense_ratio_182d": "净收入 ÷ 支出（182天）",
    "bank_txn_lender_disburse_advance_amount_max_l7d": "借贷机构预支最大金额（近7天）",
    "bank_txn_surplus_refundorreversal_1m_vs_6m": "退款/冲正 1个月 vs 6个月",
    "bank_txn_surplus_refundorreversal_min_7d": "近7天退款/冲正最小金额",
    "bank_txn_worthiness_liability_repayment_amt_max_84d": "负债还款最大金额（84天）",
    "bank_txn_lender_disburse_advance_amount_min_l14d": "借贷机构预支最小金额（近14天）",
    "bank_txn_dishonour_cash_wage_advance_ratio_7d": "工资预支拒付占比（7天）",
    "bank_txn_dishonour_lender_unresolved_amt_3gp_182d": "借贷机构未解决拒付金额（182天）",
    "bank_txn_category_cluster_transfers_share_56d": "聚合转账占比（56天）",
    "bank_txn_balance_debit_no_txn_ratio_84d": "借记无交易天数占比（84天）",
    "bank_txn_lender_repay_bnpl_amount_sum_l7d": "BNPL 还款金额合计（近7天）",
    "bank_txn_worthiness_liability_repayment_to_drawdown_ratio_28d": "负债还款 ÷ 提款（28天）",
    "bank_txn_category_non_sacc_loans_credit_cnt_28d": "非 SACC 贷款贷方笔数（28天）",
    "bank_txn_worthiness_days_since_last_liability_drawdown_168d": "距上次负债提款天数（168天）",
    "bank_txn_lender_disburse_advance_count_l56d": "借贷机构预支笔数（近56天）",
    "bank_txn_income_wages_min_consumption_rate_7d": "工资最低消费率（7天）",
    "bank_txn_expense_global_count_7d": "支出笔数（近7天）",
    "txn_raw_input_cnt": "原始流水笔数",
    "bank_txn_balance_kmeans2_c0_14d": "余额 KMeans 簇0（14天）",
    "bank_txn_balance_global_pca_pc1_loading_credit_14d": "余额 PCA 第一主成分（贷方，14天）",
    "bank_txn_balance_kmeans2_c0_7d": "余额 KMeans 簇0（7天）",
    "bank_txn_balance_credit_fortnight_amount_28d": "双周贷方金额（28天）",
    "bank_txn_income_otherincome_median_84d": "其他收入中位数（84天）",
    "bank_txn_expense_internaltransfer_cv_14d": "内部转账变异系数（14天）",
    "bank_txn_expense_diningout_median_84d": "餐饮支出中位数（84天）",
    "bank_txn_industry_wages_total_amt": "行业工资总额",
}


def fmt_num(v):
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    if abs(v) >= 10:
        return f"{v:.1f}".rstrip("0").rstrip(".")
    if abs(v) >= 1:
        return f"{v:.2f}".rstrip("0").rstrip(".")
    return f"{v:.4f}".rstrip("0").rstrip(".")


def pct(x):
    return f"{x * 100:.1f}%"


def gloss(feature):
    return GLOSS.get(feature, feature)


def bin_label(row):
    if row["is_missing"] == "True":
        return "缺失"
    lower = float(row["lower"])
    upper = float(row["upper"])
    if math.isinf(lower) and math.isinf(upper):
        return "全部"
    if math.isinf(lower):
        return f"≤ {fmt_num(upper)}"
    if math.isinf(upper):
        return f"> {fmt_num(lower)}"
    return f"{fmt_num(lower)}–{fmt_num(upper)}"


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0

    def ranks(values):
        order = sorted(range(n), key=lambda i: values[i])
        result = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and values[order[j + 1]] == values[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                result[order[k]] = avg
            i = j + 1
        return result

    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return cov / (dx * dy) if dx and dy else 0.0


def load_bins():
    path = glob.glob(INPUT_PATTERN)[0]
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    by_feature = OrderedDict()
    for row in rows:
        by_feature.setdefault(row["feature"], []).append(row)
    return path, by_feature


def feature_stats(rows, total_n, total_bad, overall):
    non_missing = [r for r in rows if r["is_missing"] == "False"]
    missing = next((r for r in rows if r["is_missing"] == "True"), None)
    modal = max(rows, key=lambda r: int(float(r["n"])))
    eligible = [r for r in non_missing if int(float(r["n"])) >= MIN_BIN_N] or non_missing
    worst = max(eligible, key=lambda r: float(r["bad_rate"]))
    best = min(eligible, key=lambda r: float(r["bad_rate"]))
    rho = spearman(
        [float(r["bin_order"]) for r in non_missing],
        [float(r["bad_rate"]) for r in non_missing],
    )
    return {
        "rows": rows,
        "iv": sum(float(r["iv_part"]) for r in rows),
        "n": sum(int(float(r["n"])) for r in rows),
        "bad": sum(int(float(r["bad"])) for r in rows),
        "modal": modal,
        "worst": worst,
        "best": best,
        "rho": rho,
        "missing": missing,
        "non_missing": non_missing,
        "total_n": total_n,
        "total_bad": total_bad,
        "overall": overall,
    }


def share_of_total(row, stats):
    return int(float(row["n"])) / stats["total_n"]


def share_of_bad(row, stats):
    return int(float(row["bad"])) / stats["total_bad"]


def lift_of(row, stats):
    return float(row["bad_rate"]) / stats["overall"] if stats["overall"] else 0.0


def pct_row(row):
    return pct(float(row["bad_rate"]))


CSS = """
:root {
  --bg: #f6f3ee;
  --surface: #fffdf9;
  --ink: #211e1a;
  --ink-2: #5f594f;
  --ink-3: #736c61;
  --line: #e4ded4;
  --risk: #b23a32;
  --good: #2f6f4e;
  --neutral: #8a6a2f;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #141311;
    --surface: #1e1c19;
    --ink: #f2ede4;
    --ink-2: #bdb5a7;
    --ink-3: #8f877a;
    --line: #332f29;
    --risk: #e07b72;
    --good: #7cc39a;
    --neutral: #d6b06a;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", system-ui, -apple-system, sans-serif;
  font-size: 14px;
  line-height: 1.5;
}
main { max-width: 1040px; margin: 0 auto; padding: 22px 24px 16px; }
.head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 28px;
  align-items: end;
  padding-bottom: 14px;
}
.kicker {
  margin: 0 0 6px;
  font-size: 10.5px;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--ink-3);
}
h1 {
  margin: 0 0 6px;
  font-family: "Songti SC", "STSong", "Noto Serif SC", serif;
  font-size: clamp(26px, 3.2vw, 36px);
  line-height: 1.2;
  letter-spacing: -.02em;
  font-weight: 600;
}
.sub {
  margin: 0;
  max-width: 640px;
  color: var(--ink-2);
  font-size: 13px;
}
.head-stats {
  display: grid;
  grid-template-columns: repeat(3, auto);
  border-left: 1px solid var(--line);
}
.head-stats div {
  padding: 0 14px;
  border-right: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.head-stats div:last-child { border-right: 0; padding-right: 0; }
.head-stats strong {
  font-size: 22px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  letter-spacing: -.02em;
  white-space: nowrap;
}
.head-stats span { font-size: 10.5px; color: var(--ink-3); white-space: nowrap; }
.takeaway {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 10px 0;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}
.label {
  flex: none;
  font-size: 9.5px;
  letter-spacing: .1em;
  color: var(--ink-3);
  text-transform: uppercase;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 2px 7px;
  line-height: 1.4;
}
.takeaway p { margin: 0; color: var(--ink-2); font-size: 12.5px; }
.cols {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
  border-top: 0;
}
.col {
  background: var(--surface);
  border-top: 3px solid var(--tone);
  padding: 12px 14px 10px;
}
.col-top {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--ink-3);
  font-size: 9.5px;
  letter-spacing: .1em;
  text-transform: uppercase;
}
.dot { width: 6px; height: 6px; border-radius: 50%; background: var(--tone); }
.col h2 { margin: 5px 0 10px; font-size: 15px; line-height: 1.3; font-weight: 600; }
.col ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.col li {
  display: grid;
  grid-template-columns: 68px 1fr;
  gap: 7px;
  align-items: start;
  padding-top: 8px;
  border-top: 1px solid var(--line);
}
.col li:first-child { border-top: 0; padding-top: 0; }
.rate { display: flex; flex-direction: column; gap: 0; }
.rate strong {
  font-size: 22px;
  line-height: 1.1;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  letter-spacing: -.02em;
}
.rate span { font-size: 9.5px; color: var(--ink-3); letter-spacing: .04em; }
.col li p { margin: 1px 0 0; color: var(--ink-2); font-size: 12px; line-height: 1.45; }
.col li b { color: var(--ink); font-weight: 600; font-variant-numeric: tabular-nums; }
.nw { white-space: nowrap; }
.insights {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
  border-top: 0;
}
.insights > div {
  background: var(--surface);
  padding: 9px 14px 10px;
  display: flex;
  align-items: baseline;
  gap: 8px;
}
.insights p { margin: 0; color: var(--ink-2); font-size: 11px; line-height: 1.45; }
footer {
  margin-top: 10px;
  color: var(--ink-3);
  font-size: 10px;
  line-height: 1.5;
}
@media screen and (max-width: 680px) {
  main { padding: 16px 14px 12px; }
  .head { grid-template-columns: 1fr; gap: 12px; align-items: start; }
  .head-stats { border-left: 0; border-top: 1px solid var(--line); padding-top: 10px; }
  .head-stats div { padding: 0 12px; }
  .head-stats div:first-child { padding-left: 0; }
  .cols { grid-template-columns: 1fr; }
  .insights { grid-template-columns: 1fr; }
  .takeaway { align-items: flex-start; }
}
@media print {
  :root {
    --bg: #fff; --surface: #fff; --ink: #211e1a; --ink-2: #5f594f;
    --ink-3: #6f685e; --line: #ddd6ca;
    --risk: #b23a32; --good: #2f6f4e; --neutral: #8a6a2f;
  }
  body { background: #fff; }
  main { max-width: none; padding: 0; }
  .col, .insights > div { break-inside: avoid; }
}
"""


def rate_row(rate_text, condition):
    return (
        f'<li><div class="rate"><strong>{rate_text}</strong><span>坏率</span></div>'
        f"<p>{condition}</p></li>"
    )


def main():
    _, by_feature = load_bins()
    totals = Counter()
    for rows in by_feature.values():
        totals[(sum(int(float(r["n"])) for r in rows), sum(int(float(r["bad"])) for r in rows))] += 1
    (total_n, total_bad), _ = totals.most_common(1)[0]
    overall = total_bad / total_n

    features = OrderedDict(
        (f, rows) for f, rows in by_feature.items() if not f.startswith("y_")
    )
    stats = {
        f: feature_stats(rows, total_n, total_bad, overall)
        for f, rows in features.items()
    }

    d = stats["bank_txn_dishonour_lender_unresolved_ratio_3gp_56d"]
    r = stats["bank_txn_worthiness_refund_or_reversal_to_drawdown_ratio_28d"]
    w = stats["bank_txn_dishonour_cash_wage_advance_unresolved_ratio_3gp_28d"]
    s = stats["bank_txn_surplus_liabilitydrawdown_sum_28d"]
    ni = stats["bank_txn_worthiness_net_income_after_expense_ratio_182d"]
    dis = stats["bank_txn_lender_disburse_advance_amount_max_l28d"]

    col_typical = f"""
    <article class="col" style="--tone: var(--neutral)">
      <div class="col-top"><span class="dot"></span>多数人</div>
      <h2>流水干净，缓冲偏薄</h2>
      <ul>
        {rate_row(pct_row(d["modal"]), f"<b>{pct(share_of_total(d['modal'], d))}</b> 的人近 56 天<span class='nw'>几乎没有未解决扣款</span>")}
        {rate_row(pct_row(w["modal"]), f"<b>{pct(share_of_total(w['modal'], w))}</b> 的人工资预支<span class='nw'>几乎没有未解决扣款</span>")}
        {rate_row(pct_row(ni["modal"]), f"<b>{pct(share_of_total(ni['modal'], ni))}</b> 的人<span class='nw'>净收入/支出</span> ≤1.7%（风险暗流）")}
      </ul>
    </article>"""

    col_high = f"""
    <article class="col" style="--tone: var(--risk)">
      <div class="col-top"><span class="dot"></span>高风险</div>
      <h2>现金流吃紧，靠预支周转</h2>
      <ul>
        {rate_row(pct_row(d["worst"]), f"<b>{pct(share_of_total(d['worst'], d))}</b> 的人<span class='nw'>未解决扣款</span>占比 >31.9%")}
        {rate_row(pct_row(w["worst"]), f"<b>{pct(share_of_total(w['worst'], w))}</b> 的人工资预支<span class='nw'>未解决扣款</span> >28.6%")}
        {rate_row(pct_row(r["worst"]), f"<b>{pct(share_of_total(r['worst'], r))}</b> 的人<span class='nw'>退款/冲正</span><span class='nw'>超过提款</span> 1.25 倍")}
      </ul>
    </article>"""

    col_low = f"""
    <article class="col" style="--tone: var(--good)">
      <div class="col-top"><span class="dot"></span>低风险</div>
      <h2>现金流稳，负债行为正常</h2>
      <ul>
        {rate_row(pct_row(r["best"]), f"<b>{pct(share_of_total(r['best'], r))}</b> 的人<span class='nw'>退款/提款比</span> ≤1.7%")}
        {rate_row(pct_row(s["best"]), f"<b>{pct(share_of_total(s['best'], s))}</b> 的人近 28 天盈余 >5,465")}
        {rate_row(pct_row(ni["best"]), f"<b>{pct(share_of_total(ni['best'], ni))}</b> 的人<span class='nw'>净收入/支出</span> >22.2%")}
      </ul>
    </article>"""

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Wagego 新客画像 · FPD15</title>
<style>{CSS}</style>
</head>
<body>
<main>
  <header class="head">
    <div>
      <p class="kicker">WAGEGO · 新客画像 · FPD15</p>
      <h1>流水干净，但经不起波动。</h1>
      <p class="sub">6,733 位首笔成交新客的流水画像：风险不在有没有流水，而在扣款失败、退款/冲正、预支依赖和还款能力。</p>
    </div>
    <div class="head-stats">
      <div><strong>{total_n:,}</strong><span>位新客</span></div>
      <div><strong>{pct(overall)}</strong><span>整体坏率</span></div>
      <div title="未解决扣款最差区间的坏率 ÷ 整体坏率"><strong>{lift_of(d['worst'], d):.1f}×</strong><span>头号风险倍数</span></div>
    </div>
  </header>

  <div class="takeaway">
    <span class="label">一句话</span>
    <p>先看扣款失败/拒付，再看现金流盈余、是否靠预支周转和退款/冲正；收入、支出、余额单独看，参考价值有限。</p>
  </div>

  <section class="cols">
    {col_typical}
    {col_high}
    {col_low}
  </section>

  <div class="insights">
    <div>
      <span class="label">没有记录也有风险</span>
      <p>{pct(share_of_total(r['missing'], r))} 的人算不出退款/提款比，坏率 {pct_row(r['missing'])}；<br>{pct(share_of_total(dis['missing'], dis))} 没有借贷预支金额，坏率 {pct_row(dis['missing'])}。</p>
    </div>
    <div>
      <span class="label">怎么读</span>
      <p>坏率 = 首期还款逾期 15 天以上的人数占比。</p>
    </div>
  </div>

  <footer>
    样本：{total_n:,} 名已成熟首笔成交新客；FPD15 = 首期还款逾期 15 天以上；画像为群体描述，不代表同一人同时具备所有特征。
  </footer>
</main>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8", newline="\n") as f:
        f.write(html_doc)

    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "feature", "gloss", "iv", "rho", "n", "bad", "bad_rate",
                "modal_bin", "modal_share", "modal_bad_rate",
                "worst_bin", "worst_share", "worst_bad_rate", "worst_lift", "worst_bad_share",
                "best_bin", "best_share", "best_bad_rate",
                "missing_share", "missing_bad_rate",
            ]
        )
        for f, s in stats.items():
            m = s["missing"]
            writer.writerow(
                [
                    f, gloss(f), f"{s['iv']:.6f}", f"{s['rho']:.4f}", s["n"], s["bad"],
                    f"{s['bad'] / s['n']:.6f}",
                    bin_label(s["modal"]), f"{share_of_total(s['modal'], s):.6f}",
                    f"{float(s['modal']['bad_rate']):.6f}",
                    bin_label(s["worst"]), f"{share_of_total(s['worst'], s):.6f}",
                    f"{float(s['worst']['bad_rate']):.6f}", f"{lift_of(s['worst'], s):.4f}",
                    f"{share_of_bad(s['worst'], s):.6f}",
                    bin_label(s["best"]), f"{share_of_total(s['best'], s):.6f}",
                    f"{float(s['best']['bad_rate']):.6f}",
                    f"{share_of_total(m, s):.6f}" if m else "0",
                    f"{float(m['bad_rate']):.6f}" if m else "",
                ]
            )

    print(f"样本: {total_n:,} / 坏样本 {total_bad:,} / 坏率 {pct(overall)}")
    print(f"候选变量: {len(stats)}")
    print(f"已生成: {OUTPUT_HTML}")
    print(f"已生成: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
