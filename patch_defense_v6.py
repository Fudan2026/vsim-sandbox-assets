# -*- coding: utf-8 -*-
"""答辩 PPT v6：P6 加 41.3% 读法注解框 + 新增 5 页（同设计体系）+ 重排 + 页码重编。"""
import re, copy
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

SRC = "/Users/Admin/Documents/kimi/tasks/2026-10-24/14-58-19-b5e2402f/提交暂存/决赛答辩PPT.pptx"
prs = Presentation(SRC)
SW, SH = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

INK    = RGBColor(0x0F, 0x17, 0x2A); GRAY = RGBColor(0x33, 0x41, 0x55)
FAINT  = RGBColor(0x64, 0x74, 0x8B); BORDER = RGBColor(0xE2, 0xE8, 0xF0)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLUE   = RGBColor(0x25, 0x63, 0xEB); ORANGE = RGBColor(0xF9, 0x73, 0x16)
EMER   = RGBColor(0x10, 0xB9, 0x81); ROSE = RGBColor(0xF4, 0x3F, 0x5E)
VIOLET = RGBColor(0x7C, 0x3A, 0xED); AMBER = RGBColor(0xF5, 0x9E, 0x0B)
BLUE_T = RGBColor(0xEF, 0xF6, 0xFF); ORAN_T = RGBColor(0xFF, 0xF7, 0xED)
EMER_T = RGBColor(0xEC, 0xFD, 0xF5); ROSE_T = RGBColor(0xFF, 0xF1, 0xF3)
VIOL_T = RGBColor(0xF5, 0xF3, 0xFF); AMBER_T = RGBColor(0xFF, 0xFB, 0xEB)
FONT = "Hiragino Sans GB"

def _set_font(run, size, color, bold=False, font=FONT):
    f = run.font
    f.size, f.bold, f.name = Pt(size), bold, font
    f.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {}); rPr.append(ea)
    ea.set('typeface', font)

def box(s, x, y, w, h, fill=None, line=None, round_=False, line_w=1.0, adj=0.09):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE, x, y, w, h)
    if round_:
        try: shp.adjustments[0] = adj
        except Exception: pass
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp

def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0, space_after=2):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = spacing; p.space_after = Pt(space_after)
        for run_ in para:
            t, sz, c, b = run_[:4]
            fnt = run_[4] if len(run_) > 4 else FONT
            r = p.add_run(); r.text = t
            _set_font(r, sz, c, b, fnt)
    return tb

def header(s, kicker, title, accent, sub=None):
    box(s, 0, 0, SW, Inches(0.1), fill=accent)
    box(s, Inches(0.6), Inches(0.5), Inches(0.1), Inches(0.9), fill=accent)
    txt(s, Inches(0.9), Inches(0.4), Inches(9.8), Inches(0.3), [[(kicker, 12, FAINT, False)]])
    txt(s, Inches(0.9), Inches(0.75), Inches(11.6), Inches(0.6), [[(title, 22, INK, True)]])
    if sub:
        txt(s, Inches(0.9), Inches(1.38), Inches(11.9), Inches(0.35), [[(sub, 11.5, FAINT, False)]])

def footer(s, n, accent):
    txt(s, Inches(0.6), Inches(7.08), Inches(8), Inches(0.3),
        [[("AI 选股信号该配多大仓位？ · 虚拟仿真实验教学案例 · 国赛答辩", 8.5, FAINT, False)]])
    txt(s, Inches(11.6), Inches(7.02), Inches(1.2), Inches(0.35),
        [[(f"{n:02d} / {TOTAL}", 10, accent, True)]], align=PP_ALIGN.RIGHT)

def card(s, x, y, w, h, accent, head=None, body=None, head_size=13, body_size=10.5):
    box(s, x, y, w, h, fill=WHITE, line=BORDER, round_=True)
    box(s, x, y, w, Inches(0.09), fill=accent)
    pad = Inches(0.22); ty = y + Inches(0.18)
    if head:
        txt(s, x + pad, ty, w - pad * 2, Inches(0.4), [[(head, head_size, INK, True)]])
        ty += Inches(0.48)
    if body:
        paras = [[(ln, body_size, GRAY, False)] for ln in body.split("\n")]
        txt(s, x + pad, ty, w - pad * 2, y + h - ty - Inches(0.15), paras, spacing=1.14)

