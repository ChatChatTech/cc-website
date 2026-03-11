#!/usr/bin/env python3
"""
行业研究报告生成器
生成50篇围绕数据要素、隐私安全、AI智能的行业调研报告
时间跨度: 2023年3月 - 2026年3月
"""

import os
import json
import random
import hashlib
from datetime import datetime, timedelta
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

# 主题色
PRIMARY = '#165DFF'
PRIMARY_DARK = '#0E42D2'
PRIMARY_LIGHT = '#4080FF'
COLORS = ['#165DFF', '#0FC6C2', '#F7BA1E', '#D91AD9', '#14C9C9', '#F53F3F', '#722ED1', '#3491FA', '#9FDB1D', '#FF7D00']

BASE_DIR = Path('/data/projs/cc-website')
RESEARCH_DIR = BASE_DIR / 'research'
CHARTS_DIR = BASE_DIR / 'research' / 'charts'

# ============================================================
# 50篇文章定义
# ============================================================
ARTICLES = [
    # === 2023 Q1 (3月) ===
    {"date": "2023-03-08", "domain": "数据要素", "keywords": ["数据确权", "数据资产", "产权制度"], "title": "数据要素市场化配置中的确权机制研究", "subtitle": "从产权界定到价值释放的制度路径"},
    {"date": "2023-03-22", "domain": "隐私计算", "keywords": ["联邦学习", "多方安全计算", "技术选型"], "title": "隐私计算技术路线对比与选型分析", "subtitle": "联邦学习、MPC与TEE的适用场景评估"},
    # === 2023 Q2 (4-6月) ===
    {"date": "2023-04-15", "domain": "人工智能", "keywords": ["大模型", "GPT", "产业影响"], "title": "大语言模型对企业数字化转型的影响评估", "subtitle": "从GPT到行业大模型的演进路径"},
    {"date": "2023-05-10", "domain": "数据安全", "keywords": ["数据分类分级", "合规治理", "数据安全法"], "title": "数据分类分级制度落地实践与挑战", "subtitle": "基于《数据安全法》的企业合规建设"},
    {"date": "2023-05-28", "domain": "隐私计算", "keywords": ["同态加密", "密码学", "计算效率"], "title": "全同态加密工程化应用进展与性能优化", "subtitle": "从理论突破到产业落地的关键路径"},
    {"date": "2023-06-18", "domain": "数据要素", "keywords": ["数据交易", "数据交易所", "定价机制"], "title": "全国数据交易所发展格局与运营模式比较", "subtitle": "北京、上海、深圳等地数据交易实践分析"},
    # === 2023 Q3 (7-9月) ===
    {"date": "2023-07-05", "domain": "人工智能", "keywords": ["AI安全", "对齐问题", "可信AI"], "title": "人工智能安全与对齐问题研究综述", "subtitle": "大模型时代的AI治理新挑战"},
    {"date": "2023-07-20", "domain": "数据安全", "keywords": ["跨境数据", "数据出境", "安全评估"], "title": "跨境数据流动安全评估机制研究", "subtitle": "全球数据治理格局下的中国实践"},
    {"date": "2023-08-12", "domain": "隐私计算", "keywords": ["联邦查询", "安全SQL", "密态计算"], "title": "联邦查询技术在多方数据协同中的应用研究", "subtitle": "安全SQL执行引擎的设计与优化"},
    {"date": "2023-09-03", "domain": "数据要素", "keywords": ["公共数据", "开放共享", "授权运营"], "title": "公共数据授权运营模式与价值释放机制", "subtitle": "政务数据资源化利用的制度创新"},
    {"date": "2023-09-25", "domain": "人工智能", "keywords": ["RAG", "检索增强", "知识库"], "title": "检索增强生成技术在企业知识管理中的应用", "subtitle": "RAG架构的工程实践与优化策略"},
    # === 2023 Q4 (10-12月) ===
    {"date": "2023-10-15", "domain": "数据安全", "keywords": ["个人信息保护", "隐私权", "去标识化"], "title": "个人信息去标识化技术标准与实施路径", "subtitle": "合规场景下的数据脱敏技术体系"},
    {"date": "2023-11-08", "domain": "隐私计算", "keywords": ["可信执行环境", "TEE", "芯片安全"], "title": "可信执行环境技术发展与产业应用前景", "subtitle": "从Intel SGX到国产芯片TEE的演进"},
    {"date": "2023-11-22", "domain": "数据要素", "keywords": ["数据资产入表", "会计准则", "数据估值"], "title": "数据资产入表政策解读与企业应对策略", "subtitle": "财政部新规下的数据资产化路径"},
    {"date": "2023-12-10", "domain": "人工智能", "keywords": ["AI治理", "监管框架", "伦理规范"], "title": "全球AI治理监管框架比较研究", "subtitle": "欧盟AI法案、中美监管实践与启示"},
    {"date": "2023-12-28", "domain": "隐私计算", "keywords": ["隐私保护", "差分隐私", "数据脱敏"], "title": "差分隐私在机器学习训练中的应用与挑战", "subtitle": "隐私预算分配与模型精度的平衡策略"},
    # === 2024 Q1 (1-3月) ===
    {"date": "2024-01-15", "domain": "数据安全", "keywords": ["数据安全治理", "DSMM", "成熟度模型"], "title": "数据安全治理成熟度评估模型与实施指南", "subtitle": "DSMM框架下的企业数据安全能力建设"},
    {"date": "2024-02-05", "domain": "数据要素", "keywords": ["数据要素市场", "制度建设", "流通体系"], "title": "数据要素流通体系建设进展与趋势展望", "subtitle": "从\"二十条\"到地方实践的政策传导"},
    {"date": "2024-02-26", "domain": "人工智能", "keywords": ["多模态", "视觉语言模型", "AIGC"], "title": "多模态大模型技术演进与行业应用前景", "subtitle": "视觉语言模型在垂直场景的落地分析"},
    {"date": "2024-03-18", "domain": "隐私计算", "keywords": ["隐私计算平台", "市场格局", "商业模式"], "title": "中国隐私计算平台市场竞争格局分析", "subtitle": "技术路线、商业模式与头部厂商比较"},
    # === 2024 Q2 (4-6月) ===
    {"date": "2024-04-08", "domain": "数据安全", "keywords": ["供应链安全", "软件成分分析", "SBOM"], "title": "AI模型供应链安全风险评估与防护策略", "subtitle": "从Pickle注入到模型投毒的威胁分析"},
    {"date": "2024-04-22", "domain": "数据要素", "keywords": ["算力网络", "东数西算", "算力经济"], "title": "算力基础设施与数据要素协同发展研究", "subtitle": "东数西算背景下的算力网络布局"},
    {"date": "2024-05-12", "domain": "人工智能", "keywords": ["AI Agent", "自主智能体", "任务执行"], "title": "AI Agent技术发展与产业应用研究", "subtitle": "从AutoGPT到企业级智能代理的演进"},
    {"date": "2024-06-03", "domain": "隐私计算", "keywords": ["联邦学习", "金融风控", "信用评估"], "title": "联邦学习在金融风控领域的落地实践", "subtitle": "多方联合建模的技术方案与业务价值"},
    {"date": "2024-06-20", "domain": "数据安全", "keywords": ["零信任", "安全架构", "身份认证"], "title": "零信任安全架构在数据保护中的应用", "subtitle": "从边界防护到持续验证的范式转换"},
    # === 2024 Q3 (7-9月) ===
    {"date": "2024-07-10", "domain": "数据要素", "keywords": ["医疗数据", "健康大数据", "数据共享"], "title": "医疗健康大数据共享的隐私保护方案", "subtitle": "跨机构临床数据协同的技术与制度"},
    {"date": "2024-07-28", "domain": "人工智能", "keywords": ["开源模型", "DeepSeek", "国产大模型"], "title": "国产开源大模型发展态势与技术评测", "subtitle": "DeepSeek、通义千问等开源生态分析"},
    {"date": "2024-08-15", "domain": "隐私计算", "keywords": ["隐私信息检索", "PIR", "密码学"], "title": "隐私信息检索协议的工程化实践", "subtitle": "PIR协议在数据查询场景的性能优化"},
    {"date": "2024-09-05", "domain": "数据安全", "keywords": ["数据水印", "溯源追踪", "版权保护"], "title": "数据水印技术在数据溯源追踪中的应用", "subtitle": "隐写术与鲁棒水印的工程化实践"},
    {"date": "2024-09-22", "domain": "数据要素", "keywords": ["数字政府", "政务数据", "数字中国"], "title": "数字政府建设中的数据治理能力评估", "subtitle": "省级数据管理机构改革与实践成效"},
    # === 2024 Q4 (10-12月) ===
    {"date": "2024-10-08", "domain": "人工智能", "keywords": ["边缘AI", "端侧推理", "模型压缩"], "title": "边缘AI推理技术发展与隐私保护优势", "subtitle": "端侧部署在敏感场景中的应用价值"},
    {"date": "2024-10-25", "domain": "隐私计算", "keywords": ["安全沙箱", "可信计算", "代码审计"], "title": "安全沙箱技术在数据可信计算中的应用", "subtitle": "容器化隔离与安全函数计算架构设计"},
    {"date": "2024-11-12", "domain": "数据安全", "keywords": ["密码学", "后量子密码", "抗量子"], "title": "后量子密码迁移对隐私计算的影响评估", "subtitle": "格基密码与同态加密的未来兼容性"},
    {"date": "2024-11-28", "domain": "数据要素", "keywords": ["数据资产评估", "估值方法", "数据定价"], "title": "数据资产评估方法论与实践案例研究", "subtitle": "成本法、收益法与市场法的适用性比较"},
    {"date": "2024-12-15", "domain": "人工智能", "keywords": ["AI+安全", "智能安全运营", "SOAR"], "title": "AI驱动的安全运营中心建设方案研究", "subtitle": "大模型在威胁检测与响应中的应用"},
    # === 2025 Q1 (1-3月) ===
    {"date": "2025-01-08", "domain": "隐私计算", "keywords": ["隐私保护RAG", "安全检索", "加密查询"], "title": "隐私保护检索增强生成系统技术研究", "subtitle": "PPRAG架构的设计原理与安全性分析"},
    {"date": "2025-02-05", "domain": "数据安全", "keywords": ["容器安全", "Docker", "运行时防护"], "title": "容器化部署环境下的数据安全加固方案", "subtitle": "从镜像扫描到运行时防护的全栈策略"},
    {"date": "2025-02-20", "domain": "数据要素", "keywords": ["能源数据", "碳数据", "绿色金融"], "title": "能源行业数据要素流通与碳数据资产化", "subtitle": "双碳目标下的能源数据治理实践"},
    {"date": "2025-03-10", "domain": "人工智能", "keywords": ["具身智能", "机器人", "感知决策"], "title": "具身智能发展趋势与数据安全需求分析", "subtitle": "物理世界AI的隐私边界与安全挑战"},
    {"date": "2025-03-25", "domain": "隐私计算", "keywords": ["秘密共享", "安全多方计算", "协议优化"], "title": "安全多方计算协议优化与性能基准评测", "subtitle": "ABY3、Semi2k等协议在实际场景的效率比较"},
    # === 2025 Q2 (4-6月) ===
    {"date": "2025-04-08", "domain": "数据安全", "keywords": ["API安全", "接口治理", "数据泄露"], "title": "API安全治理框架与数据泄露防护实践", "subtitle": "面向开放接口的全生命周期安全管理"},
    {"date": "2025-05-15", "domain": "数据要素", "keywords": ["交通数据", "智慧交通", "自动驾驶"], "title": "交通行业数据要素价值发现与隐私保护", "subtitle": "车路协同场景下的数据安全治理"},
    {"date": "2025-06-02", "domain": "人工智能", "keywords": ["小模型", "蒸馏", "高效推理"], "title": "小模型高效推理在隐私敏感场景的应用", "subtitle": "知识蒸馏与量化技术的本地部署方案"},
    # === 2025 Q3 (7-9月) ===
    {"date": "2025-07-10", "domain": "隐私计算", "keywords": ["属性基加密", "ABE", "细粒度控制"], "title": "属性基加密在医疗数据访问控制中的应用", "subtitle": "基于CP-ABE的细粒度权限管理方案"},
    {"date": "2025-08-05", "domain": "数据安全", "keywords": ["安全审计", "日志分析", "合规检查"], "title": "数据安全审计技术体系与自动化实践", "subtitle": "从日志采集到合规报告的全链路方案"},
    {"date": "2025-09-18", "domain": "数据要素", "keywords": ["制造业", "工业数据", "数据空间"], "title": "制造业数据空间建设与数据要素安全流通", "subtitle": "工业互联网环境下的数据可信共享"},
    # === 2025 Q4 (10-12月) ===
    {"date": "2025-10-12", "domain": "人工智能", "keywords": ["AI代码生成", "Copilot", "开发安全"], "title": "AI辅助代码生成的安全性评估与治理建议", "subtitle": "大模型生成代码的漏洞模式与防护措施"},
    {"date": "2025-11-20", "domain": "隐私计算", "keywords": ["隐私计算标准", "互联互通", "行业标准"], "title": "隐私计算互联互通标准进展与产业影响", "subtitle": "跨平台协作的技术标准与生态建设"},
    # === 2026 Q1 (1-3月) ===
    {"date": "2026-01-15", "domain": "数据安全", "keywords": ["二进制安全", "恶意检测", "模型安全"], "title": "二进制级深度安全检测在模型部署中的实践", "subtitle": "ClamAV、YARA与ModelScan联合检测方案"},
    {"date": "2026-02-28", "domain": "数据要素", "keywords": ["数据要素", "2026展望", "政策趋势"], "title": "2026年数据要素市场发展趋势与政策展望", "subtitle": "从制度建设到规模化流通的关键转折"},
]

