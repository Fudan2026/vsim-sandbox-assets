# -*- coding: utf-8 -*-
"""V5：《评审导览与自评分表》——对照 2026 智享杯官方评分标准（4 维度 12 观测点 100 分）
用途：供评审在三分钟内定位全部证据；逐条对照官方评分要点。论文排版体系（黑体/宋体/三线表）。
"""
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "/Users/Admin/Documents/kimi/tasks/2026-10-24/14-58-19-b5e2402f/教学指导文档/评审导览与自评分表.docx"
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

def para(doc, text, size=12, indent=True, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.5
    if indent:
        p.paragraph_format.first_line_indent = Pt(24)
    add_rich(p, text, size=size, color=color)
    return p

def caption(doc, text, above=True):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6 if above else 2)
    p.paragraph_format.space_after = Pt(4 if above else 8)
    p.paragraph_format.line_spacing = 1.2
    add_rich(p, text, size=10.5, base_bold=True, cn_font="黑体")

def three_line_table(doc, headers, rows, cap, widths=None, size=10, align_first_left=True):
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
        tr = t.add_row()
        trPr = tr._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit"); trPr.append(cant)
        cells = tr.cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if (i <= 1 and align_first_left) else WD_ALIGN_PARAGRAPH.CENTER
            add_rich(p, str(val), size=size)
    if widths:
        for i, w in enumerate(widths):
            for r in t.rows:
                r.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

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
    sec.top_margin = Cm(2.3); sec.bottom_margin = Cm(2.3)
    sec.left_margin = Cm(2.4); sec.right_margin = Cm(2.4)
add_page_number(doc)
GRAY = RGBColor(0x47, 0x55, 0x69)

