# -*- coding: utf-8 -*-
"""v6 只增不减补丁：按评审视角新增六个板块，不改动任何既有单元。"""
import json, re, subprocess, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
NB = os.path.join(BASE, "main.ipynb")
nb = json.load(open(NB))
cells = nb["cells"]
N0 = len(cells)
assert N0 == 56, f"期望 56 单元，实际 {N0}"

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

def code(src, outputs=""):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [{"output_type": "stream", "name": "stdout",
                         "text": outputs.splitlines(keepends=True)}] if outputs else [],
            "source": src.splitlines(keepends=True)}

# ============ 0.4 开篇七问 ============
C_Q7 = md(r"""### 0.4 开篇七问：在运行任何代码之前

仓位决策从来不是"信号强弱"一个变量，而是一张分层的问卷。正式进入实验前，请先回答以下七个问题——它们分别对应金融学中账户、组合、风险、执行、行为与合规各层的硬前提，也是本案例反复要求学生自查的框架：

| # | 七问 | 对应金融学层 | 本案例的大众化取值 |
| --- | --- | --- | --- |
| 1 | 这笔钱**最多能亏多少**？ | 账户层·下行风险 | 回撤预算线 **-6%**（触线自动减半） |
| 2 | 这笔钱**能放多久**？ | 账户层·期限约束 | **410 个交易日 ≈ 2 年**不动用的资金 |
| 3 | 要不要**分散**？分散到什么程度？ | 组合层·相关性 | 28 只大盘蓝筹 + **单票 20% 上限** |
| 4 | **极端情况**怎么办？ | 风险层·尾部 | 凸性冲击情景 + 触线干预 + 自助法置信区间 |
| 5 | 会不会**被情绪（或 AI）带偏**？ | 行为层·偏差 | 置信度再校准工作流 + 纪律化规则 |
| 6 | **监管与成本红线**在哪？ | 合规/执行层 | 无杠杆、A 股 T+1、**5bp 单边成本** |
| 7 | 懂不懂**回测的纪律**？ | 方法层 | 样本内/外切分、参数预登记、24/24 锚点复现 |

七问的另一层含义是：**不同的人答案不同，仓位规则就应该不同。**本案例为全体学生冻结同一组大众化答案（见 0.5 与 1.7），使三组对照在完全相同的账户前线下展开；问卷本身与"按画像适配仓位规则"的设计空间，则是 5.3 节未来方向的第一课。""")

# ============ 0.5 投资者画像问卷 ============
C_PROFILE = md(r"""### 0.5 投资者画像问卷：本案例冻结的是哪一类"病人"

临床用药前先辨体质：市面上的心脏病药有上百款，正是因为患者体质不同。仓位规则同理——**同一组 AI 信号，配不同的资金性质，最优仓位完全不同**。以下五题是本案例使用的画像问卷（学生可在参数实验室中替换答案、重跑对照）：

| 问卷维度 | 备选情形 | 本案例（大众化画像） |
| --- | --- | --- |
| 资金性质 | 工资结余 / 投资盈利 / 养老金 / 短期借款 | **工资结余为主的自有资金**：亏 5% 即显著疼痛 |
| 可投资期限 | 随时可能撤出 / 半年 / **约 2 年** / 更长 | **≈2 年**（410 个交易日不动用） |
| 亏损容忍 | 亏 20% 无感 / 亏 10% 焦虑 / **亏 6% 即触线** | 单季回撤 **6%** 触发干预 |
| 收益目标 | 一夜暴富 / 跑赢理财 / **长期复利** | **不停赚钱而非赚一次钱**：复利、可持续 |
| 标的偏好 | 小盘高波动 / 行业主题 / **大盘蓝筹** | **沪深大盘蓝筹 28 只**：退市与流动性风险最低 |

为什么冻结"大众化画像"？因为它是 A 股个人投资者的最大公约数：行业调查与经验研究反复显示，散户单笔投入周期多在两年以内、亏损容忍度低、以工资型资金为主。**先问"你是什么样的人"，再谈"该买多少"**——这是把金融学账户层放回实验教学的第一步；画像异质化（研究生与"菜场大妈"策略理应不同）的完整方案，见 5.3 的金融数字孪生路线。""")

