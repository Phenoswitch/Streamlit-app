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

default_folder_path = r"D:\\"
# subfolders = [f.path for f in os.scandir(default_folder_path)]# if f.is_dir()]
subfolders = [dirpath for dirpath, dirnames, filenames in os.walk(default_folder_path)]
# print()

subfolders.remove('D:\\\\$RECYCLE.BIN')
# subfolders.remove('D:\\\\Processing methods')
# subfolders.remove('D:\\\\System Volume Information')

option = st.selectbox(
    'Select your batch',
    subfolders)

# option = r"D:\Pr1_ZOElw_20230331_SEERmaf_canine\20231222_ZOElw_20230331_SEERmaf_canine_P02"

blank_filter = st.toggle('Exclude blank samples', value = True)

st.write("List of all samples in folder")

raw_files = [f for f in os.listdir(option) if f.endswith('.raw')]
file_names = pd.DataFrame({'File Name': raw_files})

# file_names["test"] = file_names["Filenames"].str.split('_').str[0]

try:
    if blank_filter == True:
        file_names = file_names[~file_names["File Name"].str.split('_').str[0].str.contains('b|blanks|blank|Blank')]
    file_names["File Name"] = option+ "\\" +  file_names["File Name"]
except:
    st.error("No raw file found in current folder")

if 'grid_table' not in locals():
    list_select = []
else:
    list_select = grid_table

grid_table = table_selector(file_names, list_select)

list_select = grid_table


choice_export = st.radio("Select what you want to plot", ["TIC", "Pressure trace", "XIC"])

if choice_export == 'XIC':
    XIC_mass = st.number_input("Enter mass to perform XIC")
    XIC_width = st.number_input("Enter XIC width (will render +- value)", value = 0.5)
    grid_table["Ranges"] = str(XIC_mass- XIC_width) + "-" + str(XIC_mass + XIC_width)
    grid_table["Display"] = "True"
    grid_table["Detector Type"] = "MS"
    grid_table["Trace Type"] = "Mass Range@1"
    grid_table["Filter"] = "MS"

if choice_export == 'TIC':
    grid_table["Display"] = "True"
    grid_table["Detector Type"] = "MS"
    grid_table["Trace Type"] = "TIC@0"
    grid_table["Filter"] = "MS"

if choice_export == 'Pressure trace':
    grid_table["Display"] = "True"
    grid_table["Detector Type"] = "A/D Card 2"
    grid_table["Trace Type"] = "Pump_Pressure@0"

st.write("You can directly copy/paste this table is Freestyle")

df_formated_export = pd.read_excel(os.path.join(subdirectory_folder_path, '..','XIC_lists\\XIC_list_template.xlsx'))
concatenated_df_export = pd.concat([df_formated_export, grid_table], axis=0, ignore_index=True)

concatenated_df_export = pd.concat([concatenated_df_export.columns.to_frame().T, concatenated_df_export], ignore_index=True)
st.dataframe(concatenated_df_export, hide_index=True)


st.header("Section for XIC in 1 sample")


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

edited_df["Display"] = "True"
edited_df["Detector Type"] = "MS"
edited_df["Trace Type"] = "Mass Range@1"
edited_df["Filter"] = "MS"

file_name = st.text_input("Enter File name")

edited_df["File Name"] = file_name


use_mass_tolerance = st.toggle('Use Mass tolerance (ppm)')

if use_mass_tolerance:
    edited_df["Mass Tolerance"] = str(st.number_input('Value (ppm)', value=10 ))+"@ppm"
    edited_df["Ranges"] = edited_df["MS1 mass"]
    edited_df["Ranges2"] = edited_df["MS1 mass"]
    # edited_df["Mass Tolerance"] = str(mass_tolerance)+"@ppm"
else:
    edited_df["Mass Tolerance"] = ''
    edited_df["Ranges"] = edited_df["MS1 mass"]- edited_df["XIC width (+-value)"] 
    edited_df["Ranges2"] = edited_df["MS1 mass"]+ edited_df["XIC width (+-value)"] 
    edited_df["Ranges"] = edited_df["Ranges"].astype(str) + "-" + edited_df["Ranges2"].astype(str)

st.write("You can directly copy/paste this table is Freestyle")

df_formated_XIC_list = pd.read_excel(os.path.join(subdirectory_folder_path, '..','XIC_lists\\XIC_list_template.xlsx'))

if use_mass_tolerance:
    test = ','.join(edited_df['Ranges'].astype(str))
    test = test.replace('"', "")
    new_row = {
        'File Name' : [file_name],
        'Display' : ["True"],
        'Detector Type' : ["MS"],
        'Trace Type' : ["Mass Range@1"],
        'Mass Tolerance' : [edited_df["Mass Tolerance"].iloc[0]],
        'Filter' : ["MS"], 
        'Ranges' : [test]

        # 'Ranges' : [edited_df['Ranges'].astype(str).str.join(',')]
    }

    # new_row = new_row.encode('utf-8')
    new_df_row = pd.DataFrame(new_row)
    print(new_df_row)
    # new_df_row['Ranges'] = new_df_row['Ranges'].astype(float)

    # result = ','.join(edited_df['Ranges'].astype(str))
    # print(result)

    concatenated_df = pd.concat([df_formated_XIC_list,new_df_row, edited_df], axis=0, ignore_index=True)

else:
    concatenated_df = pd.concat([df_formated_XIC_list, edited_df], axis=0, ignore_index=True)

concatenated_df.drop(columns=["MS1 mass", "XIC width (+-value)", "Ranges2"], inplace=True)
concatenated_df = pd.concat([concatenated_df.columns.to_frame().T, concatenated_df], ignore_index=True)

st.dataframe(concatenated_df, hide_index=True)