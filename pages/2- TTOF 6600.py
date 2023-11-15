import os
import sys
import locale


### Get relative subfolder path
subdirectory_folder_path = os.path.dirname(__file__)

### imports all variables in Variables.py
sys.path.append(os.path.join(subdirectory_folder_path, '..', 'Utilities'))
#imports all CONSTANTES in Constantes.py
from Constantes import *
#imports all FUNCTIONS in Functions.py
from Functions import *
# import all packages in Imports
from Imports import *

### Now time to be used in script
current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d")

### To be run once to update matplotlib default parameters
matplotlib.rcParams.update({'font.size': 14, 'xtick.color' : 'black', 'axes.labelcolor': 'black'})
st.set_page_config(layout="wide")

locale.setlocale(locale.LC_ALL, '')

#""" Setup TTOF 7600 Web page """

add_logo("https://allumiqs.com/wp-content/uploads/2022/06/AG-Icon-238x232.png", height=200) #TODO: move this to a utils module

st.title('TTOF 6600 Quality Dashboard')

st.subheader("""
Computer space""")
st.info(f'This section shows the available space on each disk.')

data_container = st.container()
with data_container:
    plot1, plot2 = st.columns(2)
    with plot1:
        st.subheader('SYSTEM (D:)')
        st.pyplot(figure_disk_space(r'\\Desktop-v8lih84\d', skipcolor = False))
    with plot2:
        st.subheader('DATA (C:)')
        st.pyplot(figure_disk_space(r'\\Desktop-v8lih84\c', skipcolor= True))


st.subheader("""
MS qualifications""")
st.info(r'Run this section to show MS qualifications and thresholds. This opens and extract the MS qualifications saved in the DESKTOP-V8LIH84\Users\6600\Desktop\QC 6600 Report\QC 30MCA 6600_A Compiler\2023 folder.')
st.write('The 6600 TTOF specifications listed here are the in-house Allumiqs thresholds for a positive tuning performed with the iPD1-CsI homemade tuning solution.')

MS_QC_path = r'\\DESKTOP-V8LIH84\Users\6600\Desktop\QC 6600 Report\QC 30MCA 6600_A Compiler\2023'

MS_QC_values = fetch_MSQC_6600(MS_QC_path)

current_values = MS_QC_values[MS_QC_values['Timestamp'] == MS_QC_values['Timestamp'].iloc[-1]]

""" Qualifications in TOF MS """
desired_tags = ['ITC00', 'ITC01']
current_QC_TOF_values = current_values[current_values['Tag'].isin(desired_tags)]

#Creates the formated table with thresholds 
df_MS_qualification_TOF =  table_MS_qualification_TOF_6600(current_QC_TOF_values)
#Renders the formated df to Streamlit
st.write(df_MS_qualification_TOF.to_html(), unsafe_allow_html= True)

""" Qualifications in TOF MSMS """
desired_tags = ['HR', 'HS']
current_QC_MSMS_values = current_values[current_values['Tag'].isin(desired_tags)]

#Creates the formated table with thresholds 
df_MSMS_qualification =  table_MS_qualification_MSMS_6600(current_QC_MSMS_values)
#Renders the formated df to Streamlit
st.write(df_MSMS_qualification.to_html(), unsafe_allow_html= True)

### Creates the timeline of QC values ###
fig = figure_MSQC_6600(MS_QC_values)

st.plotly_chart(fig, use_container_width = True, theme=None)

st.subheader("""
LC-MS calibrations""")
st.info(f'Run this section to show all LC-MS calibration informations and trends.')
st.warning('Work in progress')

st.subheader("""
Detector voltage""")
st.info(f'Run this section to show the final detector voltage reported after each Instruments optimisation reports. This opens and reads all results.pdf files located in the Desktop-v8lih84\d\Analyst Data\Projects\API Instrument\Data\Instrument Optimization folder.')
st.warning('Work in progress')


#Return the detector voltage listed in the path in a dataframe
chart_data_6600 = fetch_detector_6600(r'\\Desktop-v8lih84\d\Analyst Data\Projects\API Instrument\Data\Instrument Optimization')

#Creates a slider with the min and max date fetched
slide_min, slide_max = chart_data_6600['Date'].agg(['min', 'max'])
slider_lim = sliders_datetime(slide_min,slide_max)

### Thresholds of voltage for the plot
chart_data_6600[f'Notify Provider ({DETECTOR_WARNING_6600}V)'] = DETECTOR_WARNING_6600
chart_data_6600[f'To replace ({DETECTOR_REPLACEMENT_6600}V)'] = DETECTOR_REPLACEMENT_6600
chart_data_6600[f'Maximum ({DETECTOR_MAXIMUM_6600}V)'] = DETECTOR_MAXIMUM_6600

# Creates a container to put table and plot side by side
data_container = st.container()
with data_container:
    table, plot = st.columns(spec = [0.25,0.75]) #25% window width for table and 75% width for plot
    with table:

        # Creates the table
        if 'grid_table' not in locals():
            list_select = []
        else:
            list_select = grid_table
            # print('not created')

        grid_table = table_selector_datetime(chart_data_6600.drop([f'Notify Provider ({DETECTOR_WARNING_6600}V)',f'To replace ({DETECTOR_REPLACEMENT_6600}V)', f'Maximum ({DETECTOR_MAXIMUM_6600}V)'], axis=1), list_select, [slider_lim])

        list_select = grid_table
        # print(list_select)

    with plot:
        ### Filters the data based on checked table rows
        chart_data_6600 = chart_data_6600[chart_data_6600['Date'].isin(grid_table['Date'])]

        # Plots the detector voltage
        fig = figure_detector(chart_data_6600)
        st.plotly_chart(fig, use_container_width = True, theme=None)

### Detector Notes section
with open(os.path.join(subdirectory_folder_path, '..','Notes\\notes_6600_detector.txt'), 'a') as file:
    input_notes_detector = st.text_input(label ='Input any comments or notes',help = 'Dont know how to write?') 
    if input_notes_detector:
        file.write('\n' + input_notes_detector + ' ('+ current_date +')  ')
    
with open(os.path.join(subdirectory_folder_path, '..','Notes\\notes_6600_detector.txt'), 'r') as file:
    notes_detector = file.read()       
st.markdown(notes_detector)
