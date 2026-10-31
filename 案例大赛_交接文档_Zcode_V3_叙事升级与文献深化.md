# 案例大赛 · 交接文档 V3：叙事升级与文献深化（致 Z Code）

> **前置**：V1（任务背景/平台手册/军规/数字口径）与 V2（评分三判据/表达标杆/视觉资产）继续有效，本文不重复。本轮两件事：**① 叙事总纲从"外骨骼"全面升级为"机械臂 × 谋士 × 主公"并深化立意；② 蒸馏 40 篇国内外论文（国内 11 + 国际 29），把文献地基打厚**。
> **铁律不变**：一切产出零姓名/校名/"SuPro/苏坡"；所有数字以 V1 第 4 章为准；结果不唯一、不选择性报告。

---

## 1. 叙事总纲升级（本轮最优先）

### 1.1 旧叙事，全部废除

~~"AI 是外骨骼，扣动扳机的必须是懂风险预算的人。"~~ **不再使用。**"外骨骼"暗示 AI 只是增强人的力气、人始终完整无缺——这个比喻在决赛口径里太弱，且主人已明令改掉。

### 1.2 新叙事（主人定调，一字不改地传播）

> **AI 是机械臂（挖掘机），操纵机械臂手臂的人是主公；AI 是谋士，最终做决断的还是主公。**

三个层次，写作时按需取用：

| 层次 | 比喻 | 要点 | 用在哪 |
|---|---|---|---|
| 操作层 | 机械臂 / 挖掘机 | AI 的力气大、速度快、不知疲倦，但**挖向哪里、挖多深、何时停手，由人决定** | 讲实验设计（硬约束=操作章程） |
| 决策层 | 谋士 / 主公 | 谋士出策（信号+置信度），**采纳与否、承担后果的是主公**；好主公不替谋士背锅，但为"为何采纳"负责 | 讲置信度校准与决策可回溯 |
| 治理层 | 军师的核校 / 制度的缰绳 | 单一谋士会过度自信，所以要有校准表、回撤预算线、参数预登记——**不是不信任 AI，是把信任制度化** | 讲五层变量控制与量规 |

### 1.3 立意深化（比 V2 再进一层）

1. **从"人机分工"到"权责匹配"**：真正的分水岭不是 AI 聪不聪明、人会不会用，而是**谁为决策承担责任**。机械臂没有意图，意图全部来自操纵它的人；谋士之言可以采纳也可以否决，否决的依据必须可追溯——这正是我们"决策可回溯至输入语料与模型原始输出"设计的立意源头。
2. **从个体修为到组织制度**：风险预算不是"高手的风控直觉"，而是**可以写进系统的制度**（5bp 成本、20% 上限、-6% 预算线、参数预登记）。本案例教的不是"做一个谨慎的人"，而是"设计一套让人不得不谨慎的系统"——这正是经管实验教学要培养的治理能力。
3. **教学使命的收束句**（可直接放答辩结语）：
   > 我们不培养操作机械臂最熟练的人，我们培养**握有否决权、也担得起否决后果的主公**。
   > We do not train the most skilled arm-operators; we train sovereigns who hold — and own the consequences of — the veto.

### 1.4 全文替换清单（逐文件执行）

| 文件 | 位置 | 动作 |
|---|---|---|
| 决赛答辩PPT.pptx | p15 | ✅ 已改（Copy of 版），确认正式版同步 |
| 案例设计说明.docx | 文末"AI 是外骨骼，扣动扳机的必须是懂风险预算的人。" | **必改**为 1.2 新叙事句 |
| 案例报告.docx | 全文 grep "外骨骼" | 有则替换；结论段嵌入 1.3-3 收束句 |
| 教学指导文档.docx | 全文 grep "外骨骼" | 同上 |
| 教学指导配套PPT | 结语页 | 同上 |
| 评审导览与自评分表.docx | 全文 grep | 同上 |

