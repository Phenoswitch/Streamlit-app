import os
import sys
import locale


### Get relative subfolder path
subdirectory_folder_path = os.path.dirname(__file__)

### imports all variables in Variables.py
sys.path.append(os.path.join(subdirectory_folder_path, '..', 'Utilities'))

from Constantes import *
#imports all FUNCTIONS in Functions.py
from Functions import *
# import all packages in Imports
from Imports import *

### To be run once to update matplotlib default parameters
matplotlib.rcParams.update({'font.size': 12, 'xtick.color' : 'black', 'axes.labelcolor': 'black'})
st.set_page_config(layout="wide")

# path to QC folder
MS_QC_path = r'\\DESKTOP-V8LIH84\Users\6600\Desktop\QC 6600 Report\QC 30MCA 6600_A Compiler\2023'

fig = figure_MSQC_6600(MS_QC_path)

st.plotly_chart(fig, use_container_width = True, theme=None)


# ### To get last obtained value 
# current_values = averaged_df[averaged_df['Timestamp'] == averaged_df['Timestamp'].iloc[-1]]

# desired_tags = ['ITC00', 'ITC01']
# current_QC_TOF_values = current_values[current_values['Tag'].isin(desired_tags)]
# # print(current_QC_TOF_values)

# desired_tags = ['HR', 'HS']
# current_QC_MSMS_values = current_values[current_values['Tag'].isin(desired_tags)]