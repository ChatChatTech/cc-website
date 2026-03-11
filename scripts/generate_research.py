#!/usr/bin/env python3
"""
行业研究报告生成器 v3
生成80篇独立HTML页面的行业调研报告（Medium/WSJ风格）
每篇包含丰富的图表、表格、统计卡片与高亮框
图表数据一致性：相同标题的图表在不同文章中使用相同数据
每篇文章拥有唯一的Hero背景图
"""

import os
import json
import random
import hashlib
import html as html_mod
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 注册并配置中文字体
_CJK_FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(_CJK_FONT)
_font_prop = fm.FontProperties(fname=_CJK_FONT)
_font_name = _font_prop.get_name()
plt.rcParams['font.sans-serif'] = [_font_name] + plt.rcParams['font.sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'

PRIMARY = '#165DFF'
COLORS = ['#165DFF', '#0A1628', '#3491FA', '#86909C', '#1D2129',
          '#4E5969', '#A0B0C8', '#0E42D2', '#C9CDD4', '#2B3A52']

BASE_DIR = Path('/data/projs/cc-website')
RESEARCH_DIR = BASE_DIR / 'research'
CHARTS_DIR = RESEARCH_DIR / 'charts'

# ============================================================
# 图表数据一致性：相同标题 → 相同种子 → 相同数据
# ============================================================
def _chart_seed(title):
    """确保同一标题的图表在所有文章中产生相同的随机数据"""
    return int(hashlib.md5(title.encode()).hexdigest()[:8], 16)

# ============================================================
# Hero 背景图：每篇文章唯一映射（1:1）
# ============================================================
ALL_HERO_IMAGES = [
    'images/hero-ai-01.jpg',
    'images/hero-binary-01.jpg',
    'images/hero-circuit-01.jpg',
    'images/hero-cloud-01.jpg',
    'images/hero-code-01.jpg',
    'images/hero-code-02.jpg',
    'images/hero-code-03.jpg',
    'images/hero-data-01.jpg',
    'images/hero-data-02.jpg',
    'images/hero-digital-01.jpg',
    'images/hero-digital-02.jpg',
    'images/hero-network-01.jpg',
    'images/hero-security-01.jpg',
    'images/hero-security-02.jpg',
    'images/hero-security-03.jpg',
    'images/hero-server-01.jpg',
    'images/hero-tech-01.jpg',
    'images/hero-tech-02.jpg',
    'images/hero-tech-03.jpg',
    'images/hero-tech-04.jpg',
    'images/hero-cyber-01.jpg',
    'images/hero-server-02.jpg',
    'images/hero-matrix-01.jpg',
    'images/hero-dev-01.jpg',
    'images/hero-abstract-01.jpg',
    'images/hero-code-04.jpg',
    'images/hero-laptop-01.jpg',
    'images/hero-chip-01.jpg',
    'images/hero-globe-01.jpg',
    'images/hero-code-05.jpg',
    'images/hero-lock-01.jpg',
    'images/hero-robot-01.jpg',
    'images/hero-teamwork-01.jpg',
    'images/hero-dashboard-01.jpg',
    'images/hero-monitor-01.jpg',
    'images/hero-code-06.jpg',
    'images/hero-screen-01.jpg',
    'images/hero-retro-01.jpg',
    'images/hero-wire-01.jpg',
    'images/hero-dark-01.jpg',
    'images/hero-ai-02.jpg',
    'images/hero-lab-01.jpg',
    'images/hero-humanoid-01.jpg',
    'images/hero-purple-01.jpg',
    'images/hero-face-01.jpg',
    'images/hero-display-01.jpg',
    'images/hero-terminal-01.jpg',
    'images/hero-keyboard-01.jpg',
    'images/hero-circuit-02.jpg',
    'images/hero-quantum-01.jpg',
    'images/hero-react-01.jpg',
    'images/hero-blockchain-01.jpg',
    'images/hero-ai-03.jpg',
    'images/hero-drone-01.jpg',
    'images/hero-neon-01.jpg',
    'images/hero-smoke-01.jpg',
    'images/hero-dark-02.jpg',
    'images/hero-finance-01.jpg',
    'images/hero-study-01.jpg',
    'images/hero-chart-01.jpg',
    'images/hero-lab-02.jpg',
    'images/hero-hand-01.jpg',
    'images/hero-space-01.jpg',
    'images/hero-earth-01.jpg',
    'images/hero-office-01.jpg',
    'images/hero-team-02.jpg',
    'images/hero-science-01.jpg',
    'images/hero-man-01.jpg',
    'images/hero-vr-01.jpg',
    'images/hero-water-01.jpg',
    'images/hero-green-01.jpg',
    'images/hero-blue-01.jpg',
    'images/hero-ai-04.jpg',
    'images/hero-meeting-01.jpg',
    'images/hero-wave-01.jpg',
    'images/hero-hologram-01.jpg',
    'images/hero-city-01.jpg',
    'images/hero-skyline-01.jpg',
    'images/hero-python-01.jpg',
    'images/hero-space-02.jpg',
]

# ============================================================
# 80篇文章定义（50旧 + 30新）
# ============================================================
ARTICLES = [
    # --- 原50篇 ---
    {"date": "2023-03-08", "domain": "数据要素", "keywords": ["数据确权", "数据资产", "产权制度"], "title": "数据要素市场化配置中的确权机制研究", "subtitle": "从产权界定到价值释放的制度路径"},
    {"date": "2023-03-22", "domain": "隐私计算", "keywords": ["联邦学习", "多方安全计算", "技术选型"], "title": "隐私计算技术路线对比与选型分析", "subtitle": "联邦学习、MPC与TEE的适用场景评估"},
    {"date": "2023-04-15", "domain": "人工智能", "keywords": ["大模型", "GPT", "产业影响"], "title": "大语言模型对企业数字化转型的影响评估", "subtitle": "从GPT到行业大模型的演进路径"},
    {"date": "2023-05-10", "domain": "数据安全", "keywords": ["数据分类分级", "合规治理", "数据安全法"], "title": "数据分类分级制度落地实践与挑战", "subtitle": "基于《数据安全法》的企业合规建设"},
    {"date": "2023-05-28", "domain": "隐私计算", "keywords": ["同态加密", "密码学", "计算效率"], "title": "全同态加密工程化应用进展与性能优化", "subtitle": "从理论突破到产业落地的关键路径"},
    {"date": "2023-06-18", "domain": "数据要素", "keywords": ["数据交易", "数据交易所", "定价机制"], "title": "全国数据交易所发展格局与运营模式比较", "subtitle": "北京、上海、深圳等地数据交易实践分析"},
    {"date": "2023-07-05", "domain": "人工智能", "keywords": ["AI安全", "对齐问题", "可信AI"], "title": "人工智能安全与对齐问题研究综述", "subtitle": "大模型时代的AI治理新挑战"},
    {"date": "2023-07-20", "domain": "数据安全", "keywords": ["跨境数据", "数据出境", "安全评估"], "title": "跨境数据流动安全评估机制研究", "subtitle": "全球数据治理格局下的中国实践"},
    {"date": "2023-08-12", "domain": "隐私计算", "keywords": ["联邦查询", "安全SQL", "密态计算"], "title": "联邦查询技术在多方数据协同中的应用研究", "subtitle": "安全SQL执行引擎的设计与优化"},
    {"date": "2023-09-03", "domain": "数据要素", "keywords": ["公共数据", "开放共享", "授权运营"], "title": "公共数据授权运营模式与价值释放机制", "subtitle": "政务数据资源化利用的制度创新"},
    {"date": "2023-09-25", "domain": "人工智能", "keywords": ["RAG", "检索增强", "知识库"], "title": "检索增强生成技术在企业知识管理中的应用", "subtitle": "RAG架构的工程实践与优化策略"},
    {"date": "2023-10-15", "domain": "数据安全", "keywords": ["个人信息保护", "隐私权", "去标识化"], "title": "个人信息去标识化技术标准与实施路径", "subtitle": "合规场景下的数据脱敏技术体系"},
    {"date": "2023-11-08", "domain": "隐私计算", "keywords": ["可信执行环境", "TEE", "芯片安全"], "title": "可信执行环境技术发展与产业应用前景", "subtitle": "从Intel SGX到国产芯片TEE的演进"},
    {"date": "2023-11-22", "domain": "数据要素", "keywords": ["数据资产入表", "会计准则", "数据估值"], "title": "数据资产入表政策解读与企业应对策略", "subtitle": "财政部新规下的数据资产化路径"},
    {"date": "2023-12-10", "domain": "人工智能", "keywords": ["AI治理", "监管框架", "伦理规范"], "title": "全球AI治理监管框架比较研究", "subtitle": "欧盟AI法案、中美监管实践与启示"},
    {"date": "2023-12-28", "domain": "隐私计算", "keywords": ["隐私保护", "差分隐私", "数据脱敏"], "title": "差分隐私在机器学习训练中的应用与挑战", "subtitle": "隐私预算分配与模型精度的平衡策略"},
    {"date": "2024-01-15", "domain": "数据安全", "keywords": ["数据安全治理", "DSMM", "成熟度模型"], "title": "数据安全治理成熟度评估模型与实施指南", "subtitle": "DSMM框架下的企业数据安全能力建设"},
    {"date": "2024-02-05", "domain": "数据要素", "keywords": ["数据要素市场", "制度建设", "流通体系"], "title": "数据要素流通体系建设进展与趋势展望", "subtitle": "从\"二十条\"到地方实践的政策传导"},
    {"date": "2024-02-26", "domain": "人工智能", "keywords": ["多模态", "视觉语言模型", "AIGC"], "title": "多模态大模型技术演进与行业应用前景", "subtitle": "视觉语言模型在垂直场景的落地分析"},
    {"date": "2024-03-18", "domain": "隐私计算", "keywords": ["隐私计算平台", "市场格局", "商业模式"], "title": "中国隐私计算平台市场竞争格局分析", "subtitle": "技术路线、商业模式与头部厂商比较"},
    {"date": "2024-04-08", "domain": "数据安全", "keywords": ["供应链安全", "软件成分分析", "SBOM"], "title": "AI模型供应链安全风险评估与防护策略", "subtitle": "从Pickle注入到模型投毒的威胁分析"},
    {"date": "2024-04-22", "domain": "数据要素", "keywords": ["算力网络", "东数西算", "算力经济"], "title": "算力基础设施与数据要素协同发展研究", "subtitle": "东数西算背景下的算力网络布局"},
    {"date": "2024-05-12", "domain": "人工智能", "keywords": ["AI Agent", "自主智能体", "任务执行"], "title": "AI Agent技术发展与产业应用研究", "subtitle": "从AutoGPT到企业级智能代理的演进"},
    {"date": "2024-06-03", "domain": "隐私计算", "keywords": ["联邦学习", "金融风控", "信用评估"], "title": "联邦学习在金融风控领域的落地实践", "subtitle": "多方联合建模的技术方案与业务价值"},
    {"date": "2024-06-20", "domain": "数据安全", "keywords": ["零信任", "安全架构", "身份认证"], "title": "零信任安全架构在数据保护中的应用", "subtitle": "从边界防护到持续验证的范式转换"},
    {"date": "2024-07-10", "domain": "数据要素", "keywords": ["医疗数据", "健康大数据", "数据共享"], "title": "医疗健康大数据共享的隐私保护方案", "subtitle": "跨机构临床数据协同的技术与制度"},
    {"date": "2024-07-28", "domain": "人工智能", "keywords": ["开源模型", "DeepSeek", "国产大模型"], "title": "国产开源大模型发展态势与技术评测", "subtitle": "DeepSeek、通义千问等开源生态分析"},
    {"date": "2024-08-15", "domain": "隐私计算", "keywords": ["隐私信息检索", "PIR", "密码学"], "title": "隐私信息检索协议的工程化实践", "subtitle": "PIR协议在数据查询场景的性能优化"},
    {"date": "2024-09-05", "domain": "数据安全", "keywords": ["数据水印", "溯源追踪", "版权保护"], "title": "数据水印技术在数据溯源追踪中的应用", "subtitle": "隐写术与鲁棒水印的工程化实践"},
    {"date": "2024-09-22", "domain": "数据要素", "keywords": ["数字政府", "政务数据", "数字中国"], "title": "数字政府建设中的数据治理能力评估", "subtitle": "省级数据管理机构改革与实践成效"},
    {"date": "2024-10-08", "domain": "人工智能", "keywords": ["边缘AI", "端侧推理", "模型压缩"], "title": "边缘AI推理技术发展与隐私保护优势", "subtitle": "端侧部署在敏感场景中的应用价值"},
    {"date": "2024-10-25", "domain": "隐私计算", "keywords": ["安全沙箱", "可信计算", "代码审计"], "title": "安全沙箱技术在数据可信计算中的应用", "subtitle": "容器化隔离与安全函数计算架构设计"},
    {"date": "2024-11-12", "domain": "数据安全", "keywords": ["密码学", "后量子密码", "抗量子"], "title": "后量子密码迁移对隐私计算的影响评估", "subtitle": "格基密码与同态加密的未来兼容性"},
    {"date": "2024-11-28", "domain": "数据要素", "keywords": ["数据资产评估", "估值方法", "数据定价"], "title": "数据资产评估方法论与实践案例研究", "subtitle": "成本法、收益法与市场法的适用性比较"},
    {"date": "2024-12-15", "domain": "人工智能", "keywords": ["AI+安全", "智能安全运营", "SOAR"], "title": "AI驱动的安全运营中心建设方案研究", "subtitle": "大模型在威胁检测与响应中的应用"},
    {"date": "2025-01-08", "domain": "隐私计算", "keywords": ["隐私保护RAG", "安全检索", "加密查询"], "title": "隐私保护检索增强生成系统技术研究", "subtitle": "PPRAG架构的设计原理与安全性分析"},
    {"date": "2025-02-05", "domain": "数据安全", "keywords": ["容器安全", "Docker", "运行时防护"], "title": "容器化部署环境下的数据安全加固方案", "subtitle": "从镜像扫描到运行时防护的全栈策略"},
    {"date": "2025-02-20", "domain": "数据要素", "keywords": ["能源数据", "碳数据", "绿色金融"], "title": "能源行业数据要素流通与碳数据资产化", "subtitle": "双碳目标下的能源数据治理实践"},
    {"date": "2025-03-10", "domain": "人工智能", "keywords": ["具身智能", "机器人", "感知决策"], "title": "具身智能发展趋势与数据安全需求分析", "subtitle": "物理世界AI的隐私边界与安全挑战"},
    {"date": "2025-03-25", "domain": "隐私计算", "keywords": ["秘密共享", "安全多方计算", "协议优化"], "title": "安全多方计算协议优化与性能基准评测", "subtitle": "ABY3、Semi2k等协议在实际场景的效率比较"},
    {"date": "2025-04-08", "domain": "数据安全", "keywords": ["API安全", "接口治理", "数据泄露"], "title": "API安全治理框架与数据泄露防护实践", "subtitle": "面向开放接口的全生命周期安全管理"},
    {"date": "2025-05-15", "domain": "数据要素", "keywords": ["交通数据", "智慧交通", "自动驾驶"], "title": "交通行业数据要素价值发现与隐私保护", "subtitle": "车路协同场景下的数据安全治理"},
    {"date": "2025-06-02", "domain": "人工智能", "keywords": ["小模型", "蒸馏", "高效推理"], "title": "小模型高效推理在隐私敏感场景的应用", "subtitle": "知识蒸馏与量化技术的本地部署方案"},
    {"date": "2025-07-10", "domain": "隐私计算", "keywords": ["属性基加密", "ABE", "细粒度控制"], "title": "属性基加密在医疗数据访问控制中的应用", "subtitle": "基于CP-ABE的细粒度权限管理方案"},
    {"date": "2025-08-05", "domain": "数据安全", "keywords": ["安全审计", "日志分析", "合规检查"], "title": "数据安全审计技术体系与自动化实践", "subtitle": "从日志采集到合规报告的全链路方案"},
    {"date": "2025-09-18", "domain": "数据要素", "keywords": ["制造业", "工业数据", "数据空间"], "title": "制造业数据空间建设与数据要素安全流通", "subtitle": "工业互联网环境下的数据可信共享"},
    {"date": "2025-10-12", "domain": "人工智能", "keywords": ["AI代码生成", "Copilot", "开发安全"], "title": "AI辅助代码生成的安全性评估与治理建议", "subtitle": "大模型生成代码的漏洞模式与防护措施"},
    {"date": "2025-11-20", "domain": "隐私计算", "keywords": ["隐私计算标准", "互联互通", "行业标准"], "title": "隐私计算互联互通标准进展与产业影响", "subtitle": "跨平台协作的技术标准与生态建设"},
    {"date": "2026-01-15", "domain": "数据安全", "keywords": ["二进制安全", "恶意检测", "模型安全"], "title": "二进制级深度安全检测在模型部署中的实践", "subtitle": "ClamAV、YARA与ModelScan联合检测方案"},
    {"date": "2026-02-28", "domain": "数据要素", "keywords": ["数据要素", "2026展望", "政策趋势"], "title": "2026年数据要素市场发展趋势与政策展望", "subtitle": "从制度建设到规模化流通的关键转折"},
    # --- 新增30篇（2026-04 至 2028-12）---
    {"date": "2026-04-10", "domain": "人工智能", "keywords": ["OpenClaw", "开源AI", "法律智能"], "title": "OpenClaw开源法律AI平台技术架构与生态分析", "subtitle": "基于大语言模型的法律智能开源实践"},
    {"date": "2026-05-18", "domain": "数据安全", "keywords": ["AI数据安全", "模型隐私", "训练数据"], "title": "AI训练数据安全合规与隐私保护机制研究", "subtitle": "从数据采集到模型发布的全链路安全治理"},
    {"date": "2026-06-22", "domain": "隐私计算", "keywords": ["联邦学习", "大模型训练", "分布式隐私"], "title": "联邦学习在大模型分布式训练中的最新进展", "subtitle": "数据不出域条件下的大规模参数同步方案"},
    {"date": "2026-07-30", "domain": "数据要素", "keywords": ["新质生产力", "数据驱动", "产业升级"], "title": "新质生产力与数据要素驱动的产业升级路径", "subtitle": "十五五规划下数据要素赋能实体经济"},
    {"date": "2026-08-15", "domain": "人工智能", "keywords": ["AI+产业融合", "智能制造", "工业大模型"], "title": "AI+产业融合趋势与工业大模型应用前景", "subtitle": "人工智能赋能新型工业化的技术路径"},
    {"date": "2026-09-25", "domain": "数据安全", "keywords": ["低空经济", "无人机数据", "空域安全"], "title": "低空经济数据安全治理框架与政策建议", "subtitle": "无人机数据采集、传输与存储的安全机制"},
    {"date": "2026-10-20", "domain": "隐私计算", "keywords": ["同态加密", "FHE", "GPU加速"], "title": "全同态加密GPU加速方案与工程化瓶颈突破", "subtitle": "基于CUDA/ROCm的FHE密文运算性能优化"},
    {"date": "2026-11-12", "domain": "数据要素", "keywords": ["绿色发展", "碳数据", "ESG"], "title": "绿色发展框架下碳数据资产交易机制研究", "subtitle": "ESG数据治理标准与碳配额数据安全流通"},
    {"date": "2026-12-08", "domain": "人工智能", "keywords": ["DeepSeek", "MoE架构", "开源生态"], "title": "DeepSeek系列模型技术演进与行业影响评估", "subtitle": "MoE架构创新、训练效率优化与开源生态构建"},
    {"date": "2027-01-20", "domain": "数据安全", "keywords": ["跨境支付", "金融数据安全", "SWIFT"], "title": "跨境支付数据安全与隐私合规国际比较", "subtitle": "SWIFT替代方案与数字货币跨境数据流动机制"},
    {"date": "2027-02-15", "domain": "隐私计算", "keywords": ["零知识证明", "ZKP", "区块链隐私"], "title": "零知识证明在隐私保护数据验证中的应用", "subtitle": "zk-SNARKs与zk-STARKs工程实践与性能对比"},
    {"date": "2027-03-18", "domain": "数据要素", "keywords": ["人口数据", "老龄化", "精准服务"], "title": "人口结构变化下的数据要素精准服务机制", "subtitle": "老龄化社会养老、医疗与社保数据协同"},
    {"date": "2027-04-22", "domain": "人工智能", "keywords": ["AGI", "通用人工智能", "安全对齐"], "title": "通用人工智能安全对齐研究进展与挑战", "subtitle": "从RLHF到Constitutional AI的安全范式演进"},
    {"date": "2027-05-10", "domain": "数据安全", "keywords": ["智慧城市", "城市数据", "数据安全"], "title": "智慧城市数据安全治理架构与实施路径", "subtitle": "城市级数据中台的安全基线与隐私保护"},
    {"date": "2027-06-25", "domain": "隐私计算", "keywords": ["隐私计算", "AI推理", "模型即服务"], "title": "隐私保护AI推理服务的技术方案与商业模式", "subtitle": "模型即服务场景下的数据安全解决方案"},
    {"date": "2027-07-15", "domain": "数据要素", "keywords": ["现代产业体系", "数字供应链", "产业链安全"], "title": "现代产业体系中数据要素的核心枢纽作用", "subtitle": "数字供应链安全与产业链数据协同创新"},
    {"date": "2027-08-20", "domain": "人工智能", "keywords": ["量子计算", "量子AI", "量子优势"], "title": "量子计算与人工智能融合发展前沿研究", "subtitle": "量子机器学习算法在安全与优化中的应用"},
    {"date": "2027-09-12", "domain": "数据安全", "keywords": ["生物数据", "基因安全", "生物信息"], "title": "生物数据安全保护体系与国际监管比较", "subtitle": "基因组数据的存储加密与跨境流动管控"},
    {"date": "2027-10-28", "domain": "隐私计算", "keywords": ["可验证计算", "计算完整性", "远程证明"], "title": "可验证计算在安全外包中的关键技术进展", "subtitle": "计算完整性证明与远程证明协议优化"},
    {"date": "2027-11-15", "domain": "数据要素", "keywords": ["数据主权", "数字治理", "国际竞争"], "title": "数据主权背景下的全球数字治理竞争态势", "subtitle": "中美欧数据治理模式差异与战略博弈"},
    {"date": "2027-12-20", "domain": "人工智能", "keywords": ["AI芯片", "国产算力", "芯片安全"], "title": "国产AI芯片产业格局与算力安全评估", "subtitle": "从芯片设计到可信计算栈的自主可控路径"},
    {"date": "2028-01-25", "domain": "数据安全", "keywords": ["网络韧性", "灾备恢复", "业务连续性"], "title": "数据安全网络韧性体系建设与灾备战略", "subtitle": "关键信息基础设施的业务连续性管理"},
    {"date": "2028-03-10", "domain": "隐私计算", "keywords": ["隐私计算芯片", "硬件加速", "专用处理器"], "title": "隐私计算专用芯片设计与硬件加速前沿", "subtitle": "ASIC与FPGA在密文运算中的工程化实践"},
    {"date": "2028-04-18", "domain": "数据要素", "keywords": ["数据要素", "全球化", "数据贸易"], "title": "全球数据要素贸易格局与中国战略定位", "subtitle": "数据跨境流通规则与国际数据市场建设"},
    {"date": "2028-05-22", "domain": "人工智能", "keywords": ["AI医疗", "精准医疗", "隐私保护"], "title": "AI精准医疗场景下的数据隐私保护实践", "subtitle": "多中心临床数据联合分析的安全架构"},
    {"date": "2028-07-08", "domain": "数据安全", "keywords": ["数字信任", "信任框架", "可信生态"], "title": "数字信任基础设施建设方案与全球趋势", "subtitle": "从数字身份到可信数据空间的生态架构"},
    {"date": "2028-08-25", "domain": "隐私计算", "keywords": ["安全多方计算", "区块链", "Web3隐私"], "title": "安全多方计算与Web3隐私基础设施融合", "subtitle": "去中心化场景下的隐私保护技术方案"},
    {"date": "2028-10-15", "domain": "数据要素", "keywords": ["太空数据", "卫星数据", "遥感安全"], "title": "太空数据经济与卫星遥感数据安全治理", "subtitle": "低轨卫星通信数据的主权保护与商业流通"},
    {"date": "2028-11-20", "domain": "人工智能", "keywords": ["超级智能", "AI安全", "全球治理"], "title": "超级智能风险评估与全球AI安全治理框架", "subtitle": "从前沿模型评测到国际协调机制建设"},
    {"date": "2028-12-28", "domain": "数据安全", "keywords": ["2029展望", "数据安全趋势", "技术预测"], "title": "2029年数据安全技术与产业趋势前瞻", "subtitle": "后量子时代的安全架构演进与市场格局"},
]

assert len(ARTICLES) == 80

# ============================================================
# 图表生成函数
# ============================================================
def _save(fig, fn):
    fig.savefig(fn, facecolor='white', edgecolor='none')
    plt.close(fig)

def gen_line(fn, title, labels, series, ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for i, (k, v) in enumerate(series.items()):
        ax.plot(labels, v, color=COLORS[i % len(COLORS)], lw=2, marker='o', ms=4, label=k)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12); ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=9, framealpha=0.9); ax.grid(True, alpha=0.15)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    _save(fig, fn)

