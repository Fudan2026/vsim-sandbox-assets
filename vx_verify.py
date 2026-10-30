# -*- coding: utf-8 -*-
"""vx_verify.py —— 《AI 选股信号该配多大仓位？》一键自检与数字出生证明

用法：
    python vx_verify.py            # 全量模式：重跑实验管线 + 校验全部锚点（约 1–2 分钟）
    python vx_verify.py --quick    # 快速模式：仅校验已有 summary.json（秒级）

输出：
    1) 锚点校验表（PASS/FAIL，含容差）
    2) manifest.json —— 数字出生证明：数据血统（文件 SHA256/行数/来源）、种子、
       代码版本（本文件与 run_all.py 的 SHA256）、环境信息、锚点→出处映射

设计哲学（蒸馏自成熟量化产品的"引用区"实践）：报告中任何一个数字，
都应能回答三个问题——它从哪份数据来？由哪段代码、什么参数生成？复核通道是什么？
"""
import hashlib
import io
import json
import os
import sys
import contextlib
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

QUICK = "--quick" in sys.argv
TOL = 0.002          # 相对容差（比例类数字）
TOL_PCT = 0.0015     # 百分点类数字的绝对容差

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------- 1. 获取实验结果 ----------
if QUICK:
    with open(os.path.join(HERE, "results", "summary.json"), encoding="utf-8") as f:
        S = json.load(f)
    ran_mode = "quick（读取已有 summary.json）"
else:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import run_all as R          # 导入即全量重跑
    with open(os.path.join(HERE, "results", "summary.json"), encoding="utf-8") as f:
        S = json.load(f)
    ran_mode = "full（重新运行全部实验管线）"

def g(*keys):
    d = S
    for k in keys:
        d = d[k]
    return d

# ---------- 2. 锚点定义（锚点 → 取值函数 → 出处） ----------
G = S["groups"]
A, B, C = G["A 满仓等权(无风险预算)"], G["B 置信度分档固定分数"], G["C 1/4凯利+回撤干预"]
OOS_A = next(x for x in S["oos"] if x["组"].startswith("A")) if "oos" in S else None

ANCHORS = [
    ("全样本 A 组累计收益", lambda: A["累计收益"], 0.2323, "案例报告表3 · 正文4.3"),
    ("全样本 B 组累计收益", lambda: B["累计收益"], 0.2281, "案例报告表3"),
    ("全样本 C 组累计收益", lambda: C["累计收益"], 0.1862, "案例报告表3 · 正文4.3"),
    ("全样本 A 组最大回撤", lambda: A["最大回撤"], -0.1235, "案例报告表3"),
    ("全样本 C 组最大回撤", lambda: C["最大回撤"], -0.0933, "案例报告表3"),
    ("全样本 A 组年化成本拖累", lambda: A["年化交易成本拖累"], 0.0879, "案例报告表3 · 正文4.3"),
    ("全样本 C 组年化成本拖累", lambda: C["年化交易成本拖累"], 0.0432, "案例报告表3"),
    ("置信度均值", lambda: S["desc"]["置信度均值"], 0.8712, "案例报告4.1 · 表2"),
    ("信号总数", lambda: S["desc"]["信号总数"], 6910, "数据集 · 正文2"),
    ("交易日数", lambda: S["desc"]["交易日数"], 410, "数据集 · 正文2"),
]

def find_oos():
    for key in ("oos", "oos_table"):
        if key in S:
            return S[key]
    return None

# 样本外与拓展锚点（存在于 summary 的不同结构中，逐一探测）
_extra = []

oos_tbl = find_oos()
if oos_tbl:
    for row in oos_tbl:
        nm = row.get("组", row.get("仓位规则", ""))
        if nm.startswith("A"):
            _extra.append(("样本外 A 组年化收益", lambda r=row: r["年化收益"], 0.4132, "案例报告4.3"))
            _extra.append(("样本外 A 组最大回撤", lambda r=row: r["最大回撤"], -0.0414, "案例报告4.3"))
        if nm.startswith("C"):
            _extra.append(("样本外 C 组年化收益", lambda r=row: r["年化收益"], 0.1348, "案例报告4.3"))
            _extra.append(("样本外 C 组最大回撤", lambda r=row: r["最大回撤"], -0.0246, "案例报告4.3"))

