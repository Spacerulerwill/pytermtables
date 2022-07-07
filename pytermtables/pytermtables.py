from random import shuffle as listshuffle
from statistics import mean, median, mode, pstdev
import csv
from math import ceil

def gridToString(arr, hPadding:int=1, cChar:str="+", hChar:str= "-", vChar:str="|", titleRow:bool = False, trChar:str = "=") -> str:
  """
  Convert a 2d array 'grid' to a string and return the string\n
  arr - 2d array to convert\n
  hPadding - the horizontal padding between data and the column lines\n
  cChar - the character used for corners in the grid - str\n
  hChar - the character used for horizontal - str\n
  vChar - the character used for vertical seperations - str\n
  titleRow - if true - seperator top row from rows beneath (like using a table)\n
  trChar - the char used for the title row seperator\n
  """

  #check that variables are usable and of correct format
  if not isinstance(titleRow, bool): raise Exception("titleRow must be either true or false")
  if len(arr) == 0: raise Exception("List cannot be empty")
  if not isinstance(hPadding, int): raise Exception("hPadding must be a positive integer!")
  if hPadding < 0: raise Exception("hPadding must be a positive integer")
  if not isinstance(cChar, str): raise Exception("cChar must be a string!")
  if not isinstance(hChar, str): raise Exception("hChar must be a string!")
  if not isinstance(vChar, str): raise Exception("vChar must be a string!")
  if not isinstance(trChar, str): raise Exception("trChar must be a string!")
  if len(cChar) != 1: raise Exception("cChar must be a string of length 1")
  if len(hChar) != 1: raise Exception("hChar must be a string of length 1")
  if len(vChar) != 1: raise Exception("vChar must be a string of length 1") 
  if len(trChar) != 1: raise Exception("trChar must be a string of length 1") 
  
  #find grid cols and rows
  gridCols = len(max(arr, key=lambda x: len(x))) # <- as wide as longest sublist
  
  #iterate through data, find widest element for each column
  #this + hPadding*2 will be the width of the entire column
  columnWidths = []
  for i in range(gridCols):
    column = ([el[i] for el in arr if i < len(el)]) #get column

    #get max width of element in each column
    maxColumnElemWidth = len(str(max(column, key=lambda x: len(str(x)))))
    columnWidths.append(maxColumnElemWidth) #append to list by column index

  #if using a title row, define it
  if titleRow:
    titleSeperator = "\n"
    for width in columnWidths:
      titleSeperator += cChar + trChar * (width+hPadding * 2)
    titleSeperator += cChar

  #construct grid seperator with grid widths found
  gridSeperator = "\n"
  for width in columnWidths:
    gridSeperator += cChar + hChar * (width+hPadding * 2)
  gridSeperator += cChar

  constructedString = ""

  #print grid with new column widths
  for row, i in enumerate(arr):
    if row == 1 and titleRow:
      constructedString += titleSeperator + "\n"
    else:
      constructedString += gridSeperator + "\n"
    for col in range(gridCols):
      colWidth = columnWidths[col] + hPadding * 2
      try:
        elem = arr[row][col]
        elem = str(elem).center(colWidth, " ")
      except IndexError:
        elem = " " * colWidth
      constructedString += vChar + str(elem)
    constructedString += vChar
  constructedString += gridSeperator

  return constructedString