# ============ 标题 ============
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(2)
add_rich(p, "评审导览与自评分表", size=16, base_bold=True, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
add_rich(p, "AI 选股信号该配多大仓位？——虚拟仿真下的风险预算干预实验", size=13, base_bold=True, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(10)
add_rich(p, "（对照《2026 年“智享杯”全国大学生经济管理类实验案例分析大赛评分标准》编制 · 供评审快速定位证据）", size=10, color=GRAY)

# ============ 一、30 秒自评速览 ============
p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
add_rich(p, "一、30 秒自评速览", size=13, base_bold=True, cn_font="黑体")
para(doc, "**结论先行：自评 99.9 / 100**（四大维度：案例选题与问题界定 20/20 ｜ 实验设计 29.95/30 ｜ 案例分析 30/30 ｜ 案例分析结果 19.95/20）。两处各 0.05 分的预留缺口为主动披露的边界（滑点仅做 7bp 合成情景敏感性、未建模非线性冲击；创新属框架内创新、未引入全新模型族）——本作品的教学主张是“不选择性报告”，自评表首先对自己适用。", indent=False)
para(doc, "**评分要点对照**：本文件逐条复述官方评分标准的观测点原文（案例选题、问题界定、实验方法适配性、实验设计科学性、数据质量与处理、实验可重复性、经管理论与知识的运用、分析方法与工具的运用、分析过程、案例分析报告、解决方案的可行性、解决方案的创新性），并在每条后给出可点击核查的出处与数字锚点；全部数字由固定种子（20261029）的代码真实运行生成，可运行 vx_verify.py 得到 24/24 锚点 PASS/FAIL 清单与数字出生证明（manifest.json）。", indent=False)
three_line_table(doc,
    ["维度（官方分值）", "观测点（官方分值）", "自评", "一句话证据"],
    [
        ["案例选题与问题界定（20）", "案例选题（10）", "10", "AI 投研已落地券商基金，“信号→仓位”转化环节缺乏训练环境（报告 1.1）"],
        ["", "问题界定（10）", "10", "三个递进问题：转化 / 校准 / 干预（报告 1.2）"],
        ["实验设计（30）", "实验方法适配性（5）", "5", "虚拟仿真 + 受控对照：冻结信号只变规则（报告 3.1）"],
        ["", "实验设计科学性（10）", "10", "五层变量控制 + 四条统一约束（报告 3.2）"],
        ["", "数据质量与处理（5）", "4.95", "真实公开行情 + 透明信号 + 7bp 含滑点情景；留 0.05：未建模非线性冲击（报告 6.3）"],
        ["", "实验可重复性（10）", "10", "种子 20261029 + 一键复现 + vx_verify 24/24 锚点"],
        ["案例分析（30）", "经管理论与知识的运用（10）", "10", "Markowitz / Kelly / Deflated Sharpe / 可靠度曲线（报告第 2 章，9 条文献）"],
        ["", "分析方法与工具的运用（10）", "10", "对照→样本外→敏感性→反事实，环环相扣（报告 3.3、4）"],
        ["", "分析过程（10）", "10", "敞口匹配基准推翻自身结论，修正为“敞口＞分散度＞干预”（报告 5.4）"],
        ["案例分析结果（20）", "案例分析报告（5）", "5", "论文体例：中英摘要 / 三线表 7 张 / 图 5 幅 / GB/T 7714 文献"],
        ["", "解决方案的可行性（10）", "10", "三条建议均带可量化机制（报告 6.2）"],
        ["", "解决方案的创新性（5）", "4.95", "六项创新（含敞口匹配自我证伪）；留 0.05：未引入全新模型族"],
        ["合计", "12 个观测点", "99.9 / 100", "详表与逐条证据见第三节"],
    ],
    "表 1　30 秒自评速览（逐条证据见后文详表）",
    widths=[4.6, 5.2, 1.6, 8.2], size=9.5)
para(doc, "**关于这份自评的定位**：它是团队的自查工具，不是评分结论——最终判断权完全在评审。之所以附上它，是因为它把“证据在哪”标清楚了：第三节每条证据都指向具体文件、章节与数字；第四节给出锚点数字与复现命令，任何一条都可在一分钟内被独立复核；第五节如实列出六条局限与两处预留缺口。分数本身不重要，可核查的证据链才是。", indent=False)

# ============ 二、一分钟作品地图 ============
p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
add_rich(p, "二、一分钟作品地图", size=13, base_bold=True, cn_font="黑体")
para(doc, "本作品由六份材料构成一条完整证据链。**案例正文**（在线 Notebook，35 单元）是唯一权威数据源；**案例报告**（论文排版，12 页）是面向评审的完整学术文本；**案例设计说明**回答“为什么这样设计”；**教学指导文档**与**教学指导配套 PPT** 支撑教学实施；**数据集与脚本**（prices.csv、signals.csv、run_all.py，种子 20261029）支撑一键复现。", indent=False)
three_line_table(doc,
    ["材料", "定位", "核心章节速览"],
    [
        ["案例正文（Notebook 35 单元）", "权威数据源：全部表格图形由代码真实运行生成", "1 引言与任务书 · 2 数据 · 3 描述统计 · 4 实证（4.1–4.6）· 4.7 拓展 · 4.8 衰减 · 4.9 因子化 · 4.10 敞口基准 · 5 结论 · 附录"],
        ["案例报告（论文，12 页）", "评审主文本：摘要/Abstract/文献/实证/拓展/结论/参考文献", "1 引言 · 2 文献与理论 · 3 数据与研究设计 · 4 实证结果 · 5 拓展分析 · 6 结论 · 附录 A/B"],
        ["案例设计说明", "设计依据：选题、变量控制五层、创新点、局限边界", "1 选题依据 · 2 设计思路 · 3 实验设计 · 4 变量控制 · 7 创新点 · 9 局限"],
        ["教学指导文档（教师用）", "课堂组织：目标、流程、分层任务、量规、三层证据", "2 教学目标 · 4 组织流程 · 5 分层任务 · 6 典型错误 · 7 量规 · 9 证据"],
        ["教学指导配套 PPT（20 页）", "课堂演示：四幕结构（背景/设计/结果/教学）", "P3–5 背景 · P6–9 设计 · P10–15 结果 · P16–19 教学组织"],
        ["数据集与脚本", "复现基础：prices.csv 11480 行 · signals.csv 6910 条 · 种子 20261029", "run_all.py 一键重跑；vx_verify.py 一键自检（24 锚点 PASS/FAIL）+ manifest 数字出生证明（数据血统 SHA256）"],
    ],
    "表 2　作品材料地图", widths=[4.6, 5.4, 7.4], size=9.5)

# ============ 二、自评分表 ============
p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
add_rich(p, "三、对照官方评分标准的自评分表（逐条详表）", size=13, base_bold=True, cn_font="黑体")
para(doc, "下表逐条对照大赛评分标准的四个维度、十二个观测点。“自评依据”给出**可点击核查的证据锚点**（文件 + 章节/表号 + 关键数字）；所有数字均由案例代码真实运行生成，随机抽查任一数字，用所附 run_all.py 可在约 1 分钟内复现，或运行 vx_verify.py 一键校验全部 24 个锚点（PASS/FAIL 清单 + manifest 数字出生证明）。自评合计 99/100，两处保留扣分的理由见表内说明——本作品教授“不选择性报告”，自评表以身作则。", indent=False)

rows = [
    ["案例选题与问题界定\n（20 分）", "案例选题\n（10 分）", "选题具有显著现实意义，聚焦经济管理教育或社会经济领域的热点/难点问题", "10",
     "大模型投研工作台已批量落地券商基金，“AI 信号→仓位”是被广泛忽视的决策环节（案例报告 1.1）；第九届大赛主题“AI+经管实验教学”核心切口"],
    ["", "问题界定\n（10 分）", "案例核心问题清晰、明确，不空泛，具有可分析的范围和深度", "10",
     "三个递进问题：转化（信号→仓位）、校准（置信度能否驱动仓位）、干预（预算价值与位置）（案例报告 1.2；正文 1.2 四任务）"],
    ["实验设计\n（30 分）", "实验方法适配性\n（5 分）", "所选实验方法（如仿真、沙盘、控制实验等）能有效服务于案例问题的分析", "5",
     "虚拟仿真 + 受控对照：冻结信号、只变仓位规则，绩效差异干净归因（案例报告 3.1；设计说明 2.1–2.3）"],
    ["", "实验设计科学性\n（10 分）", "能清晰识别并合理控制关键变量，实验场景贴近现实，参数设置合理有据，实验逻辑严谨", "10",
     "五层变量控制（信号冻结/约束统一/样本预登记/参数来源限定/反事实对照）（案例报告 3.2；设计说明四）；硬约束 5bp/20%/100%/-6% 全文一致"],
    ["", "数据质量与处理\n（5 分）", "数据处理规范，分析方法先进，结论可靠", "4.95",
     "真实公开行情（腾讯接口，可重新下载核验）+ 种子公开的透明信号（11480 行/6910 条）+ **7bp 含滑点情景敏感性**（结论不变）；留 0.05 分：未建模非线性冲击成本（案例报告 6.3 明示）"],
    ["", "实验可重复性\n（10 分）", "实验步骤、参数设置记录详实，确保他人可重现", "10",
     "随机种子 20261029 + 参数预登记 + run_all.py 一键复现；附录 A 可复现性声明；每个数字可由代码重算（案例报告附录 A/B；正文附录）"],
    ["案例分析\n（30 分）", "经管理论与知识的运用\n（10 分）", "恰当、准确地运用经济、管理理论或模型构建案例分析框架；在模型应用或构建上有独到见解或改进", "10",
     "Markowitz 组合选择、Kelly 准则与 1/4 缩放、Sharpe/卡玛、Deflated Sharpe 与多重检验、可靠度曲线校准（案例报告第 2 章，GB/T 7714 九条文献）；独到处：把回撤预算线作为“干预触发器”而非静态红线（正文 1.2）"],
    ["", "分析方法与工具的运用\n（10 分）", "恰当运用定量/定性分析工具，分析过程环环相扣，推理严密，论证充分", "10",
     "pandas 回测引擎 + 蒙特卡洛信号注入 + 分桶校准 + 网格敏感性；对照→样本外→敏感性→反事实四重检验环环相扣（案例报告 3.3、4；正文 4.3–4.6、4.10）"],
    ["", "分析过程\n（10 分）", "分析深入透彻，能透过数据表面发现内在规律、因果关系，对分析结果有合理（独到）的见解", "10",
     "反事实给干预定价（1/2 档回撤 -15.9%→-12.3%）；**平均敞口匹配基准证明“回撤改善主要来自仓位更轻”（S -7.3%/1.46 优于 C -9.3%/1.19），据此把结论修正为“敞口＞分散度＞触发干预”三层排序**；成本扫描发现 10bp 排序反转；再校准闭环 0.221→0.089（案例报告 4.4、5.1–5.4；正文 4.7–4.10）"],
    ["案例分析结果\n（20 分）", "案例分析报告\n（5 分）", "报告结构完整、条理清晰", "5",
     "论文结构：摘要/Abstract→引言→文献→设计→实证→拓展→结论→参考文献→附录；三线表 7 张、图 3 幅、页码齐全"],
    ["", "解决方案的可行性\n（10 分）", "方案针对性强，实施路径清晰，预期效果可量化", "10",
     "三类建议均带可量化机制：上线策略须附样本外+反事实报告；回撤预算与仓位规模成对写入系统硬约束；置信度输出附校准曲线与分桶报告（案例报告 6.2；正文 5.2）"],
    ["", "解决方案的创新性\n（5 分）", "方案是否具有新意，能否提供新的视角、方法或前沿理念", "4.95",
     "六项创新：真实数据沙盘、置信度校准进课堂、反事实检验进课堂、开放干预设计、全链条可复现、**敞口匹配自我证伪**（设计说明七）；留 0.05 分：框架内创新，未引入全新模型族"],
]
three_line_table(doc,
    ["维度", "观测点", "官方评分要点", "自评", "自评依据（证据锚点）"],
    rows,
    "表 3　对照官方评分标准的自评分表（合计 99.9 / 100）",
    widths=[2.2, 2.4, 4.2, 1.0, 7.6], size=9)
para(doc, "自评合计：10 + 10 + 5 + 10 + 4.95 + 10 + 10 + 10 + 10 + 5 + 10 + 4.95 = **99.9 / 100**。两处各预留 0.05 分边界缺口：滑点已用 7bp 合成情景做敏感性（结论不变），但未建模非线性冲击成本；创新为框架内创新，未引入全新模型族。真正的扣分权在评审，本表的价值在证据锚点而非分数本身。", indent=False)

# ============ 三、快速核验通道 ============
p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
add_rich(p, "四、快速核验通道（供评审抽查）", size=13, base_bold=True, cn_font="黑体")
para(doc, "全部核心数字由固定种子（20261029）与公开代码生成，**随机抽查下表任一数字，运行 run_all.py 约 1 分钟即可复现**。这一通道同时回答“实验可重复性（10 分）”的核验方式。", indent=False)
three_line_table(doc,
    ["锚点数字", "含义", "出处"],
    [
        ["23.2% / 22.8% / 18.6%", "全样本 A / B / C 组累计收益", "案例报告表 3 · 正文 4.3"],
        ["-12.4% / -9.3%", "全样本最大回撤（A/B 与 C）", "案例报告表 3"],
        ["8.8% / 4.3%", "年化成本拖累（A 与 C）", "案例报告表 3 · 正文 4.3"],
        ["41.3% / 13.5%", "样本外年化收益（A 与 C）", "案例报告 4.3 · 正文 4.4"],
        ["-15.9% → -12.3%", "1/2 凯利档干预前后回撤（反事实）", "案例报告表 4 · 正文 4.5"],
        ["0.871 / 53.95%", "置信度均值 / 方向命中率", "案例报告 4.1 · 表 2"],
        ["10bp 排序反转", "C 组夏普 0.32 反超 A、B（0.19/0.15）", "案例报告表 5 · 正文 4.7.1"],
        ["0.221 → 0.089", "再校准前后样本外平均校准误差", "案例报告表 6 · 正文 4.7.2"],
        ["20261029", "信号注入随机种子", "正文附录 · run_all.py"],
        ["vx_verify 24/24", "一键自检通过率（含数据血统 SHA256）", "results/manifest.json · 附 vx_verify.py"],
    ],
    "表 4　核心数字锚点（可随机抽查复现）", widths=[4.2, 6.6, 6.6], size=9.5)

# ============ 四、诚实边界 ============
doc.add_page_break()
p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
p.paragraph_format.keep_with_next = True
add_rich(p, "五、诚实边界与局限（逐条披露）", size=13, base_bold=True, cn_font="黑体")
_p = para(doc, "一份可信的结论，应当同时交代它在哪里不成立。下表逐条列出本作品的六条局限、它们对结论的影响，以及已经采取的缓解措施——凡不能缓解的，明确标为“未解决”，请评审据此判断结论的适用边界。", indent=False)
_p.paragraph_format.keep_with_next = True
three_line_table(doc,
    ["局限", "对结论的影响", "已做的处理 / 未解决部分"],
    [
        ["① 信号为透明模拟，非真实大模型输出", "结论回答的是“已知质量的信号如何变成仓位”，不能外推为“某个具体大模型有多准”", "全部材料明示信号为实验条件（种子 20261029、规则公开）；真实信号接入列为开放挑战任务，未解决"],
        ["② 样本为 28 只大盘蓝筹、410 个交易日、单一市场段", "区间含一段蓝筹上行，样本外对比的具体数值受区间结构影响；不能外推为全市场规律", "报告 6.3 与设计说明第九节明示；股票池为当前成分股，存在成分选择偏差，未解决"],
        ["③ 仿真未建模非线性冲击与流动性枯竭", "7bp 情景只把 2bp 滑点并入成本，极端行情下的执行摩擦被低估", "已做 0–10bp 成本扫描与 7bp 含滑点情景（结论不变）；涨跌停、流动性枯竭未建模，未解决"],
        ["④ 凯利分数对收益率均值估计高度敏感", "参数微调可能改变各组绝对数值（排序结论经敏感性检验仍稳健）", "采用 1/4 缩放并做 1/8–1 倍敏感性网格；滚动再估计未做，未解决"],
        ["⑤ 未做统计显著性检验（如块状自助法、多重检验校正）", "三组差异的“量级”可信，但未给出置信区间与 p 值", "以样本外、敏感性、反事实四重检验替代；报告 2.2 引 Deflated Sharpe 说明过拟合风险，统计检验未做，未解决"],
        ["⑥ 干预规则只检验了“触线减半”一族", "其他干预形态（清仓、波动率目标制）的结论可能不同", "列为分层任务与开放作业（题 1）；结果不唯一是本案例的教学设计而非缺陷"],
    ],
    "表 5　局限清单：影响与处理（凡标“未解决”者，请按此界定结论适用范围）",
    widths=[6.2, 6.4, 6.4], size=9)
para(doc, "**为什么把“未解决”写出来**：把边界标清楚，读者才知道结论可以用到哪里；反过来，把做不到的事说成做到了，才是对评审的不诚实。本表与第三节的自评互为镜像——**自评说明作品做到了什么，本表说明它没有做到什么**；两表合读，才是这份作品完整的样子。", indent=False)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8); p.paragraph_format.line_spacing = 1.5
add_rich(p, "免责声明：本文件为教学演示文档，全部阈值与仓位参数均为统一设定的实验条件，不构成任何证券的买卖建议。", size=10, color=GRAY)

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("saved:", OUT)
