# -*- coding: utf-8 -*-
"""案例报告 v6 只增不减补丁：新增 1.4 / 2.5 / 5.7 / 5.8 / 5.9 / 6.4 与参考文献 [10]-[47]。"""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import copy

SRC = "/Users/Admin/Documents/kimi/tasks/2026-10-24/14-58-19-b5e2402f/提交暂存/案例报告.docx"
d = Document(SRC)

def east(el, font):
    rPr = el.get_or_add_rPr()
    rPr.get_or_add_rFonts().set(qn("w:eastAsia"), font)

def find_para(prefix):
    for p in d.paragraphs:
        if p.text.strip().startswith(prefix):
            return p
    raise KeyError(prefix)

def heading_before(anchor, text, size=15):
    p = anchor.insert_paragraph_before()
    r = p.add_run(text); r.bold = True; r.font.size = Pt(size)
    r.font.name = "Times New Roman"; east(r._element, "黑体")
    return p

def body_before(anchor, text, size=13, indent=True):
    p = anchor.insert_paragraph_before()
    if indent:
        p.paragraph_format.first_line_indent = Pt(size * 2)
    r = p.add_run(text); r.font.size = Pt(size)
    r.font.name = "Times New Roman"; east(r._element, "宋体")
    return p

def table_before(anchor, rows, size=9):
    ncol = max(len(r) for r in rows)
    tb = d.add_table(rows=len(rows), cols=ncol)
    try:
        tb.style = d.tables[0].style
    except Exception:
        tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j in range(ncol):
            cell = tb.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            txt = row[j] if j < len(row) else ""
            r = p.add_run(txt); r.font.size = Pt(size)
            r.font.name = "Times New Roman"; east(r._element, "宋体")
            if i == 0: r.bold = True
    anchor._p.addprevious(tb._tbl)
    return tb

def caption_before(anchor, text):
    p = anchor.insert_paragraph_before()
    p.alignment = 1
    r = p.add_run(text); r.bold = True; r.font.size = Pt(10.5)
    r.font.name = "Times New Roman"; east(r._element, "黑体")
    return p

# ============ 1.4 开篇七问与研究前提 ============
a2 = find_para("2　文献与理论基础")
heading_before(a2, "1.4　开篇七问与研究前提的金融学理由")
body_before(a2, "仓位决策从来不是\u201c信号强弱\u201d一个变量。正式进入实验前，本研究先以七个问题建立账户层的硬前提——它们分别对应金融学中账户、组合、风险、执行、行为与合规各层，也是要求学生在实验报告中逐条自查的框架（表 9）。")
caption_before(a2, "表 9　开篇七问与本研究的大众化取值")
table_before(a2, [
    ["七问", "金融学层", "本研究取值"],
    ["这笔钱最多能亏多少？", "账户层·下行风险", "回撤预算线 -6%（触线自动减半）"],
    ["这笔钱能放多久？", "账户层·期限", "410 个交易日 ≈ 2 年不动用"],
    ["要不要分散？", "组合层·相关性", "28 只大盘蓝筹 + 单票 20% 上限"],
    ["极端情况怎么办？", "风险层·尾部", "凸性冲击情景 + 触线干预 + 自助法区间"],
    ["会被情绪（或 AI）带偏吗？", "行为层·偏差", "置信度再校准 + 纪律化规则"],
    ["监管与成本红线？", "合规/执行层", "无杠杆、T+1、5bp 单边成本"],
    ["懂回测的纪律吗？", "方法层", "样本内外切分、参数预登记、24/24 锚点"],
])
body_before(a2, "七问的另一层含义是：不同的人答案不同，仓位规则就应当不同。与临床用药同理——同一组 AI 信号，配不同的资金性质，最优仓位完全不同。本研究冻结\u201c大众化画像\u201d（工资型自有资金、约两年不动用、亏损 6% 即触线、目标为长期复利而非一次性暴利、标的为退市与流动性风险最低的大盘蓝筹），使三组对照在完全相同的账户前线下展开；画像异质化的完整方案见 6.4 节金融数字孪生路线。")
body_before(a2, "每个冻结参数亦有其金融学理由：回测窗口 410 个交易日，覆盖上行、震荡、回撤多种状态，且与\u201c两年不动用的钱\u201d匹配；标的池取大盘蓝筹，匹配低亏损容忍；5bp 单边成本是印花税、佣金与冲击的保守下限，另做 0\u201310bp 扫描证明策略排序是成本的函数（5.1）；-6% 预算线对应大众化疼痛底线，敏感性显示结论稳健（4.4）；1/4 凯利是估计误差下\u201c以小幅增长换波动与回撤大幅下降\u201d的理性折中（MacLean et al., 1992）；20% 个股上限为集中度约束的大众化落点。同时明示边界：本研究未建模杠杆与融资约束、卖空、税费差异化、实时盘口冲击与投资者画像异质性，信号为透明模拟而非真实大模型在线输出——这些是前置声明的简化，而非疏漏，恰好构成 6.4 节的研究路线图。")

