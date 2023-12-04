'''
=================================
Pandas - Data Wrangling in python
=================================

If you ever work as a fancy Data Scientists, it is very likely that 80% of your
 time will be spent doing data wrangling (I prefer the term Data Cooking).
This will continue until you finally achieve a managerial position and stop 
doing useful work, all of a sudden.


Input data   -->   Data Cooking ---> Visualization   
                        |
                    Intermediate Files


ModelOps[https://en.wikipedia.org/wiki/ModelOps]
------>
MLOps
------>
DevOps
------>
DevSecOps
------>

Software development, in any form, is a human endeavor: it requires to articulate 
people working together in teams.

TDSP: Team Data Science Process

Input Data:
⏺   Data Sources

Data Cooking:
⏺   Dealing with missing data.
⏺   ETL: extract transform and load.  DTS: Data tranformation services

Visualization
⏺   Basic Visualization

This script contains several snippets, separtaed by '# %%' which is a special 
marker that allows Visual Studio Code to treat a python script as a jupyter 
console notebook.  

References:
- Wes McKinney, Python for Data Analysis, 2017
- Harrison, Learning the Pandas Library, 2016

'''

# %%  -----------------------------------------------------------------------------
print(__doc__)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import StringIO

# %%  -----------------------------------------------------------------------------

print('The whole picture, working in Data Science Project in corporate environments')
# https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/overview

# %%  -----------------------------------------------------------------------------

print('Hello Python Scientific World')

online = True
if (online == True):
    url = requests.get('https://raw.githubusercontent.com/faturita/python-scientific/master/data/blinking.dat')
    csv_raw = StringIO(url.text)
    signals = pd.read_csv(csv_raw, delimiter=' ', names = ['timestamp','counter','eeg','attention','meditation','blinking'])
else:
    signals = pd.read_csv('data/blinking.dat', delimiter=' ', names = ['timestamp','counter','eeg','attention','meditation','blinking'])


print('Signals is a dataframe, the basic pandas structure.')
print('Information:')
print(signals.head())

print('Filter records:')
print(signals[signals.counter > 45])

# Show a resume of the data contained in data
signals.describe()

# %%  -----------------------------------------------------------------------------
print('You can always extract the numpy tensor from the pandas dataframe.')
data = signals.values

print('Now in "data", you have a tensor.')
print (data)

print('Shape %2d,%2d:' % (signals.shape))

print('From here you can start working around the data structure which has a mathematical purpose.')


# %%  -----------------------------------------------------------------------------
print('You can go the other way around and convert a numpy array into a dataframe.')
print('Dataframe contain metadata information.')
databack = pd.DataFrame(data, columns=['ts', 'ct', 'e','att','med','blk'])

print ('Shape %2d,%2d:' % databack.shape)

# %%  -----------------------------------------------------------------------------
print('Visualizations')

import seaborn as sns
sns.set(style="darkgrid")
sns.lineplot(x="timestamp", y="eeg", hue="attention", data=signals)
import matplotlib.pyplot as plt
plt.show()


# %%  -----------------------------------------------------------------------------
print('Pandas is great to read data from several differentes sources.')

print('Create a Dataframe from a python dictionary.')
jsonlike = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

mydataframe = pd.DataFrame(jsonlike)
print(mydataframe)
print('The columns names are taken from the dictionary while row names are just consequitive numbers.')

# %%  -----------------------------------------------------------------------------

print('The read_xxxx methods load data in several formats.  This like Excel import, so there are hundreds of parameters.')
signals = pd.read_csv('data/blinking.dat', delimiter=' ', names = ['timestamp','counter','eeg','attention','meditation','blinking'])
# //skip_rows, index_cols, sep='\s+', nrows

print(signals.head())

print('read_sas, read_sql, read_pickle, read_json, read_excel, ...')

dat = pd.read_csv('data/laliga.csv',delimiter=';')

print(dat.head())

