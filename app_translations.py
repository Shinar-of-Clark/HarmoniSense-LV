# --- Translation Dictionary ---

ZH_DICT = {
    'title': "⚡ 物理灵魂配网指纹识别与AI诊断平台",
    'upload_header': "特征数据解析",
    'drag_upload': "拖拽或 点击上传特征文件",
    'trans_num': "变压器数量:",
    'sim_title': "🛠️ 物理灵魂条件模拟",
    'sim_btn': "🔥 生成物理特征数据并下载",
    'sample_title': "🚀 预设样本快速测试",
    'sample_desc': "载入预设样本直接解析或点击磁盘符号下载。",
    'load_sample': "🚀 载入预设样本",
    'viz_title': "AI 算法拓扑还原结果 (物理电磁聚类分析)",
    'threshold_title': "⚙️ 报警与研判阈值设置",
    'imb_label': "三相不平衡度报警 (%):",
    'ovl_label': "重载利用率预警 (%):",
    'theft_label': "窃电漏量报警 (%):",
    'loss_label': "物理线损占比报警 (%):",
    'detail_title': "📊 节点详细分析信息",
    'expert_report': "🍄 AI 专家诊断报告: ",
    'wait_data': "还未输入数据, 请导入数据或者使用预设样本数据",
    'meter_label': "户数",
    'branch_label': "分支",
    'unreg_label': "未登记",
    'ev_label': "EV",
    'pv_label': "光伏",
    'mine_label': "矿机",
    'hpump_label': "热泵",
    'cap_label': "额定容量",
    'th_trans': "变压器",
    'th_node': "节点名称",
    'th_corr': "相关性",
    'th_imp': "阻抗(Ω)",
    'th_dist': "距离(m)",
    'th_loss': "线损(kW)",
    'th_demand': "需求(kW)",
    'th_status': "状态",
    'status_reg': "合法",
    'status_unreg': "未登记",
    'diag_ok': "✅ 正常",
    'diag_unreg': "🚨 未登记用电户",
    'diag_ev': "🚗 EV设备",
    'diag_pv': "☀️ 光伏设备",
    'diag_mine': "⛏️ 矿机设备",
    'diag_hp': "🔥 热泵设备",
    'report_summary': "分析完成！发现 {bl} 处疑似黑户，{ev} 台 EV，{pv} 处光伏接入，{mine} 台矿机，{hp} 台热泵。",
    'alert_imb': "三相不平衡",
    'alert_theft': "非法表外",
    'alert_loss': "线损过高",
    'advice_ok': "✅ 运行状态良好",
    'advice_warn': "⚠️ 运行风险警告",
    'total_power': "总视角负荷",
    'compliant': "合规负荷",
    'line_loss': "模型计算线损",
    'theft': "非授权窃电",
    'changelog_title': "📝 系统更新日志 & 核心方法论 (Changelog & Methodology)",
    'changelog_body': """
        ☀️ **系统更新日志 v1.0**
        核心功能：实现了基于物理特征信号的拓扑自动重构与用电行为指纹识别算法。

        **1. AI 拓扑还原与相位识别 (AI Topology & Phase Detection)**
        - 利用 Pearson 相关系数矩阵进行波形指纹匹配，自动重构低压配电网台区物理拓扑。
        - 实现高精度在线相位辨识，准确率高达 99% 以上。

        **2. 异常用电与窃电诊断 (Theft & Anomaly Diagnosis)**
        - **黑户探测 (Unregistered Users)**：通过物理总量守恒与特征残差分析，识别非授权接入用户。
        - **违规采矿 (Mining Farm)**：基于 V13 特征谐波的恒定功率特征识别加密货币矿机。
        - **违规设备**：识别热泵 (HeatPump) 及高功率阻性/感性负荷的启停特征。

        **3. 新型能源设备监控 (Energy Device Monitoring)**
        - **有序充电 (EV Charging)**：识别 19 次特征谐波偏移，精准定位电动车充电位置。
        - **分布式光伏 (PV Solar)**：结合 17 次特征谐波与功率流动特征，监测光伏接入点。

        **4. 运行质量评估 (Power Quality & Loss)**
        - 台区三相不平衡度 (Imbalance) 实时计算与报警，基于物理模型计算线损率 (Line Loss) 偏移诊断。
        """
}