class Table():
  """
  A Table datatype\n
  headers - the headers for each table section\n
  rows - optional - add rows from intialisation\n
  """
  def __init__(self, headers:list, rows=None):
    if not isinstance(headers, list): raise Exception("Headers must be a list!")
    if len(headers) == 0: raise Exception("Headers list cannot be empty")
    if len(set(headers)) != len(headers): raise Exception("Headers must not contain duplicates!")
    self._headers = headers

    #if rows supplied, add to begin with else make it blank
    self._rows = []
    if rows != None:
      self._rows = [self.addRow(row) for row in rows]
    
  def addRow(self, row:dict) -> dict:
    """
    Creating a row for a table\n
    row - the data for the row - dict\n
    returns a copy of the row created\n
    """
    if not isinstance(row, dict): raise Exception("Row must be a dictionary")
    
    newRow = dict.fromkeys((h for h in self._headers), None) # <- create blank header dict
    for key, value in row.items():
      if key in self._headers:
        newRow[key] = value
      else:
        raise Exception(f"{key} is not an existing header!")
    self._rows.append(newRow)
    return newRow

  def __str__(self):
    """
    Pretty prints table\n
    """
    grid = [self._headers] + [[row[header] for header in self._headers] for row in self._rows]
    return gridToString(grid, titleRow=True)

  def __len__(self):
    """
    return amount of table elements that aren't None\n
    """
    totalRowLength = 0
    for row in self._rows:
      for value in row.values():
        if value != None:
          totalRowLength += 1
    return totalRowLength

  #get header using [] syntax
  def __getitem__(self, header):
    if not header in self._headers: raise Exception(f"{header} is not a header for this table!")
    #return column from specified header
    return [row[header] for row in self._rows]

  #delete header
  def __delitem__(self, headerName):
    if not headerName in self._headers: raise Exception(f"Can't delete header {headerName} as doesn't exist!")
    self._headers.remove(headerName)
    for row in self._rows:
      del row[headerName]

  #change header
  def __setitem__(self, header, value):
    if not isinstance(value, list): raise Exception("value must be a list")
    if header in self._headers:
      for count,row in enumerate(self._rows):
        try:
          row[header] = value[count]
        except IndexError:
          pass
    else:
      self._headers.append(header)
      for count, row in enumerate(self._rows):
        try:
          row[header] = value[count]
        except IndexError:
          row[header] = None

  def getRows(self, subdict:dict) -> list:
    """
    Find every row that contains subdict\n
    subdict - the subdict to check against - dict\n
    returns a list\n
    """
    if not isinstance(subdict, dict): raise Exception("Subdict must be a dictionary!")
    return [row for row in self._rows if subdict.items() <= row.items()]

  def removeRows(self, subdict:dict):
    """
    remove every row that contains subdict\n
    subdict - the subdict to check against - dict\n
    """
    if not isinstance(subdict, dict): raise Exception("Subdict must be a dictionary!")
    self._rows = [row for row in self._rows if not subdict.items() <= row.items()]

  def sort(self, header, descending:bool=False):
    """
    Sort rows by value\n
    header - the key of the dictionary used to sort by\n
    #descending - whether it should be sorted in ascending or descending order\n
    """
    if not isinstance(descending, bool): raise Exception("Descending must be a boolean!")
    self._rows = sorted(self._rows, key=lambda d: d[header], reverse=descending)

  def shuffle(self):
    """
    shuffle rows in random order\n
    """
    listshuffle(self._rows) #listshuffle is alias of shuffle from random library

  def getHeader(self, header, excludeNone=False) -> list:
    """
    Get all data from a header\n
    header - title of header\n
    excludeNone - whether to exclude None values when getting data\n
    returns list\n
    """
    if not isinstance(excludeNone, bool): raise Exception("excludeNone must be a boolean!")
    if not header in self._headers: return None
    #return column from specified header
    if excludeNone:
      return [row[header] for row in self._rows if row != None]
    else:
      return [row[header] for row in self._rows]

  def removeHeader(self, headerName):
    """
    Remove header by its name\n
    headerName - header to remove\n
    """
    if not headerName in self._headers: raise Exception(f"Can't delete header {headerName} as doesn't exist!")
    self._headers.remove(headerName)
    for row in self._rows:
      del row[headerName]

  def addHeader(self, headerName, data:list=[]):
    if not isinstance(data, list): raise Exception("Data must be a list")
    """
    Add a new header column\n
    headerName - name of header to create\n
    data - values for header\n
    """
    if headerName in self._headers: raise Exception(f"Cant create header {headerName} as it already exists")#
    self._headers.append(headerName)
    for count, row in enumerate(self._rows):
      try:
        row[headerName] = data[count]
      except IndexError:
        row[headerName] = None
    
  def getMean(self, header) -> float:
    """
    Get mean value of header's data\n
    header - name of header to get data from\n
    returns float\n
    """
    return mean([float(x) for x in self.getHeader(header, excludeNone=True) if x != None]) #converts all to floats if not none 
  
  def getMedian(self, header) -> float:
    """
    Get median of header's data\n
    header - name of header to get data from\n
    returns float\n
    """
    return median([float(x) for x in self.getHeader(header, excludeNone=True) if x != None]) #converts all to floats if not none

  def getMode(self, header) -> float:
    """
    Get mode of header's data\n
    header - name of header to get data from\n
    returns float\n
    """
    return mode([float(x) for x in self.getHeader(header, excludeNone=True) if x != None]) #converts all to floats if not none

  def getRange(self, header) -> float:
    """
    Get range of header's data\n
    header - name of header to get data from\n
    returns float\n
    """
    data = [float(x) for x in self.getHeader(header, excludeNone=True) if x != None] #converts all to floats if not none
    return max(data) - min(data)

  def getStdDev(self, header) -> float:
    """
    Get standard deviation of header's data\n
    header - name of header to get data from\n
    returns float\n
    """
    return pstdev([float(x) for x in self.getHeader(header, excludeNone=True) if x != None]) #converts all to floats if not none

  def percentile(self, header, percentile:float) -> float:
    if percentile < 0 or percentile > 100: raise Exception("Percentile must be > 0 and < 100!")
    """
    Get nth percentile of a header's data\n
    header - name of header to get data from\n
    percentile - nth percentile - float in range(0, 100)\n
    returns float\n
    """

    data = sorted([float(x) for x in self.getHeader(header, excludeNone=True) if x != None])

    if percentile == 0:
      return data[0]

    valueIndex = ceil((percentile/100) * len(data))
    return data[valueIndex-1]

  def getIQR(self, header) -> float:
    """
    Get interquartile range of a header's data\n
    header - name of header to get data from\n
    returns float\n
    """

    return self.percentile(header, 75) - self.percentile(header, 25)

