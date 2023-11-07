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


MS_QC_path = r'\\DESKTOP-V8LIH84\Users\6600\Desktop\QC 6600 Report\QC 30MCA 6600_A Compiler\2023'

MS_QC_timestamp = []
df_list = []

for folder_path, _, files in os.walk(MS_QC_path):
    for TAGS in range(len(MS_QC_TAGS)):
        for file in files:
            if file.endswith('.txt') and MS_QC_TAGS[TAGS] in file and 'NEG' not in file:

                file_path = os.path.join(folder_path, file)
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

result_df['Timestamp'] = pd.to_datetime(result_df['Timestamp'])  # Convert to datetime
result_df = result_df.sort_values(by ='Timestamp')
# result_df.set_index('Timestamp', inplace=True)

averaged_df = result_df.groupby(['Timestamp', 'Tag']).mean()
averaged_df = averaged_df.reset_index()

print(averaged_df)

current_values = averaged_df[averaged_df['Timestamp'] == averaged_df['Timestamp'].iloc[-1]]

desired_tags = ['ITC00', 'ITC01']
current_QC_TOF_values = current_values[current_values['Tag'].isin(desired_tags)]
# print(current_QC_TOF_values)


desired_tags = ['HR', 'HS']
current_QC_MSMS_values = current_values[current_values['Tag'].isin(desired_tags)]
# print(current_QC_MSMS_values)