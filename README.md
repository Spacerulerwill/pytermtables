# TerminalTables
CSV Tables and Grids in python

This module allows you to create tables via either a CSV file or through python code, export them, sort them and print them via the python console.

Currently, the module is not on pip however you can still place the file in your directory and importing it like so
```python
from terminaltables import Table, tableToCSV, tableFromCSV
```

# Creation
You can create a table in 2 ways:
```python
#table class
#headers - the headers for each table section
#rows - optional - add rows from intialisation, can be removed, edited or added at any time after
table = Table(headers=["Name", "Score"], rows=[{"Name": "Bob", "Score": 80}])
```
You can also create a table via a CSV file

```python
#filePath - path of file
#titleRow - whether CSV contains a row with headers - defaults to True
#deliminter - the char used for seperations - defaults to ,
#quotechar - the char used for quotes - defaults to "
table = tableFromCSV(filePath="scores.csv", titleRow=True, delimiter=",", quotechar='"')
```

and turn an existing table into a CSV

```python
#filePath - path of file
#titleRow - whether CSV contains a row with headers - defaults to True
#deliminter - the char used for seperations - defaults to ,
#quotechar - the char used for quotes - defaults to "
tableToCSV(filePath="output.csv", table=table, titleRow=True, delimiter=",", quotechar='"')
```

# Editing rows

Adding a row:
```python
#creating a row for table
#row - the data for the row - dictionary
#returns the copy of thre created row
table.addRow({"Name": "Joe", "Score": 100"})
```

Getting rows:
```python
#find every row that contains subdict
#dict - the subdict to check if is contained
#returns a list
table.getRows({"Name": "Joe"})
```

Editing a row
```python
#uses get rows and then you pick one with an index to change one of its values
table.getRows({"Name": "Joe"})[0]["Score"] = 10000
```

Deleting a row
```python
#remove every row that contains subdict
#subdict - the subdict to check if is contained
tables.
table.removeRows({"Name": "Joe"})
```

# Editing Headers

Getting all values from a header:
```python
#header - title of header to use
#excludeNone - whether to exlucde None values when getting data
data = table.getHeader("Score", excludeNone=True)
```

Create new header
```python
table.addHeader("Testing")

```

Remove a header
```python
table.removeHeader("Testing")
```

# Statistcal Functions

Mean, Mode, Median, Range, Standard Deviation of data in a header
```python
mean = table.getMean("Score")
mode = table.getMode("Score")
median = table.getMedian("Score")
range = table.getRange("Score")
stdDev = table.getStdDev("Score")
```

# Sorting data
Sort a header by its number data
```python
#descending - optional, defaults to False
table.sort("Score", descending=False")
```
Shuffle row order
```python
table.shuffle()
```

# Printing to console
```python
table.prettyPrint()
```


