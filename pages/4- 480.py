import os
import sys
import locale
import random
import string


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

cwd = os.path.dirname(__file__)


folder_path_container = st.container()

default_folder_path = ""

option = st.selectbox(
    'Select your batch',
    ('Email', 'Home phone', 'Mobile phone'))

blank_filter = st.toggle('Exclude blank samples', value = True)

st.write("List of all samples in folder")

# ### random text 
# def generate_random_text(length):
#     return ''.join(random.choices(string.ascii_letters, k=length))

# # Specify the length of the DataFrame
# df_length = 10

# Create a DataFrame with a single column containing random text
# df = pd.DataFrame({
#     'Text_Column': [generate_random_text(10) for _ in range(df_length)]
# })

# if 'grid_table' not in locals():
#     list_select = []
# else:
#     list_select = grid_table

# grid_table = table_selector(df, list_select)

# list_select = grid_table


# choice_export = st.radio("Select what you want to plot", ["TIC", "Pressure trace", "XIC"])

# if choice_export == 'XIC':
#     XIC_mass = st.number_input("Enter mass to perform XIC")
#     XIC_width = st.number_input("Enter XIC width (will render +- value)", value = 0.5)


st.write("You can directly copy/paste this table is Freestyle")

if st.button('Create XIC list'):
    cmd = 'start "excel" ' + '"' + os.path.join(subdirectory_folder_path, '..','XIC_lists\\XIC_list_creation.xlsx')
    os.system(cmd)

# df = pd.DataFrame(
#         [
#         {"MS1 mass": "Enter value", "XIC width (+-value)": 0.5}
#         ]
#     )

# if st.button('Import XIC list to table'):
df_XIC_list = pd.read_excel(os.path.join(subdirectory_folder_path, '..','XIC_lists\\XIC_list_creation.xlsx'))


edited_df = st.data_editor(df_XIC_list, num_rows="dynamic", use_container_width = True, hide_index=True)

edited_df["Ranges"] = edited_df["MS1 mass"]- edited_df["XIC width (+-value)"] 
edited_df["Ranges2"] = edited_df["MS1 mass"]+ edited_df["XIC width (+-value)"] 
edited_df["Ranges"] = edited_df["Ranges"].astype(str) + "-" + edited_df["Ranges2"].astype(str)
edited_df["Display"] = "True"
edited_df["Detector Type"] = "MS"
edited_df["Trace Type"] = "Mass Range@1"


file_name = st.text_input("Enter File name")

edited_df["File Name"] = file_name

st.write("You can directly copy/paste this table is Freestyle")

df_formated_XIC_list = pd.read_excel(os.path.join(subdirectory_folder_path, '..','XIC_lists\\XIC_list_template.xlsx'))


concatenated_df = pd.concat([df_formated_XIC_list, edited_df], axis=0, ignore_index=True)

concatenated_df.drop(columns=["MS1 mass", "XIC width (+-value)", "Ranges2"], inplace=True)
concatenated_df = pd.concat([concatenated_df.columns.to_frame().T, concatenated_df], ignore_index=True)

st.dataframe(concatenated_df, hide_index=True)