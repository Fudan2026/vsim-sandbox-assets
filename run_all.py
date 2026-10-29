# -*- coding: utf-8 -*-
"""
实验引擎（与案例 notebook 第 3、4 章代码一致）
受控实验设计：冻结 AI 信号，只变动"仓位规则"，比较风险预算干预的价值。
"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "dataset")
OUT = os.path.join(BASE, "results")
os.makedirs(OUT, exist_ok=True)

TC_BP = 5.0            # 单边交易成本 5bp
MAX_DD = 0.06          # 风险预算：最大回撤干预线 6%
CAP = 0.20             # 单一标的上限 20%
RF = 0.02              # 无风险利率 2%
OOS_START = 0.7        # 后 30% 为样本外

plt.rcParams["font.sans-serif"] = ["PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

# ---------------- 数据读取与预处理 ----------------
px = pd.read_csv(os.path.join(DATA, "prices.csv"), parse_dates=["date"])
sg = pd.read_csv(os.path.join(DATA, "signals.csv"), parse_dates=["date"])

pivot = px.pivot(index="date", columns="code", values="close").sort_index()
rets = pivot.pct_change().fillna(0.0)

sg = sg.sort_values(["date", "code"]).reset_index(drop=True)
last_date = pivot.index[-1]
sg = sg[sg["date"] < last_date]                      # 末日信号无次日收益，剔除
sg["dir"] = sg["signal"].map({"buy": 1, "sell": -1})

dates = pivot.index
T, N = rets.shape
codes = list(pivot.columns)
c2i = {c: i for i, c in enumerate(codes)}

# 信号矩阵（t 日收盘后的信号，作用于 t+1）
sig_mat = np.zeros((T, N))
conv_mat = np.full((T, N), np.nan)
d2i = {d: i for i, d in enumerate(dates)}
for r in sg.itertuples():
    ti, ci = d2i[r.date], c2i[r.code]
    sig_mat[ti, ci] = r.dir
    conv_mat[ti, ci] = r.conviction

# 描述性统计 -------------------------------------------------
n_sig_per_day = (sig_mat != 0).sum(axis=1)
desc = {
    "交易日数": int(T), "股票数": int(N), "信号总数": int(len(sg)),
    "日均信号数": float(n_sig_per_day.mean()),
    "信号覆盖率": float((sig_mat != 0).mean()),
    "看多占比": float((sg["dir"] == 1).mean()),
    "置信度均值": float(sg["conviction"].mean()),
    "个股日收益波动均值": float(rets.std().mean()),
    "个股年化波动均值": float(rets.std().mean() * np.sqrt(252)),
    "等权指数年化波动": float(rets.mean(axis=1).std() * np.sqrt(252)),
}
print("== 描述性统计 ==")
for k, v in desc.items():
    print(f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}")

# 回测引擎 ---------------------------------------------------
def backtest(weight_fn, t0=0, t1=None, intervene=True):
    """weight_fn(t)->目标权重向量(N)；返回逐日组合收益与换手。"""
    t1 = T if t1 is None else t1
    w = np.zeros(N)
    port, turnover = [], []
    peak = 1.0
    nav = 1.0
    for t in range(t0, t1):
        target = np.clip(np.nan_to_num(weight_fn(t)), 0.0, CAP)
        s = target.sum()
        if s > 1.0:
            target = target / s
        # 风险预算干预：回撤触线 → 仓位减半
        if intervene and peak > 0 and (nav / peak - 1.0) <= -MAX_DD:
            target = target * 0.5
        to = np.abs(target - w).sum()
        cost = to * TC_BP / 1e4
        r = float((w * rets.iloc[t].values).sum()) if t > t0 else 0.0
        nav *= (1.0 + r - cost)
        peak = max(peak, nav)
        port.append(r - cost)
        turnover.append(to)
        w = target
    port = pd.Series(port, index=dates[t0:t1])
    return port, nav, float(np.mean(turnover))

def metrics(port, nav, to_mean=None):
    n = len(port)
    ann = (nav) ** (252 / n) - 1 if n > 0 else 0.0
    vol = port.std() * np.sqrt(252)
    sharpe = (ann - RF) / vol if vol > 0 else np.nan
    cum = (1 + port).cumprod()
    mdd = float((cum / cum.cummax() - 1).min())
    calmar = ann / abs(mdd) if mdd < 0 else np.nan
    m = {"累计收益": float(nav - 1), "年化收益": float(ann), "年化波动": float(vol),
         "夏普比率": float(sharpe), "最大回撤": mdd, "卡玛比率": float(calmar)}
    if to_mean is not None:
        m["日均单边换手"] = float(to_mean)
        m["年化交易成本拖累"] = float(to_mean * 252 * TC_BP / 1e4)
    return m

# ---------------- 三组仓位规则（共用同一信号） ----------------
active = sig_mat != 0

def wA(t):  # 组A：满仓等权（无风险预算）
    a = active[t]
    return np.where(a, 1.0 / max(a.sum(), 1), 0.0)

def wB(t):  # 组B：置信度分档固定分数
    cv = conv_mat[t]
    w = np.where(cv >= 0.70, 0.30, np.where(cv >= 0.55, 0.20, 0.0))
    return np.where(active[t], w, 0.0)

# 组C：1/4 凯利 + 回撤干预。凯利参数用样本内估计。
def fit_kelly(t_end):
    hits, wins, losses = {}, [], []
    for j in range(N):
        idx = np.where((sig_mat[:t_end, j] != 0))[0]
        idx = idx[idx + 1 < t_end]
        if len(idx) < 10:
            continue
        nxt = rets.iloc[idx + 1, j].values
        d = sig_mat[idx, j]
        p = float((np.sign(nxt) == d).mean())
        win = nxt[d == 1]; los = nxt[d == -1]
        avg_w = win[win > 0].mean() if (win > 0).any() else 0.004
        avg_l = abs(los[los < 0].mean()) if (los < 0).any() else 0.004
        b = avg_w / avg_l if avg_l > 0 else 1.0
        f = max((p * b - (1 - p)) / b, 0.0)
        hits[j] = f
    return hits

t_is_end = int(T * OOS_START)
kelly_is = fit_kelly(t_is_end)

def make_wC(scale):
    def wC(t):
        w = np.zeros(N)
        for j, f in kelly_is.items():
            if active[t, j]:
                w[j] = scale * f
        return w
    return wC

groups = {
    "A 满仓等权(无风险预算)": (wA, True),
    "B 置信度分档固定分数": (wB, True),
    "C 1/4凯利+回撤干预": (make_wC(0.25), True),
}
print("\n== 全样本三组对比 ==")
navs = {}
table = {}
for name, (fn, _) in groups.items():
    port, nav, to_mean = backtest(fn)
    m = metrics(port, nav, to_mean)
    table[name] = m
    navs[name] = (1 + port).cumprod()
    print(name, {k: round(v, 4) for k, v in m.items()})

# 样本外检验（后 30%，权重函数仍用样本内参数）
print("\n== 样本外(后30%) ==")
for name, (fn, _) in groups.items():
    port, nav, to_mean = backtest(fn, t0=t_is_end)
    m = metrics(port, nav, to_mean)
    print(name, {k: round(v, 4) for k, v in m.items()})

# 敏感性分析：凯利缩放系数 × 是否干预
print("\n== 敏感性：凯利缩放 × 回撤干预(样本外) ==")
sens = []
for c in [0.125, 0.25, 0.5, 1.0]:
    for itv in [True, False]:
        port, nav, to_mean = backtest(make_wC(c), t0=t_is_end, intervene=itv)
        m = metrics(port, nav, to_mean)
        sens.append({"scale": c, "干预": "有" if itv else "无(反事实)", **m})
        print(f"c={c} 干预={itv}", {k: round(v, 4) for k, v in m.items()})

# 反事实：组C 移除风险预算干预（全样本）
print("\n== 反事实：移除回撤干预(全样本, 1/4凯利) ==")
for itv in [True, False]:
    port, nav, to_mean = backtest(make_wC(0.25), intervene=itv)
    print("干预" if itv else "移除干预", {k: round(v, 4) for k, v in metrics(port, nav, to_mean).items()})

# 干预线敏感性：风险预算线设置是否匹配仓位规模？（全样本, 1/4凯利）
print("\n== 干预线敏感性(全样本, 1/4凯利) ==")
for dd in [0.03, 0.06, 0.09]:
    globals()["MAX_DD"] = dd
    port, nav, to_mean = backtest(make_wC(0.25), intervene=True)
    print(f"预算线-{dd:.0%}", {k: round(v, 4) for k, v in metrics(port, nav, to_mean).items()})
globals()["MAX_DD"] = 0.06

# 全样本敏感性（补充，供正文对比表使用）
print("\n== 敏感性：凯利缩放 × 回撤干预(全样本) ==")
sens_full = []
for c in [0.125, 0.25, 0.5, 1.0]:
    for itv in [True, False]:
        port, nav, to_mean = backtest(make_wC(c), intervene=itv)
        m = metrics(port, nav, to_mean)
        sens_full.append({"scale": c, "干预": "有" if itv else "无(反事实)", **m})
        print(f"c={c} 干预={itv}", {k: round(v, 4) for k, v in m.items()})

# 置信度校准：分桶命中率（描述性统计 → 模型可信度诊断）
print("\n== 置信度校准（分桶命中率，全样本） ==")
cal_rows = []
for lo, hi in [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.01)]:
    sub = sg[(sg["conviction"] >= lo) & (sg["conviction"] < hi)]
    if len(sub) == 0:
        continue
    hit_rates = []
    ew_idx = rets.mean(axis=1)
    for r in sub.itertuples():
        ti, ci = d2i[r.date], c2i[r.code]
        if ti + 1 < T:
            nxt = rets.iloc[ti + 1, ci] - ew_idx.iloc[ti + 1]   # 超额收益判定方向
            want = 1 if r.signal == "buy" else -1
            hit_rates.append(int(np.sign(nxt) == want) if nxt != 0 else 0)
    cal_rows.append({"conviction桶": f"[{lo:.1f},{hi:.1f})", "信号数": len(sub),
                     "方向命中率": float(np.mean(hit_rates)) if hit_rates else np.nan})
    print(cal_rows[-1])


# 图 1：累计净值
fig, ax = plt.subplots(figsize=(9, 4.6))
for name, s in navs.items():
    ax.plot(s.index, s.values, label=name, lw=1.4)
ax.axvline(dates[t_is_end], color="gray", ls="--", lw=0.8)
ax.text(dates[t_is_end], ax.get_ylim()[1] * 0.98, " 样本外起点", fontsize=8, color="gray")
ax.set_title("固定 AI 信号、不同仓位规则下的组合累计净值（虚拟仿真数据）")
ax.legend(fontsize=8); ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig1_nav.png"), dpi=110); plt.close(fig)

# 图 2：回撤曲线
fig, ax = plt.subplots(figsize=(9, 3.6))
for name, s in navs.items():
    dd = s / s.cummax() - 1
    ax.plot(dd.index, dd.values * 100, label=name, lw=1.2)
ax.axhline(-MAX_DD * 100, color="red", ls=":", lw=0.9, label="回撤预算线 -6%")
ax.set_title("组合回撤（%）与风险预算干预线"); ax.legend(fontsize=8, ncol=2)
ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig2_drawdown.png"), dpi=110); plt.close(fig)

# 图 3：敏感性（全样本，含反事实情形——与正文 4.5 对比表同口径）
sdf = pd.DataFrame(sens_full)
fig, ax = plt.subplots(figsize=(9, 4))
x = np.arange(len(sdf))
ax.bar(x - 0.2, sdf["累计收益"] * 100, width=0.4, label="累计收益%")
ax2 = ax.twinx()
ax2.bar(x + 0.2, sdf["最大回撤"] * 100, width=0.4, color="tomato", label="最大回撤%")
ax.set_xticks(x)
ax.set_xticklabels([f"1/{int(1/r.scale)}凯利\n干预={r.干预}" for r in sdf.itertuples()], fontsize=8)
ax.set_title("仓位规模敏感性：凯利缩放系数 × 回撤干预（全样本，含反事实情形）")
ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig3_sens.png"), dpi=110); plt.close(fig)

# 图 3b：敏感性（样本外，补充检验——样本内参数冻结后的稳健性）
sdf_oos = pd.DataFrame(sens)
fig, ax = plt.subplots(figsize=(9, 4))
x = np.arange(len(sdf_oos))
ax.bar(x - 0.2, sdf_oos["累计收益"] * 100, width=0.4, label="累计收益%")
ax2 = ax.twinx()
ax2.bar(x + 0.2, sdf_oos["最大回撤"] * 100, width=0.4, color="tomato", label="最大回撤%")
ax.set_xticks(x)
ax.set_xticklabels([f"1/{int(1/r.scale)}凯利\n干预={r.干预}" for r in sdf_oos.itertuples()], fontsize=8)
ax.set_title("仓位规模敏感性：凯利缩放系数 × 回撤干预（样本外，补充检验）")
ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig3b_sens_oos.png"), dpi=110); plt.close(fig)

with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
    json.dump({"desc": desc, "groups": table, "sens": sens, "sens_full": sens_full,
               "calibration": cal_rows}, f, ensure_ascii=False, indent=2, default=float)
print("\nsaved ->", OUT)