def tableFromCSV(filePath:str, titleRow:bool=True, delimiter:str=",", quotechar:str='"'):
  """
  Create a table from a CSV file\n
  filePath - path of file - str\n
  titleRow - whether CSV contains a row with headers - bool\n
  delimiter - the char used for CSV seperations - str\n
  quotechar - the char used for quotes - str\n
  """
  #type checking
  if not isinstance(filePath, str): raise Exception("filePath must be a string!")
  if not isinstance(delimiter, str): raise Exception("delimiter must be a string!")
  if not isinstance(quotechar, str): raise Exception("quotechar must be a string!")
  if not isinstance(titleRow, bool): raise Exception("titleRow must be a boolean!")

  #length of delimter and quotechar checking
  if not len(delimiter) == 1: raise Exception("delimiter must be a single char!")
  if not len(quotechar) == 1: raise Exception("quotechar must be a single char!")
  
  #read csv file
  with open(filePath, newline='', mode="r") as csvfile:
    #read csv
    p = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar, skipinitialspace=True, dialect="excel")
    rows = list(p)

    longestRow = max(rows, key=len)
    
    #set header titles
    start = 0
    if titleRow:
      table = Table(headers=rows[0])

    else:
      table = Table(headers=[x for x in range(0, len(longestRow))])

    #add rows
    for i in range(start,len(rows)):
      row = rows[i]
      rowToAdd = {}
      for count, elem in enumerate(row):
        elem = elem.strip()
        if elem == "":
          elem = None
        rowToAdd[table._headers[count]] = elem
      table.addRow(rowToAdd)
  return table

def tableToCSV(filePath:str, table:Table, titleRow:bool = True, delimiter:str=",", quotechar:str='"'):
  """
  Convert a table to a CSV file\n
  filePath - path of file to create - str\n
  table - table to convert - Table\n
  titleRow - whether the table contains a titleRow - bool\n
  delimiter - csv seperator character - str\n
  qoutechar - char used for quotes - str\n
  """
  #type checking
  if not isinstance(filePath, str): raise Exception("filePath must be a string!")
  if not isinstance(delimiter, str): raise Exception("delimiter must be a string!")
  if not isinstance(quotechar, str): raise Exception("quotechar must be a string!")
  if not isinstance(titleRow, bool): raise Exception("titleRow must be a boolean!")

  #length of delimter and quotechar checking
  if not len(delimiter) == 1: raise Exception("delimiter must be a single char!")
  if not len(quotechar) == 1: raise Exception("quotechar must be a single char!")
    
  #write csv
  with open(filePath, 'w+', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)

    if titleRow:
      writer.writerow(table._headers)

    #iterate through rows and write
    for row in table._rows:
      elems = [row[header] for header in table._headers]
      writer.writerow(elems)

if __name__ == "__main__":
  import random
  import string

  table = Table(headers=["Name", "Score"])

  for i in range(100):
    table.addRow({"Name": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)), "Score": random.randint(0, 100)})

  tableToCSV("output.csv", table)