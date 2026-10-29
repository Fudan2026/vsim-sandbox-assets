# -*- coding: utf-8 -*-
"""
真实行情数据获取：30 只沪深大盘蓝筹日线收盘价（前复权）
来源：腾讯财经公开行情接口（web.ifzq.gtimg.cn，公开可查、无需授权）
"""
import json
import subprocess
import time
import pandas as pd

STOCKS = {
    "600519": "贵州茅台", "601318": "中国平安", "600036": "招商银行", "601166": "兴业银行",
    "600900": "长江电力", "601899": "紫金矿业", "600030": "中信证券", "601988": "中国银行",
    "600276": "恒瑞医药", "601012": "隆基绿能", "600887": "伊利股份", "601088": "中国神华",
    "600028": "中国石化", "601857": "中国石油", "600438": "通威股份", "601225": "陕西煤业",
    "600309": "万华化学", "600690": "海尔智家", "601919": "中远海控", "600406": "国电南瑞",
    "601138": "工业富联", "600050": "中国联通", "600585": "海螺水泥", "601600": "中国铝业",
    "600019": "宝钢股份", "601211": "国泰海通", "600999": "招商证券", "601066": "中信建投",
}
BEG, END = "2024-01-01", "2025-10-28"


def fetch(code):
    url = (f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?"
           f"param=sh{code},day,{BEG},{END},640,qfq")
    out = subprocess.run(["curl", "-s", "--max-time", "20", url],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    d = j["data"]["sh" + code]
    rows = d.get("qfqday") or d.get("day")
    # 字段顺序: [date, open, close, high, low, volume, (可选附加信息)]，取前6列
    rows = [r[:6] for r in rows]
    df = pd.DataFrame(rows, columns=["date", "open", "close", "high", "low", "volume"])
    df["close"] = df["close"].astype(float)
    return df[["date", "close"]]


all_rows, ok = [], 0
for code, name in STOCKS.items():
    for attempt in range(3):
        try:
            df = fetch(code)
            df["code"] = code
            all_rows.append(df)
            ok += 1
            print(code, name, len(df), "rows")
            break
        except Exception as e:
            print("retry", code, name, e)
            time.sleep(3)
    time.sleep(1.0)

px = pd.concat(all_rows)
pivot = px.pivot(index="date", columns="code", values="close").dropna()
print(f"\n成功 {ok}/30, 公共交易日 {len(pivot)} 天, 区间 {pivot.index[0]} ~ {pivot.index[-1]}")
px = pivot.stack().rename("close").reset_index()
px.columns = ["date", "code", "close"]
px.to_csv("dataset/prices.csv", index=False)
print("saved dataset/prices.csv", len(px), "rows")