if "sens_full" in S:
    sf = {(round(float(r["scale"]), 3), str(r["干预"])): r for r in S["sens_full"]}
    r18 = sf[(0.25, "有")]["累计收益"]; r22 = sf[(0.25, "无(反事实)")]["累计收益"]
    _extra.append(("反事实：1/4 凯利无干预累计", lambda: r22, 0.2273, "案例报告表4 · 正文4.5"))
    r50i = sf[(0.5, "有")]["最大回撤"]; r50n = sf[(0.5, "无(反事实)")]["最大回撤"]
    _extra.append(("反事实：1/2 凯利有干预回撤", lambda: r50i, -0.1230, "案例报告表4"))
    _extra.append(("反事实：1/2 凯利无干预回撤", lambda: r50n, -0.1588, "案例报告表4"))
    r1i = sf[(1.0, "有")]["累计收益"]; r1n = sf[(1.0, "无(反事实)")]["累计收益"]
    _extra.append(("反事实：满仓凯利有干预累计", lambda: r1i, 0.2058, "案例报告表4"))
    _extra.append(("反事实：满仓凯利无干预累计", lambda: r1n, 0.4163, "案例报告表4"))

if "signal_decay" in S:
    dd = {r["执行延迟"]: r["方向命中率"] for r in S["signal_decay"]}
    _extra.append(("信号衰减 t+1 命中率", lambda: dd["t+1"], 0.5395, "案例报告5.3 · 正文4.8"))
    _extra.append(("信号衰减 t+3 命中率", lambda: dd["t+3"], 0.4983, "案例报告5.3 · 正文4.8"))

if "factor_ic" in S:
    _extra.append(("因子 IC 均值", lambda: S["factor_ic"]["IC均值"], 0.0621, "案例报告4.1 · 正文4.9"))

if "recalibration" in S:
    _extra.append(("再校准误差（原始）", lambda: S["recalibration"]["校准误差_原始"], 0.221, "案例报告5.2 · 表6"))
    _extra.append(("再校准误差（再校准后）", lambda: S["recalibration"]["校准误差_再校准"], 0.089, "案例报告5.2 · 表6"))

ANCHORS += _extra

# ---------- 3. 校验 ----------
results = []
for name, fn, expect, source in ANCHORS:
    try:
        got = float(fn())
        ok = abs(got - expect) <= max(TOL_PCT, abs(expect) * TOL)
        results.append((name, got, expect, ok, source))
    except Exception as e:
        results.append((name, f"ERR:{e}", expect, False, source))

npass = sum(1 for r in results if r[3])
width = max(len(r[0]) for r in results)
print("=" * 86)
print(f"vx_verify 一键自检 · 模式：{ran_mode}")
print("=" * 86)
for name, got, expect, ok, source in results:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name.ljust(width)}  实得={got!s:<12} 期望={expect!s:<10}  出处：{source}")
print("-" * 86)
print(f"结果：{npass}/{len(results)} 通过" + ("  ✓ 全部锚点一致" if npass == len(results) else "  !! 存在不一致，请检查数据/种子/参数"))

# ---------- 4. manifest：数字出生证明 ----------
def lineage(path, source_desc):
    if not os.path.exists(path):
        return {"文件": os.path.basename(path), "状态": "缺失"}
    n = 0
    with open(path, "rb") as f:
        first = f.readline()
        for _ in f:
            n += 1
    return {"文件": os.path.basename(path), "SHA256": sha256(path)[:16] + "…",
            "数据行数": n + 1, "来源": source_desc}

manifest = {
    "生成时间": datetime.now().isoformat(timespec="seconds"),
    "运行模式": ran_mode,
    "自检结果": f"{npass}/{len(results)} PASS",
    "随机种子": 20261029,
    "环境": {"python": sys.version.split()[0]},
    "数据血统": [
        lineage(os.path.join(HERE, "dataset", "prices.csv"), "腾讯财经公开行情接口 · 28 只沪深大盘蓝筹 · 2024-01-02 至 2025-10-28 · 前复权收盘价"),
        lineage(os.path.join(HERE, "dataset", "signals.csv"), "gen_signals.py 透明蒙特卡洛注入 · 方向 55% 概率取对 · 置信度=幅度映射+噪声"),
    ],
    "代码版本": {
        "run_all.py": sha256(os.path.join(HERE, "run_all.py"))[:16] + "…",
        "vx_verify.py": sha256(os.path.abspath(__file__))[:16] + "…",
    },
    "锚点出处映射": {name: source for name, _, _, _, source in results},
    "说明": "报告中任何一个数字都能回答：从哪份数据来、由哪段代码什么参数生成、如何复核。",
}
mpath = os.path.join(HERE, "results", "manifest.json")
with open(mpath, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"manifest -> {mpath}")
sys.exit(0 if npass == len(results) else 1)