def insight(s, formula, note, accent, tint, y=Inches(6.15), h=Inches(0.72)):
    box(s, Inches(0.6), y, Inches(12.13), h, fill=tint, round_=True)
    txt(s, Inches(0.9), y + Inches(0.08), Inches(8.6), h - Inches(0.14),
        [[(formula, 12.5, INK, True)]])
    txt(s, Inches(9.6), y + Inches(0.08), Inches(3.0), h - Inches(0.14),
        [[(note, 10.5, accent, True)]], align=PP_ALIGN.RIGHT)

def styled_table(s, x, y, w, headers, rows, col_w=None, font_size=10.5, row_h=0.34, head_fill=INK):
    ncol = len(headers)
    tb = s.shapes.add_table(len(rows) + 1, ncol, x, y, w, Inches(row_h * (len(rows) + 1)))
    table = tb.table
    if col_w:
        total = sum(col_w)
        for j, cw in enumerate(col_w):
            table.columns[j].width = Inches(w / Inches(1) * cw / total) if False else Inches(cw)
    for j, htxt in enumerate(headers):
        c = table.cell(0, j); c.text = ""
        p = c.text_frame.paragraphs[0]; r = p.add_run(); r.text = htxt
        _set_font(r, font_size, WHITE, True)
    for i, row in enumerate(rows):
        for j in range(ncol):
            c = table.cell(i + 1, j); c.text = ""
            p = c.text_frame.paragraphs[0]; r = p.add_run(); r.text = row[j] if j < len(row) else ""
            _set_font(r, font_size, GRAY, False)
    return tb

TOTAL = 20

# ============ 1) P6 加 41.3% 注解框 ============
s6 = prs.slides[5]
ann_y = Inches(5.05)
box(s6, Inches(0.6), ann_y, Inches(12.13), Inches(0.95), fill=AMBER_T, round_=True)
box(s6, Inches(0.6), ann_y, Inches(0.09), Inches(0.95), fill=AMBER)
txt(s6, Inches(0.85), ann_y + Inches(0.07), Inches(11.7), Inches(0.85),
    [[("41.3% 的正确读法：① 同窗零成本贝塔 64.7%——满仓组跑输贝塔 23pp（差额=换手成本+路径摩擦）；② 年化是折算不是承诺（1.413 的十年复利 31.7 倍不成立）；③ 跨情景才见真章：凸性冲击下 A 组卡玛 0.47 vs C 组 0.88", 10.5, INK, False)]],
    spacing=1.12)

# ============ 2) 新增 5 页 ============
def new_slide():
    return prs.slides.add_slide(BLANK)

# N1 前提即立场（分述一 · 实验设计）
s = new_slide()
header(s, "分述一 · 实验设计", "前提即立场：每个冻结参数的金融学理由", EMER,
       sub="410 天 ≈ 两年的钱 · 蓝筹池匹配低容忍 · 5bp 是保守下限 · -6% 是大众疼痛底线 · 1/4 凯利是估计误差的折中")
styled_table(s, Inches(0.6), Inches(1.95), Inches(12.15),
             ["实验前提", "取值", "金融学理由"],
             [["回测窗口", "410 交易日", "覆盖多状态；≈2 年匹配画像资金"],
              ["标的池", "28 只大盘蓝筹", "退市与流动性风险最低"],
              ["单边成本", "5bp（0–10bp 扫描）", "印花税+佣金+冲击保守下限"],
              ["回撤预算线", "-6%（4–8% 敏感性）", "大众化疼痛底线，结论稳健"],
              ["凯利缩放", "1/4 凯利", "估计误差下的理性折中"],
              ["个股上限", "20%", "集中度约束的大众化落点"]],
             col_w=[2.0, 3.6, 6.55], font_size=10.5, row_h=0.52, head_fill=EMER)
insight(s, "参数不是随手设的，是金融学前提的具体化——学生要为每个参数辩护", "明示边界即路线图", EMER, EMER_T)
footer(s, 0, EMER)

# N2 41.3% 读法（分述二 · 实证结果）
s = new_slide()
header(s, "分述二 · 实证结果", "41.3% 的正确读法：它是贝塔，不是阿尔法", ORANGE,
       sub="数字经 24/24 锚点核验——拆开之后毫不神秘")
