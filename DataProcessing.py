import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


combined_df = pd.DataFrame()
excel_file = 'data/EDM 2021 Storm Overflow Annual Return - all water and sewerage companies.xlsx'
excel_data = pd.ExcelFile(excel_file)

first_sheet_name = excel_data.sheet_names[0]
first_sheet_df = pd.read_excel(excel_file, sheet_name=first_sheet_name, skiprows=1)
filters = first_sheet_df.columns.tolist()

for sheet_name in excel_data.sheet_names:
    print(sheet_name)
    sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=1)
    filtered_df = sheet_df[filters]
    combined_df = combined_df._append(filtered_df, ignore_index=True)

print(combined_df)
selected_columns = ['Water Company Name', 
                    #'Site Name(EA Consents Database)', 
                    'Counted spills using 12-24h count method']
selected_df = combined_df[selected_columns]

print(selected_df)
selected_df['Counted spills using 12-24h count method'] = pd.to_numeric(selected_df['Counted spills using 12-24h count method'], errors='coerce')

selected_df = selected_df.dropna(subset=['Counted spills using 12-24h count method'])
print(selected_df)
# Group the data by 'Water Company Name' and calculate the total spills
grouped_df = selected_df.groupby('Water Company Name')['Counted spills using 12-24h count method'].sum()

# Plot the bar chart
colours = plt.cm.Set3(np.arange(len(grouped_df)))
plt.bar(grouped_df.index, grouped_df.values, color=colours)
plt.xlabel('Water Company')
plt.ylabel('Total Counted Spills')
plt.title('Total Counted Spills by Water Company')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()