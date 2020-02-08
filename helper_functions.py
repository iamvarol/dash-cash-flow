from datetime import datetime
import datetime as dt
from dateutil import relativedelta
import plotly_express as px
import numpy as np
import matplotlib.colors as mcolors
import pandas as pd




def make_marks_time_slider(mini, maxi):
    """
    A helper function to generate a dictionary that should look something like:
    {1420066800: '2015', 1427839200: 'Q2', 1435701600: 'Q3', 1443650400: 'Q4',
    1451602800: '2016', 1459461600: 'Q2', 1467324000: 'Q3', 1475272800: 'Q4',
     1483225200: '2017', 1490997600: 'Q2', 1498860000: 'Q3', 1506808800: 'Q4'}
    """
    step = relativedelta.relativedelta(months=+1)
    start = datetime(year=mini.year, month=1, day=1)
    end = datetime(year=maxi.year, month=maxi.month, day=30)
    if (end.month>10):
        end = datetime(year=maxi.year+1, month=1, day=1)
    ret = {}

    current = start
    while current <= end:
        current_str = int(current.timestamp())
        if current.month == 1:
            ret[current_str] = {
                "label": str(current.year),
                "style": {"font-weight": "bold"},
            }
        elif current.month == 4:
            ret[current_str] = {
                "label": "Q2",
                "style": {"font-weight": "lighter", "font-size": 7},
            }
        elif current.month == 7:
            ret[current_str] = {
                "label": "Q3",
                "style": {"font-weight": "lighter", "font-size": 7},
            }
        elif current.month == 10:
            ret[current_str] = {
                "label": "Q4",
                "style": {"font-weight": "lighter", "font-size": 7},
            }
        else:
            pass
        current += step
    # print(ret)
    return ret


def time_slider_to_date(time_values):
    """ TODO """
    min_date = datetime.fromtimestamp(time_values[0]).strftime("%c")
    max_date = datetime.fromtimestamp(time_values[1]).strftime("%c")
    print("Converted time_values: ")
    print("\tmin_date:", time_values[0], "to: ", min_date)
    print("\tmax_date:", time_values[1], "to: ", max_date)
    return [min_date, max_date]


def get_grup_count(dataframe):
    """ TODO """
    grup_counts = dataframe["Grup"].value_counts()
    values = grup_counts.keys().tolist()
    counts = grup_counts.tolist()
    return values, counts

def make_options_grup_drop(values):
    """
    Helper function to generate the data format the dropdown dash component wants
    """
    ret = []
    for value in values:
        ret.append({"label": value, "value": value})
    return ret


def calculate_grup_sample_data(dataframe, sample_size, time_values):
    """ TODO """
    print(
        "making bank_sample_data with sample_size count: %s and time_values: %s"
        % (sample_size, time_values)
    )
    if time_values is not None:
        min_date = time_values[0]
        max_date = time_values[1]
        dataframe = dataframe[
            (dataframe["timestamp"] >= min_date)
            & (dataframe["timestamp"] <= max_date)
        ]
    grup_counts = dataframe["Grup"].value_counts()
    grup_counts_sample = grup_counts[:sample_size]
    values_sample = grup_counts_sample.keys().tolist()
    counts_sample = grup_counts_sample.tolist()

    return values_sample, counts_sample

def human_format(num):
    if num == 0:
        return "0"

    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000 ** magnitude)))
    return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]


def generate_islem_tipi_histogram(start_date, end_date, dataframe):
# def generate_islem_tipi_histogram(start_date, end_date, selector, segment, kategori):

    # filtered_df = filtered_df.sort_values("Tarih").set_index("Sevk_Tarihi")[start_date:end_date]
    filtered_df = dataframe.sort_values("timestamp").set_index("timestamp")[start_date:end_date]
    
    mycolors = np.array([color for name, color in mcolors.TABLEAU_COLORS.items()])
    
    figure = px.histogram(filtered_df,
                        x = "Tarih",
                        y = 'Tutar',
                        color = 'Islem Tipi',
                        color_discrete_sequence=mycolors,
                        # [
                        #     '#EA6A47',
                        #     '#0091D5',
                        #     ],
                        # height = 400,
                        histfunc= 'sum',
                        #marginal='box',
                        )

    figure.update_layout(
        autosize=True,
        margin=dict(l=40, r=10, b=10, t=20),
        hovermode="closest",
        xaxis_title_text='Dönem', # xaxis label
        yaxis_title_text= 'Tutar', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
        )

    return figure