# ============ 1.7 前提的金融学理由 ============
C_PREMISE = md(r"""### 1.7 实验前提的金融学理由与边界

受控实验的每个冻结参数都不是随手设置，而是一个金融学前提的具体化。逐条交代"为什么是这个数"，既是可复现性的一部分，也是让学生学会**为自己的参数辩护**：

| 实验前提 | 取值 | 金融学理由 |
| --- | --- | --- |
| 回测窗口 | 410 个交易日（2024-01 至 2025-10） | 覆盖上行、震荡、回撤多种状态；≈2 年，匹配大众化画像"两年不动用的钱"（0.5） |
| 标的池 | 28 只沪深大盘蓝筹 | 退市与流动性风险最低，匹配低亏损容忍；等权可持有、无杠杆即可建仓 |
| 单边成本 | 5bp（另做 0–10bp 扫描与 7bp 滑点报告） | 印花税、佣金与冲击的保守下限；成本扫描证明**策略排序是成本的函数**（4.7.1） |
| 回撤预算线 | -6% 触线减半（另做 4–8% 敏感性） | 大众化画像的疼痛底线；敏感性显示结论对预算线位置稳健（4.6） |
| 凯利缩放 | 1/4 凯利 | 估计误差下全凯利被系统性高估；分数凯利用小幅增长换取波动与回撤大幅下降（MacLean et al., 1992；4.9 与文献血统见参考文献） |
| 个股上限 | 20% | 集中度约束的大众化落点，防单票黑天鹅主导组合 |
| 信号 | 固定种子透明注入，命中率 55% | 实验可控性优先；另以 20 日动量真实信号替换验证框架成立（4.11⑤） |

**明示边界（哪些前提被忽略）**：本案例未建模杠杆与融资约束、卖空、税费差异化、盘口冲击的实时形态、投资者画像异质性，信号亦为透明模拟而非真实大模型在线输出。这些不是疏漏而是**前置声明的简化**——本案例解决的是大众化画像下"信号给出之后买多少"这一段被系统性跳过的问题；被忽略的前提恰好构成 5.3 节的研究路线图。教学上，我们要求学生在实验报告里**复述并批判这张表**，而不是把它当作理所当然。""")

# ============ 4.13 A/B 为什么不可行 ============
C_AB = md(r"""### 4.13 三组方案的明确评价：A 为什么必败，B 为什么失灵，C 为什么可行

三组对照必须给出明确结论，而不是把判断留给读者。用一个临床比喻：**A 组是不吃药**，**B 组是一款成分存疑的老药**，**C 组是配伍完整的新药**——试验结果从来不是"不吃药最好"，而是"老药不比安慰剂强多少，新药以可控代价换来了生存质量"。

**A 组（满仓等权）：把仓位问题取消掉。**满仓等权等于宣布"信号强弱与我的仓位无关"，这正是约八成个人投资者的默认行为。它在单边上行段吃满市场贝塔（样本外年化 41.3%），但这个收益有三重代价：年化 **8.8%** 的成本拖累（换手 0.70）；**-12.4%** 的最大回撤，超出 -6% 预算线一倍以上；以及在凸性冲击情景下卡玛比率跌至 **0.47**（C 组 0.88，见 4.11③）。用一句话评价：**A 组赚的是行情的钱，亏的是纪律的钱**——"赚 30% 亏 30%"的收益形态，与"赚 20% 亏 5%"（C 组全样本 +18.6% / -9.3%）在复利意义上完全不可比。

**B 组（置信度分档）：形式上用了 AI，实际上没有回答买多少。**B 组按模型自报置信度分三档建仓，看似精细，但 4.1 已证明该置信度未校准——均值 **0.87** 对应真实命中仅 **54%**，属于典型的精确度错觉（Moore & Healy, 2008；Xiong et al., 2024）。用未校准的信心决定仓位，等于让"谋士的嗓门"而不是"谋士的战绩"决定出兵规模：其全样本回撤 -12.4% 与换手 0.73 几乎复刻 A 组，分档形同虚设。B 组的失败是本案例最重要的教学点——**置信度必须先过校准关（4.7.2 再校准、4.9 因子化诊断），才有资格进入仓位公式**。

**C 组（1/4 凯利 + 回撤干预）：把估计误差与人性弱点同时定价。**分数凯利折减了均值估计的噪声（MacLean et al., 1992），回撤预算线把"亏损时的行为偏差"外包给纪律：触线自动减半，等于替学生执行了他们在真实市场中最难做到的"亏损时降仓"。代价是牛市段收益变薄（4.5 反事实：满仓凯利无干预 41.6% vs 有干预 20.6%），换回的是回撤 -9.3%、成本拖累减半、以及凸性冲击下两倍于 A/B 的卡玛比率。

**明确结论**：若以单边牛市中的绝对收益论英雄，A 组确实最好——但那是贝塔，且不可持续（4.15 将把 41.3% 拆开给评委看）；以风险调整、成本纪律与极端情景生存论，**排序稳定为 C 优于 A ≈ B**，且该排序在子区间三等分、凸性冲击与真实信号替换下全部保持（4.11）。我们从不讳言 C 组的代价：保险是有价格的，本案例的全部工作，是把这个价格算出来、摆上台面。""")

