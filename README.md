# 新闻联播自动推送系统

每日新闻联播自动推送功能，发送至微信

## 📋 工程概述

**项目名称**: 新闻联播自动推送系统  
**项目描述**: 这是一个自动化的新闻联播内容抓取、分析和推送系统，能够每日自动获取新闻联播内容，进行关键词分析，并通过微信推送给用户。

## 🏗️ 系统架构

### 核心模块架构

```
新闻联播自动推送系统
├── 数据采集层 (xwlb.py)
├── 内容处理层 (contextBrief.py, contextAnalyze.py)
├── 数据存储层 (jsonFile.py)
├── 消息推送层 (wxPusher.py)
└── 调度控制层 (main.py)
```

### 模块功能说明

#### 1. **数据采集模块** (`xwlb.py`)
- **功能**: 从央视官网抓取新闻联播视频链接和内容摘要
- **核心方法**:
  - `get_xwlb_url_byDate()`: 根据日期获取新闻联播视频URL
  - `get_xwlb_contextBrief()`: 提取新闻联播内容摘要

#### 2. **内容处理模块** (`contextBrief.py`)
- **功能**: 解析和结构化新闻联播文本内容
- **核心方法**:
  - `parse_structured_text()`: 将文本内容解析为结构化数据
  - `printStructuredData()`: 格式化输出结构化数据

#### 3. **关键词分析模块** (`contextAnalyze.py`)
- **功能**: 使用NLP技术分析文本，提取人名、地名和关键词
- **核心方法**:
  - `extract_keywords_from_text()`: 使用spacy提取关键词
  - `analyze_json_file()`: 分析JSON文件中的关键词
  - `plot_wordcloud()`: 生成词云图可视化

#### 4. **数据存储模块** (`jsonFile.py`)
- **功能**: 管理新闻数据的JSON格式存储
- **核心方法**:
  - `save_to_json()`: 保存结构化数据到JSON文件
  - `load_from_json()`: 从JSON文件加载数据

#### 5. **消息推送模块** (`wxPusher.py`)
- **功能**: 通过微信公众号API发布文章和图片
- **核心方法**:
  - `send_wechat_article()`: 发布文章到微信公众号
  - `send_wechat_image()`: 发布图片文章到微信公众号
  - `upload_image_to_wechat()`: 上传图片到公众号素材库
  - `WeChatOfficialAccount`类: 封装微信公众号API操作

#### 6. **主控调度模块** (`main.py`)
- **功能**: 协调各个模块，实现自动化流程
- **核心功能**:
  - 多线程并行处理多日期的新闻数据
  - 月初自动生成月度关键词分析报告
  - 定时任务调度

## 🛠️ 技术框架

### 核心依赖库

| 类别 | 技术栈 | 用途 |
|------|--------|------|
| **网络请求** | `requests` | HTTP请求和数据抓取 |
| **HTML解析** | `beautifulsoup4` | 网页内容解析 |
| **字符编码** | `chardet` | 自动检测字符编码 |
| **NLP处理** | `spacy`, `jieba`, `textrank4zh` | 中文文本分析和关键词提取 |
| **数据可视化** | `matplotlib`, `WordCloud` | 词云图生成和可视化 |
| **消息推送** | 微信公众号API | 微信公众平台官方API |
| **并发处理** | `concurrent.futures` | 多线程并行处理 |

### 开发工具和配置

- **版本控制**: Git + GitHub
- **CI/CD**: GitHub Actions (自动部署和定时任务)
- **日志系统**: Python logging模块
- **配置文件**: JSON格式数据存储

## 🔄 工作流程

1. **数据采集**: 每日自动抓取新闻联播内容
2. **内容解析**: 结构化处理新闻文本
3. **关键词分析**: 提取人名、地名和关键词
4. **数据存储**: 保存到本地JSON文件
5. **消息推送**: 通过微信推送每日新闻摘要
6. **月度报告**: 每月初生成关键词分析报告和词云图

## 📊 数据流

```
央视官网 → 内容抓取 → 文本解析 → 关键词提取 → JSON存储 → 微信推送
                                      ↓
                                 月度词云分析
```

## 🚀 特色功能

1. **自动化运行**: 通过GitHub Actions实现每日自动执行
2. **多线程处理**: 支持并行处理多日期数据
3. **智能分析**: 基于spacy的NLP关键词提取
4. **可视化报告**: 自动生成词云图月度报告
5. **微信集成**: 无缝对接微信推送服务

## 📁 项目结构

```
新闻联播自动推送系统/
├── .github/
│   └── workflows/
│       └── python-app.yml          # GitHub Actions 自动化配置
├── NotoSansSC-VariableFont_wght.ttf # 中文字体文件
├── README.md                       # 项目说明文档
├── contextAnalyze.py               # 关键词分析模块
├── contextBrief.py                # 内容解析模块
├── jsonFile.py                     # 数据存储模块
├── main.py                         # 主控调度模块
├── news_data.json                  # 新闻数据存储文件
├── requirements.txt               # Python依赖包列表
├── wxPusher.py                     # 微信推送模块
└── xwlb.py                         # 数据采集模块
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置参数

1. **编辑配置文件** (`config.py`):
   ```python
   WECHAT_APP_ID = "您的微信公众号AppID"
   WECHAT_APP_SECRET = "您的微信公众号AppSecret"
   ```

2. **或使用环境变量**:
   ```bash
   # Windows
   $env:WECHAT_APP_ID="您的AppID"
   $env:WECHAT_APP_SECRET="您的AppSecret"
   
   # Linux/Mac
   export WECHAT_APP_ID="您的AppID"
   export WECHAT_APP_SECRET="您的AppSecret"
   ```

### 运行系统

```bash
python main.py
```

### 验证配置

```bash
python config.py
```

### 自动化部署

系统已配置GitHub Actions，每日自动运行并更新数据。

## 🔄 功能变更说明

**重要更新**: 系统已从第三方WxPusher服务迁移到微信公众号官方API：

- ✅ **新增**: 微信公众号文章发布功能
- ✅ **新增**: 公众号素材库图片上传
- ✅ **保留**: 原有的新闻联播内容获取和分析功能
- ❌ **移除**: WxPusher第三方依赖

详细配置说明请参考：[微信公众号配置说明.md](./微信公众号配置说明.md)

## 📈 数据文件说明

- `news_data.json`: 存储每日新闻联播的结构化内容
- `key_name.json`: 存储提取的关键人名数据
- `key_place.json`: 存储提取的关键地名数据
- `key_words.json`: 存储提取的关键词数据

这个工程是一个完整的自动化新闻处理系统，具有良好的模块化设计和可扩展性，能够稳定运行并提供有价值的新闻分析服务。
