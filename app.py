import pathlib
from datetime import datetime
import flask
import dash
import dash_table
import matplotlib.colors as mcolors
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input, State
from dateutil import relativedelta
import helper_functions
import preprocessing

EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
LOGO = "https://avatars0.githubusercontent.com/u/55491416?s=460&v=4"
MAIN_PAGE = "https://github.com/iamvarol"
DB_DF = pd.read_csv('data/cash_data.csv')
GLOBAL_DF = preprocessing.preprocess(DB_DF, False)
TABLE_SELECTED_COLUMNS = [
    'Tarih', 
    'Grup', 
    'Tutar', 
    'Islem Tipi', 
    'Aciklama', 
    'HesapAdi',
    ]


"""
a little bit more preprocessing
"""
day_list = [
    "Sunday",
    "Saturday",
    "Friday",
    "Thursday",
    "Wednesday",
    "Tuesday",
    "Monday",
]


"""
#  Page layout and contents
"""
"""
# NAVBAR
"""
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(id="logo-image", src=LOGO, height="30px")),
                    dbc.Col(
                        dbc.NavbarBrand("Detaylı Nakit Akışı", className="ml-2"), align="center",
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href=MAIN_PAGE, target="_blank",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)
"""
# NAVBAR
"""





"""
# LEFT_COLUMN
"""
LEFT_COLUMN = dbc.Jumbotron(
    [
        html.Label("Zaman Aralığı Seçiniz", className="lead"),
        html.Div(dcc.RangeSlider(id="time-window-slider"), style={"marginTop": 10}),
        html.Label("Grup tipini seçiniz", style={"marginTop": 10}, className="lead"),
        dcc.Dropdown(
            id="grup-drop", 
            clearable=False, 
            style={"marginBottom": 10, "font-size": 12},
            multi=True,
        )
    ]
)
"""
# LEFT_COLUMN
"""


"""
# CARDS_PLOT
"""
CARDS_PLOT = [
    dbc.Row(
        [
            dbc.Card(
            [
                dbc.CardImg(src="http://www.pngmart.com/files/7/Income-PNG-Free-Download.png", top=True,  style={"height":"14rem"}),
                dbc.CardBody(
                    [
                        html.H6("Gelirler Toplamı", className="card-title"),
                        html.H4(id="gelirlerText", className="card-text",style={"color": "green"}),
                        ]
                    ),
                ],
            style={"width": "15rem"},
            ),
            html.Hr(style={"height":"14rem"}),
            dbc.Card(
            [
                dbc.CardImg(src="https://cdn1.iconfinder.com/data/icons/estate-planning-glyph/64/expense-expenditure-consumption-outgoings-salary-512.png", top=True,  style={"height":"14rem"}),
                dbc.CardBody(
                    [
                        html.H6("Giderler Toplamı", className="card-title"),
                        html.H4(id="giderlerText", className="card-text",style={"color": "red"}),
                        ]
                    ),
                ],
            style={"width": "15rem"},
            ),
            html.Hr(style={"height":"14rem"}),
            dbc.Card(
            [
                dbc.CardImg(src="https://cdn.onlinewebfonts.com/svg/img_457131.png", top=True,  style={"height":"14rem"}),
                dbc.CardBody(
                    [
                        html.H6("Ciro", className="card-title"),
                        html.H4(id="ciroText", className="card-text",style={"color": "green"}),
                        ]
                    ),
                ],
            style={"width": "15rem"},
            ),
        ]
    ),
]

"""
# CARDS_PLOT
"""