替换后全文 grep 一遍：`外骨骼` 必须零命中。

---

## 2. 文献蒸馏地图（国内 11 + 国际 29 = 40 篇）

> 原则：太阳底下无新鲜事——我们的每个设计（凯利缩放、回撤干预、反事实、校准、复现纪律）都有学术血统。案例报告第 2 章文献节按下面六簇重写，参考文献从 9 条扩到 40 条，GB/T 7714 格式。
> 链接均为本轮实际检索所得；标注〔核对〕者请打开链接确认刊名/卷期后再入参考文献表。

### 簇 A：组合选择与凯利准则（仓位的理论源头）

| # | 文献 | 一句话贡献 | 我们借什么 |
|---|---|---|---|
| A1 | Markowitz (1952) Portfolio Selection, *Journal of Finance* 7(1):77-91 | 均值—方差框架确立"收益—风险"权衡起点 | 案例报告已有，保留 |
| A2 | Kelly (1956) A New Interpretation of Information Rate, *Bell System Technical Journal* 35(4):917-926 | 对数最优下注比例，仓位公式之源 | 案例报告已有，保留 |
| A3 | MacLean, Ziemba & Blazenko (1992) Growth versus Security in Dynamic Investment Analysis, *Management Science* 38(11):1562-1585 | 半凯利约得全凯利 75% 增长、50% 波动——分数凯利的经典权衡 | **给 1/4 凯利找血统**：缩放不是拍脑袋，是估计噪声下的理性折中 |
| A4 | Rotando & Thorp (1992) The Kelly Criterion and the Stock Market, *American Mathematical Monthly* 99(10):922-931；Thorp (2006) 收入 Handbook of Asset and Liability Management | Kelly 在股市的落地与分数化实践 | "实务界从不全仓凯利"的权威出处 |
| A5 | MacLean, Thorp & Ziemba (2011) How Does the Fortune's Formula Kelly Capital Growth Model Perform?, *Journal of Portfolio Management* 37(4):96-111 | 全凯利短期高波动、分数凯利更稳的系统检验 | 支撑 C 组"集中持仓降不了波动"的解读 |
| A6 | Moreira & Muir (2017) Volatility-Managed Portfolios, *Journal of Finance* 72(4):1611-1644 | 按波动缩放仓位能提升夏普——波动目标化开山作 | **与"敞口第一杠杆"对话**：我们的三层排序是 vol-managed 思想在实验教学中的可复现版 |

### 簇 B：回撤控制与干预机制（我们 -6% 预算线的理论血统）

| # | 文献 | 一句话贡献 | 我们借什么 |
|---|---|---|---|
| B1 | Grossman & Zhou (1993) Optimal Investment Strategies for Controlling Drawdowns, *Mathematical Finance* 3(3):241-276 | 回撤约束下的最优配置=按"离底线的缓冲"成比例调整风险敞口（CPPI 思想源头） | **升格设计**：触线减半是 CPPI/Grossman-Zhou 的离散近似——软干预从工程技巧变成有理论依据的机制 |
| B2 | Black & Perold (1992) Theory of Constant Proportion Portfolio Insurance, *Journal of Economic Dynamics and Control* 16(3-4):403-426 | CPPI 常比例组合保险 | 同上，写进设计说明 3.1 |
| B3 | Magdon-Ismail & Atiya (2004) Maximum Drawdown, *Risk* 17(10):99-102 | 最大回撤的解析分布与估计 | 支撑"回撤是最难估计的指标、必须配对自助法" |
| B4 | Chekhlov, Uryasev & Zabarankin (2005) Drawdown Measure in Portfolio Optimization, *IJTAF* 8(1):13-58 | 把回撤作为优化目标的一等公民 | 支撑"回撤预算写进硬约束"而非事后观测 |
| B5 | Harvey, Hoyle, Korgaonkar, Rattray, Sargaison & Van Hemert (2018) The Impact of Volatility Targeting, *Journal of Portfolio Management* 45(1):14-33 | 波动目标化降低左尾严重度（60+ 资产实证） | 支撑"干预/缩放在极端时段自动降敞口"的价值 |
| B6 | Cederburg, O'Doherty, Wang & Yan (2020) On the Performance of Volatility-Managed Portfolios, *JFE* 138(1):95-117 | 对 vol-managed 的批判性再检验 | **平衡引用**：展示我们读过反方文献，呼应"不选择性报告" |

