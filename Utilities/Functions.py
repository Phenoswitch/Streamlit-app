import streamlit as st
import numpy as np
from streamlit_extras.app_logo import add_logo
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
import fitz
from tika import parser 


# @st.cache_data(experimental_allow_widgets=True) 
def table_selector_datetime(df, list_select,slider_lim):
    df_with_selections = df.copy()

    if not list_select:
        df_with_selections.insert(0, "Select", True)
        df_with_selections['Select'] = (df_with_selections['Date'] <= slider_lim[0][1]) & (df_with_selections['Date'] >= slider_lim[0][0])

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

# @st.cache_data(experimental_allow_widgets=True) 
def sliders_datetime(slide_min,slide_max):
    slider = st.slider(
            "Select a date range before using the table checkboxes",
            min_value= slide_min, 
            max_value= slide_max,
            value= (slide_min.to_pydatetime(), slide_max.to_pydatetime()),
            step=timedelta(days=1),
            format='DD/MM/YYYY'
        )
    return slider

def figure_detector_zeno(chart_data):
    fig, ax = plt.subplots()

    line = ax.plot(chart_data['Date'], chart_data['CEM voltage (V)'] , linestyle='-', color='#00c0f3', label='CEM voltage (V)')
    line += ax.plot(chart_data['Date'], chart_data['Notify Zef (2700V)'] , linestyle='-', color='yellow', label='Notify Zef (2700V)')
    line += ax.plot(chart_data['Date'], chart_data['To replace (2750V)'] , linestyle='-', color='red', label='To replace (2750V)')
    line += ax.plot(chart_data['Date'], chart_data['Maximum (2850V)'] , linestyle='-', color='black', label='Maximum (2850V)')

    # ax.set_xlabel("Date")
    ax.set_ylabel("CEM voltage (V)")
    ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, handles=line,handlelength=0.5, loc='center left', bbox_to_anchor=(0.87, 0.5),handletextpad=-0.2,  fontsize='small')

    dtFmt = mdates.DateFormatter('%Y-%b') # define the formatting
    plt.gca().xaxis.set_major_formatter(dtFmt) 
    # show every 12th tick on x axes
    # plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.xticks(rotation=90, fontweight='bold',  fontsize='x-small')
    plt.tight_layout()

    return fig

volta = []
def fetch_detector_zeno(search_dir_volt):
    for (root,dirs,files) in os.walk(search_dir_volt, topdown=True):
            for filename in files:
                if filename.endswith(".xps"):
                    f = os.path.join(root, filename)
                    try:
                        doc = fitz.open(f)
                        page = doc[0] #Only page 2 in revelate
                        text = page.get_text().split('\n')

                        if 'Positive Detector Optimization' in text:
                            for i in range(len(doc)):
                                page = doc[i] #Only page 2 in revelate
                                text = page.get_text().split('\n')

                                if 'Instrument Tuning Report' in text:
                                    acq_time = text[text.index('Instrument Tuning Report')+1]

                                    # input_format = "%Y-%m-%d %I:%M %p"  # For "2022-08-17 3:52 PM"
                                    # output_format = "%Y-%m-%d %H:%M:%S"  # For "2022-08-17 15:52:00"

                                    acq_time = datetime.strptime(acq_time, "%Y-%m-%d %I:%M %p")
                                    # acq_time = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
                                    # datetime.strptime(slide_min, "%Y-%m-%d %H:%M:%S")
                                    # print(acq_time)

                                text = [item.split(":") for item in text]
                                text = [item for sublist in text for item in sublist]

                                if 'Final detector voltage' in text:
                                    volt = float(text[text.index('Final detector voltage')+1][:-1])
                                    break

                        volta.append(np.array([acq_time, volt]))

                    except:
                        print(f'Error opening file : {filename}')

    df = pd.DataFrame(volta)

    current_val = int(round(float(volta[-1][1])))

    df.rename(columns={0: 'Date', 1: 'CEM voltage (V)'}, inplace=True)
    # df.rename(columns={0: 'Date', 1: f'CEM (V) ({current_val}V)'}, inplace=True)
    df = df.sort_values(by ='Date')

    # df[f'CEM (V) ({current_val}V)']=df[f'CEM (V) ({current_val}V)'].astype(float)

    return df