import dash
from dash import dcc, html, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import os
import io

# Import split modules
from app_logic import generate_datasets, run_physical_ai_logic
from app_viz import build_physical_topo
from app_components import get_sidebar_layout, get_main_layout, render_transformer_card
from app_translations import TRANSLATIONS

# --- Resource Initialization ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
server = app.server
app.title = "HarmoniSense-LV"

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

def get_b64_img(filename):
    path = os.path.join(ASSET_DIR, filename)
    if not os.path.exists(path): 
        print(f"⚠️ Warning: Image not found at {path}")
        return ""
    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('ascii')
            return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"❌ Error loading image {filename}: {e}")
        return ""

IMG_B64 = {p: get_b64_img(f'{p}_PHASE.png') for p in ['A', 'B', 'C']}
IMG_B64['T'] = get_b64_img('Transformer.png')

# Static initial layout (driven by callback later)
app.layout = html.Div([
    dbc.Container([
        dcc.Store(id='lang-store', data='en'),
        dcc.ConfirmDialog(id='error-alert', message=''),
        html.Div([
            dcc.Dropdown(id='lang-selector', options=[{'label': '中文', 'value': 'zh'}, {'label': 'English', 'value': 'en'}], value='en', clearable=False)
        ], style={'display': 'none'}), 
        
        html.Div(id='header-container'),
        dbc.Row([
            dbc.Col(id='sidebar-container', width=4),
            dbc.Col(id='main-content-container', width=8)
        ]),
        dcc.Download(id="download-dataframe-xlsx"),
        dcc.Store(id='processed-topo')
    ], fluid=False, style={"padding": "0 15px"})
], style={"background-color": "#f1f2f6", "min-height": "100vh"})

# --- Callbacks ---

@app.callback(
    [Output('header-container', 'children'),
     Output('sidebar-container', 'children'),
     Output('main-content-container', 'children'),
     Output('lang-store', 'data')],
    Input('lang-selector', 'value')
)
def switch_language(lang):
    if not lang: lang = 'en'
    t = TRANSLATIONS[lang]
    header = html.H2(t['title'], style={"text-align":"center", "margin-top":"60px", "margin-bottom":"30px", "font-weight":"bold", "color": "#2c3e50"})
    sidebar = get_sidebar_layout(lang)
    content = get_main_layout(lang)
    return header, sidebar, content, lang

@app.callback(
    [Output('sidebar-container', 'width'), Output('main-content-container', 'width')],
    Input('lang-store', 'data')
)
def adjust_layout_width(_):
    return 4, 8

@app.callback(
    Output('transformers-container', 'children'),
    [Input('n-trans', 'value'), Input('lang-store', 'data')],
    [State({'type': tid, 'index': ALL}, 'value') for tid in ['n-a', 'b-a', 'black-a', 'hp-a', 'pv-a', 'mine-a', 'hpump-a', 'n-b', 'b-b', 'black-b', 'hp-b', 'pv-b', 'mine-b', 'hpump-b', 'n-c', 'b-c', 'black-c', 'hp-c', 'pv-c', 'mine-c', 'hpump-c']]
)
def update_configs(n, lang, *states):
    if not n: return []
    def get_v(s_idx, t_idx):
        return states[s_idx][t_idx] if states[s_idx] and t_idx < len(states[s_idx]) else 0
    cards = []
    for i in range(n):
        vals = {
            'A': {'n': get_v(0,i), 'b': get_v(1,i), 'black': get_v(2,i), 'hp': get_v(3,i), 'pv': get_v(4,i), 'mine': get_v(5,i), 'hpump': get_v(6,i)},
            'B': {'n': get_v(7,i), 'b': get_v(8,i), 'black': get_v(9,i), 'hp': get_v(10,i), 'pv': get_v(11,i), 'mine': get_v(12,i), 'hpump': get_v(13,i)},
            'C': {'n': get_v(14,i), 'b': get_v(15,i), 'black': get_v(16,i), 'hp': get_v(17,i), 'pv': get_v(18,i), 'mine': get_v(19,i), 'hpump': get_v(20,i)}
        }
        cards.append(render_transformer_card(i, vals, lang))
    return cards

