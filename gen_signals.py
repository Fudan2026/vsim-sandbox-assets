# -*- coding: utf-8 -*-
"""
信号生成器：在真实行情面板上透明模拟"命中率约55%的AI选股信号"
《AI 选股信号该配多大仓位？——虚拟仿真下的风险预算干预实验》实验条件

设计要点（必须在案例正文中如实披露）：
  1) 行情为真实公开数据（腾讯财经前复权日线，28 只沪深蓝筹，410 个交易日）；
  2) 信号是【实验条件】：生成器以固定种子（20261029）在"已知次日超额收益符号"
     的条件下，以 55% 的概率给出正确方向——这是对"样本外命中率 55% 的 AI 投研
     信号"的透明蒙特卡洛模拟；命中率是可调节参数（改 HIT_RATE 即可），学生可复现；
  3) 置信度与次日超额收益的绝对幅度正相关 + 噪声（模拟大模型置信度的校准特征）。
"""
import numpy as np
import pandas as pd

SEED = 20261029
HIT_RATE = 0.55        # 信号方向命中率（实验设定参数）
COVERAGE = 0.60        # 每个 股票-日 发出观点的概率
rng = np.random.default_rng(SEED)

px = pd.read_csv("dataset/prices.csv", parse_dates=["date"])
pivot = px.pivot(index="date", columns="code", values="close").sort_index()
rets = pivot.pct_change().fillna(0.0)
ew = rets.mean(axis=1)                      # 等权指数收益
excess = rets.sub(ew, axis=0)               # 超额收益（信号判定依据）

T, N = excess.shape
codes = list(pivot.columns)
dates = pivot.index

rows = []
scale = excess.abs().median().median()      # 中位绝对超额幅度，用于置信度映射
for t in range(T - 1):
    for j in range(N):
        if rng.random() > COVERAGE:
            continue
        nxt = excess.iloc[t + 1, j]
        if nxt == 0 or np.isnan(nxt):
            continue
        true_sign = 1 if nxt > 0 else -1
        s = true_sign if rng.random() < HIT_RATE else -true_sign
        conv = float(np.clip(0.55 + 0.9 * (abs(nxt) / (2 * scale)) + rng.normal(0, 0.08), 0.05, 0.98))
        rows.append({"date": dates[t].strftime("%Y-%m-%d"), "code": codes[j],
                     "signal": "buy" if s == 1 else "sell", "conviction": round(conv, 3)})

sg = pd.DataFrame(rows)
sg.to_csv("dataset/signals.csv", index=False)

# 自检：真实命中率应接近 55%
sg["dir"] = sg["signal"].map({"buy": 1, "sell": -1})
sg["date"] = pd.to_datetime(sg["date"])
long = excess.stack().rename("exc").reset_index()
long.columns = ["date", "code", "exc"]
m = sg.merge(long, on=["date", "code"], how="left")
nxt = excess.shift(-1).stack().rename("nxt").reset_index()
nxt.columns = ["date", "code", "nxt"]
m = m.merge(nxt, on=["date", "code"], how="left")
hit = (np.sign(m["nxt"]) == m["dir"]).mean()
print(f"信号条数={len(sg)}  方向命中率={hit:.4f}（设定 {HIT_RATE}）  置信度均值={sg['conviction'].mean():.3f}")