# ============ 2.5 文献地图概览 ============
a3 = find_para("3　数据与研究设计")
heading_before(a3, "2.5　文献地图概览：六簇四十余篇")
body_before(a3, "本研究的每个设计都有学术血统，可归纳为六簇：组合选择与凯利准则（Markowitz 1952；Kelly 1956；MacLean et al., 1992, 2011；Moreira & Muir, 2017）、回撤控制与干预机制（Grossman & Zhou, 1993；Black & Perold, 1992；Chekhlov et al., 2005）、回测纪律与统计诚实（Lo, 2002；Bailey & López de Prado, 2014；Harvey & Liu, 2015）、置信度校准与不确定性（Guo et al., 2017；Kull et al., 2019；Xiong et al., 2024）、LLM 投研前沿（Kong et al., 2024；Xiao et al., 2024；姜富伟等, 2024）、交易成本与执行（Almgren & Chriss, 2001；Almgren et al., 2005）。完整列表见文末参考文献（[10]\u2013[47] 为本轮扩充）；恪守不选择性报告纪律，批判性再检验文献（如 Cederburg et al., 2020）一并列入。")

# ============ 5.7 / 5.8 / 5.9 ============
a6 = find_para("6　结论与启示")
heading_before(a6, "5.7　三组方案的明确评价：A 为什么必败，B 为什么失灵，C 为什么可行")
body_before(a6, "三组对照必须给出明确结论。以临床为喻：A 组是不吃药，B 组是一款成分存疑的老药，C 组是配伍完整的新药——试验结果从来不是\u201c不吃药最好\u201d，而是\u201c老药不比安慰剂强多少，新药以可控代价换来了生存质量\u201d。")
body_before(a6, "A 组（满仓等权）把仓位问题取消掉：满仓等权等于宣布\u201c信号强弱与仓位无关\u201d，这正是约八成个人投资者的默认行为。它在单边上行段吃满市场贝塔（样本外年化 41.3%），但代价有三：年化 8.8% 的成本拖累（换手 0.70）；-12.4% 的最大回撤，超出 -6% 预算线一倍以上；凸性冲击情景下卡玛比率 0.47（C 组 0.88，见表 8）。一句话评价：A 组赚的是行情的钱，亏的是纪律的钱——\u201c赚 30% 亏 30%\u201d与\u201c赚 20% 亏 5%\u201d（C 组全样本 +18.6%/-9.3%）在复利意义上不可比。")
body_before(a6, "B 组（置信度分档）形式上用了 AI，实际没有回答买多少：4.1 节已证明该置信度未校准——均值 0.87 对应真实命中仅 54%，属典型的精确度错觉（Moore & Healy, 2008；Xiong et al., 2024）。用未校准的信心决定仓位，等于让\u201c谋士的嗓门\u201d而非\u201c谋士的战绩\u201d决定出兵规模：其全样本回撤 -12.4% 与换手 0.73 几乎复刻 A 组，分档形同虚设。B 组的失败是本案例最重要的教学点——置信度必须先过校准关（5.2 再校准、4.1 诊断），才有资格进入仓位公式。")
body_before(a6, "C 组（1/4 凯利 + 回撤干预）把估计误差与人性弱点同时定价：分数凯利折减均值估计噪声（MacLean et al., 1992），回撤预算线把\u201c亏损时的行为偏差\u201d外包给纪律。代价是牛市段收益变薄（表 4 反事实：满仓凯利无干预 41.6% vs 有干预 20.6%），换回回撤 -9.3%、成本拖累减半、以及凸性冲击下两倍于 A/B 的卡玛比率。明确结论：以单边牛市的绝对收益论，A 组最好——但那是贝塔且不可持续（5.9 将把 41.3% 拆开）；以风险调整、成本纪律与极端情景生存论，排序稳定为 C 优于 A ≈ B，且在子区间三等分、凸性冲击与真实信号替换下全部保持（表 8）。")

