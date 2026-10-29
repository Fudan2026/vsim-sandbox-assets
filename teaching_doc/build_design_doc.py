# -*- coding: utf-8 -*-
"""案例设计说明生成器：《AI 选股信号该配多大仓位？》"""
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "/Users/Admin/Documents/kimi/tasks/2026-10-24/14-58-19-b5e2402f/教学指导文档/案例设计说明.docx"

DARK = RGBColor(0x1F, 0x3B, 0x63)
ACCENT = RGBColor(0x2E, 0x5E, 0x8C)
GRAY = RGBColor(0x59, 0x59, 0x59)

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
    bottom.set(qn("w:space"), "2"); bottom.set(qn("w:color"), "1F3B63")
    pBdr.append(bottom); pPr.append(pBdr)

def h2(doc, text, num=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)
    add_rich(p, f"{num}　{text}" if num else text, size=13.5, base_bold=True, color=ACCENT, cn_font="黑体")

def para(doc, text, size=12, indent=True, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4); p.paragraph_format.line_spacing = 1.28
    if indent:
        p.paragraph_format.first_line_indent = Pt(24)
    add_rich(p, text, size=size, color=color)

def bullet(doc, text, size=12):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2); p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.left_indent = Pt(18); p.paragraph_format.first_line_indent = Pt(0)
    add_rich(p, f"• {text}", size=size)

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
        shade(cell, "DCE6F1")
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