def gen_bar(fn, title, cats, vals, ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(cats, vals, color=[COLORS[i % len(COLORS)] for i in range(len(cats))], width=0.6)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12); ax.set_ylabel(ylabel, fontsize=10)
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+max(vals)*0.02, f'{v}', ha='center', va='bottom', fontsize=9)
    ax.grid(True, axis='y', alpha=0.15); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.xticks(rotation=20, ha='right', fontsize=9)
    _save(fig, fn)

def gen_pie(fn, title, labels, sizes):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=COLORS[:len(labels)], startangle=90, pctdistance=0.78)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    _save(fig, fn)

def gen_heatmap(fn, title, rows, cols, data):
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(data, cmap='Blues', aspect='auto')
    ax.set_xticks(range(len(cols))); ax.set_yticks(range(len(rows)))
    ax.set_xticklabels(cols, fontsize=9); ax.set_yticklabels(rows, fontsize=9)
    for i in range(len(rows)):
        for j in range(len(cols)):
            ax.text(j, i, f'{data[i][j]:.1f}', ha='center', va='center', fontsize=8,
                    color='white' if data[i][j] > np.max(data)*0.6 else 'black')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    fig.colorbar(im, ax=ax, shrink=0.8)
    _save(fig, fn)

def gen_area(fn, title, xlabels, series, ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    prev = np.zeros(len(xlabels))
    for i, (k, v) in enumerate(series.items()):
        d = np.array(v); ax.fill_between(range(len(xlabels)), prev, prev+d, alpha=0.6, color=COLORS[i%len(COLORS)], label=k); prev += d
    ax.set_xticks(range(len(xlabels))); ax.set_xticklabels(xlabels, fontsize=9, rotation=30, ha='right')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12); ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=9, loc='upper left'); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    _save(fig, fn)