# %%  -----------------------------------------------------------------------------
print('Data can finally be exported to an output file.')
dat.to_csv('data/out.csv')

# %%  -----------------------------------------------------------------------------
print('JSON is a widespread format very used in web environments.')
obj = """
    {"name": "Wes",
     "places_lived": ["United States", "Spain", "Germany"],
     "pet": null,
     "siblings": [{"name": "Scott", "age": 30, "pets": ["Zeus", "Zuko"]},
                  {"name": "Katie", "age": 38,
                   "pets": ["Sixes", "Stache", "Cisco"]}]
} """

import json

results = json.loads(obj)

results

print('We can filter what part of the JSON object do we want for the Dataframe.')
siblings = pd.DataFrame(results['siblings'], columns=['name', 'age'])

print(siblings)

json_string = json.dumps(results)

print(json_string)


# %%  -----------------------------------------------------------------------------

data = pd.read_json('data/sample2.json')

print('It is possible to put it back to json string.')
print(data.to_json())


# %%  -----------------------------------------------------------------------------
print('Python allows to crawl web pages and get HTML tables.')
tables = pd.read_html('https://www.scimagojr.com/journalrank.php')   # @NOTE Fixed

journals = tables[0]

print("Journal rankings by SciMago")
print(journals)

# %%  -----------------------------------------------------------------------------
print('Series are one-index Dataframe.')

calories = {"day1": 420, "day2": 380, "day3": 390}

cal_frame = pd.Series(calories)

print(cal_frame)
print('Day1, day2, ... are the row names.')

# %%  -----------------------------------------------------------------------------
print('Python uses pickles to serialize structures, and this can be read from pandas.')

calories = {"day1": 420, "day2": 380, "day3": 390}

cal_frame = pd.Series(calories)

cal_frame.to_pickle('data/frame.pickle')

# Store intermediate information

new_frame = pd.read_pickle('data/frame.pickle')
print(new_frame)


# %%  -----------------------------------------------------------------------------
print('Reading some json data out of a API.')
from io import StringIO
import requests

url = requests.get('https://api.github.com/repos/faturita/python-scientific/commits')
js = StringIO(url.text)
sg = pd.read_json(js)
sg.head()


# %%  -----------------------------------------------------------------------------
print('-------------------------------------------------------------------------------------')
print('Panda detects missing data by checking sentinel values like "NaN", "NULL", "NA".')
results = pd.read_csv('data/sample1.csv')

print('You can get an indicative matrix which returns true on the cell where the data is missing')

# Isnull and notnull return a boolean Panda Frame
results.isnull()
results.notnull()


print('It is also possible to specify different sentinel values for missing data.')
sentinels = {'message': ['foo', 'NA'], 'something': ['two']}

print('For each column,  the sentinel value.')
results = pd.read_csv('data/sample1.csv', na_values = sentinels)
print ( results )

print('Filter elements from the DataFrame where the specified column is NA.')
results[results.notnull()['message']]

# %%  -----------------------------------------------------------------------------
print('Handling missing data.')

from numpy import nan as NA
data = pd.Series([1, NA, 3.5, NA, 7])

newdataframe = data.dropna()
print(newdataframe)

print('The same as')

print(data[data.notnull()])

# %%  -----------------------------------------------------------------------------
print('On 2D')
data = pd.DataFrame([[1., 6.5, 3.], [1., NA, NA], [NA, NA, NA], [NA, 6.5, 3.]])
data.dropna(how='all', axis = 1)        # 0 is row, 1 is col
data.dropna(how='any', axis = 0)


# %%  -----------------------------------------------------------------------------
print('Now fillna can be used in the same way to fill in the data.')
data = pd.DataFrame([[1., 6.5, 3.], [1., NA, NA], [NA, NA, NA], [NA, 6.5, 3.]])

newframe = data.fillna(0)

