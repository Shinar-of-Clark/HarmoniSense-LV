# HarmoniSense-LV
> **Low-Voltage Distribution Network Physical Fingerprint and AI Expert Diagnostic Platform**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Physical%20AI-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20Mac-777.svg)]()

<img src="images/sys_overview.png" width="800" alt="HarmoniSense-LV System Dashboard Mastery">

HarmoniSense-LV is an AI-driven diagnostic system for low-voltage grids based on high-order physical harmonic fingerprints. It enables automatic topology reconstruction of the physical distribution network via AI algorithms, performs multi-dimensional fingerprint identification of connected loads, and quickly locates electricity theft, unregistered users, and unauthorized connections of new energy equipment.

---

## 🚀 Core Features

- **AI Topology Reconstruction**: Based on the Pearson correlation coefficient algorithm, it automatically reconstructs the physical phase and link structure of the substation area without manual record entry.
- **Load Fingerprint Identification**: Deep feature extraction technology accurately identifies specific electricity consumption patterns such as EV charging, distributed photovoltaics, cryptocurrency mining machines, and high-power heat pumps.
- **Unauthorized Node Detection**: Through physical energy conservation residual analysis, it locks onto unauthorized connection (electricity theft/unregistered user) nodes in seconds.
- **Multi-language Interaction**: Built-in dynamic switching between Chinese and English, providing an industrial-grade real-time interactive dashboard.

## 🛠️ Technical Architecture

The project adopts a modular design with a clear code structure:

- `dashboard_app.py`: **Main program entry point**. Built on Dash (Plotly), responsible for global state management and callback logic.
- `app_logic.py`: **AI core algorithm center**. Contains data cleaning, simulation engine, phase identification, and anomaly analysis logic.
- `app_viz.py`: **Topology graph rendering engine**. Responsible for NetworkX spatial computation and Plotly dynamic topology visualization.
- `app_components.py`: **UI component library**. Encapsulates sidebar, cards, expert report box, and accordion components.
- `app_translations.py`: **Internationalization dictionary**. Supports full business terminology mapping between Chinese and English.

## 📖 Auxiliary Documentation

To facilitate developers and users, the project provides detailed Markdown documentation:

- 📄 **Product Specification**: Contains detailed algorithm methodology, technical advantages, and system screenshot descriptions.
- 📘 **User Manual**: Provides step-by-step guidance on how to run the system, import data, and interpret reports.

## 🚦 Quick Start

### 1. Environment Setup
Ensure your Python environment supports the following libraries:
```bash
pip install dash dash-bootstrap-components pandas networkx numpy scipy openpyxl
```

### 2. 启动系统
执行主脚本启动 Flask/Dash 服务：
```bash
python dashboard_app.py
```
启动后访问：`http://127.0.0.1:8052`

## 📚 理论基础与致谢 (Theoretical Foundation)

本平台的算法设计理念与物理映射逻辑，深受以下学术成果的启发：

- **论文名称**: *Utilising Smart-Meter Harmonic Data for Low-Voltage Network Topology Identification*
- **核心团队**: Ali Othman, Neville R. Watson, Andrew Lapthorn (University of Canterbury); Radnya Mukhedkar (EPECentre).
- **发表期刊**: *Energies* 2025, 18(13), 3333.
- **论文链接**: [https://doi.org/10.3390/en18133333](https://doi.org/10.3390/en18133333)

**致谢**：特别感谢坎特伯雷大学研究团队在低压配网谐波分析领域的开创性工作。

---

## ⚖️ 知识共享许可协议 (License)

本项目采用 **[知识共享 署名-非商业性使用-相同方式共享 4.0 国际许可协议 (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)** 进行许可。

- **您可以**：自由地共享（复制、发行）和演绎（修改、转换）本作品。
- **但必须遵守**：
  - **署名**：必须给出适当的署名，提供许可协议链接。
  - **非商业性使用**：**不得将本作品用于商业目的。**
  - **相同方式共享**：若演绎本作品，必须采用与本作品相同的许可协议分发。

---

> **© Clark 设计与开发** | I have obtained the key to Babel, and I shall raise countless towers in Shinar