def gen_scatter(fn, title, x, y, labels=None, xlabel='', ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 5))
    sizes = np.random.uniform(40, 200, len(x))
    ax.scatter(x, y, s=sizes, c=COLORS[:len(x)], alpha=0.7, edgecolors='white', lw=1)
    if labels:
        for i, l in enumerate(labels):
            ax.annotate(l, (x[i], y[i]), fontsize=8, ha='center', va='bottom', xytext=(0, 6), textcoords='offset points')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel, fontsize=10); ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(True, alpha=0.15); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    _save(fig, fn)

def gen_violin(fn, title, labels, data_list):
    fig, ax = plt.subplots(figsize=(8, 5))
    parts = ax.violinplot(data_list, showmeans=True, showmedians=True)
    for i, pc in enumerate(parts.get('bodies', [])):
        pc.set_facecolor(COLORS[i % len(COLORS)]); pc.set_alpha(0.6)
    ax.set_xticks(range(1, len(labels)+1)); ax.set_xticklabels(labels, fontsize=9)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.grid(True, axis='y', alpha=0.15); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    _save(fig, fn)

def gen_radar(fn, title, cats, vals):
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    N = len(cats); angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    vp = vals + [vals[0]]; angles += angles[:1]
    ax.fill(angles, vp, color=PRIMARY, alpha=0.2); ax.plot(angles, vp, color=PRIMARY, lw=2, marker='o', ms=5)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(cats, fontsize=9)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=20)
    _save(fig, fn)

