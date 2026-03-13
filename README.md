# Big-Data-Based-Social-Media-Sentiment-Analysis-System

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/PyTorch-2.0%2B-orange.svg)](https://pytorch.org/)
[![Web Framework](https://img.shields.io/badge/Flask-2.3%2B-lightgrey.svg)](https://flask.palletsprojects.com/)

## 项目概述
基于大数据技术的社交媒体文本情感分析系统（以微博为核心数据源），覆盖**数据爬取 → 文本预处理 → LSTM模型训练 → 超参数对比 → Web可视化** 全流程，实现高精度情感极性分类（正向/负向），并提供交互式Web界面用于数据展示与文本预测。

## 核心功能
- 🕷️ **数据爬取与存储**：爬取微博热搜/评论数据，支持CSV/SQLite存储、批量获取与数据清洗
- 🧹 **文本预处理**：实现中文分词（Jieba）、停用词过滤、Word2Vec词向量训练/转换
- 🤖 **LSTM模型训练**：构建情感分类模型，支持损失函数/学习率/批量大小对比，集成早停机制防止过拟合
- 📊 **性能可视化**：自动生成训练损失/准确率曲线、超参数对比图表，导出Top-100预测结果
- 🌐 **Web可视化**：基于Flask实现完整Web界面，包含数据看板、情感分析、文本预测、数据表格等模块

## 技术栈
| 分类 | 技术选型 |
|------|---------|
| 编程语言 | Python 3.10+ |
| 深度学习框架 | PyTorch |
| NLP工具 | Jieba（分词）、Gensim（Word2Vec） |
| Web框架 | Flask |
| 数据库 | SQLite |
| 可视化 | Matplotlib、ECharts、WordCloud |
| 版本控制 | Git + Git LFS（大文件管理） |
| 数据处理 | Pandas、NumPy、scikit-learn |
| 爬虫 | Requests |

## 项目结构
```
PYTHONPROJECT/
├── dao/                  # 数据访问层（数据库交互封装）
│   ├── __init__.py
│   ├── dapingciyun.py    # 看板词云API
│   ├── getCommentsData.py # 评论数据API
│   ├── getDaPing.py      # 看板可视化数据API
│   ├── getEmotionData.py # 情感分析数据API
│   ├── getPageData.py    # 分页数据API
│   ├── getPublicData.py  # 公共数据API
│   ├── getTableData.py   # 表格数据API
│   └── word_cloud.py     # 词云生成API
├── file/                 # 公共数据存储目录
│   ├── weiborebang.csv   # 原始微博热搜数据
│   └── weiborebangdata.csv # 清洗后微博数据
├── predictive/           # 核心预测与模型模块
│   ├── __init__.py
│   ├── LSTM.py           # LSTM模型训练（含早停/超参数对比）
│   ├── machine.py        # 传统机器学习模型对比
│   ├── yuce.py           # 模型预测与结果导出
│   ├── getHistoryData.py # 历史数据获取脚本
│   ├── cuda_test.py      # CUDA环境测试
│   ├── hit_stopwords.txt # 哈工大停用词表
│   ├── dict.txt.pkl      # 字典缓存文件
│   ├── f.model*          # Word2Vec预训练模型文件
│   ├── pos.txt/neg.txt   # 标注好的正负样本数据
│   └── bingmayong1_with_sentiment.csv # 带情感标注的数据集
├── spider/               # 数据爬取模块
│   ├── spider.py         # 微博热搜/评论爬取主脚本
│   ├── weiboData.py      # 微博数据结构化与清洗
│   ├── weibo.sql         # SQLite表结构SQL
│   └── file/             # 爬取数据存储目录
├── static/               # Web前端静态资源
│   ├── css/              # 样式文件（Bootstrap）
│   ├── js/               # 前端交互脚本（ECharts）
│   ├── font/             # 字体资源
│   ├── image/            # 图片资源
│   └── picture/          # 项目图片
├── templates/            # Flask前端模板
│   ├── index.html        # 系统首页
│   ├── daping.html       # 数据看板页面
│   ├── emotion.html      # 情感分析结果页
│   ├── search.html       # 文本预测入口页
│   ├── yuce.html         # 预测结果页
│   ├── tableData.html    # 数据表格页
│   ├── comments.html     # 评论详情页
│   ├── recommend.html    # 推荐结果页
│   ├── pages-login.html  # 登录页
│   └── pages-register.html # 注册页
├── app.py                # Flask Web服务入口
├── db.py                 # SQLite数据库连接配置
├── .gitattributes        # Git LFS大文件配置
└── README.md             # 项目文档
```

## 快速开始

### 1. 环境配置
```bash
# 核心依赖
pip install torch>=2.0.0 pandas>=2.0.0 numpy>=1.24.0 jieba>=0.42.1 gensim>=4.3.0

# 可视化与Web依赖
pip install matplotlib>=3.7.0 flask>=2.3.0 wordcloud>=1.9.0

# 数据处理与爬虫依赖
pip install scikit-learn>=1.2.0 requests>=2.31.0
```

### 2. 数据准备
```bash
# 1. 爬取微博数据
python spider/spider.py

# 2. 文本预处理（分词/停用词过滤/词向量转换）
python predictive/data_preprocess.py
```

### 3. 模型训练
```bash
# 训练LSTM模型（含超参数对比+早停机制）
python predictive/LSTM.py
```

### 4. 启动Web服务
```bash
python app.py
```
访问 `http://127.0.0.1:5000` 进入系统界面

## 模型性能
| 配置项 | 测试准确率 |
|--------|------------|
| 基础模型（CrossEntropyLoss, lr=0.001, batch=64） | 96.37% |
| MSELoss模型（相同超参数） | 96.39% |
| 最优学习率（0.001） | 96.31% |
| 最优批量大小（16） | 96.54% |

## 输出文件说明
训练完成后自动生成以下文件：
- `performance_*.png`：模型性能可视化图表（损失曲线/准确率曲线/超参数对比）
- `predictions_*.csv`：模型预测结果数据（Top-100样本）

## 注意事项
1. 📦 **大文件管理**：项目包含大文件（>50MB，如`dict.txt.pkl`、`f.model*.npy`），已配置Git LFS管理，避免GitHub文件大小限制
2. ⚡ **CUDA加速**：模型支持GPU加速，运行`cuda_test.py`验证CUDA可用性；CPU训练兼容但速度较慢
3. 📁 **结果文件**：模型训练后自动生成性能图表（PNG）和预测结果（CSV），可直接用于论文/报告展示
4. 🔒 **数据隐私**：爬取的社交媒体数据仅用于研究，需遵守相关数据隐私法规

## 联系方式
- 作者：JunhaoJian
- 邮箱：junhao.jian@outlook.com
- GitHub：https://github.com/JunhaoJian/Big-Data-Based-Social-Media-Sentiment-Analysis-System

## 许可证
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 更新日志
1. 优化项目结构，移除冗余文件（__pycache__/.idea等），精简目录层级
2. 补充dao层和file目录说明，匹配当前项目结构
3. 明确输出文件用途，适配Python 3.10环境
4. 标准化README格式，增加徽章、emoji标识提升可读性
