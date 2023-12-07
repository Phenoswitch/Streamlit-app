import streamlit as st
import numpy as np
from streamlit_extras.app_logo import add_logo
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
import fitz
from PyPDF2 import PdfReader


#imports all CONSTANTES in Constantes.py
from Constantes import *
# import all packages in Imports
from Imports import *



"""Create a table for datetime with checkboxes selector"""
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

"""Create a table for datetime with checkboxes selector"""
def table_selector(df, list_select):
    df_with_selections = df.copy()

    if not list_select:
        df_with_selections.insert(0, "Select", True)

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

"""Create a slider for datetime"""
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

"""Creates the plot for the detector voltage of the 7600"""
def figure_detector(data):
    fig, ax = plt.subplots()

    line = ax.plot(data['Date'], data['CEM voltage (V)'] , linestyle='-', color='#00c0f3', label='CEM voltage (V)')
    line += ax.plot(data['Date'], data.iloc[:, 2] , linestyle='-', color='yellow', label= data.columns[2])
    line += ax.plot(data['Date'], data.iloc[:, 3] , linestyle='-', color='red', label= data.columns[3])
    line += ax.plot(data['Date'], data.iloc[:, 4] , linestyle='-', color='black', label= data.columns[4])

    # ax.set_xlabel("Date")
    ax.set_ylabel("CEM voltage (V)")
    ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, handles=line,handlelength=0.5, loc='center left', bbox_to_anchor=(0.87, 0.5),handletextpad=-0.2,  fontsize='small')

    dtFmt = mdates.DateFormatter('%Y-%b') # define the formatting
    plt.gca().xaxis.set_major_formatter(dtFmt) 
    # plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.xticks(rotation=90, fontweight='bold',  fontsize='x-small')
    plt.tight_layout()

    return fig

"""Fetches the detector voltage in all .xps file in the specified path for the 7600"""
@st.cache_data(experimental_allow_widgets=True) 
def fetch_detector_zeno(search_dir_volt):
    volta_7600 = []
    print('Fetching Zeno detector voltage')

    for (root,dirs,files) in os.walk(search_dir_volt, topdown=True):
            for filename in files:
                if filename.endswith(".xps"):
                    f = os.path.join(root, filename)
                    try:
                        doc = fitz.open(f)
                        page = doc[0] 
                        text = page.get_text().split('\n')

                        if 'Positive Detector Optimization' in text:
                            for i in range(len(doc)):
                                page = doc[i] #Only page 2 in revelate
                                text = page.get_text().split('\n')

                                if 'Instrument Tuning Report' in text:
                                    acq_time = text[text.index('Instrument Tuning Report')+1]
                                    acq_time = datetime.strptime(acq_time, "%Y-%m-%d %I:%M %p")

                                text = [item.split(":") for item in text]
                                text = [item for sublist in text for item in sublist]

                                if 'Final detector voltage' in text:
                                    volt = float(text[text.index('Final detector voltage')+1][:-1])
                                    break
                        volta_7600.append(np.array([acq_time, volt]))
                    except:
                        print(f'Error opening file : {filename}')

    df = pd.DataFrame(volta_7600)
    # current_val = int(round(float(volta[-1][1])))

    df.rename(columns={0: 'Date', 1: 'CEM voltage (V)'}, inplace=True)
    df = df.sort_values(by ='Date')

    ### Temporary fix because multiple Final detector voltage in same xps file ??
    df = df.drop_duplicates(subset=['Date','CEM voltage (V)'])

    return df

"""Fetches the detector voltage in all .pdf file in the specified path for the 6600"""
@st.cache_data(experimental_allow_widgets=True) 
def fetch_detector_6600(search_dir_volt):
    volta = []
    for (root,dirs,files) in os.walk(search_dir_volt, topdown=True):
        for filename in files:
            if filename.endswith(".pdf"):
                try:
                    f = os.path.join(root, filename)
                        
                    reader = PdfReader(f)
                    number_of_pages = len(reader.pages)
                    text = ''
                    for page_number in range(number_of_pages):
                        page = reader.pages[page_number]
                        text += page.extract_text()

                    text = text.split('\n')

                    try:
                        acq_time = datetime.strptime(text[0][:-2], "%Y-%m-%d at %H:%M")
                    except:
                        acq_time = 'error'
                    
                    for i in range(len(text)):
                        if 'Optimal Detector voltage:' in text[i]:
                            volt = int(text[i][-6:-2])
                            volta.append(np.array([acq_time, volt]))
                        # break            
                except:
                    print(f'Error opening file : {filename}')

    df = pd.DataFrame(volta)
    df.rename(columns={0: 'Date', 1: 'CEM voltage (V)'}, inplace=True)
    df = df.sort_values(by ='Date')

    ### Temporary fix because multiple Final detector voltage in same xps file ??
    df = df.drop_duplicates(subset=['Date','CEM voltage (V)'])

    return df