def gen_grouped_bar(fn, title, cats, groups, ylabel=''):
    fig, ax = plt.subplots(figsize=(9, 5))
    ng = len(groups); x = np.arange(len(cats)); w = 0.8 / ng
    for i, (k, v) in enumerate(groups.items()):
        ax.bar(x + i*w - 0.4 + w/2, v, w, label=k, color=COLORS[i%len(COLORS)], alpha=0.85)
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=9)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12); ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, axis='y', alpha=0.15)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    _save(fig, fn)

def gen_hbar(fn, title, cats, vals, xlabel=''):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(range(len(cats)), vals, color=[COLORS[i%len(COLORS)] for i in range(len(cats))], height=0.55)
    ax.set_yticks(range(len(cats))); ax.set_yticklabels(cats, fontsize=9)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12); ax.set_xlabel(xlabel, fontsize=10)
    for i, v in enumerate(vals):
        ax.text(v + max(vals)*0.02, i, f'{v}', va='center', fontsize=9)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.grid(True, axis='x', alpha=0.15)
    _save(fig, fn)


# ============================================================
# 为每篇文章生成 3-6 张图表
# ============================================================
def generate_charts(idx, article):
    """生成图表。
    关键改进：使用 _chart_seed(title) 保证同一标题图表数据一致。
    新增文章(idx >= 50)仅生成1-2张图表。
    """
    charts = []
    pf = f'chart_{idx+1:03d}'
    dom = article['domain']; yr = int(article['date'][:4])
    is_new = idx >= 50  # 新增30篇仅1-2张图

    # 1) 趋势折线图 — 每个domain只有一套趋势数据
    title1 = f'{dom}市场规模增长趋势'
    seed1 = _chart_seed(title1)
    random.seed(seed1); np.random.seed(seed1)
    f1 = f'{pf}_trend.png'
    # 统一使用2020-2028的数据范围
    yrs = [str(y) for y in range(2020, 2029)]
    gen_line(str(CHARTS_DIR/f1), title1, yrs,
             {'市场规模(亿元)': [random.uniform(20,50)*(1.3**i) for i in range(len(yrs))],
              '同比增长率(%)': [random.uniform(15,45) for _ in yrs]}, ylabel='规模/增长率')
    charts.append(f1)

    if is_new:
        # 新文章：仅再生成1张变体图表
        vt = idx % 5
        title_v = {
            0: f'{dom}行业需求热力矩阵',
            1: f'{dom}投资分布趋势',
            2: f'{dom}平台能力评估',
            3: f'{dom}方案性能对比',
            4: f'{dom}解决方案综合评估',
        }[vt]
        seed_v = _chart_seed(title_v)
        random.seed(seed_v); np.random.seed(seed_v)
        f4 = f'{pf}_variant.png'
        if vt == 0:
            gen_heatmap(str(CHARTS_DIR/f4), title_v,
                        ['安全性','性能','易用性','成本','合规度'], ['金融','医疗','政务','能源'],
                        np.array([[random.uniform(3,10) for _ in range(4)] for _ in range(5)]))
        elif vt == 1:
            y4 = [str(y) for y in range(2021, 2029)]
            gen_area(str(CHARTS_DIR/f4), title_v, y4,
                     {'政府投资':[random.uniform(10,30)*(1.2**i) for i in range(len(y4))],
                      '企业投资':[random.uniform(15,40)*(1.25**i) for i in range(len(y4))],
                      '风险投资':[random.uniform(5,20)*(1.3**i) for i in range(len(y4))]}, ylabel='亿元')
        elif vt == 2:
            gen_scatter(str(CHARTS_DIR/f4), title_v,
                        [random.uniform(40,95) for _ in range(8)],
                        [random.uniform(40,95) for _ in range(8)],
                        labels=[f'厂商{chr(65+i)}' for i in range(8)],
                        xlabel='技术成熟度', ylabel='市场覆盖度')
        elif vt == 3:
            gen_violin(str(CHARTS_DIR/f4), title_v,
                       ['方案A','方案B','方案C','方案D'],
                       [np.random.normal(random.uniform(50,80), random.uniform(5,15), 50) for _ in range(4)])
        else:
            gen_radar(str(CHARTS_DIR/f4), title_v,
                      ['安全性','性能','易用性','扩展性','合规性','成本效益'],
                      [random.uniform(5,10) for _ in range(6)])
        charts.append(f4)
        return charts

    # 原50篇：保持3-6张图表
    # 2) 行业分布柱状图
    title2 = f'{dom}行业应用投入分布'
    seed2 = _chart_seed(title2)
    random.seed(seed2); np.random.seed(seed2)
    f2 = f'{pf}_industry.png'; cs = ['金融','医疗','政务','能源','交通','制造']
    gen_bar(str(CHARTS_DIR/f2), title2, cs,
            [random.randint(15,95) for _ in cs], ylabel='投入占比(%)')
    charts.append(f2)

    # 3) 饼图
    title3 = f'{dom}技术路线市场份额'
    seed3 = _chart_seed(title3)
    random.seed(seed3); np.random.seed(seed3)
    f3 = f'{pf}_share.png'
    tl = {'数据要素':['数据采集','数据治理','数据交易','数据安全','数据分析'],
          '隐私计算':['联邦学习','安全多方计算','可信执行环境','差分隐私','同态加密'],
          '数据安全':['加密技术','访问控制','审计监控','脱敏脱标','漏洞防护'],
          '人工智能':['大语言模型','计算机视觉','语音识别','知识图谱','强化学习']}
    gen_pie(str(CHARTS_DIR/f3), title3,
            tl.get(dom, tl['数据要素']), [random.randint(10,40) for _ in range(5)])
    charts.append(f3)

    # 4) 变体图表
    vt = idx % 5
    title_map = {
        0: f'{dom}行业需求热力矩阵',
        1: f'{dom}投资分布趋势',
        2: f'{dom}平台能力评估',
        3: f'{dom}方案性能对比',
        4: f'{dom}解决方案综合评估',
    }
    title4 = title_map[vt]
    seed4 = _chart_seed(title4)
    random.seed(seed4); np.random.seed(seed4)
    if vt == 0:
        f4 = f'{pf}_heatmap.png'
        gen_heatmap(str(CHARTS_DIR/f4), title4,
                    ['安全性','性能','易用性','成本','合规度'], ['金融','医疗','政务','能源'],
                    np.array([[random.uniform(3,10) for _ in range(4)] for _ in range(5)]))
    elif vt == 1:
        f4 = f'{pf}_area.png'; y4 = [str(y) for y in range(2021, 2029)]
        gen_area(str(CHARTS_DIR/f4), title4, y4,
                 {'政府投资':[random.uniform(10,30)*(1.2**i) for i in range(len(y4))],
                  '企业投资':[random.uniform(15,40)*(1.25**i) for i in range(len(y4))],
                  '风险投资':[random.uniform(5,20)*(1.3**i) for i in range(len(y4))]}, ylabel='亿元')
    elif vt == 2:
        f4 = f'{pf}_scatter.png'
        gen_scatter(str(CHARTS_DIR/f4), title4,
                    [random.uniform(40,95) for _ in range(8)],
                    [random.uniform(40,95) for _ in range(8)],
                    labels=[f'厂商{chr(65+i)}' for i in range(8)],
                    xlabel='技术成熟度', ylabel='市场覆盖度')
    elif vt == 3:
        f4 = f'{pf}_violin.png'
        gen_violin(str(CHARTS_DIR/f4), title4,
                   ['方案A','方案B','方案C','方案D'],
                   [np.random.normal(random.uniform(50,80), random.uniform(5,15), 50) for _ in range(4)])
    else:
        f4 = f'{pf}_radar.png'
        gen_radar(str(CHARTS_DIR/f4), title4,
                  ['安全性','性能','易用性','扩展性','合规性','成本效益'],
                  [random.uniform(5,10) for _ in range(6)])
    charts.append(f4)

    # 5) 分组柱状图 (50%)
    if idx % 2 == 0:
        title5 = f'{dom}分领域发展对比'
        seed5 = _chart_seed(title5)
        random.seed(seed5); np.random.seed(seed5)
        f5 = f'{pf}_grouped.png'; y5 = [str(y) for y in range(2024, 2029)]
        gen_grouped_bar(str(CHARTS_DIR/f5), title5, y5,
                        {'技术研发':[random.randint(20,80) for _ in y5],
                         '产品落地':[random.randint(15,70) for _ in y5],
                         '标准建设':[random.randint(10,50) for _ in y5]}, ylabel='指数')
        charts.append(f5)

    # 6) 水平柱状图 (33%)
    if idx % 3 == 0:
        title6 = f'{dom}重点任务优先级'
        seed6 = _chart_seed(title6)
        random.seed(seed6); np.random.seed(seed6)
        f6 = f'{pf}_hbar.png'
        gen_hbar(str(CHARTS_DIR/f6), title6,
                 ['数据治理','安全合规','技术研发','人才建设','标准制定','生态建设','场景拓展'],
                 [random.randint(30,100) for _ in range(7)], xlabel='优先级指数')
        charts.append(f6)

    return charts