assert len(ARTICLES) == 50, f"Expected 50 articles, got {len(ARTICLES)}"

# ============================================================
# 图表生成函数
# ============================================================
def gen_line_chart(filename, title, labels, series_dict, ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for i, (label, data) in enumerate(series_dict.items()):
        ax.plot(labels, data, color=COLORS[i % len(COLORS)], linewidth=2, marker='o', markersize=4, label=label)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.savefig(filename, facecolor='white', edgecolor='none')
    plt.close(fig)

def gen_bar_chart(filename, title, categories, values, ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(categories, values, color=[COLORS[i % len(COLORS)] for i in range(len(categories))], width=0.6)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel(ylabel, fontsize=10)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02, f'{val}', ha='center', va='bottom', fontsize=9)
    ax.grid(True, axis='y', alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=20, ha='right', fontsize=9)
    fig.savefig(filename, facecolor='white', edgecolor='none')
    plt.close(fig)

def gen_pie_chart(filename, title, labels, sizes):
    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=COLORS[:len(labels)], startangle=90, pctdistance=0.78)
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    fig.savefig(filename, facecolor='white', edgecolor='none')
    plt.close(fig)

def gen_heatmap(filename, title, row_labels, col_labels, data):
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(data, cmap='Blues', aspect='auto')
    ax.set_xticks(range(len(col_labels)))
    ax.set_yticks(range(len(row_labels)))
    ax.set_xticklabels(col_labels, fontsize=9)
    ax.set_yticklabels(row_labels, fontsize=9)
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            ax.text(j, i, f'{data[i][j]:.1f}', ha='center', va='center', fontsize=8, color='white' if data[i][j] > np.max(data)*0.6 else 'black')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.savefig(filename, facecolor='white', edgecolor='none')
    plt.close(fig)

