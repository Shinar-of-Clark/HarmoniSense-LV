import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash import html, dcc
from app_translations import TRANSLATIONS

def build_physical_topo(data_dict, t_imb, t_ovl, t_theft_th, t_loss_th, cap_dict, IMG_B64, lang='zh'):
    t_text = TRANSLATIONS[lang]
    if not data_dict: return go.Figure(), t_text['wait_data'], None
    if 'error' in data_dict:
        return go.Figure(), f"Diagnostic Error: {data_dict['error']}", None
    if cap_dict is None: cap_dict = {}
    
    edges_df, pr_df = pd.DataFrame(data_dict['edges']), pd.DataFrame(data_dict['phases'])
    if edges_df.empty:
        n_p = len(pr_df)
        n_bus = len(data_dict.get('phases', []))
        nodes_sample = pr_df['Node_ID'].iloc[:3].tolist() if n_p > 0 else []
        total_rows = data_dict.get('total_rows', 0)
        return go.Figure(), f"AI Expert Diagnostic Report: 未发现边关联。(总行数: {total_rows}, 负载节点: {n_p}, 示例 ID: {nodes_sample}, 母线状态: {'正常' if n_bus>0 else '未发现母线'})", None
    
    G = nx.DiGraph()
    for _, row in edges_df.iterrows(): G.add_edge(row['from'], row['to'], p=row['Phase'])
    
    # ==========================================
    # Visual layout parameter configuration
    # ==========================================
    # ==========================================
    # Visual layout parameter configuration
    # ==========================================
    V_CFG = {
        'node_spacing': 60,       
        'layer_spacing': 110,     
        'phase_spacing': 280,      # Added: spacing between phase columns
        'y_top': 300,             
        'y_trans': 420,           
        'node_size_map': 28,      
        'trans_size_map': 42,     
        'anom_size_map': 12,      
        'icon_offset': 12,        
        'node_text_size': 9,      
        'trans_text_size': 14,    
        'phase_text_size': 12,    
        'phase_colors': {'A': '#27ae60', 'B': '#e74c3c', 'C': '#2980b9'},
        'phase_offset_map': {'A': -280, 'B': 0, 'C': 280} # Added: phase coordinate offset
    }

    pos, total_system_width, t_info = {}, 0, []
    # Identify true root nodes (transformers) from edges_df
    all_from = set(edges_df['from'].unique())
    all_to = set(edges_df['to'].unique())
    # Transformer nodes are typically those acting only as 'from' and containing 'Transformer' in the name (excluding 'Bus')
    # Fix: extract only true transformer nodes (excluding 'Bus' string)
    t_names = sorted(list(set([n for n in all_from if 'Transformer' in str(n) and 'Bus' not in str(n)])))
    
    if not t_names:
        # Backward compatibility: if no direct transformer root is found, infer from Bus upwards
        t_roots = edges_df['from'][edges_df['from'].str.contains('Bus', na=False)].unique()
        t_names = sorted(list(set([n.split('_Bus')[0] for n in t_roots if n and isinstance(n, str) and '_Bus' in n])))

    for t_name in t_names:
        phase_nodes_by_level = {'A': {}, 'B': {}, 'C': {}}
        phase_labels = {'A': 'Phase A', 'B': 'Phase B', 'C': 'Phase C'}
        phase_max_width = {'A': 0, 'B': 0, 'C': 0}
        for p in ['A', 'B', 'C']:
            # Get subgraph belonging to this transformer and phase
            # Start from t_name, search in edges of this phase
            p_edges = edges_df[edges_df['Phase'] == p]
            if p_edges.empty: continue
            
            # Find the starting bus for this phase (as direct child of transformer)
            phase_bus = [n for n in p_edges['to'].unique() if 'Bus' in n and n.startswith(t_name)]
            if not phase_bus: 
                # Try finding from 'from'
                phase_bus = [n for n in p_edges['from'].unique() if 'Bus' in n and n.startswith(t_name)]
            
            if not phase_bus: continue
            root = phase_bus[0]
            
            # Use DiGraph to calculate levels starting from Bus (Bus is level 1, transformer manually set to level 0)
            sub_g = G.subgraph(list(nx.descendants(G, root)) + [root])
            levels = nx.single_source_shortest_path_length(sub_g, root)
            max_d = max(levels.values()) if levels else 0
            for d in range(max_d + 1):
                nodes = [n for n, lvl in levels.items() if lvl == d]
                # Here d+1 because level 0 is reserved for transformer
                phase_nodes_by_level[p][d+1] = nodes
                phase_max_width[p] = max(phase_max_width[p], len(nodes))
        
        active_phases = [p for p in ['A', 'B', 'C'] if phase_max_width[p] > 0 or any(phase_nodes_by_level[p].values())]
        # Fix: calculate width based on max width of this phase to ensure enough distance between phases
        phase_widths = {p: max(2, phase_max_width[p]) * V_CFG['node_spacing'] for p in active_phases}
        tw = max(200, sum(phase_widths.values()) + 40)
        t_info.append({'name': t_name, 'active_phases': active_phases, 'phase_widths': phase_widths, 'phase_nodes_by_level': phase_nodes_by_level, 't_width': tw})
        total_system_width += tw

    sx = -total_system_width / 2.0
    annotations = []
    pp = {p: {tn: {'meter':0.0, 'theft':0.0, 'loss':0.0} for tn in t_names} for p in ['A', 'B', 'C']}
    
    for t in t_info:
        tx, cur_lx = sx + t['t_width'] / 2.0, sx + t['t_width'] / 2.0 - sum(t['phase_widths'].values()) / 2.0
        # Transformer position (Level 0)
        t_root_id = f"{t['name']}_ROOT"
        pos[t_root_id] = (tx, V_CFG['y_trans'])
        # Establish alias to be compatible with subsequent logic
        pos[t['name']] = pos[t_root_id] 
        
        for p in t['active_phases']:
            pw = t['phase_widths'][p]
            px = cur_lx + pw / 2.0
            
            p_sum = sum(pp[p][t['name']].values())
            annotations.append(dict(
                x=px, y=V_CFG['y_top']+40, text=f"<b>{phase_labels[p]}</b><br>{p_sum:.1f} kW", 
                showarrow=False, font=dict(color=V_CFG['phase_colors'][p], size=14)
            ))
            
            for d, nodes in t['phase_nodes_by_level'][p].items():
                x_span = len(nodes) * V_CFG['node_spacing']
                for i, n in enumerate(nodes):
                    # Y coordinate calculation: y_top corresponds to Bus (Level 1), subsequent layers shift down
                    pos[n] = (px - x_span/2.0 + i*V_CFG['node_spacing'] + V_CFG['node_spacing']/2.0,
                              V_CFG['y_top'] - (d-1)*V_CFG['layer_spacing'])
            # Important fix: only handle isolated nodes of current phase, tile horizontally to prevent overlapping
            orphans = [n for n in pr_df[pr_df['Phase'] == p].to_dict('records') if str(n['Node_ID']) not in pos]
            if orphans:
                x_span_o = len(orphans) * V_CFG['node_spacing']
                for i, n in enumerate(orphans):
                    nid = str(n['Node_ID'])
                    # Tile according to the center point of this phase
                    pos[nid] = (px - x_span_o/2.0 + i*V_CFG['node_spacing'] + V_CFG['node_spacing']/2.0,
                               V_CFG['y_top'] - V_CFG['layer_spacing'])
            cur_lx += pw
        sx += t['t_width']

    ex, ey = [], []
    for u, v in G.edges():
        # If v is an alias of transformer root, skip (or handle uniformly)
        u_id = f"{u}_ROOT" if u in t_names else u
        v_id = f"{v}_ROOT" if v in t_names else v
        
        if u_id in pos and v_id in pos:
            ex.extend([pos[u_id][0], pos[v_id][0], None])
            ey.extend([pos[u_id][1], pos[v_id][1], None])
        elif u in pos and v in pos:
            ex.extend([pos[u][0], pos[v][0], None])
            ey.extend([pos[u][1], pos[v][1], None])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ex, y=ey, line=dict(width=1, color='#bdc3c7'), mode='lines', hoverinfo='none'))
    if total_system_width > 0:
        fig.add_trace(go.Scatter(x=[-total_system_width/2 - 40, total_system_width/2 + 40], y=[10, 10], mode='markers', marker=dict(color='rgba(0,0,0,0)'), showlegend=False))

    table_rows = []
    pp = {p: {tn: {'meter':0.0, 'theft':0.0, 'loss':0.0} for tn in t_names} for p in ['A', 'B', 'C']}
    nx_list, ny_list, ntxt, htxt = [], [], [], []
    lx, ly, tx, ty = [], [], [], []
    img_list, shape_list = [], []

    # ==========================================
    # Data format strong shield (V42) - ensure all diagnostic fields exist
    # ==========================================
    required_cols = ['Node_ID', 'Phase', 'Anomaly', 'Correlation', 
                     'EV_Count', 'Black_Count', 'PV_Count', 'Mine_Count', 'HPump_Count',
                     'Impedance', 'Distance', 'Demand_kW', 'Loss_kW'] 
    pr_df = pr_df.reindex(columns=required_cols, fill_value=0)
    
    # Force convert numeric columns to native types
    for col in ['EV_Count', 'Black_Count', 'PV_Count', 'Mine_Count', 'HPump_Count']:
        pr_df[col] = pd.to_numeric(pr_df[col], errors='coerce').fillna(0).astype(int)
    for col in ['Correlation', 'Impedance', 'Distance', 'Demand_kW', 'Loss_kW']:
        pr_df[col] = pd.to_numeric(pr_df[col], errors='coerce').fillna(0.0).astype(float)
    # Ensure Node_ID is string for matching with generated pos keys
    pr_df['Node_ID'] = pr_df['Node_ID'].astype(str)

    for n, (nxv, nyv) in pos.items():
        if "ROOT" in n or "Bus" in n: continue
        m = pr_df[pr_df['Node_ID'] == n]
        if m.empty: continue
        
        # Safe read (V41 mapping: strongly aligned with app_logic.py)
        pc = str(m['Phase'].iloc[0])
        anom = str(m['Anomaly'].iloc[0])
        evc, blc, pvc, mc, hpc = int(m['EV_Count'].iloc[0]), int(m['Black_Count'].iloc[0]), int(m['PV_Count'].iloc[0]), int(m['Mine_Count'].iloc[0]), int(m['HPump_Count'].iloc[0])
        
        # Core fix: read real values identified by AI, stop using dummy formulas
        ri = float(m['Correlation'].iloc[0])
        rdist = float(m['Distance'].iloc[0])
        npow = float(m['Demand_kW'].iloc[0])
        ploss = float(m['Loss_kW'].iloc[0])
        
        # Transformer attribution identification
        if "Unregistered_Found_" in n:
            parts = n.split('_')
            try:
                idx = parts.index("Transformer")
                tnav = f"{parts[idx]}_{parts[idx+1]}"
            except: tnav = "Transformer_1"
        else:
            tnav = f"Transformer_{n.split('_')[1] if isinstance(n, str) and '_' in n else '1'}"
        
        # Update phase power summary statistics
        if tnav in pp[pc]:
            if anom == 'BlackUser_Anomaly':
                pp[pc][tnav]['theft'] += npow
            else:
                pp[pc][tnav]['meter'] += npow
            pp[pc][tnav]['loss'] += ploss
        
        dp = []
        if blc>0: dp.append(f"{t_text['diag_unreg']} ({blc})")
        if evc>0: dp.append(f"{t_text['diag_ev']} ({evc})")
        if pvc>0: dp.append(f"{t_text['diag_pv']} ({pvc})")
        if mc>0: dp.append(f"{t_text['diag_mine']} ({mc})")
        if hpc>0: dp.append(f"{t_text['diag_hp']} ({hpc})")
        
        def get_td_style(bg="transparent"):
            return {"backgroundColor": bg, "color": "black", "fontWeight": "bold" if bg != "transparent" else "normal"}

        status_val = t_text['status_unreg'] if 'BlackUser' in anom else t_text['status_reg']
        
        table_rows.append(html.Tr([
            html.Td(tnav), 
            html.Td(n), 
            html.Td(f"{ri:.4f}"), 
            html.Td(f"{m['Impedance'].iloc[0]:.3f}"), 
            html.Td(f"{m['Distance'].iloc[0]:.1f}"), 
            html.Td(f"{ploss:.2f}"), 
            html.Td(f"{npow:.2f}"), 
            html.Td(status_val, style=get_td_style("#FF4136" if 'BlackUser' in anom else "transparent")), 
            html.Td(str(evc), style=get_td_style("#FF851B" if evc > 0 else "transparent")), 
            html.Td(str(pvc), style=get_td_style("#FF851B" if pvc > 0 else "transparent")), 
            html.Td(str(mc), style=get_td_style("#FF851B" if mc > 0 else "transparent")), 
            html.Td(str(hpc), style=get_td_style("#FF851B" if hpc > 0 else "transparent"))
        ]))
        
        nx_list.append(nxv); ny_list.append(nyv)
        # Naming logic: only true BlackUser_Anomaly nodes get U_ prefix
        num_part = n.split('_')[-1] if '_' in n else n
        u_prefix = "U_" if (anom == 'BlackUser_Anomaly' and not num_part.startswith('U')) else ""
        label_text = f"<b>{u_prefix}{num_part}</b>" + (" ⚠️" if dp else "")
        ntxt.append(label_text)
        htxt.append(f"Node: {n}<br>Corr: {ri:.4f}<br>Dist: {rdist:.1f} m<br>Demand: {npow:.2f} kW<br><b>[{'<br>'.join(dp) if dp else t_text['diag_ok']}]</b>")
        
        # Map Phase A/B/C to local asset paths
        phase_asset = f"assets/{pc}_PHASE.png"
        
        # If true black user, do not show house icon, only keep red X mark
        if anom != 'BlackUser_Anomaly':
            img_list.append(dict(source=phase_asset, xref="x", yref="y", x=nxv, y=nyv, sizex=V_CFG['node_size_map'], sizey=V_CFG['node_size_map'], xanchor="center", yanchor="middle", layer="above"))
        
        # ==========================================
        # Vertical icon array layout (V35 robust fix)
        # ==========================================
        # Force check coordinate validity
        if np.isnan(nxv) or np.isnan(nyv): continue
        
        cur_x = float(nxv)
        cur_y = float(nyv)
        
        sx_os = (V_CFG.get('node_size_map', 28) / 2.0) + 5
        sy_os = 10
        step_y = 12
        asz = V_CFG.get('anom_size_map', 12) / 2.0
        
        a_idx = 0
        
        # 1. EV Charger
        if evc > 0:
            iy = cur_y + sy_os - (a_idx * step_y)
            shape_list.append(dict(type="circle", xref="x", yref="y", x0=cur_x+sx_os-asz, y0=iy-asz, x1=cur_x+sx_os+asz, y1=iy+asz, fillcolor="orange", line=dict(color="darkorange", width=1)))
            a_idx += 1
        
        # 2. PV Solar
        if pvc > 0:
            iy = cur_y + sy_os - (a_idx * step_y)
            shape_list.append(dict(type="rect", xref="x", yref="y", x0=cur_x+sx_os-asz, y0=iy-asz, x1=cur_x+sx_os+asz, y1=iy+asz, fillcolor="#2ecc71", line=dict(color="green", width=1)))
            a_idx += 1
            
        # 3. Mining
        if mc > 0:
            iy = cur_y + sy_os - (a_idx * step_y)
            # Use simplified path to draw diamond
            p_str = f"M {cur_x+sx_os} {iy-asz*1.3} L {cur_x+sx_os-asz*1.3} {iy} L {cur_x+sx_os} {iy+asz*1.3} L {cur_x+sx_os+asz*1.3} {iy} Z"
            shape_list.append(dict(type="path", xref="x", yref="y", path=p_str, fillcolor="#9b59b6", line=dict(color="#8e44ad", width=1)))
            a_idx += 1

        # 4. Heat Pump
        if hpc > 0:
            iy = cur_y + sy_os - (a_idx * step_y)
            shape_list.append(dict(type="rect", xref="x", yref="y", x0=cur_x+sx_os-asz, y0=iy-asz, x1=cur_x+sx_os+asz, y1=iy+asz, fillcolor="#3498db", line=dict(color="#2980b9", width=1)))
            a_idx += 1

        # Black user mark
        if anom == 'BlackUser_Anomaly':
            xs = V_CFG.get('node_size_map', 28) * 0.4
            shape_list.append(dict(type="line", xref="x", yref="y", x0=cur_x-xs, y0=cur_y-xs, x1=cur_x+xs, y1=cur_y+xs, line=dict(color="red", width=3)))
            shape_list.append(dict(type="line", xref="x", yref="y", x0=cur_x-xs, y0=cur_y+xs, x1=cur_x+xs, y1=cur_y-xs, line=dict(color="red", width=3)))



    # Calculate label coordinates (offset downwards relative to node center, sync spreading with map scaling)
    ly_list = [y - V_CFG['node_size_map'] * 1.3 for y in ny_list]

    # Draw base interactive layer (text labels placed on specially calculated ly_list)
    fig.add_trace(go.Scatter(
        x=nx_list, y=ly_list, mode='text', 
        text=ntxt, textposition="middle center",
        textfont=dict(size=V_CFG['node_text_size'], color="#34495e"),
        showlegend=False, hoverinfo='skip'
    ))

    # Draw hover interactive layer (placed at node center)
    fig.add_trace(go.Scatter(
        x=nx_list, y=ny_list, mode='markers', 
        marker=dict(size=V_CFG['node_size_map'], color='rgba(0,0,0,0)'),
        hovertext=htxt, hoverinfo="text", showlegend=False
    ))



    bx, by, btxt = [], [], []
    for n, (nxv, nyv) in pos.items():
        if n and isinstance(n, str) and "Bus" in n:
            parts = n.split('_')
            pc = parts[-1] if parts else 'A'
            tn = n.split('_Bus')[0]
            pp_ptr = pp.get(pc, {}).get(tn, {'meter':0})
            tp = sum(pp_ptr.values()) if isinstance(pp_ptr, dict) else 0
            bx.append(nxv); by.append(nyv); btxt.append(f"<b>Phase {pc}<br>{tp:.1f} kW</b>")
    fig.add_trace(go.Scatter(x=bx, y=by, mode='text', text=btxt, textposition="top center", textfont=dict(size=V_CFG['phase_text_size'], color="#2980b9"), showlegend=False))

    thx, thy, thtx, ttx = [], [], [], []
    for tn in t_names:
        txv, tyv = pos[f"{tn}_ROOT"]
        ta, tb, tc = [sum(pp[p].get(tn, {'m':0}).values()) for p in ['A','B','C']]
        sp, tm = ta+tb+tc, sum([pp[p].get(tn, {}).get('meter', 0) for p in ['A','B','C']])
        tl, tth = sum([pp[p].get(tn, {}).get('loss', 0) for p in ['A','B','C']]), sum([pp[p].get(tn, {}).get('theft', 0) for p in ['A','B','C']])
        t_short = f"T_{tn.split('_')[1]}" if '_' in tn else "T_1"
        thx.append(txv); thy.append(tyv); ttx.append(f"<b>{t_short}: {sp:.1f} kW</b>")
        thtx.append(f"<b>{tn}</b><br>{t_text['total_power']}: {sp:.1f} kW<br>{t_text['compliant']}: {tm:.1f} kW<br>{t_text['line_loss']}: {tl:.1f} kW<br>{t_text['theft']}: {tth:.1f} kW")
        # Transformer native image
        img_list.append(dict(source="assets/Transformer.png", xref="x", yref="y", x=txv, y=tyv, sizex=V_CFG['trans_size_map'], sizey=V_CFG['trans_size_map'], xanchor="center", yanchor="middle", layer="above"))
    
    # Transformer label coordinates (offset upwards to prevent icon covering text after zooming)
    lty_list = [y + V_CFG['trans_size_map'] * 1.0 for y in thy]
    fig.add_trace(go.Scatter(x=thx, y=lty_list, mode='text', text=ttx, textposition="middle center", textfont=dict(size=V_CFG['trans_text_size'], color="#c0392b"), hovertext=thtx, hoverinfo="text", showlegend=False))

    fig.update_layout(
        plot_bgcolor="white", images=img_list, shapes=shape_list,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1
        ),
        xaxis=dict(visible=False, range=[-(V_CFG['phase_spacing']*1.5), (V_CFG['phase_spacing']*1.5)]), 
        yaxis=dict(visible=False, range=[-600, 550], scaleanchor="x", scaleratio=1), 
        margin=dict(b=80, l=40, r=40, t=40)
    )
    
    th = [html.Thead(html.Tr([
        html.Th(t_text[c], style={"position": "sticky", "top": "0", "zIndex": "10", "backgroundColor": "rgb(230, 230, 230)"}) 
        for c in ["th_trans","th_node","th_corr","th_imp","th_dist","th_loss","th_demand","th_status","ev_label","pv_label","mine_label","hpump_label"]
    ]))]
    detail_table = html.Div(dbc.Table(th + [html.Tbody(table_rows)], bordered=True, striped=False, hover=True, size="sm", className="bg-white", style={"color": "black"}))
    
    mstr = ""
    summary_msg = data_dict.get('summary', '')
    if summary_msg: mstr += f"**{summary_msg}**\n\n---\n\n"
    for tn in t_names:
        ta, tb, tc = [sum(pp[p].get(tn, {'m':0}).values()) for p in ['A','B','C']]
        sp, tl, tth = ta+tb+tc, sum([pp[p].get(tn, {}).get('loss', 0) for p in ['A','B','C']]), sum([pp[p].get(tn, {}).get('theft', 0) for p in ['A','B','C']])
        ps = [ta, tb, tc]
        imb = (max(ps) - min(ps)) / (sp/3.0 if sp>0 else 1) * 100.0 if sp>0 else 0
        lr, tr = (tl/sp*100 if sp>0 else 0), (tth/sp*100 if sp>0 else 0)
        tcap = cap_dict.get(tn, 0); iss = []
        
        t_idx_str = tn.split('_')[1] if isinstance(tn, str) and '_' in tn else '1'
        tpv = sum(pr_df[(pr_df['Node_ID'].str.contains(t_idx_str, na=False))]['PV_Count'])
        tmine = sum(pr_df[(pr_df['Node_ID'].str.contains(t_idx_str, na=False))]['Mine_Count'])
        thp = sum(pr_df[(pr_df['Node_ID'].str.contains(t_idx_str, na=False))]['HPump_Count'])
        if tpv>0: iss.append(f"{t_text['diag_pv']} ({int(tpv)})")
        if tmine>0: iss.append(f"{t_text['diag_mine']} ({int(tmine)})")
        if thp>0: iss.append(f"{t_text['diag_hp']} ({int(thp)})")
        if imb > t_imb: iss.append(f"{t_text['alert_imb']} ({imb:.1f}%)")
        if tr > t_theft_th: iss.append(f"{t_text['alert_theft']} ({tr:.1f}%)")
        if lr > t_loss_th: iss.append(f"{t_text['alert_loss']} ({lr:.1f}%)")
        
        if tcap and float(tcap) > 0:
            util = (sp / float(tcap)) * 100.0
            label = t_text['advice_warn'] if iss or util > t_ovl else t_text['advice_ok']
            mstr += f"**{tn} {label}** (Util: {util:.1f}%) " + (" / ".join(iss) if iss else "") + "\n\n"
        else:
            label = t_text['advice_warn'] if iss else t_text['advice_ok']
            mstr += f"**{tn} {label}** " + (" / ".join(iss) if iss else "") + "\n\n"
            
    return fig, dcc.Markdown(mstr), detail_table