heading_before(a6, "5.8　金融学八层框架：本案例的位置与边界")
body_before(a6, "把 5.7 的评价放进完整的仓位决策框架（表 10），可以看清本研究覆盖了什么、留下了什么。AI 选股只回答\u201c买什么\u201d；从资产层以下，全是仓位决策的主场。")
caption_before(a6, "表 10　金融学八层框架与本研究的设计对应")
table_before(a6, [
    ["层级", "核心问题", "金融学工具", "本研究的对应设计", "覆盖"],
    ["账户层", "能亏多少？时间多长？", "效用函数、风险厌恶、下行风险", "6% 回撤预算线、两年期画像资金", "核心"],
    ["资产层", "暴露什么因子？", "CAPM、APT、因子模型、基本面估值", "4.1 信号诊断、IC/ICIR 因子化视角", "部分"],
    ["组合层", "如何分散？相关性多少？", "马科维茨、风险平价、Black-Litterman", "28 只分散、20% 上限、1/4 凯利", "部分"],
    ["风险层", "极端情况亏多少？", "VaR、CVaR、最大回撤、杠杆约束", "触线干预、CVaR 与凸性冲击（5.6）", "核心"],
    ["执行层", "能不能买进/卖出？", "市场微结构、冲击成本、滑点", "5bp 基准+0\u201310bp 扫描+7bp 滑点+平方根律情景", "部分"],
    ["行为层", "会被情绪带偏吗？", "行为偏差、自动化偏见、处置效应", "再校准工作流、纪律化规则替代手动干预", "核心"],
    ["合规层", "有没有制度红线？", "监管规则、账户限制、税务优化", "无杠杆、T+1、集中度上限的大众化设定", "部分"],
])
body_before(a6, "三行\u201c核心\u201d（账户层底线、风险层极端情景、行为层偏差治理）正是本案例的立意：它们恰是\u201c信号→仓位\u201d转化中最容易被 AI 光环遮蔽的部分。四行\u201c部分\u201d不是缺口清单，而是 6.4 节研究路线的坐标：每往下一层，都是一个可教学的课题。")

