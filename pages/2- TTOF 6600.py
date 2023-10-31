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
matplotlib.rcParams.update({'font.size': 20, 'xtick.color' : 'black', 'axes.labelcolor': 'black'})
st.set_page_config(layout="wide")

locale.setlocale(locale.LC_ALL, '')

#""" Setup TTOF 7600 Web page """

add_logo("https://allumiqs.com/wp-content/uploads/2022/06/AG-Icon-238x232.png", height=200) #TODO: move this to a utils module

st.title('TTOF 6600 Quality Dashboard')

st.subheader("""
MS qualifications""")
st.warning('Work in progress')
st.info(r'Run this section to show MS qualifications and thresholds. This opens and extract the MS qualifications saved in the C:\Users\6600plus\Desktop\QC_Report\QC 30MCA 6600plus_A Compiler folder.')
st.write('The 6600 TTOF specifications listed here are the in-house Allumiqs thresholds for a positive tuning performed with the iPD1-CsI homemade tuning solution.')
st.write('The last tuning qualifications found in the folder is from . ')

""" Qualifications in TOF MS """
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

current_ITC00_res = 37000
current_ITC00_int = 0.5*10**6
current_ITC01_res = 32000
current_ITC01_int = 0.5*10**4

if current_ITC00_res >= MS_QUALIFICATIONS_ITC00_RESOLUTION : 
    MS_QUALIFICATIONS_ITC00_RESOLUTION_COLOR = "#00ff00" 
else:
    MS_QUALIFICATIONS_ITC00_RESOLUTION_COLOR = "#ff0000"
if current_ITC00_int >= MS_QUALIFICATIONS_ITC00_INTENSITY : 
    MS_QUALIFICATIONS_ITC00_INTENSITY_COLOR = "#00ff00" 
else:
    MS_QUALIFICATIONS_ITC00_INTENSITY_COLOR = "#ff0000"
if current_ITC01_res >= MS_QUALIFICATIONS_ITC01_RESOLUTION : 
    MS_QUALIFICATIONS_ITC01_RESOLUTION_COLOR = "#00ff00" 
else:
    MS_QUALIFICATIONS_ITC01_RESOLUTION_COLOR = "#ff0000"
if current_ITC01_int >= MS_QUALIFICATIONS_ITC01_INTENSITY : 
    MS_QUALIFICATIONS_ITC01_INTENSITY_COLOR = "#00ff00" 
else:
    MS_QUALIFICATIONS_ITC01_INTENSITY_COLOR = "#ff0000"


new_row_data = ['Current value', f'<b><FONT COLOR={MS_QUALIFICATIONS_ITC00_RESOLUTION_COLOR}>{current_ITC00_res}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_ITC00_INTENSITY_COLOR}>{float(current_ITC00_int):.1e}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_ITC01_RESOLUTION_COLOR}>{current_ITC01_res}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_ITC01_INTENSITY_COLOR}>{float(current_ITC01_int):.1e}</FONT></b>']
df_MS_qualification.loc['Current value'] = new_row_data

df_MS_qualification.index = ['', '']

df_MS_qualification = df_MS_qualification.style.set_table_styles([{
    'selector': 'th',
    'props': [('text-align', 'center')]
}, {
    'selector': 'td',
    'props': [('text-align', 'center')]
}])

st.write(df_MS_qualification.to_html(), unsafe_allow_html= True)

""" Qualifications in TOF MSMS """
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

current_HR_res = 37000
current_HR_int = 0.5*10**6
current_HS_res = 32000
current_HS_int = 0.5*10**4
current_HSHR_ratio = 3.424275

if current_HR_res >= MS_QUALIFICATIONS_HR_RESOLUTION : 
    MS_QUALIFICATIONS_HR_RESOLUTION_COLOR = "#00ff00" 
else:
    MS_QUALIFICATIONS_HR_RESOLUTION_COLOR = "#ff0000"
if current_HR_int >= MS_QUALIFICATIONS_HR_INTENSITY : 
    MS_QUALIFICATIONS_HR_INTENSITY_COLOR = "#00ff00" 
else:
    MMS_QUALIFICATIONS_HR_INTENSITY_COLOR = "#ff0000"
if current_HS_res >= MS_QUALIFICATIONS_HS_RESOLUTION : 
    MS_QUALIFICATIONS_HS_RESOLUTION_COLOR = "#00ff00" 
else:
    MS_QUALIFICATIONS_HS_RESOLUTION_COLOR = "#ff0000"
if current_HS_int >= MS_QUALIFICATIONS_HS_INTENSITY : 
    MS_QUALIFICATIONS_HS_INTENSITY_COLOR = "#00ff00" 
else:
    MS_QUALIFICATIONS_HS_INTENSITY_COLOR = "#ff0000"
if current_HSHR_ratio >= MS_QUALIFICATIONS_HSHR_RATIO : 
    MS_QUALIFICATIONS_HSHR_RATIO_COLOR = "#00ff00" 
else:
    MS_QUALIFICATIONS_HSHR_RATIO_COLOR = "#ff0000"


new_row_data_MSMS = ['Current value', f'<b><FONT COLOR={MS_QUALIFICATIONS_HR_RESOLUTION_COLOR}>{current_HR_res}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_HR_INTENSITY_COLOR}>{current_HR_int}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_HS_RESOLUTION_COLOR}>{current_HS_res}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_HS_INTENSITY_COLOR}>{float(current_HS_int):.1e}</FONT></b>', f'<b><FONT COLOR={MS_QUALIFICATIONS_HSHR_RATIO_COLOR}>{round(current_HSHR_ratio,1)}</FONT></b>']
df_MSMS_qualification.loc['Current value'] = new_row_data_MSMS

df_MSMS_qualification.index = ['', '']

df_MSMS_qualification = df_MSMS_qualification.style.set_table_styles([{
    'selector': 'th',
    'props': [('text-align', 'center')]
}, {
    'selector': 'td',
    'props': [('text-align', 'center')]
}])

st.write(df_MSMS_qualification.to_html(), unsafe_allow_html= True)


st.subheader("""
LC-MS calibrations""")
st.info(f'Run this section to show all LC-MS calibration informations and trends.')
st.warning('Work in progress')

st.subheader("""
Detector voltage""")
st.info(f'Run this section to show the final detector voltage reported after each Instruments optimisation reports. This opens and reads all results.pdf files located in the Desktop-v8lih84\d\Analyst Data\Projects\API Instrument\Data\Instrument Optimization folder.')
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

main()