"""
# TABLE
"""
# https://dash.plot.ly/datatable/interactivity
# to select columns to show
TABLE = dash_table.DataTable(
        id="datatable",
        columns=[{"name": i, "id": i} for i in TABLE_SELECTED_COLUMNS],
        data=GLOBAL_DF.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_cell_conditional=[{'if': {'column_id': c},  
                                 'backgroundColor': '#EAFAF1'} for c in ['Tarih',]]
                    + [{'if': {'column_id': c}, 
                        'backgroundColor': '#FEF9E7'} for c in ['Grup', ]]
                    + [{'if': {'column_id': c}, 
                        'backgroundColor': '#EBF5FB'} for c in ['Tutar', ]]
                    + [{'if': {'column_id': c}, 
                        'backgroundColor': '#F4ECF7'} for c in ['Islem Tipi', ]]
                    + [{'if': {'column_id': c}, 
                        'backgroundColor': '#FDEDEC'} for c in ['Aciklama1', ]]
                    + [{'if': {'column_id': c}, 
                        'backgroundColor': '#F6DDCC'} for c in ['HesapAdi', ]],

        
        # style_cell_conditional=[
        #     {
        #         "if": {"column_id": "Text"},
        #         "textAlign": "left",
        #         "whiteSpace": "normal",
        #         "height": "auto",
        #         "min-width": "50%",
        #         }
        #     ],
        style_data_conditional=[{'if': {'row_index': 'odd'}, 
                                 'backgroundColor': '#D5DBDB'}]
                    + [{'if': {'column_id': c, 
                               'row_index': 'odd'}, 'backgroundColor': '#D5F5E3'} for c in ['Tarih',]]
                    + [{'if': {'column_id': c, 
                               'row_index': 'odd'}, 'backgroundColor': '#FCF3CF'} for c in ['Grup', ]]
                    + [{'if': {'column_id': c, 
                               'row_index': 'odd'}, 'backgroundColor': '#D6EAF8'} for c in ['Tutar',]]
                    + [{'if': {'column_id': c, 
                               'row_index': 'odd'}, 'backgroundColor': '#E8DAEF'} for c in ['Islem Tipi', ]]
                    + [{'if': {'column_id': c, 
                               'row_index': 'odd'}, 'backgroundColor': '#FADBD8'} for c in ['Aciklama1',]]
                    + [{'if': {'column_id': c, 
                               'row_index': 'odd'}, 'backgroundColor': '#E59866'} for c in ['HesapAdi',]],
                        
        # style_cell={
        #     "padding": "16px",
        #     "whiteSpace": "normal",
        #     "height": "auto",
        #     "max-width": "0",
        #     },
        style_header={
        # 'backgroundColor': '#0357a8',
        'fontWeight': 'bold',
        # 'color': 'white'
        },
        # style_data={"whiteSpace": "normal", "height": "auto"},
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="multi",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        )
"""
# TABLE
"""

"""
# TABLE_PLOTS
"""
TABLE_PLOTS = [
    dbc.CardHeader(html.H5("Nakit Akışı Tablosu")),
    dbc.CardBody(
        [
            html.P(
                "'filter data...' yazan bölüme sorgu yazılabilir",
                className="mb-0",
            ),
            TABLE,  
            # LDA_PLOT,
            # html.Hr(),
        ]
    ),
]
"""
# TABLE_PLOTS
"""


"""
# GRUPS_PLOT
"""
GRUPS_PLOT = [
    
    dbc.CardHeader(html.H5("Tahsilat ve Ödeme İşlemleri")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-grup-hist",
                children=[dcc.Graph(id="grup-sample")],
                type="default",
            )
        ]
    ),
]
"""
# GRUPS_PLOT
"""

"""
# ISLEM_HISTOGRAM_PLOT
"""
ISLEM_HISTOGRAM_PLOT = [
    
    dbc.CardHeader(html.H5("Haftalık Finansal Durum")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-islem-hist",
                children=[dcc.Graph(id="islem-tutar-hist")],
                type="default",
            )
        ]
    ),
]
"""
# ISLEM_HISTOGRAM_PLOT
"""

"""
# HEATMAP_PLOT
"""
HEATMAP_PLOT = [
    
    dbc.CardHeader(html.H5("Yıl-Ay Finansal Durum")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-heatmap",
                children=[dcc.RadioItems(
                            id="selector",
                            options=[
                                {"label": "Ciro", "value": "ciro"},
                                {"label": "Tahsilat", "value": "tahsilat"},
                                {"label": "Ödeme", "value": "odeme"},
                            ],
                            value="ciro",
                            labelStyle={"display": "inline-block"},
                            ),
                          html.Br(),
                          dcc.Graph(id="heatmap")
                          ],
                type="default",
            )
        ]
    ),
]
"""
# HEATMAP_PLOT
"""

