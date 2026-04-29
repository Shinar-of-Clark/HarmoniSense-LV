import dash_bootstrap_components as dbc
from dash import html, dcc, ALL
from app_translations import TRANSLATIONS

# ==========================================
# Global UI style parameter configuration
# ==========================================
UI_CONFIG = {
    'card_shadow': "0 4px 12px rgba(0,0,0,0.1)",  # Card shadow
    'card_radius': "10px",                        # Card radius
    'card_bg': "white",                           # Card background color
    'header_side': "#2c3e50",                     # Sidebar header background color
    'header_main': "#3498db",                     # Main interface header background color
    'graph_height': "520px",                      # Space for large icons
    'table_max_height': "400px",                  # Max height for details table
    'alert_bg': "#e74c3c",                        # Alert box background color
    'canvas_border': "1px solid black",           # Canvas black frame (for debugging)
}

CARD_STYLE = {
    "box-shadow": UI_CONFIG['card_shadow'], 
    "border-radius": UI_CONFIG['card_radius'], 
    "background-color": UI_CONFIG['card_bg'], 
    "margin-bottom": "20px", "padding": "20px", "border": "none"
}

def get_sidebar_layout(lang='zh'):
    t = TRANSLATIONS[lang]
    return html.Div([
        html.Div([
            html.Label("Language:", style={"font-size": "12px", "font-weight": "bold"}),
            dcc.Dropdown(id='lang-selector', options=[{'label': '中文', 'value': 'zh'}, {'label': 'English', 'value': 'en'}], value=lang, clearable=False, style={"margin-bottom": "40px"}),
            
            html.H5(t['upload_header'], style={"background-color": UI_CONFIG['header_side'], "color": "white", "padding": "10px", "border-top-left-radius": "5px", "border-top-right-radius": "5px", "margin": "-20px -20px 25px -20px"}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([t['drag_upload']]),
                style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin-bottom': '20px', 'background-color': '#f8f9fa', 'cursor': 'pointer'}
            ),
            dbc.Accordion([
                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col([html.Label(t['trans_num']), dcc.Dropdown(id="n-trans", options=[{'label': str(i), 'value': i} for i in range(1, 10)], value=1, clearable=False)]),
                    ], className="mb-3"),
                    html.Div(id="transformers-container"),
                    dbc.Button(t['sim_btn'], id="btn-simulate", color="danger", className="mt-3 w-100"),
                ], title=t['sim_title']),
                dbc.AccordionItem([
                    html.P(t['sample_desc'], style={"font-size": "12px", "color": "#7f8c8d"}),
                    *[dbc.InputGroup([
                        dbc.Button(f"{t['load_sample']} {i:02d}", id=f"btn-load-sample-{i}", color="primary", outline=True, style={"flex": "1", "font-size": "13px"}),
                        dbc.Button("💾", id=f"btn-dl-sample-{i}", color="secondary", outline=True, style={"width": "45px"})
                    ], className="mb-2") for i in [1, 2, 3]]
                ], title=t['sample_title'])
            ], start_collapsed=True),
        ], style=CARD_STYLE)
    ])

def get_main_layout(lang='zh'):
    t = TRANSLATIONS[lang]
    return html.Div([
        dbc.Accordion([
            dbc.AccordionItem([
                dcc.Graph(id="topology-graph", style={"height": UI_CONFIG['graph_height'], "border": UI_CONFIG['canvas_border']})
            ], title=t['viz_title'], item_id='item-viz')
        ], id="viz-accordion", start_collapsed=True, style={"margin-bottom": "20px"}),
        
        dbc.Accordion([
            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col([html.Label(t['imb_label']), dbc.Input(id="threshold-imbalance", type="number", value=15.0)], width=3),
                    dbc.Col([html.Label(t['ovl_label']), dbc.Input(id="threshold-overload", type="number", value=80.0)], width=3),
                    dbc.Col([html.Label(t['theft_label']), dbc.Input(id="threshold-theft", type="number", value=5.0)], width=3),
                    dbc.Col([html.Label(t['loss_label']), dbc.Input(id="threshold-loss", type="number", value=4.0)], width=3),
                ]),
                html.Div(id="dynamic-capacity-container", style={"margin-top": "15px"})
            ], title=t['threshold_title'], item_id='item-thresholds'),
            dbc.AccordionItem([
                html.Div(id="node-details-table-container", style={"max-height": UI_CONFIG['table_max_height'], "overflow-y": "auto"})
            ], title=t['detail_title'], item_id='item-details')
        ], id='results-accordion', start_collapsed=True, style={"margin-bottom": "15px"}),
        html.Div([
            html.B(t['expert_report']),
            html.Span(id="expert-alert-text", children=t['wait_data'])
        ], id="expert-alert-box", style={"background-color": UI_CONFIG['alert_bg'], "color": "white", "padding": "15px", "border-radius": "5px", "margin-bottom": "30px"}),
        
        dbc.Accordion([
            dbc.AccordionItem([
                html.Div([
                    dcc.Markdown(t['changelog_body'], style={"font-size": "14px"})
                ], style={"padding": "20px", "background-color": "#fdfdfd"})
            ], title=t['changelog_title'])
        ], start_collapsed=True, style={"margin-bottom": "80px"})
    ])

def render_transformer_card(i, vals, lang='en'):
    t = TRANSLATIONS[lang]
    return dbc.Card([
        dbc.CardHeader(html.B(f"⚡ Transformer {i+1}"), style={"padding": "5px 15px", "background-color": "#ecf0f1"}),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6(f"Phase {p}", style={"font-weight": "bold", "color": color, "margin-bottom":"5px"}),
                        *[html.Div([
                            html.Label(f"{t[label+'_label']}:", style={"font-size": "0.75em", "margin": "0"}),
                            dbc.Input(id={'type':f"{tid}-{p.lower()}", 'index':i}, type="number", value=vals[p][tid], min=0, size="sm", className="mb-1")
                        ]) for label, tid in [("meter","n"), ("branch","b"), ("unreg","black"), ("ev","hp"), ("pv","pv"), ("mine","mine"), ("hpump","hpump")]]
                    ], style={"border": f"1px solid {color}", "padding": "5px", "border-radius": "5px", "background-color": bg})
                ], width=4, style={"padding": "2px"}) for p, color, bg in [('A','#27ae60','#edf7f1'), ('B','#e74c3c','#fdf2f0'), ('C','#2980b9','#e7f1f9')]
            ])
        ], style={"padding": "5px"})
    ], className="mb-2")