### 簇 C：回测纪律与统计诚实（五层变量控制的学术背书）

| # | 文献 | 一句话贡献 | 我们借什么 |
|---|---|---|---|
| C1 | Lo (2002) The Statistics of Sharpe Ratios, *Financial Analysts Journal* 58(4):36-52 | 夏普比率的统计性质与非正态修正 | 支撑"点估计差异不作数、要看置信区间" |
| C2 | Bailey & López de Prado (2014) The Deflated Sharpe Ratio, *JPM* 40(5):94-107 | 选择性偏差下过拟合的夏普校正 | **参数预登记+网格最优须样本外复验的学术出处** |
| C3 | Bailey, Borwein, López de Prado & Zhu (2015/2016) The Probability of Backtest Overfitting, *Journal of Computational Finance* 20(4) | CSCV 框架估计回测过拟合概率 | 支撑"结果不唯一"声明的方法论 |
| C4 | Harvey & Liu (2015) Backtesting, *JPM* 42(1) | 多重检验下回测的合理显著性门槛 | 思考题 4"网格搜索=过拟合"的文献依据 |
| C5 | Harvey, Liu & Zhu (2016) …and the Cross-Section of Expected Returns, *Review of Financial Studies* 29(1):5-68 | 因子发现的 t 值通胀 | 支撑 IC 显著性解读的保守口径 |
| C6 | López de Prado (2018) Advances in Financial Machine Learning, Wiley（第 7 章交叉验证） | 金融 ML 的泄漏控制与验证集纪律 | 支撑前视偏差/样本内偷看两个坑的学术化表述 |

### 簇 D：置信度校准与不确定性（信号治理工作流的学术背书）

| # | 文献 | 一句话贡献 | 我们借什么 |
|---|---|---|---|
| D1 | Murphy & Winkler (1992) Diagnostic Verification of Probability Forecasts, *International Journal of Forecasting* | 概率预报"置信度—频率"对齐的诊断方法 | 案例报告已有，保留 |
| D2 | Moore & Healy (2008) The Trouble with Overconfidence, *Psychological Review* 115(2):502-517 | 过度自信三成分：高估、优越感、精确度错觉 | 支撑"0.871 vs 54% 是精确度错觉"的表述 |
| D3 | Guo, Pleiss, Sun & Weinberger (2017) On Calibration of Modern Neural Networks, *ICML* (arXiv:1706.04599) | 现代深度网络系统性失准；温度缩放单参数修复 | **再校准一节的理论支柱**（案例报告已有，升格为主引用） |
| D4 | Kull et al. (2019) Beyond Temperature Scaling: Dirichlet Calibration, *NeurIPS* | 温度缩放的推广与极限 | 支撑"保序替换只修标签不改排序"的数学表述 |
| D5 | Desai & Durrett (2020) Calibration of Pre-trained Transformers, *EMNLP* | 预训练 Transformer 的校准特性 | 把校准结论从 CV 延伸到 LLM |
| D6 | Xiong et al. (2024) Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs, *ICLR 2024* (arXiv:2306.13063) | LLM 口诉置信度聚集在 80–100%、系统性过度自信 | **"谋士之言必须核校"的最直接实证**——我们的置信度治理工作流不是杞人忧天 |

### 簇 E：LLM 投研前沿（我们站在哪条研究河流里）

