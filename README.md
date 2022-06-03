# pytermtables
CSV Tables and Grids in python

This module allows you to create tables via either a CSV file or through python code, export them, sort them and print them via the python console.

Install it via pip:
```
pip install pytermtables
```
And then import the neccesary items like so:
```python
from pytermtables import gridToString, Table, tableToCSV, tableFromCSV
```

# Creation

Create Table via class
```python
"""
headers - the title of the headers - list
rows - optional - add rows from initialisation - list
"""
table = Table(headers=["Name", "Score"], rows=[
{"Name": "Will", "Score": 99},
{"Name": "Joe", "Score": 111},
{"Name": "John", "Score": 2},
{"Name": "Bob", "Score": 59}
])
```

Create Table via CSV file
```python
"""
filepath - location of csv file - str
titleRow - whether the csv has a title row or not - bool
delimter - seperation char - str
quotechar - quote used for qoutation marks - str
"""
table2 = tableFromCSV(filePath="sampledata.csv", titleRow=False, delimiter=',', quotechar='"')
```

# Printing

```python
#pretty simple
print(table)
```

# Headers

Add a header
```python
"""
headerName - name of header to create - str
data - values for header - list
"""
table.addHeader("Date", ["1/1/1970", "2/12/2008"])

#OR
table["Date"] = ["1/1/1970", "2/12/2008"]
```

Remove a header
```python
"""
Remove header by its name
headerName - header to remove
"""
table.removeHeader("Date")

#OR
del table["Date"]
```

Get a header's data
```python
"""
Get all data from a header
header - title of header
excludeNone - whether to exclude None values when getting data
returns list
"""
data = table.getHeader("Score", excludeNone=True)

#OR
data = table["Score"]
```

# Rows

Add a row
```python
"""
Creating a row for a table
row - the data for the row - dict
returns a copy of the row created
"""
table.addRow({"Name": "Steve", "Score": 999})
```

Remove rows
```python
"""
remove every row that contains subdict
subdict - the subdict to check against - dict
"""
table.removeRows({"Name": "Will"})
```

Get rows
```python
"""
Find every row that contains subdict
subdict - the subdict to check against - dict
returns a list
"""
row = table.getRows({"Name": "Will"})[0]
```

# Statistical Functions

```python
mean = table.getMean("Score") #mean
mode = table.getMode("Score") #mode
median = table.getMedian("Score") #median
range = table.getRange("Score") #range
stdDev = table.getStdDev("Score") #standard deviation
percentile = table.percentile("Score", 15) #nth percentile (15)
IQR = table.getIQR("Score") #interquartile range
```

# Save as CSV

```python
"""
Convert a table to a CSV file
filePath - path of file to create - str
table - table to convert - Table
titleRow - whether the table contains a titleRow - bool
delimiter - csv seperator character - str
qoutechar - char used for quotes - str
"""
tableToCSV(filePath="output.csv", table, titleRow=True, delimiter=',', quotechar='"')
```

# Sorting and Shuffling

Sorting Header
```python
"""
Sort rows by value
header - the key of the dictionary used to sort by
#descending - whether it should be sorted in ascending or descending order
"""
table.sort("Score", descending=False)
```

Shuffling Header
```python
#easy
table.shuffle("Score")
```