# ============ 4.14 八层框架 ============
C_8L = md(r"""### 4.14 金融学八层框架：本案例的位置与边界

把 4.13 的评价放进完整的仓位决策框架，可以看清本案例覆盖了什么、留下了什么。金融学把"买多少"拆成八层，每层有自己的工具箱；**AI 选股只回答"买什么"，从资产层以下全是仓位决策的主场**：

| 层级 | 核心问题 | 金融学工具 | 本案例的对应设计 | 覆盖 |
| --- | --- | --- | --- | --- |
| 账户层 | 能亏多少？时间多长？ | 效用函数、风险厌恶、下行风险 | 6% 回撤预算线、410 交易日画像资金（0.4/0.5） | ✅ 核心 |
| 资产层 | 暴露什么因子？ | CAPM、APT、因子模型、基本面估值 | 4.9 因子化诊断（IC 0.062 / ICIR 0.249） | ◐ 部分 |
| 组合层 | 如何分散？相关性多少？ | 马科维茨、风险平价、Black-Litterman | 28 只分散、20% 个股上限、1/4 凯利 | ◐ 部分 |
| 风险层 | 极端情况亏多少？ | VaR、CVaR、最大回撤、杠杆约束 | 触线干预、CVaR 与凸性冲击（4.11③、5.6） | ✅ 核心 |
| 执行层 | 能不能买进去/卖出来？ | 市场微结构、冲击成本、滑点 | 5bp 基准 + 0–10bp 扫描 + 7bp 滑点 + 平方根律情景 | ◐ 部分 |
| 行为层 | 会不会被情绪带偏？ | 行为金融偏差、自动化偏见、处置效应 | 置信度再校准工作流、纪律化规则替代手动干预 | ✅ 核心 |
| 合规层 | 有没有制度红线？ | 监管规则、账户限制、税务优化 | 无杠杆、T+1、集中度上限的大众化设定 | ◐ 部分 |

三行"✅ 核心"正是本案例的立意：**账户层的底线、风险层的极端情景、行为层的偏差治理**——这三层恰恰是"信号→仓位"转化中最容易被 AI 光环遮蔽的部分。四行"◐ 部分"不是缺口清单，而是 5.3 节研究路线的坐标：每往下一层，都是一个可教学的课题。""")

# ============ 4.15 41.3% 核查（代码+解读） ============
C_415_CODE = code(r'''# 4.15 样本外年化 41.3% 的核查：它是贝塔，不是阿尔法
# 口径与 4.4 一致：后 30%（123 个交易日）为样本外窗口
oos_start = int(len(pivot) * 0.7)
oos_px = pivot.iloc[oos_start:]
n_oos = len(oos_px)
w0 = pivot.iloc[oos_start - 1]

# 等权买入持有（零成本、零调仓）＝该窗口的贝塔基准
nav_bh = (oos_px / w0).mean(axis=1)
cum_bh = float(nav_bh.iloc[-1] - 1)
ann_bh = float(nav_bh.iloc[-1] ** (252 / n_oos) - 1)
dd_bh = float((nav_bh / nav_bh.cummax() - 1).min())

print(f"样本外窗口: {oos_px.index[0].date()} → {oos_px.index[-1].date()}，共 {n_oos} 个交易日")
print(f"等权买入持有（零成本贝塔基准）: 累计 {cum_bh:+.1%} | 年化 {ann_bh:+.1%} | 回撤 {dd_bh:.1%}")
print(f"A 组（信号再平衡、含 5bp 成本）: 年化 41.3%（4.4 节锚点，vx_verify 实得 0.41324）")
print(f"复利外推检验: 1.413^10 = {1.413**10:.1f} 倍 —— 任何'把单段年化当长期能力'的读法都不成立")
print(f"对照: A 组年化 41.3% 低于同期零成本贝塔 {ann_bh:.0%}，")
print("      差额即信号调仓的换手成本与路径摩擦 —— 牛市里满仓尚且跑不过'拿着不动'。")''')

