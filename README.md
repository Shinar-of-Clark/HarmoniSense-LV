# HarmoniSense-LV
> **低压配网物理指纹与 AI 专家诊断平台**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Physical%20AI-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20Mac-777.svg)]()

<img src="images/sys_overview.png" width="800" alt="HarmoniSense-LV System Dashboard Mastery">

HarmoniSense-LV 是一款基于电能质量高阶谐波特征（Physical Fingerprints）开发的低压配网诊断系统。通过 AI 算法实现对配电网物理拓扑的自动化还原，并对接入负载进行多维度的指纹识别，快速定位窃电、黑户及新型能源设备的违规接入。

---

## 🚀 核心特性

- **AI 拓扑还原**：基于 Pearson 相关系数算法，无需人工录入台账，自动还原台区物理相位与链路结构。
- **负载指纹识别**：深度特征提取技术，精准识别 EV 充电、分布式光伏、加密货币矿机、大功率热泵等特定用电模式。
- **非授权节点探测**：通过物理能量守恒残差分析，秒级锁定非授权接入（窃电/黑户）节点。
- **多语言交互**：内置中英文双语动态切换，提供工业级实时交互看板。

## 🛠️ 技术架构

项目采用模块化设计，代码结构清晰：

- `dashboard_app.py`: **主程序入口**。基于 Dash (Plotly) 构建，负责全局状态管理与回调逻辑。
- `app_logic.py`: **AI 核心算法中心**。包含数据清洗、仿真引擎、相位识别及异常研判逻辑。
- `app_viz.py`: **拓扑图形渲染引擎**。负责 NetworkX 空间计算与 Plotly 动态拓扑可视化。
- `app_components.py`: **UI 组件库**。封装了侧边栏、卡片、专家报告框及风琴折叠组件。
- `app_translations.py`: **国际化字典**。支持全量业务术语的中英文映射。

## 📖 辅助文档

为了方便开发者和用户，项目中提供了详尽的 Markdown 文档：

- 📄 [**产品说明书 (Product Spec)**](./产品说明.md): 包含详细的算法方法论、技术优势及系统截图说明。
- 📘 [**用户操作手册 (User Manual)**](./用户操作手册.md): 分步骤指导如何运行系统、导入数据并解读报告。

## 🚦 快速开始

### 1. 环境准备
确保您的 Python 环境支持以下库：
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
