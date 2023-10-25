import streamlit as st
import numpy as np
from streamlit_extras.app_logo import add_logo
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import matplotlib.dates as mdates
import matplotlib
import random
import altair as alt
from datetime import datetime, timedelta
import os
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d")

matplotlib.rcParams.update({'font.size': 20, 'xtick.color' : 'black', 'axes.labelcolor': 'black'})
st.set_page_config(layout="wide")

cwd = os.path.dirname(__file__)


def tables(dataframe):
    gd = GridOptionsBuilder.from_dataframe(dataframe)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()

    grid_table = AgGrid(dataframe, gridOptions=gridoptions, use_container_width = True,
                        update_mode=GridUpdateMode.SELECTION_CHANGED)
    
    

add_logo("https://allumiqs.com/wp-content/uploads/2022/06/AG-Icon-238x232.png", height=200) #TODO: move this to a utils module

st.title('TTOF 7600 Quality Dashboard')

st.subheader("""
MS qualifications""")
st.info(f'Run this section to show MS qualifications and thresholds.')
st.warning('Work in progress')

st.subheader("""
LC-MS calibrations""")
st.info(f'Run this section to show all LC-MS calibration informations and trends.')
st.warning('Work in progress')

st.subheader("""
Detector voltage""")
st.info(f'Run this section to show the final detector voltage reported after each Detector Optimization tuning.')
st.warning('Work in progress')


# Sample data
random_numbers = [random.randint(2000, 2800) for _ in range(30)]  # Change 10 to the desired number of random numbers
chart_data = pd.DataFrame({'Detector voltage (V)': random_numbers})

start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)
random_dates = [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(30)]



chart_data['Timelapse'] = random_dates
chart_data['Timelapse'] = pd.to_datetime(chart_data['Timelapse'], format='%d/%m/%y')
slide_min, slide_max = chart_data['Timelapse'].agg(['min', 'max'])

chart_data = chart_data.sort_values(by='Timelapse')

# Thresholds of voltage
chart_data['Notify Zef (2700V)'] = 2700
chart_data['To replace (2750V)'] = 2750
chart_data['Maximum (2850V)'] = 2850

# Creates the figure to add in App
fig, ax = plt.subplots()

line = ax.plot(chart_data['Timelapse'], chart_data['Detector voltage (V)'] , linestyle='-', color='#00c0f3', label='Detector voltage (V)')
line += ax.plot(chart_data['Timelapse'], chart_data['Notify Zef (2700V)'] , linestyle='-', color='yellow', label='Notify Zef (2700V)')
line += ax.plot(chart_data['Timelapse'], chart_data['To replace (2750V)'] , linestyle='-', color='red', label='To replace (2750V)')
line += ax.plot(chart_data['Timelapse'], chart_data['Maximum (2850V)'] , linestyle='-', color='black', label='Maximum (2850V)')

# ax.set_xlabel("Date")
ax.set_ylabel("Detector voltage (V)")
ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, handles=line,handlelength=0.5, loc='center left', bbox_to_anchor=(0.87, 0.5),handletextpad=-0.2,  fontsize='small')

dtFmt = mdates.DateFormatter('%Y-%b') # define the formatting
plt.gca().xaxis.set_major_formatter(dtFmt) 
# show every 12th tick on x axes
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.xticks(rotation=90, fontweight='bold',  fontsize='x-small')

plt.tight_layout()
#Adds the figure

data_container = st.container()

with data_container:
    table, plot = st.columns(spec = [0.2,0.8])
    with table:
        tables(chart_data.drop(['Notify Zef (2700V)', 'To replace (2750V)', 'Maximum (2850V)'], axis=1))
        # @st.cache
        # df = chart_data.drop(['Notify Zef (2700V)', 'To replace (2750V)', 'Maximum (2850V)'], axis=1)
        # gd = GridOptionsBuilder.from_dataframe(df)
        # gd.configure_selection(selection_mode='multiple', use_checkbox=True)
        # gridoptions = gd.build()

        # grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
        #                     update_mode=GridUpdateMode.SELECTION_CHANGED)
            
    # st.dataframe(chart_data.drop(['Notify Zef (2700V)', 'To replace (2750V)', 'Maximum (2850V)'], axis=1), hide_index=True, use_container_width=True)
    
    with plot:
        start_date = datetime(2020, 1, 1)

 
        selected_date_range = st.slider(
            "Select a date range",
            min_value=slide_min,
            max_value=slide_max,
            value= (slide_min.to_pydatetime(), slide_max.to_pydatetime()),
            # step=timedelta(days=1),
            format='DD/MM/YY'
        )
        st.plotly_chart(fig, use_container_width = True, theme=None)



### Notes section
path_components = cwd.split(os.path.sep)
new_path_components = path_components[:-1]
notes_dir = os.path.sep.join(new_path_components)


with open(os.path.join(notes_dir,'Notes\\notes_zeno_detector.txt'), 'a') as file:
    input_notes_detector = st.text_input(label ='Input any comments or notes') 
    if input_notes_detector:
        file.write('\n' + input_notes_detector + ' ('+ current_date +')  ')
    
    # close()
with open(os.path.join(notes_dir,'Notes\\notes_zeno_detector.txt'), 'r') as file:
    notes_detector = file.read()       


st.markdown(notes_detector)