import bos_crime_vis_tool as vis_tool
import pandas as pd 

df = vis_tool.utils.import_data()
a = pd.DataFrame({'INCIDENT_NUMBER':['1']})
b = df[df['YEAR'] == 2016]
a=b.merge(a,how = 'outer', on='INCIDENT_NUMBER')
print(a)