"""
# BODY
"""
BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(LEFT_COLUMN, md=4, align="center",),
                dbc.Col(CARDS_PLOT, md=8,align="center"),
                # dbc.Col(dbc.Card(GRUPS_PLOT), md=8),
            ],
            style={"marginTop": 20, "height":"20rem"},
        ),
        # dbc.Card(ISLEM_HISTOGRAM_PLOT),
        dbc.Row([dbc.Col([dbc.Card(ISLEM_HISTOGRAM_PLOT)])], style={"marginTop": 50}),
        html.Hr(),
        dbc.Row([dbc.Col([dbc.Card(HEATMAP_PLOT)])], style={"marginTop": 50}),
        html.Hr(),
        dbc.Row([dbc.Col([dbc.Card(TABLE_PLOTS)])], style={"marginTop": 50}),
        html.Hr(),
        dbc.Row([dbc.Col([dbc.Card(GRUPS_PLOT)])], style={"marginTop": 50}),
    ],
    className="mt-12",
)
"""
# BODY
"""






server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], server=server)
app.layout = html.Div(children=[NAVBAR, BODY])











"""
#  Callbacks
"""



@app.callback(
    [
        Output("time-window-slider", "marks"),
        Output("time-window-slider", "min"),
        Output("time-window-slider", "max"),
        Output("time-window-slider", "step"),
        Output("time-window-slider", "value"),
    ],
    [Input("logo-image", "src")],
    )
def populate_time_slider(src):
    """
    Depending on our dataset, we need to populate the time-slider
    with different ranges. This function does that and returns the
    needed data to the time-window-slider.
    """
    min_date = GLOBAL_DF["timestamp"].min()
    max_date = GLOBAL_DF["timestamp"].max()

    marks = helper_functions.make_marks_time_slider(min_date, max_date)
    min_epoch = list(marks.keys())[0]
    max_epoch = list(marks.keys())[-1]

    return (
        marks,
        min_epoch,
        max_epoch,
        (max_epoch - min_epoch) / (len(list(marks.keys())) * 3),
        [min_epoch, max_epoch],
    )



@app.callback(
    [Output("grup-drop", "options"),
     Output("grup-drop", "value")],
    [Input("time-window-slider", "value")],
    )
def populate_grup_dropdown(time_values):
    # """ TODO """
    # print("grup-drop: TODO USE THE TIME VALUES")
    if time_values is not None:
        pass
    grup_names, counts = helper_functions.get_grup_count(GLOBAL_DF)
    counts.append(1)
    return helper_functions.make_options_grup_drop(grup_names), grup_names


@app.callback(
    Output("grup-sample", "figure"),
    [Input("time-window-slider", "value")],
    )
def update_grup_sample_plot(time_values):
    """ TODO """
    # print("redrawing grup-sample...")
    # print("\ttime_values is:", time_values)
    if time_values is None:
        return {}
    grup_sample_count = 5
    min_date, max_date = helper_functions.time_slider_to_date(time_values)
    values_sample, counts_sample = helper_functions.calculate_grup_sample_data(
        GLOBAL_DF, grup_sample_count, [min_date, max_date]
    )
    data = [
        {
            "x": values_sample,
            "y": counts_sample,
            "text": values_sample,
            "textposition": "auto",
            "type": "bar",
            "name": "",
            "color": values_sample,
        }
    ]
    layout = {
        "autosize": False,
        "margin": dict(t=10, b=10, l=40, r=0, pad=4),
        "xaxis": {"showticklabels": False},
    }
    # print("redrawing grup-sample...done")
    return {"data": data, "layout": layout}

