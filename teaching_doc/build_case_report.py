# -*- coding: utf-8 -*-
"""案例报告 Word 生成器（V2 6.2）：实验案例分析报告体裁
范式：判断句开头 → 证据链（数字+来源+data_cutoff）→ 配置含义 → 金句收束 → 免责声明
五件套显性：多策略对照 · 样本外检验 · 反事实分析 · 可解释归因 · 复现能力（+可验证证据/人工仅设硬约束/决策可回溯）
"""
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "/Users/Admin/Documents/kimi/tasks/2026-10-24/14-58-19-b5e2402f/教学指导文档/案例报告.docx"

DARK = RGBColor(0x0F, 0x17, 0x2A)
ACCENT = RGBColor(0x1D, 0x4E, 0xD8)   # 蓝 2563EB 的深一档，正文更稳
GRAY = RGBColor(0x47, 0x55, 0x69)
GOLD_BG = "FFF7ED"                    # 金句条浅橙底

def set_font(run, size=12, bold=False, color=None, cn_font="宋体", en_font="Times New Roman"):
    run.font.size = Pt(size); run.font.bold = bold; run.font.name = en_font
    run._element.rPr.rFonts.set(qn("w:eastAsia"), cn_font)
    if color is not None:
        run.font.color.rgb = color

BOLD_RE = re.compile(r"\*\*(.+?)\*\*")

def add_rich(p, text, size=12, base_bold=False, color=None, cn_font="宋体"):
    pos = 0
    for m in BOLD_RE.finditer(text):
        if m.start() > pos:
            set_font(p.add_run(text[pos:m.start()]), size, base_bold, color, cn_font)
        set_font(p.add_run(m.group(1)), size, True, color, cn_font)
        pos = m.end()
    if pos < len(text):
        set_font(p.add_run(text[pos:]), size, base_bold, color, cn_font)
    return p

def h1(doc, text, num=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18); p.paragraph_format.space_after = Pt(8)
    add_rich(p, f"{num}　{text}" if num else text, size=16, base_bold=True, color=DARK, cn_font="黑体")
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr"); bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "2"); bottom.set(qn("w:color"), "0F172A")
    pBdr.append(bottom); pPr.append(pBdr)

def h2(doc, text, num=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)
    add_rich(p, f"{num}　{text}" if num else text, size=13.5, base_bold=True, color=ACCENT, cn_font="黑体")

def para(doc, text, size=12, indent=True, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4); p.paragraph_format.line_spacing = 1.3
    if indent:
        p.paragraph_format.first_line_indent = Pt(24)
    add_rich(p, text, size=size, color=color)

def bullet(doc, text, size=12):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2); p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.left_indent = Pt(18); p.paragraph_format.first_line_indent = Pt(0)
    add_rich(p, f"• {text}", size=size)