| # | 文献 | 一句话贡献 | 我们借什么 |
|---|---|---|---|
| E1 | López-Lira & Tang (2023) Can ChatGPT Forecast Stock Price Movements? (arXiv:2304.07619) | 新闻情绪驱动的多空策略有效 | "AI 信号已可预测收益"的引证 |
| E2 | Yang, Liu & Wang (2023) FinGPT: Open-Source Financial Large Language Models (arXiv:2306.06031) | 开源金融大模型 | 产业背景引证 |
| E3 | Yu et al. (2023) FinMem: A Performance-Enhanced LLM Trading Agent with Layered Memory (arXiv:2311.13743) | 分层记忆增强的交易智能体 | LLM 直接交易决策的代表作 |
| E4 | Yu et al. (2024) FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement, *NeurIPS 37* | 多智能体金融决策 + 概念化语言强化 | 多智能体决策链的学术版 |
| E5 | Xiao et al. (2024) TradingAgents: Multi-Agents LLM Financial Trading Framework (arXiv:2412.20138) | 模拟交易公司：多空研究员辩论 + 风控团队 | **"谋士团队+风险管理团队"与我们"主公+校准表+预算线"的结构呼应** |
| E6 | Xie et al. (2024) FinBen: A Holistic Financial Benchmark for LLMs, *NeurIPS D&B* | 金融 LLM 综合评测 | 背景引证 |
| E7 | Kong, Nie, Dong, Mulvey, Poor, Wen & Zohren (2024) Large Language Models for Financial and Investment Management: Applications and Benchmarks, *JPM* 51(2):162-210 | 牛津团队综述：LLM 投资管理应用与基准 | **文献综述的骨架引用** |
| E8 | Kou et al. (2024) Automate Strategy Finding with LLM in Quant Investment (arXiv:2409.06289) | LLM 自动化量化策略发现 | 前沿方向引证 |

### 簇 F：交易成本与执行（成本是一等公民的学术背书）

| # | 文献 | 一句话贡献 | 我们借什么 |
|---|---|---|---|
| F1 | Almgren & Chriss (2001) Optimal Execution of Portfolio Transactions, *Journal of Risk* 3(2):5-40 | 执行成本=临时冲击+时序风险的最优权衡 | 案例报告已有，保留 |
| F2 | Almgren, Thum, Hauptmann & Li (2005) Direct Estimation of Equity Market Impact, *Risk* 18(7):58-62 | 冲击的平方根律实证 | **"凸性冲击"情景（报告 4.11）的学术依据**：冲击随规模次线性增长→大换手成本非线性放大 |

### 簇 G：国内文献（中文核心，11 篇）

