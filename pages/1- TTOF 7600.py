import os
import sys

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
matplotlib.rcParams.update({'font.size': 20, 'xtick.color' : 'black', 'axes.labelcolor': 'black'})
st.set_page_config(layout="wide")


#""" Setup TTOF 7600 Web page """

add_logo("https://allumiqs.com/wp-content/uploads/2022/06/AG-Icon-238x232.png", height=200) #TODO: move this to a utils module

st.title('TTOF 7600 Quality Dashboard')

st.subheader("""
Computer space""")
st.info(f'This section shows the available space on each disk.')

data_container = st.container()
with data_container:
    plot1, plot2 = st.columns(2)
    with plot1:
        st.subheader('SYSTEM (D:)')
        st.pyplot(figure_disk_space(r'\\Zeno-7600\d', skipcolor = False))
    with plot2:
        st.subheader('DATA (C:)')
        st.pyplot(figure_disk_space(r'\\Zeno-7600\c', skipcolor = True))

st.subheader("""
MS qualifications""")
st.info(f'Run this section to show MS qualifications and thresholds.')
st.warning('Work in progress')


st.info(r'Run this section to show MS qualifications and thresholds. This opens the positif quick MS check only and extract the MS qualifications saved in the \\Zeno-7600\v\Tuning_report\System check\Positive mode folder.')
st.info(r'While performing the Quick MS check, AUX Gas needs to be setted at 10 psi. The only threshold is for the intensity in TOF MS/MS Zeno Off ion of 494.3374 > 1e5.')


st.subheader("""
LC-MS calibrations""")
st.info(f'Run this section to show all LC-MS calibration informations and trends.')
st.warning('Work in progress')

st.subheader("""
Detector voltage""")
st.info(f'Run this section to show the final detector voltage reported after each Detector Optimization tuning. This opens and reads all Positive Detector Optimization .xps files located in the Zeno-7600\v\Tuning_report\Complete_Tuning\Positive mode folder.')
st.warning('Work in progress')


#Return the detector voltage listed in the path in a dataframe
chart_data_zeno = fetch_detector_zeno(r'\\Zeno-7600\v\Tuning_report\Complete_Tuning\Positive mode')

#Creates a slider with the min and max date fetched
slide_min, slide_max = chart_data_zeno['Date'].agg(['min', 'max'])
slider_lim = sliders_datetime(slide_min,slide_max)

### Thresholds of voltage for the plot
chart_data_zeno[f'Notify Provider ({DETECTOR_WARNING_7600}V)'] = DETECTOR_WARNING_7600
chart_data_zeno[f'To replace ({DETECTOR_REPLACEMENT_7600}V)'] = DETECTOR_REPLACEMENT_7600
chart_data_zeno[f'Maximum ({DETECTOR_MAXIMUM_7600}V)'] = DETECTOR_MAXIMUM_7600

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

        grid_table = table_selector_datetime(chart_data_zeno.drop([f'Notify Provider ({DETECTOR_WARNING_7600}V)',f'To replace ({DETECTOR_REPLACEMENT_7600}V)', f'Maximum ({DETECTOR_MAXIMUM_7600}V)'], axis=1), list_select, [slider_lim])

        list_select = grid_table
        # print(list_select)

    with plot:
        ### Filters the data based on checked table rows
        chart_data_zeno = chart_data_zeno[chart_data_zeno['Date'].isin(grid_table['Date'])]

        # Plots the detector voltage
        fig = figure_detector(chart_data_zeno)
        st.plotly_chart(fig, use_container_width = True, theme=None)

### Detector Notes section
with open(os.path.join(subdirectory_folder_path, '..','Notes\\notes_zeno_detector.txt'), 'a') as file:
    input_notes_detector = st.text_input(label ='Input any comments or notes',help = 'Dont know how to write?') 
    if input_notes_detector:
        file.write('\n' + input_notes_detector + ' ('+ current_date +')  ')
    
with open(os.path.join(subdirectory_folder_path, '..','Notes\\notes_zeno_detector.txt'), 'r') as file:
    notes_detector = file.read()       
st.markdown(notes_detector)
