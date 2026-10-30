# -*- coding: utf-8 -*-
"""案例报告 V4：规范论文排版
黑体标题 / 宋体正文（1.5倍行距、首行缩进2字符）/ 三线表 / 中英摘要 / GB-T 7714 参考文献 / 页码
内容含 V4 新分析：5.1 成本扫描、5.2 置信度再校准闭环（全部实跑数字）
"""
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "/Users/Admin/Documents/kimi/tasks/2026-10-24/14-58-19-b5e2402f/教学指导文档/案例报告.docx"
FIGDIR = "/Users/Admin/Documents/kimi/tasks/2026-10-24/14-58-19-b5e2402f/教学指导文档"

def set_font(run, size=12, bold=False, color=None, cn_font="宋体", en_font="Times New Roman"):
    run.font.size = Pt(size); run.font.bold = bold
    run.font.name = en_font
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
    p.paragraph_format.space_before = Pt(16); p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.5
    add_rich(p, f"{num}　{text}" if num else text, size=15, base_bold=True, cn_font="黑体")

def h2(doc, text, num=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    add_rich(p, f"{num}　{text}" if num else text, size=13, base_bold=True, cn_font="黑体")

def para(doc, text, size=12, indent=True, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.5
    if indent:
        p.paragraph_format.first_line_indent = Pt(24)
    add_rich(p, text, size=size, color=color)

def caption(doc, text, above=False):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6 if above else 2)
    p.paragraph_format.space_after = Pt(4 if above else 8)
    p.paragraph_format.line_spacing = 1.2
    add_rich(p, text, size=10.5, base_bold=True, cn_font="黑体")

def figure(doc, path, cap, width_cm=15.2):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))
    caption(doc, cap)