def generate_heatmap(start_date, end_date, dataframe, selector):
# def generate_heatmap(start_date, end_date, selector, segment, kategori):
    """
    :param: start: start date from selection.
    :param: end: end date from selection.
    """

    filtered_df = dataframe.sort_values("timestamp").set_index("timestamp")[
        start_date:end_date
    ]
    
    fark_df = pd.DataFrame(filtered_df.groupby(["Yil", "Ay"]).sum().reset_index())
    group_df = pd.DataFrame(filtered_df.groupby(["Yil", "Ay", "Islem Tipi"]).sum().reset_index())
    print("fark df :")
    print(fark_df)
    print("group df :")
    print(group_df.head(34))
    print(group_df.tail(34))
    # filtered_df = filtered_df[filtered_df["Segment"].isin(segment)& filtered_df["Kategori"].isin(kategori)]
    
    x_axis = []
    for i in range(1,13):
        x_axis.append((dt.date(2018, i, 1).strftime('%m')))

    year_list = filtered_df['Yil'].unique().tolist()
    y_axis = year_list

    month = ""
    year = ""
    
    if selector == "fark":
        hovertemplate = "<b> %{y}  %{x} <br><br> %{z} TL Tahsilat-Ödeme Farkı"
        # record = "Tutar"
        title="Fark"
    elif selector == "tahsilat":
        hovertemplate = "<b> %{y}  %{x} <br><br> %{z} TL tahsilat"
        # record = "Tutar"
        # record = group_df[group_df["Islem Tipi"]=="Tahsilat"]["Tutar"]
        title="Tahsilat Miktarı"
    else:
        hovertemplate = "<b> %{y}  %{x} <br><br> %{z} TL Ödeme"
        # record = "Tutar"
        title="Ödeme Miktarı"
        
    # Get z value : sum(number of records) based on x, y,

    z = np.zeros((len(year_list), 12))
    annotations = []

    for ind_y, yil in enumerate(y_axis):
        if selector == "fark":
            filtered_yil = fark_df[fark_df["Yil"] == yil]
        else:
            filtered_yil = group_df[group_df["Yil"] == yil]

        print(enumerate(x_axis))
        for ind_x, x_val in enumerate(x_axis):
            # print(ind_x)
            # print(x_val)
            if selector == "fark":
                sum_of_record = filtered_yil[filtered_yil["Ay"] == x_val]["Tutar"]
            elif selector == "tahsilat":
                sum_of_record = filtered_yil[(filtered_yil["Ay"] == x_val)& (filtered_yil["Islem Tipi"]=="Tahsilat")]["Tutar"]
            else:
                sum_of_record = filtered_yil[(filtered_yil["Ay"] == x_val)& (filtered_yil["Islem Tipi"]=="Ödeme")]["Tutar"]
            
            # print(sum_of_record)
            # print(sum_of_record.dtype)
            sum_of_record = np.round(sum_of_record)
            # print(sum_of_record)
            # sum_of_record = '{:,.0f}'.format(sum_of_record)
            # sum_of_record = f'{sum_of_record:.0f}'
            z[ind_y][ind_x] = sum_of_record
            # print(z[ind_y][ind_x])

            annotation_dict = dict(
                showarrow=False,
                text="<b>" + str(z[ind_y][ind_x]) + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=yil,
                font=dict(family="sans-serif"),
            )
            print(annotation_dict)

            annotations.append(annotation_dict)


    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=True,
            colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
            #colorscale=[[0, "#fdffca"], [1, "#02f502"]],
            #colorscale='Jet',
        )
    ]

    layout = dict(
        title=f"Ay-Yıl Bazında {title}",
        margin=dict(l=70, b=20, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="sans-serif"),
        annotations=annotations,
        xaxis=dict(
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(
            side="left",
            ticks="",
            tickfont=dict(family="sans-serif"),
            ticksuffix=" "
        ),
        hovermode="closest",
        showlegend=False,
    )
    return {"data": data, "layout": layout}



if __name__ == "__main__":
    pass