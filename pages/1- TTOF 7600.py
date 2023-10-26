import os
import sys

### Get relative subfolder path
subdirectory_folder_path = os.path.dirname(__file__)

### imports all variables in Variables.py
sys.path.append(os.path.join(subdirectory_folder_path, '..', 'Utilities'))
from Constantes import *
#imports all variables in Variables.py
from Functions import *
# import Functions as functions
from Imports import *

### Now time to be used in script
current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d")

### To be run once to update matplotlib default parameters
matplotlib.rcParams.update({'font.size': 20, 'xtick.color' : 'black', 'axes.labelcolor': 'black'})
st.set_page_config(layout="wide")


""" Setup TTOF 7600 Web page """

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

    chart_data = fetch_detector_zeno(r'\\Zeno-7600\v\Tuning_report\Complete_Tuning\Positive mode')

    # print(chart_data['Date'])

    # chart_data['Date'] = pd.to_datetime(chart_data['Date'], format="%Y-%m-%d %I:%M %p")

    slide_min, slide_max = chart_data['Date'].agg(['min', 'max'])

    # print(type(slide_min))#, type(datetime.strptime(slide_min, "%Y-%m-%d %H:%M:%S")))

    slider_lim = sliders_datetime(slide_min,slide_max)



    ### Thresholds of voltage for the plot
    chart_data['Notify Zef (2700V)'] = DETECTOR_WARNING_7600
    chart_data['To replace (2750V)'] = DETECTOR_REPLACEMENT_7600
    chart_data['Maximum (2850V)'] = DETECTOR_MAXIMUM_7600

    # Creates a container to put table and plot side by side
    data_container = st.container()
    with data_container:
        table, plot = st.columns(spec = [0.25,0.75]) #25% window width for table and 75% width for plot
        with table:

            # Creates the table
            list_select = []
            grid_table = table_selector_datetime(chart_data.drop(['Notify Zef (2700V)', 'To replace (2750V)', 'Maximum (2850V)'], axis=1), list_select, [slider_lim])

        with plot:
            ### Filters the data based on checked table rows
            chart_data = chart_data[chart_data['Date'].isin(grid_table['Date'])]

            # Plots the detector voltage
            fig = figure_detector_zeno(chart_data)
            st.plotly_chart(fig, use_container_width = True, theme=None)

    ### Detector Notes section
    with open(os.path.join(subdirectory_folder_path, '..','Notes\\notes_zeno_detector.txt'), 'a') as file:
        input_notes_detector = st.text_input(label ='Input any comments or notes',help = 'Dont know how to write?') 
        if input_notes_detector:
            file.write('\n' + input_notes_detector + ' ('+ current_date +')  ')
        
    with open(os.path.join(subdirectory_folder_path, '..','Notes\\notes_zeno_detector.txt'), 'r') as file:
        notes_detector = file.read()       
    st.markdown(notes_detector)

main()