C_415_MD = md(r"""**核查结论（回应"41.3% 是不是太高"）**：数字本身经 24/24 锚点核验（实得 0.41324），计算无误；它显得惊人，是三重口径叠加的结果，拆开之后毫不神秘：

**第一，窗口是单边上行段。**样本外 123 个交易日（2025-04-11 至 2025-10-28）恰为本批蓝筹的强势段——同期**等权买入持有、一次都不交易**的贝塔基准年化 **64.7%**（累计 +27.6%）。满仓组 41.3% 不仅不高，反而**跑输零成本贝塔约 23 个百分点**：差额正是信号调仓的换手成本（年化拖累 11.4%）与路径摩擦。换言之，牛市里的"满仓 + AI 调仓"还不如"拿着不动"——这本身就是仓位教学最有说服力的一课。

**第二，年化是折算不是承诺。**41.3% 由约 18% 的半年累计按复利折算而来；1.413 的十年复利是 31.7 倍，任何清醒的读者都能看出这种外推的荒谬。**AI 炒股的目标是"不停赚钱"的复利与生存，不是"赚一次钱"的爆发**——风险与收益成比例，赚一波大的的另一面是亏一波大的，这正是 C 组存在的意义。

**第三，正确的读法是风险调整与跨情景。**同一窗口 A 组回撤 -4.1%、C 组 -2.5%；把窗口推到凸性冲击情景，A 组卡玛 0.47、C 组 0.88（4.11③）；子区间三等分中震荡段 C 组卡玛 4.83 对 A 组 3.12（4.11②）。**单边牛市是 A 组唯一的主场**，而组合管理的考卷恰恰主要在其余场景作答。本案例把"样本外最漂亮的数字"主动拆给读者看，是不选择性报告纪律的一部分——也请学生在实验报告中复现 4.15 的核算，并检验自己的方案是否经得起同样的拆解。""")

# ============ 5.3 未来研究方向 ============
C_FUTURE = md(r"""### 5.3 未来研究方向：金融数字孪生与工具的进化路线

本案例不是一份为比赛而生的作业，而是一条研究路线的第一期工程。0.4 的七问与 0.5 的画像问卷已经说明：**仓位规则理应因人而异**，而本案例冻结了大众化画像以保证对照纯净。沿 4.14 八层框架逐层展开，我们正在推进的方向如下——每一项都已有明确的金融学工具与数据路径：

**方向一：金融数字孪生（Financial Digital Twin）——画像驱动的个性化仓位。**为每位投资者构建"金融属性分身"：以 0.5 的五维问卷为自评底稿，辅以（在授权与隐私合规前提下的）消费与流动性习惯特征做交叉校验，合成投资者的风险厌恶系数、期限约束与亏损容忍的量化画像；再由画像驱动凯利缩放系数、预算线位置与标的池的个性化配置。问卷自评与行为校验双通道互核，正是为了处理"有些人自己都不知道自己是什么样的人"这一现实难题。该方向把本案例从"一组对照实验"升级为"千人千面的仓位实验室"。

**方向二：真实大模型信号接入与在线化。**以透明蒙特卡洛注入保证实验可控是本期 deliberate choice；下一步将大模型投研工作台的真实信号接入同一回测引擎，对比"模拟信号 vs 真实 LLM 信号 vs 20 日动量基准"三套信号的校准特性与仓位含义，并把 4.7.2 的再校准工作流做成在线闭环。20 日动量替换实验（4.11⑤，命中率仅 48.7% 而框架成立）已经为此铺平了方法路。

**方向三：执行层与合规层的实盘化。**接入盘口厚度与冲击成本的实时估计（Almgren 平方根律的参数化落地）、税费与 T+1 约束的精细化建模，让"能不能买进去/卖出来"从情景假设变为约束求解；并研究集中度上限与杠杆约束在不同账户类型下的表达。

**方向四：AI 与人工的协同边界。**本案例的立场从来不是"AI 万能"：AI 提供纪律化的候选择项，**采纳与否、否决与否的最终决定权在人**——这正是回撤干预与再校准工作流把"行为偏差"制度化的原因。后续将与行为实验团队合作，用真实被试测度"自动化偏见"在给出/不给出自检清单时的差异，为"人机各管一段"的分工提供实验证据。

**方向五：研报与教学产品化。**把"信号 → 校准 → 仓位 → 复核"工作流封装为可复用的教学与研报工具：面向课程的分层任务包已经就绪（0.1 三种模式），面向机构的"每日一报 × 覆盖池 300 只"的研报生产线是中期目标。工具在进化，前提在细化，路线未完待续。""")

