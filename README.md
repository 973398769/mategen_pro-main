# MateGen: Interactive Intelligent Programming Assistant

![MateGen Banner](https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/136439902d507ef41f9f746bddd47fc.jpg)

<p align="center">
  <a href="README_zh.md"><strong>中文</strong></a> | 
  <a href="docs/MateGen_Tutorial.ipynb"><strong>Tutorial</strong></a> | 
  <a href="docs/wechat.png"><strong>WeChat</strong></a>
</p>

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-mategen-orange.svg)](https://pypi.org/project/mategen/)

## 📖 Table of Contents

- [What is MateGen?](#what-is-mategen)
- [Key Features](#key-features)
- [API Key Acquisition](#api-key-acquisition)
- [Demo Showcase](#demo-showcase)
- [Installation & Deployment](#installation--deployment)
- [Quick Start](#quick-start)
- [Configuration Guide](#configuration-guide)
- [Architecture Overview](#architecture-overview)
- [Use Cases](#use-cases)
- [Contributing](#contributing)
- [Support](#support)

## What is MateGen?

**MateGen is an Interactive Intelligent Programming Assistant developed by the Jiutian AI Research Team.** It can be conveniently called within Jupyter code environments to assist users in efficiently completing intelligent data analysis, machine learning, deep learning, and large model development tasks. It can also be customized with knowledge bases and extended functionality based on actual user needs.

## 🚀 Key Features

### Core Capabilities

- 🤖 **High Usability, Zero Barrier Entry**: MateGen provides online large model application services with **no hardware or network proxy requirements**. One-click installation and dialogue initiation.

- 🚀 **Powerful High-Precision RAG System**: 
  - One-click synchronization of local documents for RAG retrieval Q&A
  - **Supports up to 1,000 documents and 10GB of content for retrieval**
  - High-precision Q&A for mainstream document formats (md, ppt, word, pdf)
  - Efficiently handles massive document summarization, needle-in-haystack content testing, and sentiment analysis
  - Automatically identifies when RAG retrieval is needed based on user questions

- 🏅 **Local Python Code Interpreter**:
  - Connects to local Python environment for programming tasks
  - Supports data cleaning, visualization, machine learning, deep learning, and large model development
  - Can learn from code repositories before programming
  - Automatic debugging based on actual situations
  - Automatic visualization image upload to image hosting

- 🚩 **High-Precision NL2SQL**:
  - Writes SQL based on user requirements
  - Connects to local MySQL environment for automatic execution
  - Automatic debugging support
  - Can retrieve data dictionaries and enterprise data knowledge bases before SQL writing to improve accuracy

- 🛩️ **Vision and Internet Capabilities**:
  - Input image URLs during dialogue to enable MateGen's vision capabilities
  - Automatic internet search mode when encountering unanswerable questions

- 🚅 **Unlimited Dialogue Context**:
  - Unlimited context dialogue length
  - Intelligently processes historical dialogue based on information density
  - Saves tokens while enabling unlimited context

- 💰 **Extremely Low Usage Cost**:
  - Despite being driven by online large models, actual usage cost is extremely low
  - **500,000 tokens cost only ¥1 in normal mode!**

### Advanced Features

- **High Stability & Availability**
- **Multi Function Calling** (multiple features for one task)
- **Parallel Function Calling** (multiple executors for one feature)
- **Automatic Complex Task Decomposition**
- **Automatic Debugging**
- **Self-Awareness** capabilities
- **Self-Review** and deep **user intent mining**

## 🔑 API Key Acquisition

MateGen currently only offers an online service version, leveraging online large models to complete various services without local hardware or network environment requirements for zero-barrier usage. **Calling MateGen requires API-KEY authentication.** 

During the testing phase, a limited quantity of **300 million free tokens is available while supplies last. For API-KEY acquisition, joining technical discussion groups, or any other questions, <span style="color:red;">scan the QR code to add customer service (WeChat: littlelion_1215), reply "MG" for details 👇</span>**

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240713010710534.png" alt="WeChat QR Code" width="200"/>
</div>

**We welcome support from course students and users. If the project exceeds 10k stars, we will release an open-source version and educational tutorials!**

## 🎬 Demo Showcase

Note: Demonstration operations can be implemented by referring to the relevant code in the [MateGen Tutorial](docs/MateGen_Tutorial.ipynb).

### Zero-Barrier Convenient Calling

Just three steps to call MateGen in Jupyter: **Install, Import, Dialogue**!

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240712185454166.png" alt="Quick Start" width="800"/>
</div>

### Local Massive Text Knowledge Base Q&A

With MateGen, high-precision local knowledge base Q&A can be achieved. MateGen's RAG system **supports up to 1,000 texts + 10GB scale** text retrieval!

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240712212936156.png" alt="Knowledge Base" width="600"/>
</div>

### Interactive Visualization Drawing

MateGen has both vision capabilities and local code interpreter functionality, so it can **imitate and draw based on user-input images**!

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240712193604820.png" alt="Visualization" width="600"/>
</div>

### High-Precision NL2SQL

MateGen supports **fully automatic RAG+NL2SQL joint execution**, so it can **first learn field information and business information from the knowledge base before writing SQL, with automatic review and debugging support**, greatly improving SQL accuracy.

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240712222633885.png" alt="NL2SQL" width="600"/>
</div>

### Automatic Machine Learning

MateGen supports **fully automatic RAG+code interpreter** joint execution, reads enterprise machine learning code libraries before ML modeling, and **one-click natural language invocation of different machine learning modeling strategies** to create your machine learning "JARVIS".

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240712225738564.png" alt="AutoML" width="600"/>
</div>

### Cutting-edge Deep Learning Paper Interpretation & Architecture Reproduction

Based on its powerful RAG system and Multi-Function capabilities, MateGen can conduct in-depth **paper tutoring**, helping users **translate and interpret papers paragraph by paragraph → summarize core knowledge points → write hundreds of lines of code to reproduce paper architecture and directly run verification in local code environment**!

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240712231230708.png" alt="Paper Analysis" width="600"/>
</div>

### Kaggle Competition Guidance

Leveraging MateGen's internet capabilities + knowledge base Q&A + NL2Python capabilities, MateGen can **assist users in participating in Kaggle competitions**. MateGen can automatically obtain competition explanations and dataset interpretation information based on user-provided topics, **automatically crawl high-scoring Kernels and build competition knowledge bases, then assist users in competition programming, automatically submit competition results to the Kaggle platform, and finally prompt users to adjust competition strategies based on submission results to strive for higher scores**!

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240713003522041.png" alt="Kaggle" width="600"/>
</div>

### Intelligent Teaching Assistant

Based on MateGen's powerful massive text retrieval Q&A capability and coding ability, a MateGen with course materials knowledge base can fully serve as an intelligent teaching assistant, assisting users in pre-class preparation, specifying study plans before learning, providing 7*24 real-time Q&A during learning, assisting users in completing programming or other code tasks at any time, and generating exercises based on user questions after class, analyzing weak knowledge points and summarizing them into after-class review documents!

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240726003714902.png" alt="Teaching Assistant" width="600"/>
</div>

More MateGen application scenarios coming soon.

## 📦 Installation & Deployment

MateGen is lightweight and easy to call. It can be installed directly using pip, with a calling style similar to sklearn. Simply instantiate a MateGen agent to start the dialogue!

### Installation Method

MateGen is now available on the PyPI platform and can be installed directly via `pip install mategen`. Note that MateGen requires many dependencies, so installation using a virtual environment is recommended.

**Step 1: Create a virtual environment named `mategen`:**

```bash
conda create -n mategen python=3.8
```

**Step 2: Activate the virtual environment:**

```bash
conda activate mategen
```

**Step 3: Install MateGen in the virtual environment:**

```bash
pip install mategen
```

**Step 4: Install IPython Kernel for Jupyter usage:**

```bash
pip install ipykernel
```

**Step 5: Add the virtual environment to Jupyter's Kernel list:**

```bash
python -m ipykernel install --user --name mategen --display-name "mategen"
```

**Step 6: Start Jupyter service:**

```bash
jupyter lab
```

Then select the mategen kernel in Jupyter to enter the corresponding virtual environment and run MateGen:

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240713012151873.png" alt="Jupyter Kernel" width="400"/>
</div>

## 🚀 Quick Start

### Basic Usage

The MateGen calling process is very simple. Just import it in your code environment and input a valid API-KEY to start the dialogue!

```python
from mategen import MateGenClass

# Initialize MateGen with your API key
mategen = MateGenClass(api_key='YOUR_API_KEY')
```

Then use the chat function for single or multi-round dialogues:

```python
mategen.chat("Hello, nice to meet you!")
```

```markdown
▌ MateGen initialization complete, welcome!

Hello! Nice to meet you! How can I help you?
```

For more MateGen usage methods, see the [MateGen Tutorial](docs/MateGen_Tutorial.ipynb).

### API Key Request

👉 MateGen is currently in the testing phase, offering a limited quantity of **300 million free tokens while supplies last. For API-KEY acquisition, joining technical discussion groups, or any other questions, <span style="color:red;">scan the QR code to add customer service (WeChat: littlelion_1215), reply "MG" for details 👇</span>**

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240713010710534.png" alt="WeChat QR Code" width="200"/>
</div>

## ⚙️ Configuration Guide

### Configuration for Different Environments

When deploying MateGen in different environments, you may need to configure the following:

1. **Modify proxy settings in mategen class** - Configure network proxy if needed
2. **Modify .env file** - Set environment variables including API keys and database credentials
3. **Modify port mapping in Dockerfile** - Adjust container port mappings
4. **Modify port mapping in docker-compose.yml** - Configure service port mappings
5. **Pay attention to proxy and non-proxy issues** - Ensure correct network configuration

### Environment Variables

Create a `.env` file in the project root directory with the following variables:

```bash
# API Configuration
API_KEY=your_api_key_here
BASE_URL=your_base_url_here

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=mategen

# Knowledge Base Path
KNOWLEDGE_LIBRARY_PATH=/path/to/knowledge/base

# Other Configurations
VISION_MODEL=gpt-4o
```

### Docker Deployment

For Docker deployment, use the provided `docker-compose.yml`:

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🏗️ Architecture Overview

### Basic Architecture

MateGen adopts the most advanced threads-runs architecture for better user historical message dialogue management and automatic repair of various issues encountered during operation. It also uses a client-server separation architecture to ensure maximum Agent operation stability, while supporting multiple different types of underlying large models. The basic structure of MateGen is as follows:

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240715001340035.png" alt="Architecture" width="600"/>
</div>

### Technology Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL 5.7+
- **AI Models**: OpenAI GPT-4, GPT-4o
- **Vector Database**: OpenAI Vector Store
- **Code Execution**: Local Python Interpreter
- **Containerization**: Docker & Docker Compose

## 💼 Use Cases

### MateGen as Intelligent Teaching Assistant

MateGen can also be applied to various specific business scenarios. For example, MateGen is currently used in the teaching assistance of various courses by Jiutian's teaching team as an intelligent teaching assistant. The basic functional execution flow of MateGen as an intelligent teaching assistant is as follows:

<div align="center">
<img src="https://ml2022.oss-cn-hangzhou.aliyuncs.com/img/image-20240715001720425.png" alt="Teaching Assistant Flow" width="700"/>
</div>

### Other Application Scenarios

- **Data Analysis Assistant**: Automated data cleaning, analysis, and visualization
- **Code Review & Optimization**: Intelligent code review and optimization suggestions
- **Research Assistant**: Paper reading, summarization, and experiment reproduction
- **Database Query Assistant**: Natural language to SQL query generation
- **Documentation Generator**: Automatic documentation generation from code

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support, questions, or feedback:

- **Technical Discussion Group**: Scan the WeChat QR code above
- **Email**: Contact via WeChat customer service
- **Issues**: [GitHub Issues](https://github.com/yourusername/mategen/issues)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Special thanks to all contributors and the Jiutian AI Research Team for their continuous support and development of MateGen.

---

<div align="center">
Made with ❤️ by Jiutian AI Research Team
</div>