heading_before(a6, "5.9　样本外年化 41.3% 的核查与正确读法")
body_before(a6, "样本外 A 组年化 41.3% 需要正面核查与解释。数字本身经 24/24 锚点核验（实得 0.41324），计算无误；它显得惊人，是三重口径叠加的结果。第一，窗口是单边上行段：样本外 123 个交易日（2025-04-11 至 2025-10-28）恰为本批蓝筹的强势段，同期等权买入持有、一次都不交易的贝塔基准年化 64.7%（累计 +27.6%，表 11）——满仓组 41.3% 不仅不高，反而跑输零成本贝塔约 23 个百分点，差额正是信号调仓的换手成本（年化拖累 11.4%）与路径摩擦。牛市里\u201c满仓+AI 调仓\u201d尚且跑不过\u201c拿着不动\u201d，这本身就是仓位教学最有说服力的一课。")
caption_before(a6, "表 11　样本外窗口的贝塔基准对照（2025-04-11 至 2025-10-28，123 个交易日）")
table_before(a6, [
    ["口径", "累计收益", "年化收益", "最大回撤"],
    ["等权买入持有（零成本贝塔基准）", "+27.6%", "+64.7%", "-2.9%"],
    ["A 组（信号再平衡，含 5bp 成本）", "+18.4%（由年化反推）", "+41.3%", "-4.1%"],
    ["C 组（1/4 凯利+回撤干预，含 5bp 成本）", "—", "+13.5%", "-2.5%"],
])
body_before(a6, "第二，年化是折算不是承诺：41.3% 由约 18% 的半年累计按复利折算而来，1.413 的十年复利是 31.7 倍，外推显然不成立。AI 炒股的目标是\u201c不停赚钱\u201d的复利与生存，不是\u201c赚一次钱\u201d的爆发——风险与收益成比例，赚一波大的的另一面是亏一波大的，这正是 C 组存在的意义。第三，正确的读法是风险调整与跨情景：同一窗口 A 组回撤 -4.1%、C 组 -2.5%；凸性冲击情景下 A 组卡玛 0.47、C 组 0.88（表 8）；子区间三等分中震荡段 C 组卡玛 4.83 对 A 组 3.12。单边牛市是 A 组唯一的主场，而组合管理的考卷主要在其余场景作答。本研究把\u201c样本外最漂亮的数字\u201d主动拆给读者看，正是不选择性报告纪律的一部分。")

# ============ 6.4 未来研究方向 ============
aref = find_para("参考文献")
heading_before(aref, "6.4　未来研究方向：金融数字孪生与工具的进化路线", size=15)
body_before(aref, "本研究不是一份为比赛而生的作业，而是一条研究路线的第一期工程。沿 5.8 的八层框架逐层展开，五个方向均已具备明确的金融学工具与数据路径。")
body_before(aref, "方向一，金融数字孪生（Financial Digital Twin）：为每位投资者构建\u201c金融属性分身\u201d——以投资者画像问卷（资金性质、可投资期限、亏损容忍、收益目标、标的偏好五维自评）为底稿，辅以授权与隐私合规前提下的消费与流动性习惯特征做交叉校验，合成风险厌恶系数、期限约束与亏损容忍的量化画像；再由画像驱动凯利缩放系数、预算线位置与标的池的个性化配置。问卷自评与行为校验双通道互核，正是为了处理\u201c有些人自己都不知道自己是什么样的人\u201d的现实难题；该方向把本研究从\u201c一组对照实验\u201d升级为\u201c千人千面的仓位实验室\u201d。")
body_before(aref, "方向二，真实大模型信号接入与在线化：将大模型投研工作台的真实信号接入同一回测引擎，对比模拟信号、真实 LLM 信号与 20 日动量基准的校准特性与仓位含义，并把再校准工作流做成在线闭环。20 日动量替换实验（命中率仅 48.7% 而框架成立）已为此铺平方法路。方向三，执行层与合规层的实盘化：接入盘口厚度与冲击成本的实时估计、税费与 T+1 约束的精细化建模，让\u201c能不能买进去/卖出来\u201d从情景假设变为约束求解。方向四，AI 与人工的协同边界：本研究的立场从来不是 AI 万能——AI 提供纪律化的候选择项，采纳与否、否决与否的最终决定权在人；后续将与行为实验团队合作，用真实被试测度自动化偏见在给出/不给出自检清单时的差异，为\u201c人机各管一段\u201d提供实验证据。方向五，研报与教学产品化：把\u201c信号→校准→仓位→复核\u201d工作流封装为可复用的教学与研报工具，面向课程的分层任务包已经就绪，面向机构的日频研报生产线是中期目标。工具在进化，前提在细化，路线未完待续。")