def table_MS_qualification_TOF_6600(current_QC_TOF_values):
    current_QC_TOF_values = [current_QC_TOF_values[current_QC_TOF_values['Tag'] == 'ITC00']['Resolution'].values[0], current_QC_TOF_values[current_QC_TOF_values['Tag'] == 'ITC00']['Intensity sum'].values[0], current_QC_TOF_values[current_QC_TOF_values['Tag'] == 'ITC01']['Resolution'].values[0], current_QC_TOF_values[current_QC_TOF_values['Tag'] == 'ITC01']['Intensity sum'].values[0]] 

    #Creates the multiindex df to have merged column headers in the table
    columns_MS = pd.MultiIndex.from_tuples([
        ('', 'Mass (Da)'),
        ('TOF MS+ ITC 00', 'Resolution'),
        ('TOF MS+ ITC 00', 'Intensity Sum'),
        ('TOF MS+ ITC 01', 'Resolution'),
        ('TOF MS+ ITC 01', 'Intensity Sum')
    ])

    # Create the data for the DataFrame
    data_MS = [['Tuning Sol 829.54', MS_QUALIFICATIONS_ITC00_RESOLUTION, f'{float(MS_QUALIFICATIONS_ITC00_INTENSITY):.1e}' , MS_QUALIFICATIONS_ITC01_RESOLUTION, f'{float(MS_QUALIFICATIONS_ITC01_INTENSITY):.1e}']]
    df_MS_qualification = pd.DataFrame(data_MS, columns=columns_MS)
 
    #Here is to have green for values over the thresholds and red if under in the rendered table
    MS_QUALIFICATIONS_TOF_COLOR = []
    for i in range(len(current_QC_TOF_values)):
        if current_QC_TOF_values[i] >= MS_QUALIFICATIONS_TOFQC_ITC00[i]:
            MS_QUALIFICATIONS_TOF_COLOR.append("#00ff00")
        else:
            MS_QUALIFICATIONS_TOF_COLOR.append("#ff0000")

    new_row_data = ['Current value', f'<b><FONT COLOR={MS_QUALIFICATIONS_TOF_COLOR[0]}>{int(current_QC_TOF_values[0])}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_TOF_COLOR[1]}>{float(current_QC_TOF_values[1]):.1e}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_TOF_COLOR[2]}>{int(current_QC_TOF_values[2])}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_TOF_COLOR[3]}>{float(current_QC_TOF_values[3]):.1e}</FONT></b>']
    df_MS_qualification.loc['Current value'] = new_row_data

    #Remove the index 0 from the render
    df_MS_qualification.index = ['', '']
    #Centers the text in the df for beauty
    df_MS_qualification = df_MS_qualification.style.set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center')]
    }, {
        'selector': 'td',
        'props': [('text-align', 'center')]
    }])

    return(df_MS_qualification)