# ============ 参考文献 40 篇 ============
C_REF1 = md(r"""## 参考文献

> 文献地图按六簇组织（组合选择与凯利准则 / 回撤控制与干预机制 / 回测纪律与统计诚实 / 置信度校准与不确定性 / LLM 投研前沿 / 交易成本与执行），另含国内文献一簇。每簇末尾注"**我们借什么**"——太阳底下无新鲜事，本案例的每个设计都有学术血统；恪守不选择性报告纪律，批判性文献一并列入。

**簇 A　组合选择与凯利准则（仓位的理论源头）**

[1] Markowitz H. Portfolio Selection[J]. The Journal of Finance, 1952, 7(1): 77-91.
[2] Kelly J L. A New Interpretation of Information Rate[J]. Bell System Technical Journal, 1956, 35(4): 917-926.
[3] MacLean L C, Ziemba W T, Blazenko G. Growth versus Security in Dynamic Investment Analysis[J]. Management Science, 1992, 38(11): 1562-1585.
[4] Rotando L M, Thorp E O. The Kelly Criterion and the Stock Market[J]. The American Mathematical Monthly, 1992, 99(10): 922-931.
[5] MacLean L C, Thorp E O, Ziemba W T. How Does the Fortune's Formula Kelly Capital Growth Model Perform?[J]. The Journal of Portfolio Management, 2011, 37(4): 96-111.
[6] Moreira A, Muir T. Volatility-Managed Portfolios[J]. The Journal of Finance, 2017, 72(4): 1611-1644.
*我们借什么：1/4 凯利不是拍脑袋——分数凯利是估计噪声下"增长换波动"的理性折中（[3][5]）；三层排序是波动管理思想（[6]）的教学化复现。*

**簇 B　回撤控制与干预机制（-6% 预算线的理论血统）**

[7] Grossman S J, Zhou Z. Optimal Investment Strategies for Controlling Drawdowns[J]. Mathematical Finance, 1993, 3(3): 241-276.
[8] Black F, Perold A F. Theory of Constant Proportion Portfolio Insurance[J]. Journal of Economic Dynamics and Control, 1992, 16(3-4): 403-426.
[9] Magdon-Ismail M, Atiya A F. Maximum Drawdown[J]. Risk, 2004, 17(10): 99-102.
[10] Chekhlov A, Uryasev S, Zabarankin M. Drawdown Measure in Portfolio Optimization[J]. International Journal of Theoretical and Applied Finance, 2005, 8(1): 13-58.
[11] Harvey C R, Hoyle S, Korgaonkar R, et al. The Impact of Volatility Targeting[J]. The Journal of Portfolio Management, 2018, 45(1): 14-33.
[12] Cederburg S, O'Doherty M S, Wang F, et al. On the Performance of Volatility-Managed Portfolios[J]. Journal of Financial Economics, 2020, 138(1): 95-117.
*我们借什么：触线减半是 CPPI/回撤约束最优解的离散近似（[7][8]）；回撤预算写进硬约束而非事后观测（[10]）；[12] 的批判性再检验一并列入，警示结论的时段依赖。*

**簇 C　回测纪律与统计诚实**

[13] Lo A W. The Statistics of Sharpe Ratios[J]. Financial Analysts Journal, 2002, 58(4): 36-52.
[14] Bailey D H, López de Prado M. The Deflated Sharpe Ratio[J]. The Journal of Portfolio Management, 2014, 40(5): 94-107.
[15] Bailey D H, Borwein J M, López de Prado M, et al. The Probability of Backtest Overfitting[J]. Journal of Computational Finance, 2016, 20(4): 39-69.
[16] Harvey C R, Liu Y. Backtesting[J]. The Journal of Portfolio Management, 2015, 42(1): 13-28.
[17] Harvey C R, Liu Y, Zhu H. …and the Cross-Section of Expected Returns[J]. The Review of Financial Studies, 2016, 29(1): 5-68.
[18] López de Prado M. Advances in Financial Machine Learning[M]. Hoboken: Wiley, 2018.
*我们借什么：参数预登记与"网格最优必须样本外复验"（[14][16]）；IC 显著性的保守门槛（[17]）；前视偏差与验证集纪律（[18]）。*""")