# ============================================================
# HTML 辅助
# ============================================================
E = html_mod.escape

def fig_html(chart, caption):
    return f'<figure class="article-figure"><img src="{chart}" alt="{E(caption)}" loading="lazy"><figcaption>{E(caption)}</figcaption></figure>'

def stat_row(items):
    c = ''.join(f'<div class="article-stat-card"><span class="stat-val">{E(v)}</span><span class="stat-label">{E(l)}</span></div>' for v, l in items)
    return f'<div class="article-stat-row">{c}</div>'

def highlight(title, text):
    return f'<div class="article-highlight"><h4>{E(title)}</h4><p>{E(text)}</p></div>'

def table(headers, rows):
    ths = ''.join(f'<th>{E(h)}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{E(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>'


# ============================================================
# 正文 HTML
# ============================================================
def generate_body(idx, article, charts):
    random.seed(idx * 99 + 13)
    d = article; yr = d['date'][:4]; dom = d['domain']
    kw = '、'.join(d['keywords'])

    abstracts = {
        '数据要素': f"随着数字经济的快速发展，数据作为新型生产要素的战略价值日益凸显。本报告围绕{kw}等核心议题，系统梳理了{yr}年度数据要素领域的政策动态、技术进展与产业实践，为相关机构的战略决策提供参考依据。",
        '隐私计算': f"隐私计算作为实现\"数据可用不可见\"的关键技术，在{yr}年持续获得政策支持与产业关注。本报告聚焦{kw}等技术方向，深入分析当前技术进展、工程化挑战与市场格局，为技术选型与方案建设提供系统性参考。",
        '数据安全': f"在日趋复杂的网络安全态势下，数据安全已成为国家安全的重要组成部分。本报告围绕{kw}等重点领域，全面评估当前安全威胁形势、技术防护能力与合规建设进展，为安全治理体系建设提供分析支撑。",
        '人工智能': f"人工智能技术的快速迭代正深刻重塑各行业的生产方式与服务模式。本报告聚焦{kw}等前沿方向，对{yr}年度技术演进、产业应用与治理挑战进行系统分析，为AI战略布局提供决策参考。",
    }
    ab = abstracts.get(dom, abstracts['数据要素'])
    ms = random.randint(80, 350); gr = random.randint(25, 55)
    dg = random.randint(50, 65); gp = random.randint(42, 48)
    fp = random.randint(28, 40); gg = random.randint(40, 70); rp = random.randint(65, 80)
    pt = random.randint(20, 60); kb = random.choice(['128位','256位'])
    cr = random.randint(40, 70); vp = random.randint(60, 85)
    al = random.randint(2, 5); fg = random.randint(30, 50)

    p = []

    # Abstract
    p.append(f'<div class="article-abstract">{E(ab)}</div>')

    # Info table
    p.append(f'''<table class="article-info-table">
<tr><td>发布日期</td><td>{d["date"]}</td></tr>
<tr><td>研究领域</td><td>{dom}</td></tr>
<tr><td>关键词</td><td>{", ".join(d["keywords"])}</td></tr>
<tr><td>作者</td><td>Chatchat Technology 行业研究中心</td></tr>
</table>''')

    # 第一章
    p.append(f'''<h2>一、研究背景与目的</h2>
<h3>1.1 研究背景</h3>
<p>{yr}年，{dom}领域迎来了重要的发展节点。从政策层面看，国家持续出台系列指导文件，为行业发展提供明确的制度框架与政策导向。从技术层面看，{kw}等核心技术取得显著进展，工程化成熟度不断提升。从市场层面看，越来越多的行业场景开始规模化应用相关技术方案，产业生态日趋完善。</p>
<p>当前，数字经济已成为推动经济增长的重要引擎。据统计，{yr}年我国数字经济规模预计突破{dg}万亿元，占GDP比重超过{gp}%。在此背景下，{dom}的战略价值进一步凸显，成为各方竞相布局的重点领域。</p>''')

    p.append(stat_row([(f'{dg}万亿','数字经济规模'),(f'{gp}%','GDP占比'),
                        (f'{ms}亿',f'{dom}市场'),(f'{gr}%','同比增长')]))

    p.append(f'''<h3>1.2 研究目的</h3>
<p>本报告旨在系统梳理{dom}领域的最新进展，重点分析{kw}等方向的技术演进、应用实践与发展趋势，为决策者提供全局性的认知框架与行动参考。</p>''')

    p.append(fig_html(f'charts/{charts[0]}', f'图1: {dom}市场规模增长趋势'))

    # 第二章
    py = int(yr)
    p.append(f'''<h2>二、行业发展现状</h2>
<h3>2.1 政策环境</h3>
<p>在政策层面，近年来围绕{dom}的制度供给持续加强。从中央到地方，已形成较为完整的政策体系：</p>
<ul>
<li><strong>国家层面</strong>：多部委联合发文，从顶层设计角度明确{dom}的发展方向与重点任务</li>
<li><strong>行业层面</strong>：金融、医疗、政务等重点领域出台专项指导意见，推动技术标准与规范建设</li>
<li><strong>地方层面</strong>：北京、上海、广东、浙江等数字经济先发地区先行先试，形成可复制推广的经验</li>
</ul>''')

    p.append(highlight('政策要点',
        f'{py}年，国务院及相关部委共发布{dom}领域相关政策文件{random.randint(8,20)}项，'
        f'地方配套措施{random.randint(30,80)}项，标志着{dom}进入全面加速推进阶段。'))

    p.append(f'''<h3>2.2 市场规模</h3>
<p>据行业研究机构统计，{yr}年中国{dom}市场规模达到约{ms}亿元，同比增长{gr}%。其中，金融行业仍是最大的应用市场，占比约{fp}%；政务领域增速最快，年增长率超过{gg}%。</p>
<p>从区域分布看，长三角、京津冀和粤港澳大湾区是三大核心市场，合计占全国市场份额的{rp}%以上。</p>''')

    if len(charts) > 1:
        p.append(fig_html(f'charts/{charts[1]}', f'图2: {dom}行业应用投入分布'))

    p.append(table(['区域','市场占比','增速','代表城市'],
                    [['长三角',f'{random.randint(25,35)}%',f'{random.randint(30,55)}%','上海、杭州、南京'],
                     ['京津冀',f'{random.randint(20,30)}%',f'{random.randint(25,45)}%','北京、天津'],
                     ['粤港澳',f'{random.randint(15,25)}%',f'{random.randint(35,60)}%','深圳、广州'],
                     ['中西部',f'{random.randint(8,15)}%',f'{random.randint(40,70)}%','成都、武汉、西安']]))

    # 第三章
    p.append(f'''<h2>三、核心技术分析</h2>
<h3>3.1 技术发展脉络</h3>
<p>{dom}的技术发展经历了从理论探索到工程落地的演进过程。在{kw}等方向，{yr}年取得了以下重要进展：</p>
<p><strong>技术成熟度提升</strong>：核心算法的工程化实现日趋完善，性能指标持续优化。以隐私计算为例，千万级数据规模的处理效率已从小时级提升至分钟级，为大规模商业化应用奠定了基础。</p>
<p><strong>标准化进程加速</strong>：行业标准的制定与发布明显提速，国家标准、行业标准与团体标准形成多层次的标准体系，为技术互联互通与产品评测认证提供了依据。</p>
<p><strong>开源生态活跃</strong>：国内外开源社区持续贡献高质量的技术实现，降低了技术门槛，加速了创新扩散。</p>''')

    if len(charts) > 2:
        p.append(fig_html(f'charts/{charts[2]}', f'图3: {dom}技术路线市场份额'))

    p.append('<h3>3.2 关键技术指标</h3>')
    p.append(table(['指标维度','当前水平','发展趋势'],
                    [['计算效率',f'千万级数据{pt}秒处理','持续优化，向亿级突破'],
                     ['安全强度',f'{kb}密钥安全','后量子密码迁移推进'],
                     ['部署成本',f'较三年前降低{cr}%','容器化与云原生持续降本'],
                     ['易用性',f'可视化配置覆盖{vp}%场景','低代码化趋势明显'],
                     ['互联互通',f'已支持{random.randint(3,8)}种主流协议','标准统一进程加快']]))

    p.append(stat_row([(f'{pt}秒','千万级处理'),(kb,'安全强度'),(f'{cr}%','成本降低'),(f'{vp}%','可视化覆盖')]))

    if len(charts) > 3:
        p.append(fig_html(f'charts/{charts[3]}', f'图4: {dom}多维度分析'))

    # 第四章
    p.append(f'''<h2>四、典型应用场景与实践</h2>
<h3>4.1 金融行业</h3>
<p>金融行业是{dom}技术应用最为成熟的领域。在信用评估、反欺诈、反洗钱等场景中，隐私计算技术已从POC验证进入规模化生产阶段。多家头部银行与金融科技公司建立了跨机构联合建模能力，在不共享原始数据的前提下实现了风控模型AUC指标{al}%以上的提升。</p>''')

    p.append(highlight('案例：某股份制银行联合建模',
        f'通过联邦学习技术实现跨机构信用评估模型训练，模型AUC提升{al}%，'
        f'不良贷款识别率提高{random.randint(10,25)}%，数据全程不出域。'))

    p.append(f'''<h3>4.2 医疗健康</h3>
<p>医疗数据的敏感性使其成为隐私保护技术的典型应用场景。跨院区的临床数据协同分析、药物研发中的多方数据联合建模、医疗影像的联邦学习等方向均取得实质性进展。</p>
<h3>4.3 政务治理</h3>
<p>数字政府建设推动政务数据的跨部门、跨层级共享需求持续增长。通过联邦查询等技术手段，在保障数据安全边界的前提下实现了公安、社保、税务等多部门数据的联合分析。</p>''')

    p.append(table(['应用领域','典型场景','数据规模','技术方案','成效'],
                    [['金融','联合风控',f'{random.randint(1,10)}亿条','联邦学习',f'AUC+{al}%'],
                     ['医疗','临床协同',f'{random.randint(500,5000)}万条','安全多方计算',f'研究效率×{random.randint(2,5)}'],
                     ['政务','综合研判',f'{random.randint(2,20)}亿条','联邦查询',f'响应时间-{random.randint(40,70)}%'],
                     ['能源','电力调度',f'{random.randint(1,8)}亿条','TEE计算',f'预测精度+{random.randint(5,15)}%']]))

    if len(charts) > 4:
        p.append(fig_html(f'charts/{charts[4]}', f'图5: {dom}分领域发展对比'))

    # 第五章
    p.append(f'''<h2>五、挑战与发展建议</h2>
<h3>5.1 当前挑战</h3>
<p>尽管{dom}领域取得了显著进展，但仍面临以下核心挑战：</p>
<ol>
<li><strong>技术与业务匹配度不足</strong> — 部分技术方案在实验环境表现优异，但在真实业务场景中面临数据质量、系统集成、运维复杂度等问题</li>
<li><strong>标准体系有待完善</strong> — 技术标准与业务标准的衔接不够紧密，跨平台互联互通能力不足</li>
<li><strong>复合型人才短缺</strong> — 兼具密码学、机器学习、系统工程与行业知识的复合型人才供给严重不足</li>
<li><strong>商业模式探索中</strong> — 从技术能力到商业价值的转化路径尚不清晰</li>
</ol>''')

    p.append('<blockquote><p>"数据要素的价值释放，需要技术、制度、生态三者的协同创新。单纯的技术突破并不足以驱动产业规模化发展。" — 行业专家观点</p></blockquote>')

    if len(charts) > 5:
        p.append(fig_html(f'charts/{charts[5]}', f'图6: {dom}重点任务优先级排序'))

    p.append(f'''<h3>5.2 发展建议</h3>
<ul>
<li><strong>强化顶层设计</strong>：完善法律法规与标准规范，为技术应用提供清晰的合规边界</li>
<li><strong>推进技术攻关</strong>：在高性能密码学算法、大规模联邦计算引擎等方向持续投入研发</li>
<li><strong>深化场景落地</strong>：以金融、医疗、政务等关键行业为突破口，建立可复制的标杆案例</li>
<li><strong>构建人才体系</strong>：加强高校学科建设与产教融合，培养多层次的专业人才队伍</li>
<li><strong>推动生态建设</strong>：通过开源协作、产业联盟等方式，构建开放共赢的产业生态</li>
</ul>''')

    # 第六章
    p.append(f'''<h2>六、发展展望</h2>
<p>展望未来，{dom}领域将呈现以下发展趋势：</p>
<p><strong>技术融合加速</strong>：隐私计算与人工智能、区块链、云计算等技术的深度融合将催生新的技术范式与应用场景。</p>
<p><strong>应用规模化</strong>：随着技术成熟度提升与成本持续下降，{dom}应用将从头部机构向中小企业延伸，市场规模有望保持{fg}%以上的年均增速。</p>
<p><strong>治理体系完善</strong>：全球范围内的数据治理制度将持续演进，中国在制度建设与技术标准方面的国际影响力将进一步提升。</p>
<p><strong>产业生态成熟</strong>：从基础技术到应用平台，从咨询服务到运营支撑，完整的产业链条将逐步形成。</p>''')

    p.append(stat_row([(f'{fg}%+','年均增速预期'),
                        (f'{random.randint(500,2000)}亿',f'{int(yr)+2}年市场预测'),
                        (f'{random.randint(3,8)}倍','应用场景扩展')]))

    p.append('<hr>')
    p.append('<p style="color:#86909C;font-size:0.9rem;font-style:italic;">本报告由 Chatchat Technology 行业研究中心撰写发布，仅供行业参考与学术交流使用。</p>')

    return ab, '\n'.join(p)


# ============================================================
# 生成独立 HTML 页面
# ============================================================
def build_html(idx, article, charts, body_html):
    d = article
    slug = f'{d["date"].replace("-","")}-{idx+1:03d}'
    # 1:1 唯一映射：每篇文章对应唯一Hero图片，不使用random
    hero_img = ALL_HERO_IMAGES[idx]
    read_min = max(5, len(body_html) // 800)

    # Related articles
    related = [a for i, a in enumerate(ARTICLES) if a['domain'] == d['domain'] and i != idx]
    random.seed(idx + 1000); random.shuffle(related)
    related = related[:3]
    rel_html = ''
    if related:
        rc = []
        for r in related:
            ri = ARTICLES.index(r)
            rs = f'{r["date"].replace("-","")}-{ri+1:03d}'
            rc.append(f'<a class="related-card" href="{rs}.html"><span class="rc-domain">{E(r["domain"])}</span><span class="rc-title">{E(r["title"])}</span><span class="rc-date">{r["date"]}</span></a>')
        rel_html = f'<section class="article-related"><div class="container"><h3>相关研究</h3><div class="related-grid">{"".join(rc)}</div></div></section>'

    tags = ''.join(f'<span class="article-tag">{E(k)}</span>' for k in d['keywords'])

    page_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(d["title"])} - Chatchat Technology</title>
<meta name="description" content="{E(d["subtitle"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
<link rel="stylesheet" href="../css/article.css">
</head>
<body>
<header class="header" id="header">
<div class="container header-inner">
<a href="../index.html" class="logo"><span class="logo-icon">CC</span><span class="logo-text">查特查特科技</span></a>
<nav class="nav" id="nav">
<a href="../index.html" class="nav-link">首页</a>
<a href="../index.html#products" class="nav-link">核心产品</a>
<a href="../index.html#components" class="nav-link">技术组件</a>
<a href="../index.html#advantages" class="nav-link">技术优势</a>
<a href="../research.html" class="nav-link active">行业研究</a>
<a href="../index.html#about" class="nav-link">关于我们</a>
</nav>
<button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="菜单"><span></span><span></span><span></span></button>
</div>
</header>

<section class="article-hero">
<div class="article-hero-bg" style="background-image:url('{hero_img}')"></div>
<div class="article-hero-overlay"></div>
<div class="article-hero-content">
<span class="article-meta-domain">{E(d["domain"])}</span>
<h1>{E(d["title"])}</h1>
<p class="article-subtitle">{E(d["subtitle"])}</p>
<div class="article-byline">
<div class="article-byline-avatar">CC</div>
<div class="article-byline-info">
<span class="article-byline-name">Chatchat Technology 行业研究中心</span>
<div class="article-byline-detail"><span>{d["date"]}</span><span>约 {read_min} 分钟阅读</span></div>
</div>
</div>
</div>
</section>

<article class="article-body">
<a href="../research.html" class="article-back">&larr; 返回研究列表</a>
{body_html}
<div class="article-tags">{tags}</div>
<div class="article-author-box">
<div class="article-author-avatar">CC</div>
<div class="article-author-info">
<h4>Chatchat Technology 行业研究中心</h4>
<p>聚焦数据要素、隐私计算、数据安全与人工智能前沿领域的深度研究</p>
</div>
</div>
</article>

{rel_html}

<footer class="footer">
<div class="container">
<div style="display:flex;justify-content:space-between;align-items:center;padding:24px 0;">
<div class="footer-brand"><div class="logo"><span class="logo-icon">CC</span><span class="logo-text">查特查特科技</span></div></div>
<div style="font-size:0.85rem;color:#86909C;"><a href="mailto:ink@chatchat.space" style="color:#86909C;text-decoration:none;">ink@chatchat.space</a></div>
</div>
<div class="footer-bottom" style="text-align:center;padding:16px 0;border-top:1px solid rgba(255,255,255,0.08);font-size:0.8rem;color:#4E5969;">
<p>&copy; 2024-2028 Chatchat Technology 查特查特科技有限公司. All rights reserved.</p>
</div>
</div>
</footer>

<button class="back-to-top" id="backToTop" aria-label="回到顶部" style="display:none;position:fixed;bottom:32px;right:32px;z-index:999;">
<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 16V4M4 10l6-6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>

<script src="../js/dotmatrix.js"></script>
<script>
(function(){{
var h=document.getElementById("header");
window.addEventListener("scroll",function(){{h.classList.toggle("scrolled",window.scrollY>20)}});
var mb=document.getElementById("mobileMenuBtn"),nv=document.getElementById("nav");
if(mb)mb.addEventListener("click",function(){{nv.classList.toggle("active");mb.classList.toggle("active")}});
var bt=document.getElementById("backToTop");
window.addEventListener("scroll",function(){{bt.style.display=window.scrollY>400?"flex":"none"}});
if(bt)bt.addEventListener("click",function(){{window.scrollTo({{top:0,behavior:"smooth"}})}});
}})();
</script>
</body>
</html>'''
    return page_html, hero_img


# ============================================================
# 主流程
# ============================================================
def main():
    os.makedirs(CHARTS_DIR, exist_ok=True)
    meta = []

    for idx, art in enumerate(ARTICLES):
        print(f'[{idx+1:02d}/80] {art["title"]}')
        charts = generate_charts(idx, art)
        _, body = generate_body(idx, art, charts)
        slug = f'{art["date"].replace("-","")}-{idx+1:03d}'
        html, hero_img = build_html(idx, art, charts, body)
        with open(RESEARCH_DIR / f'{slug}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        meta.append({
            'index': idx + 1, 'slug': slug, 'filename': f'{slug}.html',
            'title': art['title'], 'subtitle': art['subtitle'],
            'date': art['date'], 'domain': art['domain'],
            'keywords': art['keywords'], 'charts': charts,
            'hero_image': hero_img,
        })

    with open(RESEARCH_DIR / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f'\n✓ 已生成 {len(meta)} 篇 HTML 研究报告（包含未来预发布文章）')
    print(f'  图表: {CHARTS_DIR}')
    print(f'  报告: {RESEARCH_DIR}')

if __name__ == '__main__':
    main()