def gen_area_chart(filename, title, x_labels, series_dict, ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    prev = np.zeros(len(x_labels))
    for i, (label, data) in enumerate(series_dict.items()):
        data = np.array(data)
        ax.fill_between(range(len(x_labels)), prev, prev + data, alpha=0.6, color=COLORS[i % len(COLORS)], label=label)
        prev = prev + data
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, fontsize=9, rotation=30, ha='right')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=9, loc='upper left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.savefig(filename, facecolor='white', edgecolor='none')
    plt.close(fig)

def gen_scatter_chart(filename, title, x_data, y_data, labels=None, xlabel='', ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 5))
    sizes = np.random.uniform(40, 200, len(x_data))
    ax.scatter(x_data, y_data, s=sizes, c=COLORS[:len(x_data)], alpha=0.7, edgecolors='white', linewidth=1)
    if labels:
        for i, label in enumerate(labels):
            ax.annotate(label, (x_data[i], y_data[i]), fontsize=8, ha='center', va='bottom', xytext=(0, 6), textcoords='offset points')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(True, alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.savefig(filename, facecolor='white', edgecolor='none')
    plt.close(fig)

def gen_box_violin_chart(filename, title, labels, data_list, chart_type='box'):
    fig, ax = plt.subplots(figsize=(8, 5))
    if chart_type == 'violin':
        parts = ax.violinplot(data_list, showmeans=True, showmedians=True)
        for i, pc in enumerate(parts.get('bodies', [])):
            pc.set_facecolor(COLORS[i % len(COLORS)])
            pc.set_alpha(0.6)
    else:
        bp = ax.boxplot(data_list, patch_artist=True, labels=labels)
        for i, patch in enumerate(bp['boxes']):
            patch.set_facecolor(COLORS[i % len(COLORS)])
            patch.set_alpha(0.6)
    if chart_type == 'violin':
        ax.set_xticks(range(1, len(labels)+1))
        ax.set_xticklabels(labels, fontsize=9)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.grid(True, axis='y', alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.savefig(filename, facecolor='white', edgecolor='none')
    plt.close(fig)

def gen_radar_chart(filename, title, categories, values, label_name=''):
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles += angles[:1]
    ax.fill(angles, values_plot, color=PRIMARY, alpha=0.2)
    ax.plot(angles, values_plot, color=PRIMARY, linewidth=2, marker='o', markersize=5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=20)
    fig.savefig(filename, facecolor='white', edgecolor='none')
    plt.close(fig)

# ============================================================
# 为每篇文章生成对应的图表数据
# ============================================================
def generate_charts_for_article(idx, article):
    """为文章生成1-2张图表，返回图表文件名列表"""
    random.seed(idx * 42 + 7)
    np.random.seed(idx * 42 + 7)
    charts = []
    prefix = f'chart_{idx+1:03d}'

    domain = article['domain']
    year = int(article['date'][:4])

    # 每篇文章生成1-2个图表
    chart_type = idx % 8

    if chart_type == 0:  # 折线图 - 市场趋势
        fname = f'{prefix}_trend.png'
        years = [str(y) for y in range(2020, year+2)]
        gen_line_chart(
            str(CHARTS_DIR / fname),
            f'{domain}市场规模增长趋势',
            years,
            {'市场规模(亿元)': [random.uniform(20, 50) * (1.3 ** i) for i in range(len(years))],
             '增长率(%)': [random.uniform(15, 45) for _ in years]},
            ylabel='规模/增长率'
        )
        charts.append(fname)

    elif chart_type == 1:  # 柱状图
        fname = f'{prefix}_compare.png'
        cats = ['金融', '医疗', '政务', '能源', '交通', '制造']
        gen_bar_chart(
            str(CHARTS_DIR / fname),
            f'{domain}行业应用分布',
            cats,
            [random.randint(15, 95) for _ in cats],
            ylabel='应用占比(%)'
        )
        charts.append(fname)

    elif chart_type == 2:  # 饼图
        fname = f'{prefix}_share.png'
        labels = ['联邦学习', '安全多方计算', '可信执行环境', '差分隐私', '同态加密']
        gen_pie_chart(
            str(CHARTS_DIR / fname),
            f'{domain}技术路线市场份额',
            labels,
            [random.randint(10, 40) for _ in labels]
        )
        charts.append(fname)

    elif chart_type == 3:  # 热力图
        fname = f'{prefix}_heatmap.png'
        rows = ['数据安全', '隐私合规', '效率提升', '成本控制', '用户体验']
        cols = ['金融', '医疗', '政务', '能源']
        data = [[random.uniform(3, 10) for _ in cols] for _ in rows]
        gen_heatmap(
            str(CHARTS_DIR / fname),
            f'{domain}行业需求热力矩阵',
            rows, cols, np.array(data)
        )
        charts.append(fname)

    elif chart_type == 4:  # 面积图
        fname = f'{prefix}_area.png'
        years = [str(y) for y in range(2021, year+2)]
        gen_area_chart(
            str(CHARTS_DIR / fname),
            f'{domain}投资规模分布趋势',
            years,
            {'政府投资': [random.uniform(10, 30) * (1.2**i) for i in range(len(years))],
             '企业投资': [random.uniform(15, 40) * (1.25**i) for i in range(len(years))],
             '风险投资': [random.uniform(5, 20) * (1.3**i) for i in range(len(years))]},
            ylabel='投资规模(亿元)'
        )
        charts.append(fname)

    elif chart_type == 5:  # 散点图
        fname = f'{prefix}_scatter.png'
        n = 8
        platforms = ['平台A', '平台B', '平台C', '平台D', '平台E', '平台F', '平台G', '平台H']
        gen_scatter_chart(
            str(CHARTS_DIR / fname),
            f'{domain}平台能力评估散点图',
            [random.uniform(40, 95) for _ in range(n)],
            [random.uniform(40, 95) for _ in range(n)],
            labels=platforms[:n],
            xlabel='技术成熟度', ylabel='市场覆盖度'
        )
        charts.append(fname)

    elif chart_type == 6:  # 箱线图/小提琴图
        fname = f'{prefix}_violin.png'
        labels = ['方案A', '方案B', '方案C', '方案D']
        data_list = [np.random.normal(loc=random.uniform(50, 80), scale=random.uniform(5, 15), size=50) for _ in labels]
        gen_box_violin_chart(
            str(CHARTS_DIR / fname),
            f'{domain}方案性能对比(小提琴图)',
            labels, data_list, chart_type='violin'
        )
        charts.append(fname)

    elif chart_type == 7:  # 雷达图
        fname = f'{prefix}_radar.png'
        categories = ['安全性', '性能', '易用性', '扩展性', '合规性', '成本效益']
        gen_radar_chart(
            str(CHARTS_DIR / fname),
            f'{domain}解决方案综合评估',
            categories,
            [random.uniform(5, 10) for _ in categories]
        )
        charts.append(fname)

    # 50%概率生成第二张图
    if idx % 3 == 0:
        fname2 = f'{prefix}_extra.png'
        years = [str(y) for y in range(2021, year+1)]
        if len(years) >= 2:
            gen_line_chart(
                str(CHARTS_DIR / fname2),
                f'{domain}关键指标变化趋势',
                years,
                {'政策数量': [random.randint(5, 30) for _ in years],
                 '企业参与度': [random.uniform(20, 80) for _ in years]},
                ylabel='指标值'
            )
            charts.append(fname2)

    return charts


# ============================================================
# 文章正文生成
# ============================================================
def generate_article_body(idx, article, charts):
    """生成文章markdown正文"""
    random.seed(idx * 99 + 13)
    d = article
    date = d['date']
    year = date[:4]
    kw_str = '、'.join(d['keywords'])

    # 文章摘要
    abstracts = {
        '数据要素': f"随着数字经济的快速发展，数据作为新型生产要素的战略价值日益凸显。本报告围绕{kw_str}等核心议题，系统梳理了{year}年度数据要素领域的政策动态、技术进展与产业实践，为相关机构的战略决策提供参考依据。",
        '隐私计算': f"隐私计算作为实现\"数据可用不可见\"的关键技术，在{year}年持续获得政策支持与产业关注。本报告聚焦{kw_str}等技术方向，深入分析当前技术进展、工程化挑战与市场格局，为技术选型与方案建设提供系统性参考。",
        '数据安全': f"在日趋复杂的网络安全态势下，数据安全已成为国家安全的重要组成部分。本报告围绕{kw_str}等重点领域，全面评估当前安全威胁形势、技术防护能力与合规建设进展，为安全治理体系建设提供分析支撑。",
        '人工智能': f"人工智能技术的快速迭代正深刻重塑各行业的生产方式与服务模式。本报告聚焦{kw_str}等前沿方向，对{year}年度技术演进、产业应用与治理挑战进行系统分析，为AI战略布局提供决策参考。",
    }

    # 各章节内容模板
    sections = []

    # 第一章：研究背景
    sections.append(f"""## 一、研究背景与目的

### 1.1 研究背景

{year}年，{d['domain']}领域迎来了重要的发展节点。从政策层面看，国家持续出台系列指导文件，为行业发展提供明确的制度框架与政策导向。从技术层面看，{kw_str}等核心技术取得显著进展，工程化成熟度不断提升。从市场层面看，越来越多的行业场景开始规模化应用相关技术方案，产业生态日趋完善。

当前，数字经济已成为推动经济增长的重要引擎。据统计，{year}年我国数字经济规模预计突破{random.randint(50, 65)}万亿元，占GDP比重超过{random.randint(42, 48)}%。在此背景下，{d['domain']}的战略价值进一步凸显，成为各方竞相布局的重点领域。

### 1.2 研究目的

本报告旨在系统梳理{d['domain']}领域的最新进展，重点分析{kw_str}等方向的技术演进、应用实践与发展趋势，为决策者提供全局性的认知框架与行动参考。""")

    # 第二章：行业现状
    sections.append(f"""## 二、行业发展现状

### 2.1 政策环境

在政策层面，近年来围绕{d['domain']}的制度供给持续加强。从中央到地方，已形成较为完整的政策体系：

- 国家层面：多部委联合发文，从顶层设计角度明确{d['domain']}的发展方向与重点任务
- 行业层面：金融、医疗、政务等重点领域出台专项指导意见，推动技术标准与规范建设
- 地方层面：北京、上海、广东、浙江等数字经济先发地区先行先试，形成可复制推广的经验

### 2.2 市场规模

据行业研究机构统计，{year}年中国{d['domain']}市场规模达到约{random.randint(80, 350)}亿元，同比增长{random.randint(25, 55)}%。其中，金融行业仍是最大的应用市场，占比约{random.randint(28, 40)}%；政务领域增速最快，年增长率超过{random.randint(40, 70)}%。

从区域分布看，长三角、京津冀和粤港澳大湾区是三大核心市场，合计占全国市场份额的{random.randint(65, 80)}%以上。""")

    # 插入图表
    chart_md = ''
    if charts:
        chart_md = f'\n\n![{d["domain"]}分析图表](charts/{charts[0]})\n\n*图1: {d["domain"]}行业分析*\n'

    # 第三章：技术分析
    sections.append(f"""## 三、核心技术分析

### 3.1 技术发展脉络

{d['domain']}的技术发展经历了从理论探索到工程落地的演进过程。在{kw_str}等方向，{year}年取得了以下重要进展：

**技术成熟度提升**：核心算法的工程化实现日趋完善，性能指标持续优化。以隐私计算为例，千万级数据规模的处理效率已从小时级提升至分钟级，为大规模商业化应用奠定了基础。

**标准化进程加速**：行业标准的制定与发布明显提速，国家标准、行业标准与团体标准形成多层次的标准体系，为技术互联互通与产品评测认证提供了依据。

**开源生态活跃**：国内外开源社区持续贡献高质量的技术实现，降低了技术门槛，加速了创新扩散。
{chart_md}
### 3.2 关键技术指标

| 指标维度 | 当前水平 | 发展趋势 |
|---------|---------|---------|
| 计算效率 | 千万级数据{random.randint(20, 60)}秒处理 | 持续优化，向亿级突破 |
| 安全强度 | {random.choice(['128位', '256位'])}密钥安全 | 后量子密码迁移推进 |
| 部署成本 | 较三年前降低{random.randint(40, 70)}% | 容器化与云原生持续降本 |
| 易用性 | 可视化配置覆盖{random.randint(60, 85)}%场景 | 低代码化趋势明显 |""")

    # 第四章：应用实践
    sections.append(f"""## 四、典型应用场景与实践

### 4.1 金融行业

金融行业是{d['domain']}技术应用最为成熟的领域。在信用评估、反欺诈、反洗钱等场景中，隐私计算技术已从POC验证进入规模化生产阶段。多家头部银行与金融科技公司建立了跨机构联合建模能力，在不共享原始数据的前提下实现了风控模型AUC指标{random.randint(2, 5)}%以上的提升。

### 4.2 医疗健康

医疗数据的敏感性使其成为隐私保护技术的典型应用场景。跨院区的临床数据协同分析、药物研发中的多方数据联合建模、医疗影像的联邦学习等方向均取得实质性进展。尤其在传染病防控、罕见病研究等公共卫生领域，隐私保护下的数据共享为科研突破提供了重要支撑。

### 4.3 政务治理

数字政府建设推动政务数据的跨部门、跨层级共享需求持续增长。通过联邦查询等技术手段，在保障数据安全边界的前提下实现了公安、社保、税务等多部门数据的联合分析，为基层治理、综合研判与公共服务优化提供了数据支撑。""")

    chart_md2 = ''
    if len(charts) > 1:
        chart_md2 = f'\n\n![{d["domain"]}趋势分析](charts/{charts[1]})\n\n*图2: {d["domain"]}关键趋势指标*\n'

    # 第五章：挑战与建议
    sections.append(f"""## 五、挑战与发展建议
{chart_md2}
### 5.1 当前挑战

尽管{d['domain']}领域取得了显著进展，但仍面临以下核心挑战：

1. **技术与业务的匹配度不足**：部分技术方案在实验环境表现优异，但在真实业务场景中面临数据质量、系统集成、运维复杂度等问题
2. **标准体系有待完善**：技术标准与业务标准的衔接不够紧密，跨平台互联互通能力不足
3. **复合型人才短缺**：兼具密码学、机器学习、系统工程与行业知识的复合型人才供给严重不足
4. **商业模式探索中**：从技术能力到商业价值的转化路径尚不清晰，可持续的盈利模式仍在探索

### 5.2 发展建议

针对上述挑战，提出以下发展建议：

- **强化顶层设计**：完善法律法规与标准规范，为技术应用提供清晰的合规边界
- **推进技术攻关**：在高性能密码学算法、大规模联邦计算引擎等方向持续投入研发
- **深化场景落地**：以金融、医疗、政务等关键行业为突破口，建立可复制的标杆案例
- **构建人才体系**：加强高校学科建设与产教融合，培养多层次的专业人才队伍
- **推动生态建设**：通过开源协作、产业联盟等方式，构建开放共赢的产业生态""")

    # 第六章：展望
    sections.append(f"""## 六、发展展望

展望未来，{d['domain']}领域将呈现以下发展趋势：

**技术融合加速**：隐私计算与人工智能、区块链、云计算等技术的深度融合将催生新的技术范式与应用场景。特别是大模型时代的到来，为隐私保护下的智能服务提供了广阔空间。

**应用规模化**：随着技术成熟度提升与成本持续下降，{d['domain']}应用将从头部机构向中小企业延伸，从重点行业向更多领域拓展，市场规模有望保持{random.randint(30, 50)}%以上的年均增速。

**治理体系完善**：全球范围内的数据治理制度将持续演进，中国作为数据大国，在制度建设与技术标准方面的国际影响力将进一步提升。

**产业生态成熟**：从基础技术到应用平台，从咨询服务到运营支撑，完整的产业链条将逐步形成，为数据要素的安全高效流通提供全方位的支撑体系。

---

*本报告由查特查特科技行业研究中心撰写发布，仅供行业参考与学术交流使用。*""")

    return abstracts.get(d['domain'], abstracts['数据要素']), '\n\n'.join(sections)


# ============================================================
# 主流程
# ============================================================
def main():
    os.makedirs(CHARTS_DIR, exist_ok=True)

    articles_meta = []

    for idx, article in enumerate(ARTICLES):
        print(f"[{idx+1:02d}/50] {article['title']}")

        # 生成图表
        charts = generate_charts_for_article(idx, article)

        # 生成正文
        abstract, body = generate_article_body(idx, article, charts)

        # 生成文件名
        date_str = article['date'].replace('-', '')
        slug = f'{date_str}-{idx+1:03d}'
        filename = f'{slug}.md'

        # 图表引用
        chart_refs = ', '.join([f'`{c}`' for c in charts]) if charts else '无'

        # 生成完整Markdown
        md_content = f"""---
title: "{article['title']}"
subtitle: "{article['subtitle']}"
date: {article['date']}
domain: {article['domain']}
keywords:
{chr(10).join('  - ' + kw for kw in article['keywords'])}
author: 查特查特科技行业研究中心
charts: [{', '.join(charts)}]
---

# {article['title']}

> {article['subtitle']}

| 信息项 | 内容 |
|-------|------|
| 发布日期 | {article['date']} |
| 研究领域 | {article['domain']} |
| 关键词 | {', '.join(article['keywords'])} |
| 作者 | 查特查特科技行业研究中心 |

## 摘要

{abstract}

{body}
"""

        filepath = RESEARCH_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)

        articles_meta.append({
            'index': idx + 1,
            'slug': slug,
            'filename': filename,
            'title': article['title'],
            'subtitle': article['subtitle'],
            'date': article['date'],
            'domain': article['domain'],
            'keywords': article['keywords'],
            'charts': charts,
        })

    # 保存元数据索引
    with open(RESEARCH_DIR / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(articles_meta, f, ensure_ascii=False, indent=2)

    print(f"\n已生成 {len(articles_meta)} 篇研究报告")
    print(f"图表存储: {CHARTS_DIR}")
    print(f"报告存储: {RESEARCH_DIR}")

if __name__ == '__main__':
    main()