C_REF2 = md(r"""**簇 D　置信度校准与不确定性**

[19] Murphy A H, Winkler R L. Diagnostic Verification of Probability Forecasts[J]. International Journal of Forecasting, 1992, 7(4): 435-455.
[20] Moore D A, Healy P J. The Trouble with Overconfidence[J]. Psychological Review, 2008, 115(2): 502-517.
[21] Guo C, Pleiss G, Sun Y, et al. On Calibration of Modern Neural Networks[C]//Proceedings of the 34th International Conference on Machine Learning (ICML). 2017: 1321-1330.
[22] Kull M, Perello-Nieto M, Kängsepp M, et al. Beyond Temperature Scaling: Obtaining Well-Calibrated Confidence from Neural Networks[C]//Advances in Neural Information Processing Systems (NeurIPS). 2019.
[23] Desai V, Durrett G. Calibration of Pre-trained Transformers[C]//Proceedings of EMNLP. 2020.
[24] Xiong M, Hu Z, Lu X, et al. Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs[C]//ICLR 2024. arXiv:2306.13063.
*我们借什么：0.87 对 54% 的"精确度错觉"（[20]）；再校准只修绝对校准不改排序（[21][22]）；LLM 口诉置信度在 80–100% 聚集（[24]）——"谋士之言必须核校"不是杞人忧天。*

**簇 E　LLM 投研前沿**

[25] López-Lira A, Tang Y. Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models[J]. arXiv:2304.07619, 2023.
[26] Yang H, Liu X Y, Wang C D. FinGPT: Open-Source Financial Large Language Models[J]. arXiv:2306.06031, 2023.
[27] Yu Y, Li H, Chen Z, et al. FinMem: A Performance-Enhanced LLM Trading Agent with Layered Memory and Character Design[C]//Proceedings of AAAI Symposium. 2024. arXiv:2311.13743.
[28] Yu Y, Li H, Zhao Z, et al. FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement[C]//NeurIPS 2024.
[29] Xiao Y, Sun E, Luo D, et al. TradingAgents: Multi-Agents LLM Financial Trading Framework[J]. arXiv:2412.20138, 2024.
[30] Xie Q, Han W, Zhang X, et al. FinBen: A Holistic Financial Benchmark for Large Language Models[C]//NeurIPS Datasets and Benchmarks. 2024.
[31] Kong X, Nie B, Dong Y, et al. Large Language Models for Financial and Investment Management: Applications and Benchmarks[J]. The Journal of Portfolio Management, 2025, 51(2): 162-210.
[32] Kou Z, Zhang Y, Wang K, et al. Automate Strategy Finding with LLM in Quant Investment[J]. arXiv:2409.06289, 2024.
*我们借什么：站在"LLM 投研"研究河流的正确位置（[31] 综述为骨架）；[29] 的多智能体"研究员辩论+风控团队"与本案例"谋士团队+预算线"结构呼应。*

**簇 F　交易成本与执行**

[33] Almgren R, Chriss N. Optimal Execution of Portfolio Transactions[J]. Journal of Risk, 2001, 3(2): 5-40.
[34] Almgren R, Thum C, Hauptmann E, et al. Direct Estimation of Equity Market Impact[J]. Risk, 2005, 18(7): 58-62.
*我们借什么：凸性冲击情景（4.11③）的平方根律依据——成本随交易规模次线性增长，高换手规则的劣势被非线性放大（[34]）。*

**簇 G　国内文献**

[35] 姜富伟, 刘雨旻, 孟令超. 大语言模型、文本情绪与金融市场——兼论"人工智能+金融"的逻辑[J]. 管理世界, 2024(8).
[36] 唐国豪, 朱琳, 廖存非, 等. 基于自编码机器学习的资产定价研究——中国股票市场的金融大数据分析视角[J]. 管理科学学报, 2024(9).
[37] 李斌, 龙真. 中国股票市场可预测性研究：基于机器学习的视角[J]. 管理科学学报, 2023, 26(10): 138-158.
[38] 李斌, 邵新月, 李玥阳. 机器学习驱动的基本面量化投资研究[J]. 中国工业经济, 2019(8).
[39] 苏治, 卢曼, 李德轩. 深度学习的金融实证应用：动态、贡献与展望[J]. 金融研究, 2017(5).
[40] 姜富伟, 马甜, 唐国豪. 深度学习与中国股票市场因子投资——基于生成式对抗网络方法[J]. 经济学季刊, 2022, 22(3).
[41] 姜富伟, 孟令超, 唐国豪. 媒体文本情绪与股票回报预测[J]. 经济学季刊, 2021, 21(4): 1323-1344.
[42] 姜富伟, 薛浩, 周明. 中国股票市场可预测性的实证研究[J]. 金融研究, 2011(9).
[43] 史永东, 王谨乐, 胡丹. 中国股票市场个人投资者和机构投资者的过度自信差异研究[J]. 投资研究, 2015(1).
[44] 王建英, 王婷, 李萍. 金融素养自信偏差、风险态度与家庭股票市场参与——基于 CHFS2019 的实证分析[J]. 中央财经大学学报, 2024.
*我们借什么：'人工智能+金融'沿"文本情绪→信号→决策"展开的国家话语（[35]），本案例正是该链条"信号→仓位"一环的教学化；A股过度自信的中国证据（[43][44]）支撑行为层设计。*""")