def table_MS_qualification_MSMS_6600(current_QC_MSMS_values):
    current_QC_MSMS_values = [current_QC_MSMS_values[current_QC_MSMS_values['Tag'] == 'HR']['Resolution'].values[0], current_QC_MSMS_values[current_QC_MSMS_values['Tag'] == 'HR']['Intensity sum'].values[0], current_QC_MSMS_values[current_QC_MSMS_values['Tag'] == 'HS']['Resolution'].values[0], current_QC_MSMS_values[current_QC_MSMS_values['Tag'] == 'HS']['Intensity sum'].values[0], current_QC_MSMS_values[current_QC_MSMS_values['Tag'] == 'HS']['Intensity sum'].values[0]/current_QC_MSMS_values[current_QC_MSMS_values['Tag'] == 'HR']['Intensity sum'].values[0]] 


    #Creates the multiindex df to have merged column headers in the table
    columns_MSMS = pd.MultiIndex.from_tuples([
        ('', 'Mass (Da)'),
        ('MS/MS+ HR ITC 10', 'Resolution'),
        ('MS/MS+ HR ITC 10', 'Intensity Sum'),
        ('MS/MS+ HS ITC 10', 'Resolution'),
        ('MS/MS+ HS ITC 10', 'Intensity Sum'), 
        ('HS/HR ITC 10', 'Intensity gain')
    ])

    # Create the data for the DataFrame
    data_MSMS = [['Tuning Sol 829>381', MS_QUALIFICATIONS_HR_RESOLUTION, MS_QUALIFICATIONS_HR_INTENSITY , MS_QUALIFICATIONS_HS_RESOLUTION, f'{float(MS_QUALIFICATIONS_HS_INTENSITY):.1e}', f'{round(MS_QUALIFICATIONS_HSHR_RATIO,1)}']]
    df_MSMS_qualification = pd.DataFrame(data_MSMS, columns=columns_MSMS)

    MSMS_QUALIFICATIONS_TOF_COLOR = []
    for i in range(len(current_QC_MSMS_values)):
        if current_QC_MSMS_values[i] >= MS_QUALIFICATIONS_MSMSQC_ITC00[i]:
            MSMS_QUALIFICATIONS_TOF_COLOR.append("#00ff00")
        else:
            MSMS_QUALIFICATIONS_TOF_COLOR.append("#ff0000")


    new_row_data_MSMS = ['Current value', f'<b><FONT COLOR={MSMS_QUALIFICATIONS_TOF_COLOR[0]}>{int(current_QC_MSMS_values[0])}</FONT></b>', f'<b><FONT COLOR={MSMS_QUALIFICATIONS_TOF_COLOR[1]}>{int(current_QC_MSMS_values[1])}</FONT></b>', f'<b><FONT COLOR={MSMS_QUALIFICATIONS_TOF_COLOR[2]}>{int(current_QC_MSMS_values[2])}</FONT></b>', f'<b><FONT COLOR={MSMS_QUALIFICATIONS_TOF_COLOR[3]}>{float(current_QC_MSMS_values[3]):.1e}</FONT></b>', f'<b><FONT COLOR={MSMS_QUALIFICATIONS_TOF_COLOR[4]}>{round(current_QC_MSMS_values[4],1)}</FONT></b>']
    df_MSMS_qualification.loc['Current value'] = new_row_data_MSMS

    df_MSMS_qualification.index = ['', '']

    df_MSMS_qualification = df_MSMS_qualification.style.set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center')]
    }, {
        'selector': 'td',
        'props': [('text-align', 'center')]
    }])

    return df_MSMS_qualification


"""Creates the pie chart for the disk space of drives"""
def figure_disk_space(path, skipcolor):
    labels = 'Free space (GB)', 'Total space (GB)'

    total, used, free = shutil.disk_usage(path)
    sizes = [free/ (2**30), total/ (2**30)]

    if skipcolor == False:

        if sizes[0] < 50 :
            color = ['red', '#f4950d'] 
        else: 
            color = ['#00b5da', '#f4950d']
    else:
        color = ['#00b5da', '#f4950d']

    explode = (0, 0.1)  
    fig1, ax1 = plt.subplots()
    total = sum(sizes)
    ax1.pie(sizes, explode=explode, labels=labels,  autopct=lambda p: '{:.0f}'.format(p * total / 100),
            shadow=True, startangle=90, wedgeprops=dict(width=.5), textprops={'fontsize':10}, colors=color)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig1