def three_line_table(doc, headers, rows, cap, widths=None, size=10.5):
    """三线表：表题在上；顶线/底线 1.5pt，栏目线 0.75pt，无竖线无底纹"""
    caption(doc, cap, above=True)
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = t._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge, szv in [("top", "12"), ("bottom", "12")]:
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single"); el.set(qn("w:sz"), szv)
        el.set(qn("w:space"), "0"); el.set(qn("w:color"), "000000")
        borders.append(el)
    for edge in ["left", "right", "insideH", "insideV"]:
        el = OxmlElement(f"w:{edge}"); el.set(qn("w:val"), "nil")
        borders.append(el)
    tblPr.append(borders)
    for i, htext in enumerate(headers):
        cell = t.rows[0].cells[i]; cell.text = ""
        tcPr = cell._tc.get_or_add_tcPr()
        tcB = OxmlElement("w:tcBorders")
        bot = OxmlElement("w:bottom")
        bot.set(qn("w:val"), "single"); bot.set(qn("w:sz"), "6")
        bot.set(qn("w:space"), "0"); bot.set(qn("w:color"), "000000")
        tcB.append(bot); tcPr.append(tcB)
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_rich(p, htext, size=size, base_bold=True, cn_font="黑体")
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
            add_rich(p, str(val), size=size)
    if widths:
        for i, w in enumerate(widths):
            for r in t.rows:
                r.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def disclaimer(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.line_spacing = 1.3
    add_rich(p, "免责声明：本文为虚拟仿真环境下的实验教学演示文本，全部阈值与仓位参数均为统一设定的实验条件，不构成任何证券的买卖建议；历史与模拟回测结果不代表未来收益。", size=10, color=RGBColor(0x47, 0x55, 0x69))

def add_page_number(doc):
    for sec in doc.sections:
        p = sec.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = "PAGE"
        f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
        run._r.append(f1); run._r.append(it); run._r.append(f2)
        set_font(run, size=9)

doc = Document()
for sec in doc.sections:
    sec.top_margin = Cm(2.54); sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(3.0); sec.right_margin = Cm(3.0)
add_page_number(doc)

GRAY = RGBColor(0x47, 0x55, 0x69)

# ============ 标题与摘要 ============
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(4)
add_rich(p, "AI 选股信号该配多大仓位？", size=16, base_bold=True, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(10)
add_rich(p, "——虚拟仿真下的风险预算干预实验", size=14, base_bold=True, cn_font="黑体")

p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
add_rich(p, "**摘要：**", size=12, base_bold=True, cn_font="黑体")
para(doc, "大模型投研工作台每日输出买/卖观点与置信度，但“信号配多大仓位”这一直接决定账户损益与回撤的转化环节，长期缺乏可训练、可考核、可复现的实验环境。本文构建虚拟仿真条件下的受控对照实验：以 28 只沪深大盘蓝筹 2024-01-02 至 2025-10-28 共 410 个交易日的真实公开行情为沙盘，以固定随机种子（20261029）透明注入 6910 条 AI 选股信号，在统一规则约束（单边成本 5bp、个股上限 20%、总仓上限 100% 为硬约束；回撤触线 -6% 为软干预）下比较多策略对照（满仓等权 A、置信度分档 B、1/4 凯利+回撤干预 C），并依次实施样本外检验、参数敏感性与反事实分析。结果表明：置信度均值 0.871 而真实命中率约 54% 且分桶无单调性，校准失败的置信度不能驱动仓位；交易成本是仓位决策的一等公民（A 组年化成本拖累 8.8%，C 组 4.3%）；风险预算干预是有条件的保险，其价值随仓位规模上升而显现。拓展分析进一步发现：策略排序是成本的函数，单边成本升至 10bp 时 C 组夏普反超 A、B 组；对置信度做样本内分桶再校准可将样本外平均校准误差从 0.221 降至 0.089，但桶间区分度不变——“校准能修复模型说的，修不了模型知的”。全部结果可由所附代码一键复现。", indent=False)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(10); p.paragraph_format.line_spacing = 1.5
add_rich(p, "关键词", size=12, base_bold=True, cn_font="黑体")
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(12); p.paragraph_format.line_spacing = 1.5
para(doc, "仓位决策；风险预算；置信度校准；受控对照实验；交易成本；虚拟仿真", indent=False)

p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
add_rich(p, "Abstract", size=12, base_bold=True, cn_font="黑体")
para(doc, "Large language model research platforms now emit daily buy/sell calls with confidence scores, yet the mapping from signals to position sizes—the last mile of the AI-driven decision chain—remains untrained. We build a controlled virtual-simulation experiment: 410 trading days of real, publicly verifiable quotes for 28 CSI large-cap stocks, into which 6,910 transparently simulated AI signals (fixed seed 20261029) are injected. Three position-sizing rules—full equal-weight (A), confidence-tiered (B), and quarter-Kelly with drawdown intervention (C)—are compared under identical hard constraints (5bp cost, 20% single-stock cap, 100% gross cap, -6% drawdown budget), with out-of-sample validation, parameter sensitivity, counterfactual analysis and a full reproducibility chain. Confidence proves poorly calibrated (mean 0.871 versus about 54% realized accuracy), transaction cost emerges as a first-class citizen (8.8% annual drag for A versus 4.3% for C), and risk-budget intervention behaves as priced insurance whose value rises with position scale. Two extensions sharpen the lessons: a cost scan shows the strategy ranking inverts at 10bp, and a recalibration loop (in-sample bucket rates applied out-of-sample) cuts mean calibration error from 0.221 to 0.089 while leaving bucket-level discrimination unchanged—calibration fixes what the model says, not what it knows.", indent=False, color=GRAY)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(10)
para(doc, "Keywords: position sizing; risk budgeting; confidence calibration; controlled experiment; transaction cost; virtual simulation", size=12, indent=False, color=GRAY)

# ============ 1 引言 ============
h1(doc, "引言", "1")
h2(doc, "研究背景：AI 投研链条上的“最后一厘米”", "1.1")
para(doc, "证券公司、基金公司正在批量引入大模型投研工作台：每日对数百只标的输出看多/看空观点与置信度，AI 生成的信号已成投研流程的标准输入。信号“准不准”已被大量研究讨论，但信号“配多大仓位”——从信号到资金的转化规则——才直接决定账户损益与回撤，而这一环节在现实中长期依赖交易员临场经验，缺乏可训练、可考核、可复现的实验环境。从决策链的构成看，AI 的输出处在“信号生成”环节，其与最终交易决策的拟合程度取决于“信号→仓位”的转化规则设计：方向与置信度经仓位规则直接决定组合权重，移除信号则决策链失效；人工不介入逐笔判断，仅设定换手率、集中度与回撤预算等硬约束；每一笔决策都可回溯至信号生成规则（种子固定）与模型原始输出（置信度）。")
h2(doc, "研究问题", "1.2")
para(doc, "本文回答三个递进的问题：其一（转化），同一组 AI 信号在不同的仓位规则下，会产生多大差异的风险形态与成本结构？其二（校准），AI 输出的置信度是否具备直接驱动仓位的校准质量，若不足，工程上的再校准能否补救？其三（干预），风险预算干预在不同仓位规模下价值几何，回撤预算线设在哪里最合理？")
h2(doc, "研究贡献", "1.3")
para(doc, "本文的贡献在于把“AI 在投研决策链条中所处环节及其与最终交易决策的拟合程度”变成一组可检验的命题，并以五项可验证证据支撑：**多策略对照**（三组规则共用同一冻结信号与约束）、**样本外检验**（前 70% 估计、后 30% 验证）、**反事实分析**（同一规则移除干预重跑）、**可解释归因**（绩效差异分解至仓位结构与成本拖累）与**复现能力**（随机种子固定、参数预登记、一键重跑）。在既有 AI+实验教学案例普遍“演示有余、检验不足”的背景下，本实验把成本、约束与不确定性全部写回沙盘，并给出干预机制的反事实定价。")

# ============ 2 文献与理论基础 ============
h1(doc, "文献与理论基础", "2")
h2(doc, "组合选择与凯利准则", "2.1")
para(doc, "均值—方差框架确立了“收益—风险”权衡的组合选择起点（Markowitz, 1952）；凯利准则从信息率角度给出使长期复合增长率最大化的最优下注比例（Kelly, 1956），并因其在全下注时的巨大波动而被普遍建议缩放使用（Thorp, 2006）。本文的 C 组规则即采用样本内估计的 1/4 凯利作为仓位基准，并以回撤预算线作为主动干预触发器。")
h2(doc, "回测过拟合与多重检验", "2.2")
para(doc, "策略评估的可靠性依赖对选择偏差与过拟合的控制。Deflated Sharpe Ratio 指出：在多次试验与长回测中，夏普比率会被系统性高估（Bailey & López de Prado, 2014）；横截面研究中广泛存在的 t 统计量筛选同样夸大发现（Harvey, Liu & Zhu, 2016）。这构成本文“参数预登记 + 样本外检验 + 敏感性网格”设计的文献依据：任何在样本外子区间上调过的参数都须声明并降级为探索性结果。")
h2(doc, "过度自信与置信度校准", "2.3")
para(doc, "心理学研究早已证明人类与模型均存在系统性过度自信（Moore & Healy, 2008）；概率预报的诊断性检验提供了“置信度—频率”对齐的标准方法（Murphy & Winkler, 1992）。本文把故意保留校准误差的置信度作为诊断素材，将可靠度曲线（分桶命中率）引入投资决策教学，并进一步以“样本内再校准 → 样本外验证”的闭环量化校准工程能修复什么、不能修复什么。")
h2(doc, "交易成本与执行", "2.4")
para(doc, "交易成本是策略从“纸面”到“账户”的核心摩擦，最优执行文献将其形式化为价格冲击与换手节奏的权衡（Almgren & Chriss, 2000）。本文不建模滑点与流动性冲击，但把单边成本作为统一硬约束写入全部规则，并通过成本扫描刻画策略排序对成本参数的敏感性。")

# ============ 3 数据与研究设计 ============
h1(doc, "数据与研究设计", "3")
h2(doc, "数据：真实行情 × 透明信号的二元结构", "3.1")
para(doc, "行情层为真实公开数据：腾讯财经公开行情接口的 28 只沪深大盘蓝筹前复权日线收盘价，样本期 2024-01-02 至 2025-10-28（数据截至 data_cutoff = 2025-10-28），共 410 个交易日、11480 行，任何人可重新下载核验。信号层为透明模拟的实验条件：以固定种子 20261029 注入 6910 条买/卖信号，方向等于次日超额收益符号以 55% 概率取对（实测命中率 53.95%），置信度取真实超额幅度的线性映射加噪声（**故意保留校准误差**，作为 4.1 节与 5.2 节的诊断与治理素材）。二元结构的理由：行情真实保证背景事实可核查；信号机制公开保证全班在同一条件下实验，任何绩效差异都能干净地归因于仓位规则，而非信号噪声。")
h2(doc, "硬约束与变量控制", "3.2")
para(doc, "全部规则在统一约束下运行：单边交易成本 5bp、单一标的上限 20%、组合总仓位上限 100% 为硬约束（违反即方案无效）；**回撤触线 -6% 为软干预线**——触及即仓位减半，降低回撤概率但不保证回撤不突破（本案例 C 组最大回撤 -9.3% 即为明证，4.10 节将进一步拆解）。**人工仅设这些约束**，不介入逐笔买卖判断。变量控制由五层构成：信号冻结（6910 条由固定种子一次生成，全实验共享）、约束统一（四条硬约束对三组一致）、样本划分预登记（前 70% 样本内估计、后 30% 样本外检验）、参数来源限定（凯利分数与干预参数只用样本内估计）、反事实对照（同一规则在干预有无两种情形下分别运行）。")
h2(doc, "三组仓位规则与检验设计", "3.3")
three_line_table(doc,
    ["组别", "仓位规则", "设计意图"],
    [
        ["A 对照组", "有信号即满仓等权，无风险预算", "锚定“直觉做法”的基准"],
        ["B 实验组", "置信度分档固定分数（≥0.7 → 30%，0.55–0.7 → 20%）", "检验“置信度直接映射仓位”是否可行"],
        ["C 实验组", "样本内估计凯利分数 × 1/4 + 回撤触线减半", "定量风险预算 + 主动干预"],
    ],
    "表 1　三组仓位规则", widths=[2.4, 8.6, 5.0])
para(doc, "检验设计为四重：样本外检验（参数不动，回测起点移至 70% 分位，后 123 个交易日）；敏感性分析（凯利缩放 1/8、1/4、1/2、1 倍 × 干预有无，全样本）；干预线敏感性（预算线 -3%、-6%、-9%，固定 1/4 凯利）；反事实分析（同一规则移除干预）。此外，第 5 节增加两项拓展分析：交易成本扫描（0/2.5/5/10bp）与置信度再校准闭环（样本内校准 → 样本外验证）。")

# ============ 4 实证结果 ============
h1(doc, "实证结果", "4")
h2(doc, "信号诊断：置信度存在系统性过度自信", "4.1")
para(doc, "6910 条信号的方向命中率 53.95%（设定 55%），日均 16.9 条，覆盖率 60.2%，看多占比 50.3%。置信度均值 0.871，但按置信度分桶的真实命中率在 50.9%–58.3% 之间波动、无单调性（表 2）。这意味着置信度并不携带真实的区分度信息：模型“说 0.9”的信号，真实命中概率与“说 0.6”的信号几乎相同。")
three_line_table(doc,
    ["置信度桶", "[0.5,0.6)", "[0.6,0.7)", "[0.7,0.8)", "[0.8,0.9)", "[0.9,1.0)"],
    [
        ["信号数", "446", "709", "746", "712", "4214（占 61%）"],
        ["真实方向命中率", "58.3%", "50.9%", "54.3%", "54.1%", "54.0%"],
    ],
    "表 2　置信度校准分桶（全样本；其余 83 条信号置信度低于 0.5，不在分桶内）",
    widths=[3.4, 2.5, 2.5, 2.5, 2.5, 3.1])
para(doc, "把信号当作一个因子、用量化行业的语言重述：全样本 IC（信号方向与次日超额收益的每日截面秩相关）均值为 0.062、ICIR 0.249、t 值 5.04、IC 为正占比 60.1%——**预测力微弱但统计显著**，属弱因子的典型量级。进一步按置信度固定宽度分桶考察次日超额收益：各桶无单调结构，最高置信桶 [0.95,1.0) 日均超额 +6.05bp 而中位数深达 -66.7bp（均值被 2024 年 10 月暴涨日的尾部收益主导），最低置信桶命中率反而最高（63.1%）——均值型与中位数型度量交叉印证：置信度不携带稳定的区分度。教学要点：**评估任何 AI 信号，先问 IC 与 ICIR，再谈仓位规则**。")
h2(doc, "全样本对照：同样的信号，不同的风险形态", "4.2")
three_line_table(doc,
    ["组别", "累计收益", "年化波动", "夏普比率", "最大回撤", "卡玛比率", "日均换手", "年化成本拖累"],
    [
        ["A 满仓等权", "23.2%", "16.8%", "0.70", "-12.4%", "1.11", "0.70", "8.8%"],
        ["B 置信度分档", "22.8%", "16.8%", "0.68", "-12.4%", "1.09", "0.73", "9.2%"],
        ["C 1/4凯利+干预", "18.6%", "16.6%", "0.55", "-9.3%", "1.19", "0.34", "4.3%"],
    ],
    "表 3　全样本三组对照（同一信号与硬约束，差异全部来自仓位规则）",
    widths=[2.9, 1.9, 1.8, 1.7, 1.8, 1.8, 1.7, 2.4], size=9.5)
para(doc, "三组绩效差异全部来自仓位规则：信号、行情与约束完全相同。C 组以约 4.6 个百分点的收益代价（18.6% 对 23.2%）换取最大回撤压缩 3.1 个百分点（-9.3% 对 -12.4%）与成本拖累减半（4.3% 对 8.8%），卡玛比率 1.19 优于 A 组的 1.11。成本归因显示：A 组日均换手 0.70，乘以单边 5bp 即年化约 8.8 个百分点的拖累；C 组低换手（0.34）使成本近乎减半。值得注意的是，三组年化波动几乎相同——凯利集中持仓并未降低波动，风险预算的价值须以回撤与成本衡量，而非夏普。")
figure(doc, FIGDIR + "/report_fig1_nav.png",
       "图 1　固定 AI 信号、不同仓位规则下的组合累计净值（虚线为样本外起点）")
h2(doc, "样本外检验：风险预算是“有价格的保险”", "4.3")
para(doc, "后 30% 样本（123 个交易日）恰为蓝筹上行段：A 组年化 41.3%、夏普 2.71、最大回撤 -4.1%、换手升至 0.91（成本拖累约 11.4%）；C 组年化 13.5%、波动 7.4%、最大回撤 -2.5%、夏普 1.56、卡玛 5.49。上行段风险预算组大幅落后——这不是失败，而是保险的定价：机会成本可见、可计量。评估干预机制不能只看单一区间：只看上行段会得出“预算无用”的误判，只看回撤段又会得出“预算万能”的误判；两个区间合起来读才是完整证据。")
figure(doc, FIGDIR + "/report_fig2_dd.png",
       "图 2　三组组合回撤曲线与 -6% 风险预算干预线")
h2(doc, "敏感性与反事实：干预的价值随仓位规模显现", "4.4")
three_line_table(doc,
    ["凯利缩放", "有干预（累计收益）", "无干预（累计收益）", "最大回撤（有/无）", "解读"],
    [
        ["1/8", "-4.7%", "-4.7%", "-4.7% / -4.7%", "仓位足够轻，干预无事可做"],
        ["1/4", "18.6%", "22.7%", "-9.3% / -9.3%", "-6% 预算线对轻仓位偏松"],
        ["1/2", "28.9%", "34.7%", "-12.3% / -15.9%", "干预价值开始显现"],
        ["1 倍", "20.6%", "41.6%", "-12.6% / -15.7%", "满仓凯利不可取"],
    ],
    "表 4　凯利缩放 × 干预有无的敏感性与反事实（全样本）",
    widths=[1.8, 3.2, 3.2, 3.4, 5.4], size=10)
para(doc, "反事实分析（移除干预）证明干预是“有条件的保险”：1/8 档有无干预完全相同；1/2 档回撤从 -15.9% 收窄至 -12.3%；1 倍档累计收益从 41.6% 降至 20.6% 但回撤同步收窄。干预线敏感性（1/4 凯利全样本）显示 -3% 线卡玛 1.49、-6% 线 1.19、-9% 线 1.41——太松等于没有干预，太紧则过度止损；预算线必须与仓位规模成对设计。")
figure(doc, FIGDIR + "/report_fig3_sens.png",
       "图 3　仓位规模敏感性：凯利缩放系数 × 回撤干预（全样本，含反事实情形）")

# ============ 5 拓展分析 ============
h1(doc, "拓展分析", "5")
h2(doc, "交易成本扫描：策略排序是成本的函数", "5.1")
para(doc, "前述结论均建立在单边成本 5bp 的设定上。固定信号与规则，把单边成本从 0 扫描至 10bp（全样本），结果见表 5。")
three_line_table(doc,
    ["单边成本(bp)", "A 累计", "A 夏普", "B 累计", "B 夏普", "C 累计", "C 夏普"],
    [
        ["0", "56.3%", "1.16", "58.8%", "1.21", "29.1%", "0.90"],
        ["2.5", "48.0%", "0.99", "48.0%", "0.99", "25.7%", "0.78"],
        ["5（基准）", "23.2%", "0.70", "22.8%", "0.68", "18.6%", "0.55"],
        ["10", "8.3%", "0.19", "7.2%", "0.15", "12.0%", "0.32"],
    ],
    "表 5　交易成本扫描：三组绩效对成本参数的敏感性（全样本）",
    widths=[2.6, 2.3, 2.0, 2.3, 2.0, 2.3, 2.0])
para(doc, "三点发现：其一，策略排序不是常数，而是成本的函数——零成本下 B 组（58.8%，夏普 1.21）反超 A 组（56.3%，1.16），说明置信度分档并非毫无信息，高置信桶信号确有微弱毛利；但 5bp 时这份毛利恰被 B 组更高的换手成本（9.2% 对 8.8%）吃平；**单边成本升至 10bp 时 C 组夏普（0.32）反超 A、B 组（0.19、0.15），排序反转**。其二，成本每翻一倍，A、B 组夏普近乎腰斩，C 组只温和下降——低换手规则对成本参数的敏感度显著更低，仓位规则的选择本质上是换手率预算的选择。其三，评估任何“AI 信号 → 仓位”方案，必须报告结论对成本参数的稳健性。0 与 10bp 是机制实验的极端情形，不代表现实报价。")
figure(doc, FIGDIR + "/report_fig4_cost.png",
       "图 4　交易成本扫描：三组夏普比率随单边成本的变化（全样本；竖虚线为基准 5bp）")
h2(doc, "置信度再校准闭环：样本内校准，样本外验证", "5.2")
para(doc, "既然 4.1 节诊断出置信度系统性过度自信，一个自然的工程问题是：再校准能否补救？做法：在样本内把置信度按 0.05 宽度分十桶，计算每桶真实命中率；将全部信号的置信度替换为其所在桶的样本内命中率（即“再校准”——模型此后输出的不再是 0.9，而是“我这一档历史上对 0.53”）；再到样本外检验校准质量与区分度的变化（表 6）。")
three_line_table(doc,
    ["置信度桶", "原始 OOS 条数", "原始 OOS 命中率", "再校准 OOS 条数", "再校准 OOS 命中率"],
    [
        ["[0.50,0.55)", "91", "63.7%", "1735", "53.8%"],
        ["[0.55,0.60)", "96", "53.1%", "220", "54.1%"],
        ["[0.60,0.65)", "111", "47.7%", "91", "63.7%"],
        ["[0.65,0.70)", "112", "54.5%", "0", "—"],
        ["[0.70,0.75)", "109", "59.6%", "0", "—"],
        ["[0.75,0.80)", "117", "56.4%", "0", "—"],
        ["[0.80,0.85)", "125", "54.4%", "0", "—"],
        ["[0.85,0.90)", "115", "47.8%", "0", "—"],
        ["[0.90,0.95)", "105", "61.0%", "0", "—"],
        ["[0.95,1.00)", "1065", "53.4%", "0", "—"],
    ],
    "表 6　置信度再校准前后的样本外校准对比（固定宽度十桶）",
    widths=[3.2, 3.0, 3.2, 3.0, 3.2], size=9.5)
para(doc, "三点结论。其一，**校准在工程上完全可行**：再校准把样本外平均校准误差（各桶命中率与所报置信度之差的绝对值均值）从 0.221 压到 0.089——“说 0.9”被修正为“该档历史命中 0.53”，模型输出的“说”与“做”重新对齐，任何大模型供应商都应内建这一步。其二，**校准修复不了区分度**：再校准是保序替换，只修标签、不改排序，桶间命中率依旧无单调结构，且样本外约 85% 的信号落入同一桶（[0.50,0.55)）——置信度仍不构成仓位依据。一句话：**再校准能修复“模型说的”，修复不了“模型知的”——置信度能否驱动仓位，取决于桶间真实区分度，而非校准技巧。**其三，**分布漂移真实存在**：样本外置信度均值由 0.876 降至 0.860，12.7% 的样本外信号跌破样本内十分位（P10 = 0.63）——AI 系统上线后置信度分布本身会漂移，校准必须定期重做，这为“可解释归因 + 持续监控”提供了又一实证。")

figure(doc, FIGDIR + "/report_fig5_calib.png",
       "图 5　置信度再校准前后的样本外校准曲线（对角线为完美校准；玫红点为原始十桶，绿方块为再校准）")
h2(doc, "信号衰减分析：执行时点的量化依据", "5.3")
para(doc, "全部仓位规则建立在“t 日收盘后生成信号、t+1 执行”之上，其量化依据来自信号衰减检验：把“次日超额收益取对”的命中判定分别放到 t+1、t+2、t+3、t+5 上重算（同一样本、同一口径，6910 条信号），方向命中率从 t+1 的 53.95% 单调衰减——t+2 跌至 50.6%，t+3 起跌破 50%（49.8%），t+5 已无信息含量。三点含义：其一，**信号有效期以日计**，“AI 说买”之后每拖延一天，信息的价值就折损一截，“信号→仓位”必须是日频闭环；其二，仓位规则无需预测信号何时失效，只需在有效期内完成转化——转化链路的摩擦（成本、干预、约束）因此比信号本身更值得优化；其三，对 AI 系统建设方而言，投研信号的交付时点与执行时点之间的每一分钟延迟，都是未被计量的 alpha 损耗。")

h2(doc, "平均敞口匹配基准：风险预算的第一杠杆是仓位规模", "5.4")
para(doc, "A/B/C 三组同时改变了平均敞口、集中度、换手与干预机制，因此“C 组回撤更低”不能直接归因于干预机制。本节补上基准：先测各规则的平均总敞口（A 满仓 77.7%、C′ 1/4 凯利无干预 48.5%、C 1/4 凯利+干预 43.8%），再构造“平均敞口与 C 相同、等权持有、不触发干预”的静态基准 S，四者同表比较（表 7）。")
three_line_table(doc,
    ["基准", "累计收益", "年化波动", "夏普比率", "最大回撤", "卡玛比率", "日均换手", "平均敞口"],
    [
        ["S 静态等权（敞口匹配 C，无干预）", "18.1%", "11.8%", "0.74", "-7.3%", "1.46", "0.39", "43.8%"],
        ["C 1/4凯利+回撤干预", "18.6%", "16.6%", "0.55", "-9.3%", "1.19", "0.34", "43.8%"],
        ["C′ 1/4凯利（无干预）", "22.7%", "16.8%", "0.68", "-9.3%", "1.44", "0.38", "48.5%"],
        ["A 满仓等权", "23.2%", "16.8%", "0.70", "-12.4%", "1.11", "0.70", "77.7%"],
    ],
    "表 7　平均敞口匹配基准对照（全样本；S 的平均敞口被标定为 C 组水平）",
    widths=[5.0, 1.8, 1.8, 1.7, 1.8, 1.8, 1.7, 1.8], size=9.5)
para(doc, "三点发现。其一，**平均敞口是第一杠杆**：A 组敞口 77.7%，C′ 组仅 48.5%，敞口降约三成，回撤从 -12.4% 收窄至 -9.3%，累计收益几乎不变（23.2% vs 22.7%）——所谓“风险预算”，首先就是“少拿仓位”本身。其二，**敞口匹配后凯利集中持仓并不优于静态等权**：同样约 43.8% 敞口，静态基准 S 的最大回撤 -7.3%（比 C 浅 2.0 个百分点）、卡玛 1.46（高于 C 的 1.19）、夏普 0.74（高于 0.55）——C 组相对 S 并无优势，其优势全部来自仓位更轻。其三，**触线减半在轻仓位下几乎不产生作用**：C 与 C′ 的最大回撤同为 -9.3%，而 C 的累计收益少 4.1 个百分点——-6% 触线对 1/4 凯利规模过松。")
para(doc, "因此本报告的结论修正为三层排序：**平均敞口 ＞ 持仓分散度 ＞ 触发式干预**。先把总仓位管住，再谈分散，最后才是触发规则；跳过前两层直接设计干预线，等于在错误的规模上做精细化管理。这一处自我修正是方法论示范：如果一个基准能推翻自己的结论，就必须补上这个基准并如实报告——这比任何漂亮的回测数字更接近“可验证、可复核”的本意。")

# ============ 6 结论与启示 ============
h1(doc, "结论与启示", "6")
h2(doc, "研究结论", "6.1")
bullet_l = [
    "**预测力 ≠ 盈利能力，分水岭在转化规则**：方向命中率 53.95% 的同一信号，在不同仓位规则下产生完全不同的风险形态；决定“AI 在决策链中最终贡献了什么”的，是“信号→仓位”这一环，而非信号本身。",
    "**交易成本是仓位决策的一等公民**：满仓等权日均换手 0.70，年化成本拖累 8.8 个百分点，样本外上行段换手升至 0.91、拖累约 11.4%；成本扫描进一步显示策略排序是成本的函数——10bp 时低换手的 C 组夏普反超 A、B 组。",
    "**校准失败的置信度不能驱动仓位**：置信度均值 0.871 而真实命中率约 54%，分桶无单调性；B 组与 A 组在基准成本下几乎重合；再校准可修复“说的部分”（校准误差 0.221 → 0.089）却无法创造区分度——置信度只能作为参考输入，须经凯利打折与硬约束双重衰减。",
    "**风险预算的第一杠杆是仓位规模，而非触发机制**：平均敞口匹配后，1/4 凯利+触线干预（回撤 -9.3%、卡玛 1.19）并不优于同敞口的静态等权（-7.3%、1.46）；三层排序为 平均敞口 ＞ 持仓分散度 ＞ 触发式干预。干预作为“有条件的保险”只在仓位较重时显效（1/2 档回撤 -15.9% → -12.3%），预算线须与仓位规模成对设计（-3% 线卡玛 1.49、-6% 线 1.19、-9% 线 1.41）。",
    "**方法论价值**：多策略对照 + 样本外检验 + 反事实分析 + 可解释归因 + 复现能力的五项可验证证据，使“AI 在决策链条中发挥了什么作用”变得可验证、可复核、可追溯。",
]
for t in bullet_l:
    para(doc, t, indent=False)
h2(doc, "启示与建议", "6.2")
para(doc, "对金融机构：把“仓位规则”纳入 AI 投研系统的强制评审项，与信号本身同等对待；任何上线策略须同时提交样本外检验与反事实分析报告；将最大回撤预算与仓位规模成对写入系统级硬约束。对监管与教学：推广“虚拟仿真先行”原则，高校金融实验课程应把“从信号到仓位”的转化训练列为 AI 投研教学的核心环节。对 AI 系统建设方：置信度输出必须附带校准曲线与历史命中率分桶报告，并内建“样本内再校准 → 样本外验证”的定期闭环与分布漂移监控；未经验证的置信度不得直接驱动资金分配——**AI 是外骨骼，扣动扳机的必须是懂风险预算的人**。")
h2(doc, "局限与边界", "6.3")
para(doc, "仿真未建模滑点、流动性冲击与涨跌停摩擦，结论不能直接外推至实盘执行环节；样本期为含一段蓝筹上行的单一市场段，区间结构会影响样本外对比的具体数值；信号为透明模拟而非真实大模型输出——这是受控归因的设计前提，真实信号的接入列为开放挑战；凯利分数对收益率均值估计高度敏感，1/4 缩放是保守化处理而非最优解，滚动再估计与多周期验证列为扩展方向。明示边界本身是数据诚实素养的一部分。")
disclaimer(doc)

# ============ 参考文献 ============
h1(doc, "参考文献", None)
refs = [
    "[1] MARKOWITZ H. Portfolio selection[J]. The Journal of Finance, 1952, 7(1): 77-91.",
    "[2] KELLY J L. A new interpretation of information rate[J]. Bell System Technical Journal, 1956, 35(4): 917-926.",
    "[3] THORP E O. The Kelly criterion in blackjack, sports betting, and the stock market[M]//Handbook of Asset and Liability Management. Amsterdam: North-Holland, 2006: 385-428.",
    "[4] SHARPE W F. The Sharpe ratio[J]. Journal of Portfolio Management, 1994, 21(1): 49-58.",
    "[5] BAILEY D H, LÓPEZ DE PRADO M. The deflated Sharpe ratio: correcting for selection bias, backtest overfitting and non-normality[J]. Journal of Portfolio Management, 2014, 40(5): 94-107.",
    "[6] HARVEY C R, LIU Y, ZHU H. …and the cross-section of expected returns[J]. The Review of Financial Studies, 2016, 29(1): 5-68.",
    "[7] MOORE D A, HEALY P J. The trouble with overconfidence[J]. Psychological Review, 2008, 115(2): 502-517.",
    "[8] MURPHY A H, WINKLER R L. Diagnostic verification of probability forecasts[J]. International Journal of Forecasting, 1992, 7(4): 435-455.",
    "[9] ALMGREN R, CHRISS N. Optimal execution of portfolio transactions[J]. Journal of Risk, 2000, 3(2): 5-39.",
]
for r in refs:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_after = Pt(2)
    add_rich(p, r, size=10.5)

# ============ 附录 ============
h1(doc, "附录 A　数据与实验可复现性声明", None)
para(doc, "本报告全部数据与结果可一键复现，链条分三部分：其一，行情（真实公开数据）——调用腾讯财经公开行情接口下载 28 只沪深大盘蓝筹 2024-01-02 至 2025-10-28 共 410 个交易日的前复权日线收盘价（prices.csv，11480 行）；其二，信号（透明模拟实验条件）——以固定随机种子 20261029 注入买/卖信号与置信度（signals.csv，6910 条），信号生成规则完全公开，复跑结果逐字节一致；其三，实验（notebook 与 run_all.py）——全部回测、样本外检验、敏感性分析、反事实分析、成本扫描与再校准闭环由所附代码执行，文中每个表格与图形均由代码真实运行生成，无手工录入数字。随机种子、参数与硬约束在全文明示；对照组、样本外区间、反事实情形在实验设计表中预先声明，不存在事后挑选结果。")
h1(doc, "附录 B　符号与参数表", None)
three_line_table(doc,
    ["符号 / 参数", "含义", "取值"],
    [
        ["TC_BP", "单边交易成本（基准 / 扫描范围）", "5bp / 0–10bp"],
        ["CAP", "单一标的仓位上限", "20%"],
        ["GROSS", "组合总仓位上限", "100%"],
        ["MAX_DD", "回撤触线（软干预，非硬约束；基准 / 敏感性）", "-6% / -3%、-9%"],
        ["OOS", "样本外起点（前 70% 之后）", "第 287 个交易日"],
        ["种子", "信号蒙特卡洛随机种子", "20261029"],
        ["RF", "无风险利率（夏普计算用）", "0（简化设定）"],
    ],
    "表 7　符号与参数表", widths=[3.6, 8.0, 4.4])

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("saved:", OUT)