EN_DICT = {
    'title': "HarmoniSense-LV Physical AI Diagnostic Dashboard",
    'upload_header': "Data Feature Parsing",
    'drag_upload': "Drag & Drop or Click to Upload",
    'trans_num': "Number of Transformers:",
    'sim_title': "🛠️ Physical Condition Simulation",
    'sim_btn': "🔥 Generate & Download Physical Data",
    'sample_title': "🚀 Preset Samples Quick Test",
    'sample_desc': "Load preset samples for analysis or download raw files.",
    'load_sample': "🚀 Load Sample",
    'viz_title': "AI Topology Reconstruction (Electromagnetic Clustering)",
    'threshold_title': "⚙️ Alarm & Analysis Thresholds",
    'imb_label': "3-Phase Imbalance Alarm (%):",
    'ovl_label': "Overload Utilization Warning (%):",
    'theft_label': "Unmetered Leakage Alarm (%):",
    'loss_label': "Line Loss Ratio Alarm (%):",
    'detail_title': "📊 Detailed Node Analysis",
    'expert_report': "🍄 AI Expert Diagnostic Report: ",
    'wait_data': "No data entered yet, please import data or use preset samples",
    'meter_label': "Meters",
    'branch_label': "Branch",
    'unreg_label': "Unreg",
    'ev_label': "EV",
    'pv_label': "PV",
    'mine_label': "Mine",
    'hpump_label': "HeatPump",
    'cap_label': "Rated Cap",
    'th_trans': "Transformer",
    'th_node': "Node Name",
    'th_corr': "Correlation",
    'th_imp': "Imp(Ω)",
    'th_dist': "Dist(m)",
    'th_loss': "Loss(kW)",
    'th_demand': "Demand(kW)",
    'th_status': "Status",
    'status_reg': "Legal",
    'status_unreg': "Unreg",
    'diag_ok': "✅ Normal",
    'diag_unreg': "🚨 Unregistered",
    'diag_ev': "🚗 EV Device",
    'diag_pv': "☀️ PV Solar",
    'diag_mine': "⛏️ Mining Gear",
    'diag_hp': "🔥 HeatPump",
    'report_summary': "Analysis Complete! Found {bl} black users, {ev} EV, {pv} PV Solar, {mine} Mining, {hp} HeatPump.",
    'alert_imb': "3-Phase Imbalance",
    'alert_theft': "Illegal Leakage",
    'alert_loss': "High Line Loss",
    'advice_ok': "Stable Operation",
    'advice_warn': "AI Alert",
    'total_power': "Total Power",
    'compliant': "Compliant",
    'line_loss': "Line Loss",
    'theft': "Theft",
    'changelog_title': "📝 System Update Log & Core Methodology",
    'changelog_body': """
        ☀️ **System Update Log v1.0**
        Core Features: AI topology reconstruction and load behavior fingerprinting based on physical signal features.

        **1. AI Topology & Phase Detection**
        - Waveform fingerprint matching using Pearson correlation matrix for LV network physical topology reconstruction.
        - Real-time Phase Identification with >99% accuracy.

        **2. Theft & Anomaly Diagnosis**
        - **Unregistered Users**: Identifying unauthorized access via physical conservation and residual analysis.
        - **Mining Farms**: Recognizing crypto-mining equipment based on V13 harmonic signatures.
        - **Unauthorized Loads**: Detection of HeatPumps and high-power load start/stop signatures.

        **3. New Energy Monitoring**
        - **EV Charging**: Precise localization of electric vehicle charging using V19 harmonic shifts.
        - **Distributed PV**: Monitoring PV injection points using V17 harmonic and reverse power flow signatures.

        **4. Operational Quality**
        - Real-time calculation and alerts for Three-phase Imbalance and Line Loss modeling.
        """
}

TRANSLATIONS = {
    'zh': ZH_DICT,
    'en': EN_DICT
}