data.fillna({0: 0.5, 2:0})  # When NaN is found, for the row 0 put 0.5, for the row 2, put 0

print('An interpolation can be performed to fill in the missing values.')
data.fillna(method='ffill')

data[np.abs(data) > 1.5] = np.sign(data) * 10

# %%  -----------------------------------------------------------------------------
print('None, the python Null marker, can also be considered as NA sentinel.')
string_data = pd.Series(['aardvark', 'artichoke', np.nan, 'avocado'])

string_data[0] = None

print(string_data)


# %%  -----------------------------------------------------------------------------
print('Removing duplicates')
string_data = pd.Series(['Newark', 'Manchester', 'Halifax', 'Manchester'])

newframe = string_data.drop_duplicates()

print(string_data)

print(newframe)

# %% ----------------------------------------------------------------------------
print('Replacing values')
newframe = string_data.replace({'Newark': np.nan, 'Halifax': 'Ottawa'})
print(string_data)

print(newframe)
# %%  -----------------------------------------------------------------------------
print('Pandas Series can be used to handle sequential data.')

import pandas as pd

a = [1, 7, 2]

series = pd.Series(a)

print(series)

print('By default, indexes are created with range on the number of elements.')
series = pd.Series(a, index = ["x", "y", "z"])

print(series)
print(series.values)
print(series.index)


# %%  -----------------------------------------------------------------------------
print('String indexes can be used on series.')
a = [1, 7, 2]
series = pd.Series(a, index = ["x", "y", "z"])

print(series['x'])

print(series[series > 1])

print(series * 2)

print(np.exp(series))

print('x' in series) 

print('r' in series) 
# %%  -----------------------------------------------------------------------------
print('Index are automatically used to operate on the data.')
a = [1, 7, 2]
series1 = pd.Series(a, index = ["x", "y", "z"])
b = [-1, -8, 3]
series2 = pd.Series(a, index = ["y", "z", "r"])

# WARNING !
series3 = series1 + series2 

print(series1)
print(series2)
print(series3)


# %%  -----------------------------------------------------------------------------
print('Dataframes are dynamics structures')
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002, 2003],
            'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)

print(frame)
print(frame.state) 
print(frame['state'])
print(frame.pop)

# %%  -----------------------------------------------------------------------------
print('Row can also have names (instead of index numbers)')
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002, 2003],
            'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)

print(frame)

frame.index = ['one','two','three','four','five','six']

print(frame)

# %%  -----------------------------------------------------------------------------
print('Entire rows or columns can be updated')
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002, 2003],
            'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)

print(frame)

frame['pop'] = 9.0              # References the column 'pop'
frame.loc['three']=9.0              # References the row indexed 'three'

print(frame)

# %%  -----------------------------------------------------------------------------
print('Colums/Rows can be updated or easily created')
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002, 2003],
            'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)

print(frame)

val = pd.Series([11, 12, 13], index=['two', 'four', 'five'])

frame['pop'] = val              # This means that pop is REPLACED by val.

print('Now pop has been replaced with a new series')
print(frame)

print('Now add a new column')
frame['Casinos'] = frame.state == 'Nevada'

print(frame)

del frame['Casinos']            # Removes the column 'Casinos'

print('And delete it later')

print(frame)

frame.columns.name = 'Variables'
frame.index.name = 'Locations'

print('Now we can add index names (name for the column and the row)')
print(frame)

# %%  -----------------------------------------------------------------------------
print('Reindexing: mapping the values with new indexes.')
a = [1, 7, 2]
series1 = pd.Series(a, index = ["x", "y", "z"])

series2 = series1.reindex(["x","z","e"])

series2.index = ['x','p','d']               # Is the same result ?

# %%  -----------------------------------------------------------------------------
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
            index=['Ohio', 'Colorado', 'Utah', 'New York'],
            columns=['one', 'two', 'three', 'four'])

data.drop(['Colorado', 'Ohio'])

