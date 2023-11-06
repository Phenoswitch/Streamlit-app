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

st.title('TTOF 6600plus Quality Dashboard')


st.subheader("""
Computer space""")
st.info(f'This section shows the available space on each disk.')

data_container = st.container()
with data_container:
    plot1, plot2 = st.columns(2)
    with plot1:
        st.subheader('SYSTEM (D:)')
        st.pyplot(figure_disk_space('D:'))
    with plot2:
        st.subheader('DATA (C:)')
        st.pyplot(figure_disk_space('C:'))

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
st.info(f'Run this section to show the final detector voltage reported after each Instruments optimisation reports. This opens and reads all results.pdf files located in the D:\Analyst Data\Projects\API Instrument\Data\Instrument Optimization folder.')
st.warning('Work in progress')

def main():
    ## Generates data (Dectector voltage and datetime)
    # random_numbers = np.arange(0, 3000, 30, dtype=None)  # Change 10 to the desired number of random numbers
    # x = np.linspace(0, 4 * np.pi, 20)
    # random_numbers = 1500 * np.sin(x) + 1500
    # chart_data = pd.DataFrame({'Detector voltage (V)': random_numbers})

    # start_date = datetime(2021, 1, 1)
    # end_date = datetime(2023, 12, 31)
    # base = datetime(2000, 1, 1)
    # random_dates = np.array([base + timedelta(days=i) for i in range(20)])

    # chart_data['Timelapse'] = random_dates
    # chart_data['Timelapse'] = pd.to_datetime(chart_data['Timelapse'], format='%d/%m/%y')
    # slide_min, slide_max = chart_data['Timelapse'].agg(['min', 'max'])
    # print(type(slide_min), type(slide_min.to_pydatetime()))
    # slider_lim = sliders_datetime(slide_min,slide_max)
    

    # chart_data = chart_data.sort_values(by='Timelapse')

    #Return the detector voltage listed in the path in a dataframe
    chart_data = fetch_detector_6600(r'D:\Analyst Data\Projects\API Instrument\Data\Instrument Optimization')

    #Creates a slider with the min and max date fetched
    slide_min, slide_max = chart_data['Date'].agg(['min', 'max'])
    slider_lim = sliders_datetime(slide_min,slide_max)

    ### Thresholds of voltage for the plot
    chart_data[f'Notify Provider ({DETECTOR_WARNING_6600}V)'] = DETECTOR_WARNING_6600
    chart_data[f'To replace ({DETECTOR_REPLACEMENT_6600}V)'] = DETECTOR_REPLACEMENT_6600
    chart_data[f'Maximum ({DETECTOR_MAXIMUM_6600}V)'] = DETECTOR_MAXIMUM_6600

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

            grid_table = table_selector_datetime(chart_data.drop([f'Notify Provider ({DETECTOR_WARNING_6600}V)',f'To replace ({DETECTOR_REPLACEMENT_6600}V)', f'Maximum ({DETECTOR_MAXIMUM_6600}V)'], axis=1), list_select, [slider_lim])

            list_select = grid_table
            # print(list_select)

        with plot:
            ### Filters the data based on checked table rows
            chart_data = chart_data[chart_data['Date'].isin(grid_table['Date'])]

            # Plots the detector voltage
            fig = figure_detector(chart_data)
            st.plotly_chart(fig, use_container_width = True, theme=None)

    ### Detector Notes section
    with open(os.path.join(subdirectory_folder_path, '..','Notes\\notes_6600plus_detector.txt'), 'a') as file:
        input_notes_detector = st.text_input(label ='Input any comments or notes',help = 'Dont know how to write?') 
        if input_notes_detector:
            file.write('\n' + input_notes_detector + ' ('+ current_date +')  ')
        
    with open(os.path.join(subdirectory_folder_path, '..','Notes\\notes_6600plus_detector.txt'), 'r') as file:
        notes_detector = file.read()       
    st.markdown(notes_detector)

main()