def golden(doc, text):
    """金句收束条：浅底圆角段落"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.left_indent = Pt(12); p.paragraph_format.right_indent = Pt(12)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), GOLD_BG)
    pPr.append(shd)
    add_rich(p, "**" + text + "**", size=12.5, cn_font="黑体")

def disclaimer(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    add_rich(p, "免责声明：本文为虚拟仿真环境下的实验教学演示文本，全部阈值与仓位参数均为统一设定的实验条件，不构成任何证券的买卖建议；历史与模拟回测结果不代表未来收益。", size=10, color=GRAY)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)

def table(doc, headers, rows, widths=None, size=10.5, caption=None):
    if caption:
        c = doc.add_paragraph(); c.paragraph_format.space_before = Pt(6); c.paragraph_format.space_after = Pt(3)
        add_rich(c, caption, size=10.5, base_bold=True, color=ACCENT, cn_font="黑体")
    t = doc.add_table(rows=1, cols=len(headers)); t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, htext in enumerate(headers):
        cell = t.rows[0].cells[i]; cell.text = ""
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_rich(p, htext, size=size, base_bold=True, cn_font="黑体")
        shade(cell, "E2E8F0")
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            add_rich(cells[i].paragraphs[0], str(val), size=size)
    if widths:
        for i, w in enumerate(widths):
            for r in t.rows:
                r.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

doc = Document()
for sec in doc.sections:
    sec.top_margin = Cm(2.3); sec.bottom_margin = Cm(2.3)
    sec.left_margin = Cm(2.0); sec.right_margin = Cm(2.0)

# ============ 封面 ============
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(90)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_rich(p, "智享杯 · 全国大学生经济管理类实验案例分析大赛（学生赛区）", size=13, color=GRAY, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(24)
add_rich(p, "实验案例分析报告", size=30, base_bold=True, color=DARK, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(14)
add_rich(p, "AI 选股信号该配多大仓位？", size=19, base_bold=True, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_rich(p, "——虚拟仿真下的风险预算干预实验", size=15, base_bold=True, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(26)
add_rich(p, "关键词：仓位决策；风险预算；置信度校准；受控对照实验；虚拟仿真", size=11.5, color=GRAY)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_rich(p, "数据区间：2024-01-02 至 2025-10-28（数据截至 data_cutoff = 2025-10-28）", size=11, color=GRAY)
doc.add_page_break()

# ============ 摘要 ============
h1(doc, "摘要")
para(doc, "大模型投研工作台每日输出买/卖观点与置信度，但“信号配多大仓位”这一决定账户损益与回撤的环节，长期缺乏可训练、可考核、可复现的实验环境。本报告在虚拟仿真条件下构建受控对照实验：以 28 只沪深大盘蓝筹 2024-01-02 至 2025-10-28 共 410 个交易日的真实公开行情为沙盘，以固定种子（20261029）透明注入 6910 条 AI 选股信号，冻结信号与硬约束（单边成本 5bp、个股上限 20%、总仓上限 100%、回撤预算 -6%），仅变动“信号→仓位”转化规则，比较多策略对照（满仓等权 A、置信度分档 B、1/4 凯利+回撤干预 C），并依次实施样本外检验、参数敏感性与反事实分析。结果显示：校准失败的置信度不能驱动仓位（B 组与 A 组几乎重合）；交易成本是仓位规则的一等公民（A 组年化成本拖累 8.8%，C 组 4.3%）；风险预算干预是有条件的保险，其价值随仓位规模显现。全部结果可由所附代码一键复现。")
para(doc, "免责声明：本报告为教学演示文本，所有阈值与参数均为实验设定，不构成任何投资建议。", size=10.5, color=GRAY)

# ============ 一、问题提出 ============
h1(doc, "问题提出", "一、")
h2(doc, "背景：AI 投研链条上的“最后一厘米”", "1.1")
para(doc, "证券公司、基金公司正在批量引入大模型投研工作台：每日对数百只标的给出看多/看空观点与置信度。信号“准不准”已被大量研究讨论，但**信号“配多大仓位”——从信号到资金之间的转化规则——才是直接决定账户损益与回撤的环节**。现实中，这一环节往往依赖交易员临场经验，缺乏可训练、可考核、可复现的实验环境。")
para(doc, "从决策链的构成看，AI 的输出处在“信号生成”环节，其与最终交易决策的拟合程度，取决于“信号→仓位”的转化规则设计：**方向与置信度经仓位规则直接决定组合权重，移除信号则决策链失效**；人工不介入逐笔判断，仅设定换手率、集中度与回撤预算等硬约束；每一笔决策都可回溯至信号生成规则（种子固定）与模型原始输出（置信度）。本实验的全部设计围绕这一环节展开。")
h2(doc, "研究问题", "1.2")
bullet(doc, "**问题一（转化）**：同一组 AI 信号，在不同的仓位规则下，会产生多大差异的风险形态与成本结构？")
bullet(doc, "**问题二（校准）**：AI 输出的置信度，是否具备直接驱动仓位的校准质量？")
bullet(doc, "**问题三（干预）**：风险预算干预在不同仓位规模下价值几何？回撤预算线设在哪里最合理？")
h2(doc, "实验定位与证据承诺", "1.3")
para(doc, "本实验以**可验证证据**为纲，预先承诺五项证据设计：**多策略对照**（A/B/C 三组共用同一信号与约束）、**样本外检验**（前 70% 估计、后 30% 验证）、**反事实分析**（同一规则移除干预重跑）、**可解释归因**（绩效差异分解至仓位规则与成本拖累）、**复现能力**（随机种子固定、代码与参数全量公开、一键重跑）。结果不唯一：干预规则的设计空间开放，不同设计应得出不同结论并接受数据检验。")

# ============ 二、数据与方法 ============
h1(doc, "数据与方法", "二、")
h2(doc, "数据：真实行情 × 透明信号", "2.1")
table(doc,
    ["数据层", "性质", "来源与规则", "规模"],
    [
        ["行情层", "真实公开数据", "腾讯财经公开行情接口，28 只沪深大盘蓝筹前复权日线收盘价，2024-01-02 至 2025-10-28", "11480 行"],
        ["信号层", "透明模拟实验条件", "gen_signals.py 固定种子 20261029：方向 = 次日超额收益符号以 55% 概率取对（实测命中率 53.95%）；置信度 = 真实超额幅度线性映射 + 噪声（故意保留校准误差）", "6910 条"],
    ],
    widths=[2.0, 2.8, 9.0, 3.0], size=10)
para(doc, "采用“真实行情 + 透明信号”的二元结构，理由有二：其一，行情真实可重新下载核验，保证背景事实可核查；其二，信号生成机制完全公开，使全班在同一条件下实验，任何绩效差异都能干净地归因于仓位规则，而非信号噪声。每个数字都有“出生证明”：来源接口、生成脚本、随机种子全部明示，这是复现能力的根基。")
h2(doc, "方法：受控对照 + 四重检验", "2.2")
para(doc, "核心方法是**冻结信息集、只变动转化规则**的受控对照设计，配合四重检验：多策略对照识别规则效应，样本外检验排除运气与过拟合，参数敏感性刻画结论的适用边界，反事实分析分离干预机制本身的价值。归因方法上，将各组绩效差异分解为仓位结构差异与成本拖累差异两部分，使“AI 在决策链中起了什么作用”变得可解释、可追溯。")
h2(doc, "硬约束与变量控制", "2.3")
bullet(doc, "硬约束（教师统一设定，违反即方案无效）：单边交易成本 5bp；单一标的上限 20%；组合总仓位上限 100%；最大回撤预算 -6%（触及即触发干预）。")
bullet(doc, "时序纪律：信号在 t 日收盘后生成，只作用于 t+1 收益；任何参数估计只使用前 70% 样本内数据。")
bullet(doc, "人工角色：**人工仅设硬约束**（上述四条），不介入逐笔买卖判断——决策由规则对信号的响应自动生成，可回溯、可复核。")

# ============ 三、实验设计 ============
h1(doc, "实验设计", "三、")
h2(doc, "三组仓位规则", "3.1")
table(doc,
    ["组别", "规则", "设计意图"],
    [
        ["A 对照组", "有信号即满仓等权，无风险预算", "锚定“直觉做法”的基准"],
        ["B 实验组", "置信度分档固定分数（≥0.7 → 30%，0.55–0.7 → 20%）", "检验“置信度直接映射仓位”是否可行"],
        ["C 实验组", "样本内估计凯利分数 × 1/4 + 回撤触线减半", "定量风险预算 + 主动干预"],
    ],
    widths=[2.6, 9.4, 4.8], size=10)
h2(doc, "检验设计", "3.2")
bullet(doc, "**样本外检验**：参数不动，回测起点移至 70% 分位（后 123 个交易日）。")
bullet(doc, "**敏感性分析**：凯利缩放 1/8、1/4、1/2、1 倍 × 干预有无（全样本），识别结论成立的参数范围。")
bullet(doc, "**干预线敏感性**：回撤预算线 -3%、-6%、-9%（固定 1/4 凯利），回答“预算线设在哪里”。")
bullet(doc, "**反事实分析**：同一规则分别在有干预、无干预两种情形下运行，把“干预价值”从“仓位规模”中分离。")
h2(doc, "实验设计表", "3.3")
table(doc,
    ["环节", "设计", "目的"],
    [
        ["① 提出任务", "风险预算官任务书：角色、硬约束、五项交付物", "任务边界清晰"],
        ["② 说明条件", "数据规则说明表：来源、股票池、信号规则、样本划分", "条件可核查"],
        ["③ 设计方案", "三组对照 + 三重检验，参数预登记", "方案可比较"],
        ["④ 运行实验", "在线 Notebook 30 单元真实运行；run_all.py 一键复现", "过程可追溯"],
        ["⑤ 分析结果", "全样本、样本外、敏感性与反事实、干预线敏感性", "结果可解释"],
        ["⑥ 形成建议", "对金融机构、监管与教学、AI 系统建设方的三条建议", "建议可落地"],
    ],
    widths=[2.6, 9.2, 5.0], size=10)

# ============ 四、结果与发现 ============
h1(doc, "结果与发现", "四、")
h2(doc, "信号诊断：置信度存在系统性过度自信", "4.1")
para(doc, "6910 条信号的方向命中率 53.95%（设定 55%），日均 16.9 条，覆盖率 60.2%，看多占比 50.3%。置信度均值 0.871，但按置信度分桶的真实命中率在 50.9%–58.3% 之间波动、**无单调性**：[0.5,0.6) 桶 58.3%（446 条）、[0.6,0.7) 桶 50.9%（709 条）、[0.7,0.8) 桶 54.3%（746 条）、[0.8,0.9) 桶 54.1%（712 条）、[0.9,1.0) 桶 54.0%（4214 条，占 61%）。")
golden(doc, "模型说出的 0.9，是它的情绪，不是市场的概率——未经校准的置信度直接映射仓位，等于把模型的过度自信放大成账户的过度敞口。")
h2(doc, "全样本对照：同样的信号，完全不同的风险形态", "4.2")
table(doc,
    ["组别", "累计收益", "年化波动", "夏普", "最大回撤", "卡玛", "日均换手", "年化成本拖累"],
    [
        ["A 满仓等权", "23.2%", "16.8%", "0.70", "-12.4%", "1.11", "0.70", "8.8%"],
        ["B 置信度分档", "22.8%", "16.8%", "0.68", "-12.4%", "1.09", "0.73", "9.2%"],
        ["C 1/4凯利+干预", "18.6%", "16.6%", "0.55", "-9.3%", "1.19", "0.34", "4.3%"],
    ],
    widths=[3.2, 2.0, 1.9, 1.6, 2.0, 1.6, 2.0, 2.7], size=9.5)
para(doc, "**判断先行**：三组的差异全部来自仓位规则——信号、行情、约束完全相同。C 组以约 4.6 个百分点的收益代价（18.6% vs 23.2%），把最大回撤压缩 3.1 个百分点（-9.3% vs -12.4%），年化成本拖累从 8.8% 降到 4.3%，卡玛比率 1.19 优于 A 组的 1.11。**证据链**：成本归因显示 A 组日均换手 0.70、乘以单边 5bp 即年化约 8.8 个百分点的拖累；C 组低换手（0.34）使成本近乎减半。**配置含义**：凯利集中持仓降不了波动（三组波动几乎相同），风险预算的价值要用回撤与成本衡量，而不是夏普。数据截至 2025-10-28，全部数字可由所附代码一键复现。")
golden(doc, "同样的信号，不同的仓位规则，买到的是完全不同的风险——分水岭不在预测，在转化。")
h2(doc, "样本外检验：风险预算是“有价格的保险”", "4.3")
para(doc, "后 30% 样本（123 个交易日）恰为蓝筹上行段：A 组年化 41.3%、夏普 2.71、最大回撤 -4.1%、换手升至 0.91（成本拖累约 11.4%）；C 组年化 13.5%、波动 7.4%、最大回撤 -2.5%、夏普 1.56、卡玛 5.49。")
para(doc, "**判断先行**：上行段风险预算组大幅落后——这不是失败，而是保险的定价。**证据链**：满仓组的高换手在上行段被成本进一步放大（11.4%），而 C 组以更低的波动（7.4% vs 14.5%）与更浅的回撤（-2.5% vs -4.1%）换取了绝对收益的落后。**配置含义**：评估干预机制不能只看单一区间——只看这一段会得出“预算无用”的误判，只看回撤段又会得出“预算万能”的误判；两个区间合起来读，才是完整的证据。")
golden(doc, "牛市里嫌它贵、回撤来临时谢它还在的风险预算，是账户里真正的安全带——保费看得见的年份，恰是它最便宜的年份。")
h2(doc, "敏感性与反事实：干预的价值随仓位规模显现", "4.4")
table(doc,
    ["凯利缩放", "有干预（累计）", "无干预（累计）", "最大回撤（有/无）", "解读"],
    [
        ["1/8", "-4.7%", "-4.7%", "-4.7% / -4.7%", "仓位足够轻，干预无事可做"],
        ["1/4", "18.6%", "22.7%", "-9.3% / -9.3%", "-6% 预算线对轻仓位偏松"],
        ["1/2", "—", "—", "-12.3% / -15.9%", "干预价值开始显现"],
        ["1 倍", "20.6%", "41.6%", "-12.6% / -15.7%", "满仓凯利不可取"],
    ],
    widths=[2.2, 3.0, 3.0, 4.0, 4.6], size=10)
para(doc, "**判断先行**：反事实分析（移除干预）证明干预是“有条件的保险”——1/8 档有无干预完全相同，1/2 档回撤从 -15.9% 收窄至 -12.3%，1 倍档累计收益从 41.6% 降至 20.6% 但回撤同时收窄。**证据链**：干预线敏感性（1/4 凯利全样本）显示 -3% 线卡玛 1.49、-6% 线 1.19、-9% 线 1.41——太松等于没干预，太紧则过度止损。**配置含义**：机构应像管理保费一样成对设计“仓位规模 × 干预线”，预算线必须与仓位规模匹配。")
golden(doc, "干预线不是画在哪都行的红线——仓位多大、线就得多紧，错配的预算等于没有预算。")

# ============ 五、结论与启示 ============
h1(doc, "结论与启示", "五、")
h2(doc, "三条结论", "5.1")
bullet(doc, "**预测力 ≠ 盈利能力，分水岭在转化规则**：方向命中率 53.95% 的同一信号，在不同仓位规则下产生完全不同的风险形态；决定“AI 在决策链中最终贡献了什么”的，是“信号→仓位”这一环，而非信号本身。")
bullet(doc, "**校准失败的置信度不能驱动仓位**：置信度均值 0.871 而分桶命中率无单调性（高置信桶仅 54.0%），B 组与 A 组几乎重合（22.8% vs 23.2%）——置信度只能作为参考输入，须经凯利打折与硬约束双重衰减。")
bullet(doc, "**风险预算干预是有条件的保险**：其价值随仓位规模上升而显现，且预算线须与仓位规模匹配（1/4 凯利配 -3% 线卡玛 1.49、配 -6% 线 1.19）；移除干预的反事实（1/2 档回撤 -15.9%、1 倍档累计 41.6% 但回撤 -15.7%）是评估其代价的必要基准。")
h2(doc, "方法论启示：让 AI 的作用可验证、可复核、可追溯", "5.2")
para(doc, "本实验的方法论价值在于把“AI 在决策链中起了什么作用”变成一组可检验的命题：**多策略对照**识别规则效应，**样本外检验**排除运气，**反事实分析**给干预定价，**可解释归因**把绩效差异分解到仓位结构与成本拖累，**复现能力**（种子固定、参数预登记、一键重跑）使每一个数字可回查。这五项可验证证据，同样适用于评审任何“AI 参与决策”的方案：凡不能提供者，其结论应视为未经验证。")
para(doc, "对 AI 系统建设方的对应要求：置信度输出必须附带校准曲线与历史命中率分桶报告；未经验证的置信度不得直接驱动资金分配；人工仅保留硬约束设定权，决策链路对输入语料与模型原始输出完全可回溯。")
h2(doc, "局限与边界", "5.3")
bullet(doc, "仿真未建模滑点、流动性冲击与涨跌停摩擦，结论不能直接外推至实盘执行环节；")
bullet(doc, "样本期为 2024-01 至 2025-10 的单一市场段（含一段蓝筹上行），区间结构会影响样本外对比的具体数值；")
bullet(doc, "信号为透明模拟而非真实大模型输出——这是受控归因的设计前提，真实信号的接入（保持规则不变重跑并分解贡献）列为开放挑战任务；")
bullet(doc, "凯利分数对收益率均值估计高度敏感，1/4 缩放是保守化处理而非最优解；滚动再估计与多周期验证列为扩展方向。")
para(doc, "上述边界在全部配套材料中如实标注——明示边界本身是数据诚实素养的一部分，也是本实验区别于“演示型作品”的特征。")
golden(doc, "AI 是外骨骼，扣动扳机的必须是懂风险预算的人。")
disclaimer(doc)

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("saved:", OUT)
