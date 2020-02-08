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
import db_util
import helper_functions
import preprocessing

EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
LOGO = "http://www.optimateknoloji.com.tr/images/logo@2x.png"
MAIN_PAGE = "http://www.optimateknoloji.com.tr/"
DB_DF = db_util.get_data()
TABLE_SELECTED_COLUMNS = [
    'Tarih', 
    'Grup', 
    'Tutar', 
    'Islem Tipi', 
    'Aciklama1', 
    'HesapAdi',
    ]

GLOBAL_DF = preprocessing.preprocess(DB_DF)

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
                        dbc.NavbarBrand("Detaylı Nakit Akışı", className="ml-2")
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
        html.Label("Select time frame", className="lead"),
        html.Div(dcc.RangeSlider(id="time-window-slider"), style={"marginTop": 30}),
        html.Label("Grup tipini seçiniz", style={"marginTop": 50}, className="lead"),
        dcc.Dropdown(
            id="grup-drop", 
            clearable=False, 
            style={"marginBottom": 50, "font-size": 12},
            multi=True,
        ),
        
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
                dbc.CardImg(src="http://www.pngmart.com/files/7/Income-PNG-Free-Download.png", top=True,  style={"height":"200px"}),
                dbc.CardBody(
                    [
                        html.H6("Gelirler Toplamı", className="card-title"),
                        html.H4(id="gelirlerText", className="card-text",style={"color": "green"}),
                        ]
                    ),
                ],
            style={"width": "15rem"},
            ),
            dbc.Card(
            [
                dbc.CardImg(src="https://cdn1.iconfinder.com/data/icons/estate-planning-glyph/64/expense-expenditure-consumption-outgoings-salary-512.png", top=True,  style={"height":"200px"}),
                dbc.CardBody(
                    [
                        html.H6("Giderler Toplamı", className="card-title"),
                        html.H4(id="giderlerText", className="card-text",style={"color": "red"}),
                        ]
                    ),
                ],
            style={"width": "15rem"},
            ),
            dbc.Card(
            [
                dbc.CardImg(src="https://cdn.onlinewebfonts.com/svg/img_457131.png", top=True,  style={"height":"200px"}),
                dbc.CardBody(
                    [
                        html.H6("Kazanç", className="card-title"),
                        html.H4(id="ciroText", className="card-text",style={"color": "green"}),
                        ]
                    ),
                ],
            style={"width": "15rem"},
            ),
            # dbc.Card(
            # [
            #     dbc.CardImg(src="https://pngimage.net/wp-content/uploads/2018/06/money-transfer-png-7.png", top=True,  style={"height":"200px"}),
            #     dbc.CardBody(
            #         [
            #             html.H6("Toplam İşlem", className="card-title"),
            #             html.H4(id="islemlerText", className="card-text",style={"color": "blue"}),
            #             ]
            #         ),
            #     ],
            # style={"width": "15rem"},
            # ),
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
        # style_cell_conditional=[
        #     {
        #         "if": {"column_id": "Text"},
        #         "textAlign": "left",
        #         "whiteSpace": "normal",
        #         "height": "auto",
        #         "min-width": "50%",
        #         }
        #     ],
        style_data_conditional=[
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#75CAEB',
            'color': 'yellow'
            },
        ],
        # style_cell={
        #     "padding": "16px",
        #     "whiteSpace": "normal",
        #     "height": "auto",
        #     "max-width": "0",
        #     },
        style_header={
        'backgroundColor': '#033C73',
        'fontWeight': 'bold',
        'color': 'white'
        },
        # style_data={"whiteSpace": "normal", "height": "auto"},
        editable=True,
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
    dbc.CardHeader(html.H5("İşlemlerin Tablo Gösterimi")),
    dbc.CardBody(
        [
            # html.P(
            #     "Tablo Gösterimi",
            #     className="mb-0",
            # ),
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
    
    dbc.CardHeader(html.H5("İşlem Sayılarının Dağılımı")),
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
                dbc.Col(LEFT_COLUMN, md=4, align="center"),
                dbc.Col(CARDS_PLOT, md=8,),
                # dbc.Col(dbc.Card(GRUPS_PLOT), md=8),
            ],
            style={"marginTop": 20},
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






SERVER = flask.Flask(__name__)
APP = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], server=SERVER)
APP.layout = html.Div(children=[NAVBAR, BODY])











"""
#  Callbacks
"""



@APP.callback(
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



@APP.callback(
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


@APP.callback(
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

@APP.callback(
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
        
        # print('After group by')
        # print(df.head())
        # print(df.tail())
        
        gelirlerToplami = df.iat[0,1]
        gelirlerToplami = '{:,.2f}'.format(gelirlerToplami)
        
        giderlerToplami = df.iat[1,1]
        giderlerToplami = '{:,.2f}'.format(giderlerToplami)
         
        ciro  = df.iat[0,1] + df.iat[1,1]
        ciro = '{:,.0f}'.format(ciro)
        
        # if fark<0:
        #     color = "red"
        # else:
        #     color = "green"
        # style={"color": color}
        
        
        # islemlerToplami  = len(filtered_df.index)
        # islemlerToplami = '{:,.0f}'.format(islemlerToplami)
        
        # print(gelirlerToplami)
        # print(giderlerToplami)
        # print(islemlerToplami)
        result = gelirlerToplami, giderlerToplami, ciro
    else:
        result = "no result", "no result", "no result"

    return result

@APP.callback(
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

@APP.callback(
    Output("heatmap", "figure"),
    [
        Input("time-window-slider", "value"),
        Input("selector", "value"),
    ],
)
def update_heatmap(time_values, selector_value):
    #print("\t time values first heatmap : type ", type(time_values))
    if time_values is not None:
    # Return to original hm(no colored annotation) by resetting
        min_date, max_date = helper_functions.time_slider_to_date(time_values)
        return helper_functions.generate_heatmap(min_date, max_date, GLOBAL_DF, selector_value)

    return {"data":[]}

# @APP.callback(
#     Output("grup-drop", "value"), 
#     [Input("grup-sample", "clickData")],
#     )
# def update_grup_drop_on_click(value):
#     """ TODO """
#     if value is not None:
#         selected_grup = value["points"][0]["x"]
#         return selected_grup
#     return grup_list

# @APP.callback(
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
    

# @APP.callback(
#     Output('datatable', 'style_data_conditional'),
#     [Input('datatable', 'selected_columns')]
# )
# def update_styles(selected_columns):
#     return [{
#         'if': { 'column_id': i },
#         'background_color': '#D2F3FF'
#     } for i in selected_columns]


if __name__ == "__main__":
    APP.run_server(debug=True)