# 封面
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(90)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_rich(p, "智享杯 · 全国大学生经济管理类实验案例分析大赛（学生赛区）", size=13, color=GRAY, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(24)
add_rich(p, "案例设计说明", size=30, base_bold=True, color=DARK, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(14)
add_rich(p, "AI 选股信号该配多大仓位？", size=19, base_bold=True, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_rich(p, "——虚拟仿真下的风险预算干预实验", size=15, base_bold=True, cn_font="黑体")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(20)
add_rich(p, "（选题依据 · 设计思路 · 实验设计与变量控制 · 评价设计 · 创新点）", size=11.5, color=GRAY)
doc.add_page_break()

# 一、选题依据
h1(doc, "选题依据", "一、")
h2(doc, "现实需求：AI 投研链条上的“最后一厘米”", "1.1")
para(doc, "证券公司、基金公司正在批量引入大模型投研工作台：每日对数百只标的输出买/卖观点与置信度，AI 生成的“信号”已成投研流程的标准输入。然而信号“准不准”已被大量研究讨论，**信号“配多大仓位”——从信号到资金的转化规则——才直接决定账户损益与回撤**，而这一环节在现实中长期依赖交易员临场经验，缺乏可训练、可考核、可复现的环境。这是 AI 进入投资决策链条后真实存在、又很少被搬进课堂的“最后一厘米”。")
h2(doc, "教学空白：传统教学的三重断裂", "1.2")
table(doc,
    ["传统教学形态", "断裂点", "本案例的补位"],
    [
        ["信号类课程只讲“预测准确率”", "预测力 ≠ 盈利能力，中间隔着仓位规则与成本", "把仓位规则作为唯一实验变量，让学生亲眼看到同信号不同结局"],
        ["回测类作业忽略成本与约束", "5bp 成本在满仓换手下年化拖累可达约 8.8 个百分点，被默认抹去", "把成本、个股上限、总仓上限、回撤预算全部写为硬约束（违反即无效）"],
        ["AI 素养教育只讲工具使用", "不训练“识别 AI 输出是否可信”，过度自信直接变成过度敞口", "把故意保留校准误差的置信度变成诊断素材，训练批判性使用 AI"],
    ],
    widths=[5.0, 6.0, 6.0])
h2(doc, "与大赛主题的契合", "1.3")
para(doc, "第九届大赛主题为“推动 AI+经管实验教学案例研发”。本案例同时占据大赛倡导的两个 AI 切口：**AI 作为实验对象**（评测 AI 置信度的校准质量）与 **AI 作为实验情境**（学生作为“风险预算官”与 AI 信号协同完成决策）。案例全部取材于真实公开行情，信号生成规则完全公开，符合“实践原则（真实性）”与“实验原则（探究性）”的双重要求。")

# 二、设计思路
h1(doc, "设计思路", "二、")
h2(doc, "总体思路：受控对照的“信号 → 仓位 → 后果”沙盘", "2.1")
para(doc, "设计的核心判断是：**要让学生看清“仓位规则”这一个环节的作用，就必须把其他一切冻结**。因此实验将同一组 AI 信号作用于完全相同的行情与约束，只变动“信号 → 仓位”的转化规则；任何绩效差异都只能归因于规则本身——这是受控对照思想在金融决策教学中的直接落地。学生以“风险预算官”身份完成任务链：诊断信号（描述）→ 设计规则并回测（实验）→ 样本外与敏感性检验（检验）→ 一页纸仓位建议（决策）。")
h2(doc, "数据二元结构：真实行情 × 透明信号", "2.2")
table(doc,
    ["数据层", "性质", "来源与规则", "教学功能"],
    [
        ["行情层", "真实公开数据", "腾讯财经公开行情接口：28 只沪深大盘蓝筹，2024-01-02 至 2025-10-28，410 个交易日前复权收盘价，任何人可重新下载核验", "保证背景事实可核查，满足真实性要求"],
        ["信号层", "透明模拟实验条件", "gen_signals.py 以固定种子 20261029 注入：方向 = 次日超额收益符号以 55% 概率取对（实测命中率 53.95%）；置信度 = 真实超额幅度线性映射 + 噪声（故意保留校准误差）", "保证实验条件可复现、可归因；校准误差成为诊断素材"],
    ],
    widths=[2.2, 2.8, 7.4, 4.6], size=10)
para(doc, "为什么不用真实 AI 信号：真实信号的生成机制不透明、噪声与规则效应混杂，将无法把绩效差异干净地归因于仓位规则；透明信号使全班在同一条件下实验，差异即证据。为什么不用纯随机数据：真实行情的波动聚集、板块联动与成本约束是教学目标的一部分，纯随机数据会让实验失真。二元结构是二者权衡的最优解。")
h2(doc, "虚拟仿真的定位", "2.3")
para(doc, "本案例是“虚拟仿真先行”的完整样本：在零真实资金风险的条件下让学生亲历“预测力 → 收益”转化中的全部摩擦（成本、约束、回撤、干预）。仿真未含滑点与流动性冲击，这一局限在案例中明示，并作为“实盘前必须完成全链条压力测试”职业规范的引子。")

# 三、实验设计
h1(doc, "实验设计", "三、")
h2(doc, "硬约束（教师统一设定，违反即方案无效）", "3.1")
bullet(doc, "单边交易成本 5bp；单一标的仓位上限 20%；组合总仓位上限 100%；最大回撤预算 -6%（触及即触发干预）。")
bullet(doc, "信号在 t 日收盘后生成、作用于 t+1 收益；任何参数估计只允许使用样本内（前 70%）数据。")
h2(doc, "实验设计表", "3.2")
table(doc,
    ["环节", "设计", "目的"],
    [
        ["对照组 A", "有信号即满仓等权，无风险预算", "锚定“直觉做法”的基准"],
        ["实验组 B", "置信度分档固定分数（≥0.7 → 30%，0.55–0.7 → 20%）", "检验“置信度直接映射仓位”是否可行"],
        ["实验组 C", "样本内估计凯利分数 × 1/4 + 回撤触线减半", "定量风险预算 + 主动干预"],
        ["样本外检验", "参数不动，回测起点移至 70% 分位（后 123 个交易日）", "检验结论稳健性"],
        ["敏感性分析", "凯利缩放 1/8、1/4、1/2、1 × 干预有无（全样本）", "识别结论成立的参数范围（含反事实）"],
        ["干预线敏感性", "回撤预算线 -3%、-6%、-9%（固定 1/4 凯利）", "回答“预算线设在哪里”"],
    ],
    widths=[3.0, 7.4, 6.6])
h2(doc, "与大赛“六个必要环节”的对应", "3.3")
table(doc,
    ["大赛要求环节", "本案例落点"],
    [
        ["① 提出任务（任务书）", "正文 1.3：风险预算官任务书，含角色、硬约束与五项交付物"],
        ["② 说明条件（数据规则说明）", "正文 1.4：数据规则说明表（来源、股票池、信号规则、样本划分）"],
        ["③ 设计方案（实验设计表）", "正文 1.5：三组对照 + 三重检验，参数预登记"],
        ["④ 运行实验（运行记录）", "在线 Notebook 30 单元真实运行；run_all.py 一键复现"],
        ["⑤ 分析结果（结果分析报告）", "正文 4.3–4.6：全样本、样本外、敏感性与反事实、干预线敏感性"],
        ["⑥ 形成建议（决策建议）", "正文 5.2：对金融机构、监管与教学、AI 系统建设方的三条建议"],
    ],
    widths=[5.4, 11.6], size=10)

# 四、变量控制
h1(doc, "变量控制说明", "四、")
para(doc, "本实验内部有效性由五层控制共同保证：")
table(doc,
    ["控制层", "做法", "控制的变量"],
    [
        ["信号冻结", "6910 条信号由固定种子一次生成，全实验共享，不得重生成", "信息集：任何组的可用信息完全相同"],
        ["约束统一", "5bp 成本、20% 个股上限、100% 总仓上限、-6% 回撤预算对三组一致", "交易环境：绩效差异不含约束宽严差异"],
        ["样本划分预登记", "前 70% 样本内 / 后 30% 样本外在实验前声明", "时间泄漏：杜绝用后段行情调参"],
        ["参数来源限定", "凯利分数与干预参数只用样本内估计；样本外参数不动", "参数偷看：保证检验的真实性"],
        ["反事实对照", "同一规则分别在有干预、无干预两种情形下运行", "干预机制本身：把“干预价值”从“仓位规模”中分离"],
    ],
    widths=[3.2, 8.2, 5.6], size=10)
para(doc, "外部有效性通过敏感性分析检验：凯利缩放从 1/8 到 1 倍、干预线从 -3% 到 -9% 的网格显示结论的适用边界（干预价值随仓位规模显现、预算线须与仓位规模匹配），避免把单一参数点上的偶然结果当成规律。")

# 五、核心结果
h1(doc, "核心结果（设计有效性的证据）", "五、")
para(doc, "以下数字全部由案例代码真实运行生成，可作为“受控对照确实分离出了规则效应”的证据（详细表格见案例正文 4.3–4.6）：")
h2(doc, "全样本三组对照", "5.1")
table(doc,
    ["组别", "累计收益", "年化波动", "夏普", "最大回撤", "卡玛", "日均换手", "年化成本拖累"],
    [
        ["A 满仓等权", "23.2%", "16.8%", "0.70", "-12.4%", "1.11", "0.70", "8.8%"],
        ["B 置信度分档", "22.8%", "约同 A", "0.68", "-12.4%", "约同 A", "约同 A", "9.2%"],
        ["C 1/4 凯利+干预", "18.6%", "16.6%", "0.55", "-9.3%", "1.19", "0.34", "4.3%"],
    ],
    widths=[3.2, 2.0, 1.9, 1.6, 2.0, 1.6, 2.0, 2.7], size=9.5)
para(doc, "三条教学结论直接可读：①同样的信号，C 组以约 4.6 个百分点的收益代价换取回撤压缩 3.1 个百分点与成本减半；②B 组与 A 组几乎重合——校准失败的置信度连加权价值都没有；③凯利集中持仓降不了波动，风险预算的价值要用回撤与成本衡量。")
h2(doc, "样本外检验（后 30%，123 个交易日）", "5.2")
para(doc, "样本外恰为蓝筹上行段：A 组年化 41.3%、夏普 2.71、回撤 -4.1%、换手 0.91（成本拖累约 11.4%）；C 组年化 13.5%、波动 7.4%、回撤 -2.5%、夏普 1.56、卡玛 5.49。上行段风险预算组大幅落后——这不是失败，而是**保险的定价**：机会成本可见、可计量，学生必须为“要不要这份保险”给出自己的论证（结果不唯一的落点之一）。")
h2(doc, "敏感性与反事实（全样本）", "5.3")
bullet(doc, "1/8 凯利档：有无干预完全相同（累计 -4.7%）——仓位足够轻时干预无事可做；")
bullet(doc, "1/4 档：有干预 18.6% / 无干预 22.7%，回撤同为 -9.3%——6% 预算线对轻仓位偏松；")
bullet(doc, "1/2 档：回撤 -12.3%（有）vs -15.9%（无）——干预价值开始显现；")
bullet(doc, "1 倍档：累计 20.6%（有）vs 41.6%（无），回撤 -12.6% vs -15.7%——满仓凯利不可取；")
bullet(doc, "干预线敏感性（1/4 凯利）：-3% 线卡玛 1.49、-6% 线 1.19、-9% 线 1.41——太松等于没干预，预算线须与仓位规模匹配。")

# 六、评价设计
h1(doc, "评价设计", "六、")
para(doc, "评价与教学目标严格对齐，采用**四维 100 分制量规：过程可追溯 30 + 解释合理性 30 + 实验完整性 20 + 报告规范 20**，每维给出四档可观察描述；量规随任务书先行发布，高收益不加分、不可复现扣分。8 道分层作业（基础必做 / 进阶选做 / 挑战 / 思考题）的得分嵌入量规对应维度。完整量规、典型错误引导（五坑三段式）与前后测证据设计详见《教学指导文档》。")

# 七、创新点
h1(doc, "创新点", "七、")
table(doc,
    ["创新点", "传统做法", "本案例的改变"],
    [
        ["① 真实数据沙盘", "虚构理想化数据或无出处数据", "真实公开行情 + 种子公开的透明信号，二元结构使每个数字可核验、可复现"],
        ["② 把“置信度校准”变成教学素材", "AI 输出直接采信", "故意保留过度自信误差，让学生诊断出“均值 0.871 vs 真实命中约 54%”并论证其后果"],
        ["③ 反事实检验进课堂", "只报告“有效”的结果", "“移除干预”的反事实表与主表并列，代价与收益双向陈述"],
        ["④ 开放干预设计", "线性流程直达标准答案", "干预规则的设计空间向学生开放，不同设计得出不同结论并接受数据检验"],
        ["⑤ 全链条过程可追溯", "只交最终报告", "种子、参数、代码、运行记录全明示；随机种子 20261029 复跑逐字节一致"],
    ],
    widths=[3.6, 5.2, 8.2], size=10)

# 八、适用性与推广
h1(doc, "适用性与推广", "八、")
h2(doc, "适用范围", "8.1")
para(doc, "适用于投资学、量化投资 / 金融工程、金融风险管理、Python 金融数据分析、行为金融等课程的实验教学（本科高年级与金融专硕），提供 2 课时标准版与 4 课时扩展版两套组织方案。")
h2(doc, "复用路径", "8.2")
bullet(doc, "**换信号**：修改 gen_signals.py 的命中率与校准参数即可生成新实验条件（题 3、题 5 的出口）；")
bullet(doc, "**换行情**：fetch_prices.py 可更新行情区间或股票池，实验链路不变；")
bullet(doc, "**换规则**：三组仓位规则均为独立函数，学生自设计规则即插即测；")
bullet(doc, "**零安装复用**：运行共享包（脚本 + 种子与参数说明）使任何院校可在案例平台在线环境直接开课。")

# 九、局限
h1(doc, "局限与诚实边界", "九、")
bullet(doc, "仿真未建模滑点、流动性冲击与涨跌停摩擦，结论不能直接外推至实盘执行环节；")
bullet(doc, "样本期为 2024-01 至 2025-10 的单一市场段，行情结构（含一段蓝筹上行）会影响样本外对比的具体数值；")
bullet(doc, "信号为透明模拟而非真实 AI 产品输出——这是受控归因的设计前提，同时限制了“评测某个具体大模型”的外推；")
bullet(doc, "凯利分数对收益率均值估计高度敏感，1/4 缩放是保守化处理而非最优解，其自身即教学讨论点。")
para(doc, "上述局限在案例正文与教学指导文档中均如实标注。我们相信，**明示边界本身是数据诚实素养的一部分**，也是本案例区别于“演示型作品”的关键特征。")

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(16)
add_rich(p, "版本说明：本设计说明与案例正文、数据集、教学指导文档、配套 PPT 同版本发布；数字口径与案例正文一致，如实验数据更新以正文可复现性声明所载种子与参数为准。", size=10, color=GRAY)

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("saved:", OUT)