data.drop('four', axis=1)               # inplace=True, mutate the object.
print(data)
# %%  -----------------------------------------------------------------------------

print('Slicing, the end-point is inclusive')
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
            index=['Ohio', 'Colorado', 'Utah', 'New York'],
            columns=['one', 'two', 'three', 'four'])

data['Ohio':'Utah']                     # Filters from Ohio to Utah inclusive.

data.loc['Colorado', ['two', 'three']]

data.iloc[2, [3, 0, 1]]

data.loc[:'Utah', 'two']

data.iloc[:, :3][data.three > 5]
# %%  -----------------------------------------------------------------------------
print('Mappings')
frame = pd.DataFrame(np.random.randn(4,3), columns=list('bde'), 
                    index=['Utah','Ohio','Texas','Oregon'])

np.abs(frame)

f = lambda x: x.max() - x.min()

# Mappings can be applied directly on dataframes.
frame.apply(f)

# Or they can also be applied specifically to certain columns or rows.
frame.apply(f, axis=1)
frame.apply(f, axis='columns')
# %%  -----------------------------------------------------------------------------
frame = pd.DataFrame(np.random.randn(4,3), columns=list('bde'), 
                    index=['Utah','Ohio','Texas','Oregon'])
format = lambda x: '%.2f' % x 

print(frame.applymap(format))

print(frame['e'].map(format))

# %%  -----------------------------------------------------------------------------
print('Index uniqueness')
obj = pd.Series(range(5), index=['a', 'a', 'b', 'b', 'c'])

obj.index.is_unique 
obj['a']                # This is now a Series
obj['c']                # This is a scalar value

# %%  -----------------------------------------------------------------------------
print('Aggregating by hierarchical indexing.')
data = pd.Series(np.random.randn(9),
    index=[['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'],
            [1,2,3,1,3,1,2,2,3]])

data['b']

data['b':'c']

data.unstack()                  # Set the doble index as a matrix.

data.unstack().stack()          # Put it back into hierarchical

# %%  -----------------------------------------------------------------------------
print('Aggregating indexes.')
frame = pd.DataFrame({'a': range(7), 'b': range(7,0,-1),
                        'c': ['one','one','one','two','two','two','two'],
                        'd': [0,1,2,0,1,2,3]})

frame.set_index(['c','d'], drop=False)          # 'c' and 'd' are now indexes.  Should we keep the columns or not.

frame.reset_index()


# %%  -----------------------------------------------------------------------------
print('Aggregating by two columnds.')
data = [{'Year':2000, 'Yields': np.random.randint(60), 'Location':'Colchester'},
        {'Year':2000, 'Yields': np.random.randint(60), 'Location':'Manchester'},
        {'Year':2001, 'Yields': np.random.randint(60), 'Location':'Colchester'},
        {'Year':2001, 'Yields': np.random.randint(60), 'Location':'Oxford'},
        {'Year':2002, 'Yields': np.random.randint(60), 'Location':'Colchester'},
        {'Year':2002, 'Yields': np.random.randint(60), 'Location':'Oxford'},
        {'Year':2003, 'Yields': np.random.randint(60), 'Location':'Manchester'}]

df = pd.DataFrame(data, columns=['Year', 'Yields', 'Location'])

grp = df.groupby(['Location','Year']).agg({'Yields':['mean','min','max']})
grp.columns = ['yield_mean','yield_min','yield_max']
grp = grp.reset_index()

print(grp)

# %%  -----------------------------------------------------------------------------
print('Data frames can be easily be used for basic plotting.')
df = pd.read_csv('data/laliga.csv',delimiter=';')

df.plot(kind='scatter', x = 'MP', y = 'FA_GIVEN')

plt.show()


# %%  -----------------------------------------------------------------------------
print('Data frames can be easily be used for basic plotting.')

df['GOAL'].plot(kind = 'hist')

plt.show()

                                                


# %%