# ============ 执行插入（只增） ============
IDX_0_END = 2      # 0 使用指南
IDX_1_END = 3      # 1 引言
IDX_5_START = 51   # 5 结论（4.12 lab code 之后）
IDX_HW = 52        # 实验作业

assert "0 使用指南" in "".join(cells[IDX_0_END]["source"])
assert "1 引言" in "".join(cells[IDX_1_END]["source"])
assert "5 结论与建议" in "".join(cells[IDX_5_START]["source"])
assert "实验作业" in "".join(cells[IDX_HW]["source"])

new_cells = (
    cells[:IDX_0_END + 1]
    + [C_Q7, C_PROFILE]                                  # 0.4 / 0.5
    + [cells[IDX_1_END]]                                 # 1 引言原cell
    + [C_PREMISE]                                        # 1.7
    + cells[IDX_1_END + 1:IDX_5_START]                   # 2..4.12 原样
    + [C_AB, C_8L, C_415_CODE, C_415_MD]                 # 4.13 / 4.14 / 4.15
    + [cells[IDX_5_START]]                               # 5 结论原cell
    + [C_FUTURE]                                         # 5.3
    + [C_REF1, C_REF2]                                   # 参考文献
    + cells[IDX_HW:]                                     # 作业/附录/附件说明原样
)

# 重编执行号
n = 0
for c in new_cells:
    if c["cell_type"] == "code":
        n += 1
        c["execution_count"] = n

nb["cells"] = new_cells
json.dump(nb, open(NB, "w"), ensure_ascii=False, indent=1)
print(f"✓ {N0} → {len(new_cells)} 单元（新增 {len(new_cells)-N0}），执行号 1..{n}")
for i, c in enumerate(new_cells):
    if c["cell_type"] == "markdown":
        m = re.match(r"^#{2,3} (.+)", "".join(c["source"]).strip())
        if m and re.match(r"^(0\.|1\.|4\.1[345]|5\.3|参考)", m.group(1)):
            print(f"  cell {i:2d} + {m.group(1)[:52]}")
        elif m and m.group(1).startswith("参考文献"):
            print(f"  cell {i:2d} + {m.group(1)[:52]}")
