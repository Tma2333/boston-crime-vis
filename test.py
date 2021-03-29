import bos_crime_vis_tool as vis_tool

df = vis_tool.utils.import_data()

print(vis_tool.utils.get_range(df, 'Lat'))
yearOptions = list(df['YEAR'].unique().astype('str'))
yearOptions.append('all')
print(yearOptions)
print(type(yearOptions))