@app.callback(
    [
        Output("gelirlerText", "children"),
        Output("giderlerText", "children"),
        Output("ciroText", "children"),
        # Output("farkText", "style"),
    ],
    [
        Input("time-window-slider", "value"),
        Input("grup-drop", "value"),
    ],
)
def update_texts(time_values, grup):
    
    if time_values is not None:
        min_date, max_date = helper_functions.time_slider_to_date(time_values)

        filtered_df = GLOBAL_DF.sort_values("timestamp").set_index("timestamp")[min_date:max_date]

        if grup:
            # print(grup)
            filtered_df = filtered_df[filtered_df["Grup"].isin(grup)]
        
        df = pd.DataFrame(filtered_df.groupby(["Islem Tipi"]).sum().reset_index())
        
        # print(df)
        # print('After group by')
        # print(df.head())
        # print(df.tail())
        
        if df.size > 2 :
            if df.iat[0,0] == "Tahsilat":
                gelirlerToplami = ciro_gel = df.iat[0,1]
                gelirlerToplami = '{:,.2f}'.format(gelirlerToplami)
        else:
            gelirlerToplami = ciro_gel = 0
            
        if df.size > 2 :
            if df.iat[1,0]=="Ödeme":
                giderlerToplami = ciro_gid = df.iat[1,1]
                giderlerToplami = '{:,.2f}'.format(giderlerToplami)
        else:
            giderlerToplami = ciro_gid = 0
            
        ciro  = ciro_gel + ciro_gid
        ciro = '{:,.0f}'.format(ciro)
        
        result = gelirlerToplami, giderlerToplami, ciro
    else:
        result = "no result", "no result", "no result"

    return result

@app.callback(
    Output("islem-tutar-hist", "figure"),
    [
        Input("time-window-slider", "value"),
    ],
)
def update_islem_tutar_histogram(time_values):
    """
    Depending on our dataset, we need to draw the initial histogram.
    """

    if time_values is not None:
        min_date, max_date = helper_functions.time_slider_to_date(time_values)
        return helper_functions.generate_islem_tipi_histogram(min_date, max_date, GLOBAL_DF)

    return {"data":[]}

@app.callback(
    Output("heatmap", "figure"),
    [
        # Input("time-window-slider", "value"),
        Input("selector", "value"),
    ],
)
def update_heatmap(selector_value):
    #print("\t time values first heatmap : type ", type(time_values))
    # if time_values is not None:
    # Return to original hm(no colored annotation) by resetting
        # min_date, max_date = helper_functions.time_slider_to_date(time_values)
    return helper_functions.generate_heatmap(GLOBAL_DF, selector_value)

    # return {"data":[]}

# @app.callback(
#     Output("grup-drop", "value"), 
#     [Input("grup-sample", "clickData")],
#     )
# def update_grup_drop_on_click(value):
#     """ TODO """
#     if value is not None:
#         selected_grup = value["points"][0]["x"]
#         return selected_grup
#     return grup_list

# @app.callback(
#     [
#         Output("table", "data"),
#         Output("table", "columns"),
#         # Output("tsne-lda", "figure"),
#     ],
#     [
#         Input("grup-drop", "value"),
#         Input("time-window-slider", "value"),
#         # Input("n-selection-slider", "value"),
#     ],
# )
# def update_table(grup, time_values):
#     if time_values is not None:
#         min_date, max_date = helper_functions.time_slider_to_date(time_values)

#         filtered_df = GLOBAL_DF.sort_values("Tarih").set_index("Tarih")[
#         min_date:max_date]

#         if grup:
#             # print(grup)
#             filtered_df = filtered_df[filtered_df["Grup"].isin(grup)]
        
#         columns = [{"name": i, "id": i} for i in filtered_df.columns]
#         data = filtered_df.to_dict("records")
#         # print(gelirlerToplami)
#         # print(giderlerToplami)
#         # print(islemlerToplami)
#         result = (data, columns)
#     else:
#         result = (None, None)

#     return result
    

# @app.callback(
#     Output('datatable', 'style_data_conditional'),
#     [Input('datatable', 'selected_columns')]
# )
# def update_styles(selected_columns):
#     return [{
#         'if': { 'column_id': i },
#         'background_color': '#D2F3FF'
#     } for i in selected_columns]


if __name__ == "__main__":
    app.run_server(debug=True)