@st.cache_data(experimental_allow_widgets=True) 
def fetch_MSQC_6600(MS_QC_path):
    MS_QC_timestamp = []
    df_list = []

    for folder_path, _, files in os.walk(MS_QC_path):
        #Filters QC type by tags
        for TAGS in range(len(MS_QC_TAGS)):
            for file in files:
                if file.endswith('.txt') and MS_QC_TAGS[TAGS] in file and 'NEG' not in file:
                    print(file)

                    file_path = os.path.join(folder_path, file)
                    print(file_path)

                    MS_QC_timestamp  = file.split('_')[0]

                    with open(file_path, 'r') as file:
                        content = file.read()
                        content = content.split('\n')
                        data_split = [line.split('\t') for line in content]

                        try:
                            df = pd.DataFrame(data_split, columns=['Mz found (Da)', 'Resolution', 'Intensity sum'])
                            df['Mz found (Da)'] = pd.to_numeric(df['Mz found (Da)'])
                            df['Resolution'] = pd.to_numeric(df['Resolution'])
                            df['Intensity sum'] = pd.to_numeric(df['Intensity sum'])
                            closest_index = (df['Mz found (Da)'] - MS_QC_TARGETS[TAGS]).abs().idxmin()
                            closest_row = df.iloc[closest_index]

                            closest_row["Tag"] = MS_QC_TAGS[TAGS]
                            closest_row['Timestamp'] = MS_QC_timestamp

                            df_list.append(closest_row)
                        except:
                            print(f'Failed to compile {file}')


    result_df = pd.concat(df_list, ignore_index=True, axis=1).T

    result_df.to_excel(r"C:\Users\6600plus\Downloads\output.xlsx")

    result_df['Timestamp'] = pd.to_datetime(result_df['Timestamp'])  # Convert to datetime
    result_df = result_df.sort_values(by ='Timestamp') #Sorts by timestamp

    #Does the mean of  n1, n2 
    averaged_df = result_df.groupby(['Timestamp', 'Tag']).mean()
    averaged_df = averaged_df.reset_index()

    return averaged_df

def figure_MSQC_6600(averaged_df):
    #Dropdown to select between Intensity sum and resolution
    dropdown, plot = st.columns(spec = [0.25,0.75])
    with dropdown:
        option = st.selectbox(
            'Data to be plotted',
            ('Intensity sum', 'Resolution'))

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex=True, figsize=(10, 8))

    ax1.plot(averaged_df[averaged_df['Tag'] == 'ITC00']['Timestamp'],averaged_df[averaged_df['Tag'] == 'ITC00'][option] , linestyle='-', color='k')
    ax1.plot(averaged_df[averaged_df['Tag'] == 'ITC00']['Timestamp'],[MS_QUALIFICATIONS_TOF_QC_ITC00[option]]*averaged_df[averaged_df['Tag'] == 'ITC00']['Timestamp'].shape[0]  , linestyle='-', color='r')

    ax2.plot(averaged_df[averaged_df['Tag'] == 'ITC01']['Timestamp'],averaged_df[averaged_df['Tag'] == 'ITC01'][option] , linestyle='-', color='k')
    ax2.plot(averaged_df[averaged_df['Tag'] == 'ITC01']['Timestamp'],[MS_QUALIFICATIONS_TOF_QC_ITC01[option]]*averaged_df[averaged_df['Tag'] == 'ITC01']['Timestamp'].shape[0]  , linestyle='-', color='r')

    ax3.plot(averaged_df[averaged_df['Tag'] == 'HS']['Timestamp'],averaged_df[averaged_df['Tag'] == 'HS'][option] , linestyle='-', color='k')
    ax3.plot(averaged_df[averaged_df['Tag'] == 'HS']['Timestamp'],[MS_QUALIFICATIONS_MSMS_QC_HS[option]]*averaged_df[averaged_df['Tag'] == 'HS']['Timestamp'].shape[0]  , linestyle='-', color='r')

    ax4.plot(averaged_df[averaged_df['Tag'] == 'HR']['Timestamp'],averaged_df[averaged_df['Tag'] == 'HR'][option] , linestyle='-', color='k')
    ax4.plot(averaged_df[averaged_df['Tag'] == 'HR']['Timestamp'],[MS_QUALIFICATIONS_MSMS_QC_HR[option]]*averaged_df[averaged_df['Tag'] == 'HR']['Timestamp'].shape[0]  , linestyle='-', color='r')

    ax5.plot(averaged_df[averaged_df['Tag'] == 'HR']['Timestamp'],averaged_df[averaged_df['Tag'] == 'HS']['Intensity sum'].values/averaged_df[averaged_df['Tag'] == 'HR']['Intensity sum'].values , linestyle='-', color='k')
    ax5.plot(averaged_df[averaged_df['Tag'] == 'HR']['Timestamp'],[MS_QUALIFICATIONS_MSMS_QC_HR['Ratio']]*averaged_df[averaged_df['Tag'] == 'HR']['Timestamp'].shape[0]  , linestyle='-', color='r')

    # Sets titles for each subplots
    ax1.set_title('TOF MS+ ITC 00')
    ax2.set_title('TOF MS+ ITC 01')
    ax3.set_title('MS/MS+ HS ITC 10')
    ax4.set_title('MS/MS+ HR ITC 10')
    ax5.set_title('HS/HR ITC 10 intensity gain')

    plt.tight_layout()

    return fig