styled_table(s, Inches(0.6), Inches(1.95), Inches(12.15),
             ["口径（样本外 123 个交易日，2025-04-11 ~ 10-28）", "累计", "年化", "最大回撤"],
             [["等权买入持有（零成本贝塔基准）", "+27.6%", "+64.7%", "-2.9%"],
              ["A 组：满仓等权 + 信号再平衡（含 5bp）", "+18.4%", "+41.3%", "-4.1%"],
              ["C 组：1/4 凯利 + 回撤干预（含 5bp）", "—", "+13.5%", "-2.5%"]],
             col_w=[6.2, 1.9, 1.9, 2.15], font_size=10.5, row_h=0.46, head_fill=ORANGE)
card(s, Inches(0.6), Inches(3.85), Inches(3.95), Inches(1.95), ORANGE, "① 窗口是单边上行段",
     "同期蓝筹强势段：一次都不交易的\\n零成本贝塔年化 64.7%。满仓组\\n41.3% 反而跑输贝塔 23pp", body_size=10.5)
card(s, Inches(4.7), Inches(3.85), Inches(3.95), Inches(1.95), ROSE, "② 年化是折算不是承诺",
     "41.3% 由约 18% 的半年累计复利\\n折算；1.413 的十年复利 31.7 倍\\n——外推不成立", body_size=10.5)
card(s, Inches(8.8), Inches(3.85), Inches(3.95), Inches(1.95), EMER, "③ 风险调整+跨情景",
     "同窗回撤 A -4.1% vs C -2.5%；\\n凸性冲击卡玛 A 0.47 vs C 0.88\\n——单边牛市是 A 唯一的主场", body_size=10.5)
insight(s, "AI 炒股的目标是「不停赚钱」的复利生存，不是「赚一次钱」", "风险与收益成比例", ORANGE, ORAN_T)
footer(s, 0, ORANGE)

# N3 AB 明确评价（分述三 · 稳健性）
s = new_slide()
header(s, "分述三 · 稳健性", "三组方案的明确评价：A 必败，B 失灵，C 可行", VIOLET,
       sub="A 是不吃药 · B 是成分存疑的老药 · C 是配伍完整的新药")
card(s, Inches(0.6), Inches(1.95), Inches(3.95), Inches(3.6), ROSE, "A 满仓等权：取消仓位问题",
     "≈八成散户的默认行为\\n成本拖累 8.8% · 换手 0.70\\n回撤 -12.4% 超预算线一倍\\n凸性冲击卡玛 0.47\\n——赚行情的钱，亏纪律的钱", body_size=10.5)
card(s, Inches(4.7), Inches(1.95), Inches(3.95), Inches(3.6), AMBER, "B 置信度分档：老药失灵",
     "未校准置信度定仓位：\\n均值 0.87 vs 命中 54%\\n用「谋士的嗓门」定出兵规模\\n回撤/换手几乎复刻 A 组\\n——分档形同虚设", body_size=10.5)
card(s, Inches(8.8), Inches(1.95), Inches(3.95), Inches(3.6), EMER, "C 1/4 凯利+干预：新药",
     "分数凯利折减估计误差\\n预算线把行为偏差外包给纪律\\n代价：牛市变薄（41.6%→20.6%）\\n换回：-9.3% 回撤、成本减半、\\n极端情景两倍卡玛", body_size=10.5)
insight(s, "明确结论：风险调整排序 C ＞ A ≈ B，跨子区间/凸性/真实信号全部保持", "保险有价格，算出来摆上台面", VIOLET, VIOL_T)
footer(s, 0, VIOLET)

# N4 八层框架（分述三 · 稳健性）
s = new_slide()
header(s, "分述三 · 稳健性", "金融学八层框架：本案例的位置与边界", VIOLET,
       sub="AI 选股只回答「买什么」；从账户层到合规层，全是仓位决策的主场")