# ============ 参考文献 [10]-[47] ============
apx = find_para("附录 A")
NEW_REFS = [
 "[10] MACLEAN L C, ZIEMBA W T, BLAZENKO G. Growth versus security in dynamic investment analysis[J]. Management Science, 1992, 38(11): 1562-1585.",
 "[11] ROTANDO L M, THORP E O. The Kelly criterion and the stock market[J]. The American Mathematical Monthly, 1992, 99(10): 922-931.",
 "[12] MACLEAN L C, THORP E O, ZIEMBA W T. How does the Fortune's formula Kelly capital growth model perform?[J]. The Journal of Portfolio Management, 2011, 37(4): 96-111.",
 "[13] MOREIRA A, MUIR T. Volatility-managed portfolios[J]. The Journal of Finance, 2017, 72(4): 1611-1644.",
 "[14] GROSSMAN S J, ZHOU Z. Optimal investment strategies for controlling drawdowns[J]. Mathematical Finance, 1993, 3(3): 241-276.",
 "[15] BLACK F, PEROLD A F. Theory of constant proportion portfolio insurance[J]. Journal of Economic Dynamics and Control, 1992, 16(3-4): 403-426.",
 "[16] MAGDON-ISMAIL M, ATIYA A F. Maximum drawdown[J]. Risk, 2004, 17(10): 99-102.",
 "[17] CHEKHLOV A, URYASEV S, ZABARANKIN M. Drawdown measure in portfolio optimization[J]. International Journal of Theoretical and Applied Finance, 2005, 8(1): 13-58.",
 "[18] HARVEY C R, HOYLE S, KORGAONKAR R, et al. The impact of volatility targeting[J]. The Journal of Portfolio Management, 2018, 45(1): 14-33.",
 "[19] CEDERBURG S, O'DOHERTY M S, WANG F, et al. On the performance of volatility-managed portfolios[J]. Journal of Financial Economics, 2020, 138(1): 95-117.",
 "[20] LO A W. The statistics of Sharpe ratios[J]. Financial Analysts Journal, 2002, 58(4): 36-52.",
 "[21] BAILEY D H, BORWEIN J M, LÓPEZ DE PRADO M, et al. The probability of backtest overfitting[J]. Journal of Computational Finance, 2016, 20(4): 39-69.",
 "[22] HARVEY C R, LIU Y. Backtesting[J]. The Journal of Portfolio Management, 2015, 42(1): 13-28.",
 "[23] LÓPEZ DE PRADO M. Advances in financial machine learning[M]. Hoboken: Wiley, 2018.",
 "[24] GUO C, PLEISS G, SUN Y, et al. On calibration of modern neural networks[C]//Proceedings of the 34th International Conference on Machine Learning. Sydney: ICML, 2017: 1321-1330.",
 "[25] KULL M, PERELLO-NIETO M, KÄNGSEPP M, et al. Beyond temperature scaling: obtaining well-calibrated confidence from neural networks[C]//Advances in Neural Information Processing Systems. Vancouver: NeurIPS, 2019.",
 "[26] DESAI V, DURRETT G. Calibration of pre-trained transformers[C]//Proceedings of EMNLP. 2020.",
 "[27] XIONG M, HU Z, LU X, et al. Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs[C]//ICLR 2024. arXiv:2306.13063.",
 "[28] LÓPEZ-LIRA A, TANG Y. Can ChatGPT forecast stock price movements? Return predictability and large language models[J]. arXiv:2304.07619, 2023.",
 "[29] YANG H, LIU X Y, WANG C D. FinGPT: open-source financial large language models[J]. arXiv:2306.06031, 2023.",
 "[30] YU Y, LI H, CHEN Z, et al. FinMem: a performance-enhanced LLM trading agent with layered memory and character design[C]//AAAI Spring Symposium. 2024. arXiv:2311.13743.",
 "[31] YU Y, LI H, ZHAO Z, et al. FinCon: a synthesized LLM multi-agent system with conceptual verbal reinforcement[C]//NeurIPS 2024.",
 "[32] XIAO Y, SUN E, LUO D, et al. TradingAgents: multi-agents LLM financial trading framework[J]. arXiv:2412.20138, 2024.",
 "[33] XIE Q, HAN W, ZHANG X, et al. FinBen: a holistic financial benchmark for large language models[C]//NeurIPS Datasets and Benchmarks. 2024.",
 "[34] KONG X, NIE B, DONG Y, et al. Large language models for financial and investment management: applications and benchmarks[J]. The Journal of Portfolio Management, 2025, 51(2): 162-210.",
 "[35] KOU Z, ZHANG Y, WANG K, et al. Automate strategy finding with LLM in quant investment[J]. arXiv:2409.06289, 2024.",
 "[36] ALMGREN R, THUM C, HAUPTMANN E, et al. Direct estimation of equity market impact[J]. Risk, 2005, 18(7): 58-62.",
 "[37] 姜富伟, 刘雨旻, 孟令超. 大语言模型、文本情绪与金融市场——兼论“人工智能+金融”的逻辑[J]. 管理世界, 2024(8).",
 "[38] 唐国豪, 朱琳, 廖存非, 等. 基于自编码机器学习的资产定价研究——中国股票市场的金融大数据分析视角[J]. 管理科学学报, 2024(9).",
 "[39] 李斌, 龙真. 中国股票市场可预测性研究：基于机器学习的视角[J]. 管理科学学报, 2023, 26(10): 138-158.",
 "[40] 李斌, 邵新月, 李玥阳. 机器学习驱动的基本面量化投资研究[J]. 中国工业经济, 2019(8).",
 "[41] 苏治, 卢曼, 李德轩. 深度学习的金融实证应用：动态、贡献与展望[J]. 金融研究, 2017(5).",
 "[42] 姜富伟, 马甜, 唐国豪. 深度学习与中国股票市场因子投资——基于生成式对抗网络方法[J]. 经济学季刊, 2022, 22(3).",
 "[43] 姜富伟, 孟令超, 唐国豪. 媒体文本情绪与股票回报预测[J]. 经济学季刊, 2021, 21(4): 1323-1344.",
 "[44] 姜富伟, 薛浩, 周明. 中国股票市场可预测性的实证研究[J]. 金融研究, 2011(9).",
 "[45] 史永东, 王谨乐, 胡丹. 中国股票市场个人投资者和机构投资者的过度自信差异研究[J]. 投资研究, 2015(1).",
 "[46] 王建英, 王婷, 李萍. 金融素养自信偏差、风险态度与家庭股票市场参与——基于 CHFS2019 的实证分析[J]. 中央财经大学学报, 2024.",
 "[47] 唐亮, 万相昱, 张晨. 中国股票市场存在过度自信么？行为机制和实证检验[J]. 投资研究.",
]
# 插到参考文献最后一条之后（即附录A之前）
for ref in NEW_REFS:
    p = apx.insert_paragraph_before()
    r = p.add_run(ref); r.font.size = Pt(10.5)
    r.font.name = "Times New Roman"; east(r._element, "宋体")

d.save(SRC)
print("✓ 案例报告已更新:", SRC)

# 校验
d2 = Document(SRC)
full = "\n".join(p.text for p in d2.paragraphs)
for a in ["1.4　开篇七问", "2.5　文献地图", "5.7　三组方案", "5.8　金融学八层框架", "5.9　样本外年化 41.3%", "6.4　未来研究方向", "[47]", "金融数字孪生", "64.7%"]:
    print(("✓" if a in full else "✗"), a)
print("表格数:", len(d2.tables), "段落:", len(d2.paragraphs))