@app.callback(
    Output('processed-topo', 'data'),
    [Input('upload-data', 'contents'), Input('btn-load-sample-1', 'n_clicks'), Input('btn-load-sample-2', 'n_clicks'), Input('btn-load-sample-3', 'n_clicks')],
    [State('upload-data', 'filename'), State('lang-store', 'data'), State('n-trans', 'value')] + [State({'type': tid, 'index': ALL}, 'value') for tid in ['n-a', 'b-a', 'black-a', 'hp-a', 'pv-a', 'mine-a', 'hpump-a', 'n-b', 'b-b', 'black-b', 'hp-b', 'pv-b', 'mine-b', 'hpump-b', 'n-c', 'b-c', 'black-c', 'hp-c', 'pv-c', 'mine-c', 'hpump-c']],
    prevent_initial_call=True
)
def handle_input(contents, n1, n2, n3, filename, lang, n_trans, *states):
    ctx = dash.callback_context
    if not ctx.triggered: return dash.no_update
    trig = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Core: Determine trigger type
    try:
        if trig == 'upload-data':
            if not contents or ',' not in contents: return dash.no_update
            _, b64 = contents.split(',')
            buf = io.BytesIO(base64.b64decode(b64))
            df = pd.read_csv(buf) if filename.endswith('.csv') else pd.concat(pd.read_excel(buf, sheet_name=None).values(), ignore_index=True)
        else:
            # Load template
            sample_idx = trig.split('-')[-1]
            path = os.path.join(ASSET_DIR, f"sample_{sample_idx}.xlsx")
            if not os.path.exists(path): return {'error': f"File Missing: {path}"}
            df = pd.concat(pd.read_excel(path, sheet_name=None).values(), ignore_index=True)
        
        # Execute analysis logic
        topo = run_physical_ai_logic(df)
        pr_df = pd.DataFrame(topo['phases'])
        def safe_sum(pdf, col): return pdf[col].sum() if not pdf.empty and col in pdf.columns else 0
        
        t = TRANSLATIONS[lang]
        topo['summary'] = t['report_summary'].format(
            bl=int(safe_sum(pr_df, 'Black_Count')), 
            ev=int(safe_sum(pr_df, 'EV_Count')), 
            pv=int(safe_sum(pr_df, 'PV_Count')), 
            mine=int(safe_sum(pr_df, 'Mine_Count')), 
            hp=int(safe_sum(pr_df, 'HPump_Count'))
        )
        return topo
    except Exception as e:
        debug_vals = [str(s)[:20] for s in states[:5]]
        return {'error': f"Processing Error: {str(e)} | Debug States: {debug_vals}"}

@app.callback(
    [Output('results-accordion', 'active_item'), Output('viz-accordion', 'active_item')],
    Input('processed-topo', 'data'),
    prevent_initial_call=True
)
def auto_expand_panels(data):
    if not data or 'error' in data: return dash.no_update, dash.no_update
    return 'item-details', 'item-viz'

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    [Input('btn-simulate', 'n_clicks'), Input('btn-dl-sample-1', 'n_clicks'), Input('btn-dl-sample-2', 'n_clicks'), Input('btn-dl-sample-3', 'n_clicks')],
    [State('n-trans', 'value')] + [State({'type': tid, 'index': ALL}, 'value') for tid in ['n-a', 'b-a', 'black-a', 'hp-a', 'pv-a', 'mine-a', 'hpump-a', 'n-b', 'b-b', 'black-b', 'hp-b', 'pv-b', 'mine-b', 'hpump-b', 'n-c', 'b-c', 'black-c', 'hp-c', 'pv-c', 'mine-c', 'hpump-c']],
    prevent_initial_call=True
)
def handle_downloads(n_sim, n1, n2, n3, n_trans, *states):
    ctx = dash.callback_context
    if not ctx.triggered: return dash.no_update
    trig = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Core safety check: Only allow download if clicks > 0
    val = dash.callback_context.triggered[0]['value']
    if val is None or val == 0: return dash.no_update

    if 'dl-sample' in trig:
        path = os.path.join(ASSET_DIR, f"sample_{trig.split('-')[-1]}.xlsx")
        return dcc.send_file(path) if os.path.exists(path) else dash.no_update
    data = generate_datasets(n_trans, *states)
    def to_xlsx(bytes_io):
        with pd.ExcelWriter(bytes_io, engine='openpyxl') as writer:
            for s, d in data.items(): d.to_excel(writer, sheet_name=s, index=False)
    return dcc.send_bytes(to_xlsx, "harmo_sim_data.xlsx")

@app.callback(
    [Output('topology-graph', 'figure'), Output('expert-alert-text', 'children'), Output('node-details-table-container', 'children')],
    [Input('processed-topo', 'data'), Input('threshold-imbalance', 'value'), Input('threshold-overload', 'value'), Input('threshold-theft', 'value'), Input('threshold-loss', 'value'), Input({'type': 'dynamic-t-cap', 'index': ALL}, 'value'), Input('lang-store', 'data')],
    [State({'type': 'dynamic-t-cap', 'index': ALL}, 'id')]
)
def update_viz(data, t_imb, t_ovl, t_thf, t_los, caps, lang, cids):
    cap_dict = {cid['index']: caps[i] for i, cid in enumerate(cids)}
    return build_physical_topo(data, t_imb, t_ovl, t_thf, t_los, cap_dict, IMG_B64, lang)

@app.callback(
    Output('dynamic-capacity-container', 'children'),
    [Input('processed-topo', 'data'), Input('lang-store', 'data')]
)
def update_cap_inputs(data, lang):
    if not data or 'phases' not in data: return []
    t = TRANSLATIONS[lang]
    t_names = sorted(list(set([f"Transformer_{x['Node_ID'].split('_')[1]}" for x in data['phases'] if x.get('Node_ID') and '_' in x['Node_ID']])))
    return [dbc.Col([html.Label(f"📝 {tn} {t['cap_label']}:"), dbc.Input(id={'type': 'dynamic-t-cap', 'index': tn}, type="number")], width=4) for tn in t_names]

if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=8053)
    except Exception as e:
        import traceback
        with open("crash_log.txt", "w") as f:
            f.write(traceback.format_exc())
        raise e
