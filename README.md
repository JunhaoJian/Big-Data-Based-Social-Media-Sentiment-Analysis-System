# Big-Data-Based-Social-Media-Sentiment-Analysis-System

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/PyTorch-2.0%2B-orange.svg)](https://pytorch.org/)
[![Web Framework](https://img.shields.io/badge/Flask-2.3%2B-lightgrey.svg)](https://flask.palletsprojects.com/)

### Project Overview
A social media text sentiment analysis system based on big data technology (with Weibo as the core data source), covering the full workflow of **data crawling → text preprocessing → LSTM model training → hyperparameter comparison → Web visualization**. It achieves high-precision sentiment polarity classification (positive/negative) and provides an interactive Web interface for data display and text prediction.

### Core Features
- 🕷️ **Data Crawling & Storage**: Crawls Weibo hot search/comment data, supporting CSV/SQLite storage, batch acquisition, and data cleaning
- 🧹 **Text Preprocessing**: Implements Chinese word segmentation (Jieba), stop word filtering, and Word2Vec word vector training/conversion
- 🤖 **LSTM Model Training**: Builds sentiment classification models, supports comparison of loss functions/learning rates/batch sizes, and integrates an early stopping mechanism to prevent overfitting
- 📊 **Performance Visualization**: Automatically generates training loss/accuracy curves, hyperparameter comparison charts, and exports Top-100 prediction results
- 🌐 **Web Visualization**: Implements a complete Web interface based on Flask, including modules for data dashboard, sentiment analysis, text prediction, and data tables

### Technology Stack
| Category          | Technology Selection                          |
|-------------------|-----------------------------------------------|
| Programming Language | Python 3.10+                                   |
| Deep Learning Framework | PyTorch                                      |
| NLP Tools         | Jieba (Word Segmentation), Gensim (Word2Vec)  |
| Web Framework     | Flask                                         |
| Database          | SQLite                                        |
| Visualization     | Matplotlib, ECharts, WordCloud                |
| Version Control   | Git + Git LFS (Large File Storage)            |
| Data Processing   | Pandas, NumPy, scikit-learn                   |
| Web Crawler       | Requests                                      |

### Summary
1. The translation adheres to **universally accepted terminology in the technical field** (e.g., Early Stopping, Word Segmentation, Hyperparameter) to ensure readability for industry professionals;
2. Chinese-specific tool names (e.g., Jieba) are retained with supplementary English explanations to balance recognizability and comprehensibility;
3. Functional descriptions adopt a **concise verb-phrase structure** (e.g., Crawls, Implements, Builds) that aligns with the expressive conventions of technical documentation, while retaining the original emoji symbols to enhance readability.

## Project Structure
```
PYTHONPROJECT/
├── dao/                  # Data Access Layer (database interaction encapsulation)
│   ├── __init__.py
│   ├── dapingciyun.py    # Dashboard Word Cloud API
│   ├── getCommentsData.py # Comment Data API
│   ├── getDaPing.py      # Dashboard Visualization Data API
│   ├── getEmotionData.py # Sentiment Analysis Data API
│   ├── getPageData.py    # Pagination Data API
│   ├── getPublicData.py  # Public Data API
│   ├── getTableData.py   # Table Data API
│   └── word_cloud.py     # Word Cloud Generation API
├── file/                 # Public Data Storage Directory
│   ├── weiborebang.csv   # Raw Weibo Hot Search Data
│   └── weiborebangdata.csv # Cleaned Weibo Hot Search Data
├── predictive/           # Core Prediction & Model Module
│   ├── __init__.py
│   ├── LSTM.py           # LSTM Model Training (incl. early stopping/hyperparameter comparison)
│   ├── machine.py        # Traditional Machine Learning Model Comparison
│   ├── yuce.py           # Model Prediction & Result Export
│   ├── getHistoryData.py # Historical Data Retrieval Script
│   ├── cuda_test.py      # CUDA Environment Test
│   ├── hit_stopwords.txt # HIT (Harbin Institute of Technology) Stop Words List
│   ├── dict.txt.pkl      # Dictionary Cache File
│   ├── f.model*          # Word2Vec Pre-trained Model File
│   ├── pos.txt/neg.txt   # Annotated Positive/Negative Sample Data
│   └── bingmayong1_with_sentiment.csv # Dataset with Sentiment Annotations
├── spider/               # Data Crawling Module
│   ├── spider.py         # Main Script for Weibo Hot Search/Comment Crawling
│   ├── weiboData.py      # Weibo Data Structuring & Cleaning
│   ├── weibo.sql         # SQLite Table Structure SQL
│   └── file/             # Crawled Data Storage Directory
├── static/               # Web Frontend Static Resources
│   ├── css/              # Style Files (Bootstrap)
│   ├── js/               # Frontend Interaction Scripts (ECharts)
│   ├── font/             # Font Resources
│   ├── image/            # Image Resources
│   └── picture/          # Project Images
├── templates/            # Flask Frontend Templates
│   ├── index.html        # System Homepage
│   ├── daping.html       # Data Dashboard Page
│   ├── emotion.html      # Sentiment Analysis Results Page
│   ├── search.html       # Text Prediction Entry Page
│   ├── yuce.html         # Prediction Results Page
│   ├── tableData.html    # Data Table Page
│   ├── comments.html     # Comment Details Page
│   ├── recommend.html    # Recommendation Results Page
│   ├── pages-login.html  # Login Page
│   └── pages-register.html # Registration Page
├── app.py                # Flask Web Service Entry Point
├── db.py                 # SQLite Database Connection Configuration
├── .gitattributes        # Git LFS Large File Configuration
└── README.md             # Project Documentation
```

### Recommended Technical Documentation Translation Tools
Here are professional tools tailored for technical documentation translation (with a focus on code/engineering terminology accuracy):

| Tool Type       | Recommended Tools                          | Key Advantages                                                                 |
|-----------------|--------------------------------------------|--------------------------------------------------------------------------------|
| AI-Powered Translators | DeepL Pro / ChatGPT-4o / Claude 3          | - DeepL: Superior technical term accuracy, preserves code formatting<br>- GPT-4o/Claude 3: Understands context of code snippets/technical workflows |
| Specialized CAT Tools | SDL Trados Studio / MemoQ                  | - Manages translation memories for consistent terminology<br>- Supports batch translation of technical docs (Markdown/HTML) |
| Open-Source Tools | OmegaT / translate-shell                   | - Free for personal use<br>- Integrates with version control (Git) for codebase translation |
| Code-Friendly Tools | Localize / Crowdin                         | - Preserves code syntax while translating comments/docs<br>- Supports Markdown/JSON/YAML formats |

---

### Quick Start

#### 1. Environment Setup
```bash
# Core Dependencies
pip install torch>=2.0.0 pandas>=2.0.0 numpy>=1.24.0 jieba>=0.42.1 gensim>=4.3.0

# Visualization & Web Dependencies
pip install matplotlib>=3.7.0 flask>=2.3.0 wordcloud>=1.9.0

# Data Processing & Crawler Dependencies
pip install scikit-learn>=1.2.0 requests>=2.31.0
```

#### 2. Data Preparation
```bash
# 1. Crawl Weibo Data
python spider/spider.py

# 2. Text Preprocessing (Word Segmentation/Stop Word Filtering/Word Vector Conversion)
python predictive/data_preprocess.py
```

#### 3. Model Training
```bash
# Train LSTM Model (including hyperparameter comparison + early stopping mechanism)
python predictive/LSTM.py
```

#### 4. Start Web Service
```bash
python app.py
```
Access `http://127.0.0.1:5000` to enter the system interface

### Model Performance
| Configuration Item                              | Test Accuracy |
|-------------------------------------------------|---------------|
| Basic Model (CrossEntropyLoss, lr=0.001, batch=64) | 96.37%        |
| MSELoss Model (same hyperparameters)            | 96.39%        |
| Optimal Learning Rate (0.001)                   | 96.31%        |
| Optimal Batch Size (16)                         | 96.54%        |

### Output File Description
The following files are automatically generated after training:
- `performance_*.png`: Model performance visualization charts (loss curves/accuracy curves/hyperparameter comparisons)
- `predictions_*.csv`: Model prediction results (Top-100 samples)

### Notes
1. 📦 **Large File Management**: The project contains large files (>50MB, e.g., `dict.txt.pkl`, `f.model*.npy`), managed with Git LFS to avoid GitHub file size limits
2. ⚡ **CUDA Acceleration**: The model supports GPU acceleration; run `cuda_test.py` to verify CUDA availability; CPU training is compatible but slower
3. 📁 **Result Files**: Performance charts (PNG) and prediction results (CSV) are auto-generated post-training, ready for use in papers/reports
4. 🔒 **Data Privacy**: Crawled social media data is for research only and must comply with relevant data privacy regulations

### Contact Information
- Author: JunhaoJian
- Email: junhao.jian@outlook.com
- GitHub: https://github.com/JunhaoJian/Big-Data-Based-Social-Media-Sentiment-Analysis-System

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