| # | 文献 | 一句话贡献 | 我们借什么 |
|---|---|---|---|
| G1 | 姜富伟、刘雨旻、孟令超（2024）《大语言模型、文本情绪与金融市场——兼论"人工智能+金融"的逻辑》，《管理世界》第 8 期 | 系统论证"AI+金融"的决策链逻辑 | **国内最权威背书**：我们的案例正是这条链的"最后一环"教学化 |
| G2 | 唐国豪、朱琳、廖存非、姜富伟（2024）《基于自编码机器学习的资产定价研究——中国股票市场的金融大数据分析视角》，《管理科学学报》第 9 期 | 自编码因子在 A 股提取有效预测信号 | 国内 ML 选股前沿 |
| G3 | 李斌、龙真（2023）《中国股票市场可预测性研究：基于机器学习的视角》，《管理科学学报》26(10):138-158 | BRT 对收益率/波动率/最优风险权重做样本外预测 | **样本外检验的中文范本** |
| G4 | 李斌、邵新月、李玥阳（2019）《机器学习驱动的基本面量化投资研究》，《中国工业经济》第 8 期 | 机器学习+基本面量化 | 国内基本面量化代表作 |
| G5 | 苏治、卢曼、李德轩（2017）《深度学习的金融实证应用：动态、贡献与展望》，《金融研究》第 5 期 | 深度学习金融应用的早期综述 | 文献节综述段引用 |
| G6 | 姜富伟、马甜、唐国豪（2022）《深度学习与中国股票市场因子投资——基于生成式对抗网络方法》，《经济学季刊》22(3) | GAN 因子投资 | 因子化诊断（IC/ICIR）的中文语境 |
| G7 | 姜富伟、孟令超、唐国豪（2021）《媒体文本情绪与股票回报预测》，《经济学季刊》21(4):1323-1344 | 文本情绪预测收益 | 非结构化文本→信号的国内实证 |
| G8 | 姜富伟等（2011）《中国股票市场可预测性的实证研究》，《金融研究》第 9 期 | A 股可预测性的奠基实证 | 经典引用 |
| G9 | 史永东、王谨乐、胡丹（2015）《中国股票市场个人投资者和机构投资者的过度自信差异研究》，《投资研究》第 1 期 | 个人投资者过度自信强于机构，牛市中加剧 | **"过度自信不是散户专利、模型也会"的中国市场证据** |
| G10 | 王建英、王婷、李萍（2024）《金融素养自信偏差、风险态度与家庭股票市场参与——基于 CHFS2019》，《中央财经大学学报》 | 自信偏差提升股市参与 | 过度自信的经济后果 |
| G11 | 唐亮、万相昱、张晨《中国股票市场存在过度自信么？行为机制和实证检验》〔核对：刊名请打开链接确认〕 | 连续上涨第三日过度自信显著 | 过度自信的 A 股微观结构证据 |

> 教学类参照（不计入 40 篇，供设计说明"教学空白"一节引证）：南京师范大学"股票量化投资虚拟仿真实验"国家级项目申报书（ Southeast Univ. 镜像：<http://jsxngx.seu.edu.cn/CoverFile/nsd75144709.pdf> ）；《股指期货虚拟仿真量化投资平台建设与教学探索》（<http://www.knowcat.cn/x/20240906/894706.html>）——证明"量化投资虚拟仿真"在国内实验教学界已获国家项目立项，**我们的差异化在于把仓位决策与置信度治理做成了受控实验**。

### 检索起点链接（Z Code 续查前沿用）

- arXiv 检索：`site:arxiv.org position sizing Kelly fractional drawdown control LLM agent finance`
- 国内：知网/万方 检索式 `主题=(凯利 OR 仓位管理 OR 回撤控制) AND 主题=(量化 OR 投资组合)`；`主题=(大语言模型 OR 生成式人工智能) AND 主题=(金融 OR 投资决策)`
- 综述入口：Kong et al. 2024（E7）与 Awesome-FinFMs（GitHub: EFundAI/Awesome-FinFMs，278 篇 2024–2026 前沿清单）

---

## 3. 六个可直接写进文档的深化点（每条都已完成文献挂钩）

1. **触线减半的理论升格**：在案例设计说明 3.1 加一句——"本案例的回撤触线干预是常比例组合保险（Black & Perold, 1992; Grossman & Zhou, 1993）的离散近似：风险敞口按离回撤底线的缓冲成比例收缩。"设计从此有理论血统。
2. **1/4 凯利的理性化**：在报告 2.1 加——"凯利分数的估计误差使全凯利在实务中被系统性高估；分数凯利用增长的小幅牺牲换取波动与回撤的大幅降低（MacLean et al., 1992; MacLean et al., 2011），1/4 缩放即此权衡的保守落点。"
3. **预登记与多重检验**：在正文/说明的方法节加——"参数预登记与'网格最优必须样本外复验'对应回测文献对选择性偏差的标准修正（Bailey & López de Prado, 2014; Harvey & Liu, 2015）。"
4. **敞口第一杠杆与波动目标化文献对话**：报告 5.4 讨论段加——"我们的'平均敞口＞分散度＞干预'三层排序与波动管理组合文献（Moreira & Muir, 2017; Harvey et al., 2018）的结论同向：仓位的规模纪律优先于持仓结构微调；Cederburg et al. (2020) 的批判也提醒该结论依赖时段与资产类别。"
5. **信号治理工作流的学术闭环**：报告 5.2 加——"置信度再校准属后校准（post-hoc calibration）路径：温度缩放可修复绝对校准但不改变排序（Guo et al., 2017; Kull et al., 2019）；LLM 口诉置信度被证实在 80–100% 区间聚集且过度自信（Xiong et al., 2024），'先问 IC、再谈仓位'因此是必要流程而非可选优化。"
6. **凸性冲击的出处**：报告 4.11 加——"冲击的平方根律意味着成本随交易规模次线性增长（Almgren et al., 2005），高换手规则在含冲击情景下的劣势被非线性放大，这解释了 10bp 情景的排序反转。"
7. **国内定位**：设计说明 1.3 加——"《管理世界》已系统论证'人工智能+金融'沿'文本情绪→信号生成→投资决策'链条展开（姜富伟等, 2024）；本案例把该链条中'信号→仓位'的转化环节首次做成受控虚拟仿真实验。"

