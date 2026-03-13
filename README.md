Big Data Based Social Media Sentiment Analysis System



Project Overview

A full-stack sentiment analysis system for social media text (with Weibo as the primary data source) based on big data technologies. It covers the complete workflow: data crawling → text preprocessing → LSTM model training → hyperparameter comparison → web visualization. The system achieves high-precision sentiment polarity classification (positive/negative) and provides an interactive web interface for data display and text sentiment prediction.

Core Features

- 🕷️ Data Crawling & Storage: Crawl Weibo hot search and comment data, support CSV/SQLite storage, batch data acquisition and data cleaning

- 🧹 Text Preprocessing: Implement Chinese word segmentation (Jieba), stop word removal, and Word2Vec word vector training/conversion

- 🤖 LSTM Model Training: Build sentiment classification model with support for loss function/learning rate/batch size comparison, integrated early stopping mechanism to prevent overfitting

- 📊 Performance Visualization: Automatically generate training loss/accuracy curves, hyperparameter comparison charts, and export Top-100 prediction results

- 🌐 Web Visualization: Complete web interface based on Flask, including data dashboard, sentiment analysis, text prediction, data tables and other modules

Technology Stack

Category

Technologies

Programming Language

Python 3.10+

Deep Learning Framework

PyTorch

NLP Tools

Jieba (Word Segmentation), Gensim (Word2Vec)

Web Framework

Flask

Database

SQLite

Visualization

Matplotlib (Backend), ECharts (Frontend), WordCloud

Version Control

Git + Git LFS (Large File Storage)

Data Processing

Pandas, NumPy, scikit-learn

Web Crawling

Requests

Project Structure

PYTHONPROJECT/
├── dao/                  # Data Access Layer (Database interaction encapsulation)
│   ├── __init__.py
│   ├── dapingciyun.py    # Dashboard word cloud API
│   ├── getCommentsData.py # Comment data API
│   ├── getDaPing.py      # Dashboard visualization data API
│   ├── getEmotionData.py # Sentiment analysis data API
│   ├── getPageData.py    # Pagination data API
│   ├── getPublicData.py  # Public data API
│   ├── getTableData.py   # Table data API
│   └── word_cloud.py     # Word cloud generation API
├── file/                 # Public data storage directory
│   ├── weiborebang.csv   # Raw Weibo hot search data
│   └── weiborebangdata.csv # Cleaned Weibo data
├── predictive/           # Core prediction and model module
│   ├── __init__.py
│   ├── LSTM.py           # LSTM model training (with early stopping/hyperparameter comparison)
│   ├── machine.py        # Traditional machine learning model comparison
│   ├── yuce.py           # Model prediction and result export
│   ├── getHistoryData.py # Historical data acquisition script
│   ├── cuda_test.py      # CUDA environment test
│   ├── hit_stopwords.txt # HIT Chinese stop word list
│   ├── dict.txt.pkl      # Dictionary cache file
│   ├── f.model*          # Pre-trained Word2Vec model files
│   ├── pos.txt/neg.txt   # Labeled positive/negative sample data
│   └── bingmayong1_with_sentiment.csv # Social media text dataset with sentiment labels
├── spider/               # Data crawling module
│   ├── spider.py         # Main Weibo hot search/comment crawling script
│   ├── weiboData.py      # Weibo data structuring and cleaning
│   ├── weibo.sql         # SQLite table structure SQL
│   └── file/             # Crawled data storage directory
├── static/               # Web frontend static resources
│   ├── css/              # Style files (Bootstrap)
│   ├── js/               # Frontend interactive scripts (ECharts)
│   ├── font/             # Font resources
│   ├── image/            # Image resources
│   └── picture/          # Project images
├── templates/            # Flask frontend templates
│   ├── index.html        # System homepage
│   ├── daping.html       # Data dashboard page
│   ├── emotion.html      # Sentiment analysis result page
│   ├── search.html       # Text sentiment prediction entry page
│   ├── yuce.html         # Prediction result page
│   ├── tableData.html    # Data table display page
│   ├── comments.html     # Comment details page
│   ├── recommend.html    # Recommendation result page
│   ├── pages-login.html  # User login page
│   └── pages-register.html # User registration page
├── app.py                # Flask web service entry point
├── db.py                 # SQLite database connection configuration
├── .gitattributes        # Git LFS large file configuration
└── README.md             # Project documentation

Quick Start

1. Environment Setup

# Core dependencies
pip install torch>=2.0.0 pandas>=2.0.0 numpy>=1.24.0 jieba>=0.42.1 gensim>=4.3.0

# Visualization and Web dependencies
pip install matplotlib>=3.7.0 flask>=2.3.0 wordcloud>=1.9.0

# Data processing and crawling dependencies
pip install scikit-learn>=1.2.0 requests>=2.31.0

2. Data Preparation

# 1. Crawl Weibo data
python spider/spider.py

# 2. Preprocess text data (segmentation/stopword removal/word vector conversion)
python predictive/data_preprocess.py

3. Model Training

# Train LSTM model (with hyperparameter comparison and early stopping)
python predictive/LSTM.py

4. Start Web Service

python app.py

Accesshttp://127.0.0.1:5000 to enter the system interface.

Model Performance

Configuration

Test Accuracy

Base Model (CrossEntropyLoss, lr=0.001, batch=64)

96.37%

MSELoss Model (same hyperparameters)

96.39%

Optimal Learning Rate (0.001)

96.31%

Optimal Batch Size (16)

96.54%

Output File Description

The following files are automatically generated after model training:

- performance_*.png: Model performance visualization charts (loss curves/accuracy curves/hyperparameter comparison)

- predictions_*.csv: Model prediction results (Top-100 samples)

Notes

- 📦 Large File Management: The project contains large files (>50MB, e.g., dict.txt.pkl, f.model*.npy). Git LFS is configured to manage these files to avoid GitHub file size limits

- ⚡ CUDA Acceleration: The model supports GPU acceleration. Run cuda_test.py to verify CUDA availability; CPU training is compatible but runs slower

- 📁 Result Files: Performance charts (PNG) and prediction results (CSV) are automatically generated after model training, which can be directly used for papers/reports

- 🔒 Data Privacy: Crawled social media data is for research purposes only; comply with relevant data privacy regulations

Contact

- Author: JunhaoJian

- Email: junhao.jian@outlook.com

- GitHub: https://github.com/JunhaoJian/Big-Data-Based-Social-Media-Sentiment-Analysis-System

License

This project is licensed under the MIT License - see the LICENSE file for details.
