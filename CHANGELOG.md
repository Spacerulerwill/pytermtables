# Changelog

## V1.0.3 (3/06/2022)

* Renamed printGrid method to gridToString - now returns the constructed string instead of printing it
* Replaced ```table.prettyPrint()``` with:
    ```python
    print(table) # <- same functionality as .prettyPrint()
    ```
* Added
    ```python
    len(table) # <- returns amount of items in table that are not None
    ```
* Renamed ```rows``` and ```headers``` to ```_rows``` and ```_headers``` (private variables)
* ```getHeader()``` will now return None if the header doesn't exist
* Added
  ```python
    table[header] # <- same functionality as getHeader() except will raise an exception if it doesn't exist
  ```
* Added
  ```python
    table[header] = [] # <- changes header data to data in list
  ```
* Added
  ```python
    del[header] # <- same functionality as removeHeader()
  ```
* Added function hints for all functions
* Added
  ```python
    table.percentile("Score", 50) # get's nth percentile
  ```
* Added
  ```python
    table.getIQR("Score") # get interquartile range of data
  ```


## V1.0.2 (22/05/2022)

Improvement - Lines when reading from CSV file are stripped

## V1.0.1 (22/05/2022)

Bug Fix - statistical functions not convert data in tables to floats when calculating

## V1.0.0 (22/05/2022)

Initial Release - released on https://pypi.org/project/pytermtables/