---

## 4. 自评分表反映的问题与修复口径

自评表（12 观测点 99.9，两处各留 0.05 主动缺口、16 锚点、3 条保留局限）本身写得诚实，但有三处需要处理：

1. **"99.9"的答辩口径风险**：精确到小数点的自评容易被评委反感。答辩话术改为——"自评表上的 99.9 不是我们的分数观；它的意思是：我们对照 12 个观测点逐条自查，没有发现可以被扣分而未披露的项，同时我们主动留下了两个没做完的缺口。"把数字的锋芒转成"披露完备"的锋芒。文档里这句话放在自评表评审总述之后。
2. **"外骨骼"残留**：案例设计说明文末（及其他文件）仍有旧叙事句——按第 1.4 节清单替换。
3. **参考文献单薄**：案例报告目前 GB/T 7714 仅 9 条——按第 2 章六簇扩到 40 条；文献节 2.1–2.4 按簇重组，每段以"经典—前沿—批判"三层行文（批判层必须有，呼应不选择性报告）。

---

## 5. Z Code 执行清单（按序）

1. [ ] 六份材料 grep "外骨骼"，按 1.4 替换，替换后复 grep 零命中。
2. [ ] 案例设计说明.docx：3.1 加深化点 1；1.3 加深化点 7；文末换叙事句。
3. [ ] 案例报告.docx：第 2 章按六簇重写、扩至 40 条 GB/T 7714 参考文献；2.1 加深化点 2；5.2 加深化点 5；5.4 加深化点 4；4.11 加深化点 6；结论段嵌入 1.3-3 收束句。
4. [ ] 教学指导文档.docx：素养目标 Q 系列补"权责匹配"一句（1.3-1）；FAQ 增一题："AI 都这么强了，人还学什么？"——完整段落回答（谋士/主公叙事 + 证据：置信度 0.871 vs 命中 54%、干预价值随仓位规模显现）。
5. [ ] 答辩 PPT：p15 已改确认；自评分表评审总述后加 4.1 话术段。
6. [ ] 禁词终扫：四人名/校名/SuPro/苏坡/外骨骼。
7. [ ] 推送 GitHub 备份（sandbox 仓库），更新本文件状态列。

---

## 6. 本轮检索方法（供复核）

- 国际文献经 WebSearch 多轮检索确认（Kelly/MacLean/Grossman-Zhou/Bailey/Guo/Xiong/TradingAgents 等均有 arXiv 或期刊页直链）；簇 G 国内文献经期刊官网（管理科学学报 jmsc.tju.edu.cn、中央财经大学学报、厦门大学/湖南大学官网）交叉确认。
- 标注〔核对〕的条目（G11）请在知网打开确认刊名卷期后再入参考文献表；其余可直接引用。

*文档版本：v3.0（2026-10-31）。与 V1、V2 合读。*
