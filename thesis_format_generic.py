# -*- coding: utf-8 -*-
"""同类报告文档博士论文排版（通用）：封面+目录两遍法+章前换页+全表框线+页码。
用法：python thesis_format_generic.py <docx路径> <文档类型标签> <章级正则> <节级正则>
第一遍：结构改造（页码占位 0）；第二遍：--fill 用 PDF 页码回填。
"""
import sys, re
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PATH, LABEL, CH_PAT, SEC_PAT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
FILL = "--fill" in sys.argv

def east(el, font):
    rPr = el.get_or_add_rPr(); rPr.get_or_add_rFonts().set(qn("w:eastAsia"), font)

d = Document(PATH)

# ---------- 全表框线 ----------
def set_grid(tbl, sz=6, color="000000"):
    tblPr = tbl._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None: tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), color)
        borders.append(e)
    tblPr.append(borders)

for t in d.tables:
    set_grid(t)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER

# ---------- 页脚页码（清重复字段，重建单一） ----------
sec = d.sections[0]
sec.different_first_page_header_footer = True
fp = sec.footer.paragraphs[0]
for r in list(fp.runs):
    r._element.getparent().remove(r._element)
run = fp.add_run()
f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " PAGE "
fs = OxmlElement("w:fldChar"); fs.set(qn("w:fldCharType"), "separate")
tx = OxmlElement("w:t"); tx.text = "1"
f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
run._element.append(f1); run._element.append(it); run._element.append(fs); run._element.append(tx); run._element.append(f2)
run.font.size = Pt(9); run.font.name = "Times New Roman"

# ---------- 收集章/节标题（按文档顺序） ----------
plan = []
for p in d.paragraphs:
    t = p.text.strip()
    if not t or len(t) > 48: continue
    bold = any(r.bold for r in p.runs if r.text.strip())
    if not bold: continue
    if re.match(CH_PAT, t):
        plan.append((1, p, t))
    elif re.match(SEC_PAT, t):
        plan.append((2, p, t))
chapters = [(p, t) for lvl, p, t in plan if lvl == 1]
print(f"{LABEL}: 章级 {len(chapters)} 个，节级 {sum(1 for l,_,_ in plan if l==2)} 个，表格 {len(d.tables)} 张")

if not FILL:
    # ---------- 封面 ----------
    first = d.paragraphs[0]
    def cover_line(text, size, bold, font, before=0, after=6):
        p = first.insert_paragraph_before()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text); r.bold = bold; r.font.size = Pt(size)
        r.font.name = "Times New Roman"; east(r._element, font)
    cover_line("第九届“智享杯”全国大学生经济管理类实验案例分析大赛", 16, True, "黑体", 24, 4)
    cover_line("（学生赛区 · 数据分析案例）", 14, False, "黑体", 0, 90)
    title_main = d.paragraphs[0]
    # 找正文首段非空文本做主标题（通常即文档标题）
    main_title = None
    for p in d.paragraphs:
        if p is first: continue
        # 跳过刚插的封面行
        if p.text.startswith(("第九届", "（学生赛区", "参赛团队", "完成日期")): continue
        if p.text.strip():
            main_title = p.text.strip().split("\n")[0][:30]
            break
    cover_line(main_title or LABEL, 24, True, "黑体", 40, 16)
    cover_line(LABEL, 18, True, "仿宋", 0, 90)
    cover_line("参赛团队：大赛匿名评审版", 14, False, "仿宋", 0, 8)
    cover_line("完成日期：2026 年 10 月 31 日", 14, False, "仿宋", 0, 0)

    # ---------- 目录（页码占位 0） ----------
    anchor = first
    toc_head = anchor.insert_paragraph_before()
    toc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    toc_head.paragraph_format.page_break_before = True
    toc_head.paragraph_format.space_after = Pt(18)
    r = toc_head.add_run("目　　录"); r.bold = True; r.font.size = Pt(22)
    r.font.name = "Times New Roman"; east(r._element, "黑体")
    for lvl, p, t in plan:
        ep = anchor.insert_paragraph_before()
        pf = ep.paragraph_format
        pf.left_indent = Cm(0 if lvl == 1 else 0.75); pf.space_after = Pt(4)
        pf.tab_stops.add_tab_stop(Cm(15.4), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r1 = ep.add_run(t); r1.font.size = Pt(12 if lvl == 1 else 11); r1.bold = (lvl == 1)
        r1.font.name = "Times New Roman"; east(r1._element, "宋体")
        r2 = ep.add_run("\t0"); r2.font.size = Pt(12 if lvl == 1 else 11)
        r2.font.name = "Times New Roman"; east(r2._element, "宋体")

    # ---------- 章前换页 ----------
    n = 0
    seen_toc = False
    for p in d.paragraphs:
        t = p.text.strip()
        if t == "目　　录": seen_toc = True; continue
        if not seen_toc: continue
        if re.match(CH_PAT, t):
            p.paragraph_format.page_break_before = True; n += 1
    # 正文首段（目录后第一个非空段）换页
    for p in d.paragraphs:
        if p.text.strip() == "目　　录": seen_toc = "passed"; continue
        if seen_toc == "passed" and p.text.strip():
            p.paragraph_format.page_break_before = True; n += 1
            break
    print(f"章前换页 {n} 处（含正文首页）")
else:
    # ---------- 第二遍：从同名 PDF 读页码回填 ----------
    import os
    from pypdf import PdfReader
    pdf = PATH.replace(".docx", ".pdf")
    reader = PdfReader(pdf)
    pages = [pg.extract_text() or "" for pg in reader.pages]
    def norm(s): return re.sub(r"[“”\"‘’\s]", "", s)
    pnorm = []
    for i, t in enumerate(pages):
        nt = norm(t)
        dbl = str(i + 1) * 2
        if nt.startswith(dbl): nt = nt[len(dbl):]
        pnorm.append(nt)
    mapping = {}
    for lvl, p, t in plan:
        key = norm(t)
        if lvl == 1:
            for i in range(3, len(pnorm)):
                if pnorm[i].startswith(key[:min(len(key), 16)]):
                    mapping[key] = i + 1; break
        else:
            for i in range(3, len(pnorm)):
                if key in pnorm[i]:
                    mapping[key] = i + 1; break
    filled, missed = 0, []
    in_toc = False
    for p in d.paragraphs:
        t = p.text.strip()
        if t == "目　　录": in_toc = True; continue
        if in_toc:
            if not t: continue
            if "\t" not in p.text: break
            base = t.rsplit("\t", 1)[0].strip()
            pg = mapping.get(norm(base))
            if pg:
                p.runs[-1].text = "\t" + str(pg); filled += 1
            else:
                missed.append(base[:24])
    print(f"回填 {filled} 条，未匹配 {len(missed)}: {missed[:4]}")

d.save(PATH)
print("✓ 已保存:", PATH)
