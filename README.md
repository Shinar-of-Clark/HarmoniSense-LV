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

- 📄 [**Product Specification**](Product%20Specification.md): Contains detailed algorithm methodology, technical advantages, and system screenshot descriptions.
- 📘 [**User Manual**](User%20Manual.md): Provides step-by-step guidance on how to run the system, import data, and interpret reports.
- 🍄 [**White Paper**](HarmoniSense_Core%20Functions%20and%20Principles%20White%20Paper.md): Core functions and principles documentation.

## 🚦 Quick Start

### 1. Environment Setup
Ensure your Python environment supports the following libraries:
```bash
pip install dash dash-bootstrap-components pandas networkx numpy scipy openpyxl
```

### 2. Launch the System
Run the main script to start the Flask/Dash service:
```bash
python dashboard_app.py
```
After launching, visit: `http://127.0.0.1:8053`

## 📚 Theoretical Foundation & Acknowledgements

The algorithm design philosophy and physical mapping logic of this platform are deeply inspired by the following academic achievements:

- **Paper Title**: *Utilising Smart-Meter Harmonic Data for Low-Voltage Network Topology Identification*
- **Core Team**: Ali Othman, Neville R. Watson, Andrew Lapthorn (University of Canterbury); Radnya Mukhedkar (EPECentre).
- **Published Journal**: *Energies* 2025, 18(13), 3333.
- **Paper Link**: [https://doi.org/10.3390/en18133333](https://doi.org/10.3390/en18133333)

**Acknowledgements**: Special thanks to the research team at the University of Canterbury for their pioneering work in the field of harmonic analysis for low-voltage distribution networks.

---

## ⚖️ License

This project is licensed under the **[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)**.

- **You are free to**: Share (copy and redistribute) and Adapt (remix, transform, and build upon) the material.
- **Under the following terms**:
  - **Attribution**: You must give appropriate credit and provide a link to the license.
  - **Non-Commercial**: **You may not use the material for commercial purposes.**
  - **Share-Alike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

---

> **© Designed & Developed by Clark** | I have obtained the key to Babel, and I shall raise countless towers in Shinar