styled_table(s, Inches(0.6), Inches(1.95), Inches(12.15),
             ["层级", "核心问题", "本案例的对应设计", "覆盖"],
             [["账户层", "能亏多少？时间多长？", "6% 预算线、两年期画像资金", "核心"],
              ["资产层", "暴露什么因子？", "信号诊断 + IC/ICIR 因子化", "部分"],
              ["组合层", "如何分散？", "28 只、20% 上限、1/4 凯利", "部分"],
              ["风险层", "极端亏多少？", "触线干预、CVaR、凸性冲击", "核心"],
              ["执行层", "能不能买卖？", "5bp+扫描+滑点+平方根律", "部分"],
              ["行为层", "会被带偏吗？", "再校准工作流、纪律化规则", "核心"],
              ["合规层", "制度红线？", "无杠杆、T+1、集中度上限", "部分"]],
             col_w=[1.6, 3.4, 5.75, 1.4], font_size=10, row_h=0.44, head_fill=VIOLET)
insight(s, "三行「核心」= 最易被 AI 光环遮蔽的部分；四行「部分」= 未来路线坐标", "每层都是可教学的课题", VIOLET, VIOL_T)
footer(s, 0, VIOLET)

# N5 未来方向（展望）
s = new_slide()
header(s, "展望 · 未完待续", "未来研究方向：金融数字孪生与工具进化", ROSE,
       sub="不是为比赛而生的作业，而是一条研究路线的第一期工程")
card(s, Inches(0.6), Inches(1.95), Inches(6.0), Inches(1.85), ROSE, "① 金融数字孪生",
     "五维画像自评 × 行为校验 → 量化画像\\n→ 驱动凯利缩放/预算线/标的池个性化\\n千人千面的仓位实验室", body_size=10.5)
card(s, Inches(6.75), Inches(1.95), Inches(6.0), Inches(1.85), BLUE, "② 真实 LLM 信号接入",
     "模拟 vs 真实 vs 20 日动量三套信号\\n校准对比；再校准升级为在线闭环", body_size=10.5)
card(s, Inches(0.6), Inches(3.95), Inches(6.0), Inches(1.85), EMER, "③ 执行与合规层实盘化",
     "盘口厚度+冲击成本实时估计\\n税费与 T+1 约束求解", body_size=10.5)
card(s, Inches(6.75), Inches(3.95), Inches(6.0), Inches(1.85), VIOLET, "④ AI×人工协同 ⑤ 产品化",
     "AI 提供纪律化候选，否决权在人\\n真实被试测自动化偏见；教学包+日频研报", body_size=10.5)
insight(s, "工具在进化，前提在细化，路线未完待续", "下一期工程已开工", ROSE, ROSE_T)
footer(s, 0, ROSE)

# ============ 3) 重排 ============
# 期望顺序（原 15 页 + 新 5 页）：
# 原1..4, N1(前提), 原5..6, N2(41.3), 原7..11, N3(AB), N4(八层), 原12..14, N5(未来), 原15
slides = list(prs.slides)
order = (
    slides[0:4] + [slides[15]] + slides[4:6] + [slides[16]] +
    slides[6:11] + [slides[17], slides[18]] + slides[11:14] + [slides[19]] + slides[14:15]
)
assert len(order) == 20
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
# 删除前缓存：slide 身份 → slide_id → sldId 元素
slide_ids = [s.slide_id for s in slides]
id_by_sid = {sid: sldId for sldId, sid in zip(ids, slide_ids)}
obj_to_sid = {id(s): sid for s, sid in zip(slides, slide_ids)}
for sldId in ids:
    sldIdLst.remove(sldId)
for s in order:
    sldIdLst.append(id_by_sid[obj_to_sid[id(s)]])

# ============ 4) 页码重编 ============
for idx, slide in enumerate(prs.slides, 1):
    for sh in slide.shapes:
        if sh.has_text_frame and re.fullmatch(r"\d{2} / \d{2}", sh.text_frame.text.strip()):
            for para in sh.text_frame.paragraphs:
                for r in para.runs:
                    if "/" in r.text:
                        r.text = f"{idx:02d} / 20"

prs.save(SRC)
print("✓ 答辩 PPT 已更新:", SRC, "| 页数:", len(prs.slides._sldIdLst))
for idx, slide in enumerate(prs.slides, 1):
    t = ""
    for sh in slide.shapes:
        if sh.has_text_frame:
            tt = sh.text_frame.text.strip()
            if tt and len(tt) > 6: t = tt.split("\n")[0][:34]; break
    print(f"P{idx:02d}: {t}")
