# User Manual: HarmoniSense-LV Low-Voltage Distribution Network AI Diagnostic System

Welcome to **HarmoniSense-LV**. This manual aims to guide you through the system's operation process, enabling precise substation area diagnostics by applying high-order power quality feature data.

---

## 1. System Startup
1. Ensure that your Python environment has the necessary dependencies installed: `dash`, `dash-bootstrap-components`, `pandas`, `networkx`, `scipy`.
2. Execute the following command in your terminal:
   ```bash
   python dashboard_app.py
   ```
3. Access in your browser: `http://127.0.0.1:8053`

---

## 2. Step-by-Step Operation Guide

### Step One: Select Interface Language
After startup, you can select **中文 (zh)** or **English (en)** from the dropdown menu at the top of the left sidebar. The interface will instantly switch the language of all menus and reports.

### Step Two: Import Data for Analysis
The system provides two ways to input data:
1. **Formal Analysis**: Click the "Drag & Drop or Click to Upload" area on the left to select an Excel or CSV file containing high-order harmonic features.
2. **Quick Demo**: Click "Load Preset Sample," and the system will automatically load test data to demonstrate the AI logic.

<div align="center">
  <img src="images/manual_import.png" width="800">
  <p><b>📸 Figure 1: Data Import and Preset Sample Loading Area</b></p>
</div>

### Step Three: Configure Analysis Thresholds
In the "Alarm & Analysis Thresholds" panel in the middle, you can adjust the following parameters based on actual substation area operating standards:
- **3-Phase Imbalance**: Exceeding this value will trigger a substation area risk warning.
- **Overload Utilization**: Defines the alert line for transformer utilization.
- **Unmetered Leakage/Physical Line Loss**: Sets the sensitivity for identifying unauthorized connections.

### Step Four: Interpret the AI Topology View
- **View Phases**: Observe the branch colors of node connections (A/B/C correspond to green, red, and blue, respectively).
- **Drill Down Node Information**: Hover your mouse over any node icon to view real-time electromagnetic fingerprint data.

<div align="center">
  <img src="images/manual_topo.png" width="800">
  <p><b>📸 Figure 2: Topology Graph Interactive View and Node Drill-Down Function</b></p>
</div>

### Step Five: Consult the AI Expert Diagnostic Report
The red alert box at the bottom of the page summarizes major hidden dangers in the current substation area:
- Number of "black users" (unregistered users) detected.
- Distribution of EV charging, PV access, and mining machine access.
- Line loss anomalies and operational risk warnings.
    
<div align="center">
  <img src="images/load_fingerprint.png" width="800">
  <p><b>📸 Figure 3: AI Expert Diagnostic Report and Recommended Actions Display</b></p>
</div>

---

## 3. Advanced Feature: Physical Condition Simulation
If you need to verify specific logic, you can use the "Physical Condition Simulation" panel:
1. Set the number of transformers.
2. Configure parameters such as the number of legal users, unregistered users, and EV quantities for each phase.
3. Click **🔥 Generate Physical Feature Data**, and the system will synthesize a set of simulated data conforming to physical laws for your analysis.

---

## 4. Common Troubleshooting
- **Webpage cannot be opened**: Please check the command line window for any obvious Python syntax errors.
- **No response after uploading data**: Please ensure that the Excel file contains core column names such as `Node_ID`, `THD`, `V13-V19`, `Timestamp`.
- **Display of abnormal characters**: Ensure that your system supports UTF-8 encoding, or try switching the language.

---

> **© Designed and Optimized by Clark**
> *HarmoniSense-LV v1.0 User Guide*
