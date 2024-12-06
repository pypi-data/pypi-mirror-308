# vsort


[![PyPI version](https://badge.fury.io/py/vsort.svg)](https://badge.fury.io/py/vsort)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This library was created to simplify sorting algorithms by visually displaying them in the form of a horizontal table, using colors to illustrate the sorting steps, giving the ability to control the sorting speed and manually switching between items, all this is especially for beginners in sorting algorithms.


## Installation


You can install `vsort` via pip:


```bash
pip install vsort
```


## Usage 


### For selection sort algorithm


```python
from vsort import sortVisualizer


x = sortVisualizer([70, 10, 7, 100, 96, 85, 83, 8, 87, 29])
x.selection_sort()
```


#### Output


https://drive.google.com/file/d/1-uqA1tvz0QjtyAjhPJY_HarxoBKQZ9-o/view?usp=drive_link


### For bubble sort algorithm


```python
from vsort import sortVisualizer


x = sortVisualizer([70, 10, 7, 100, 96, 85, 83, 8, 87, 29])
x.bubble_sort()
```


#### Output


https://drive.google.com/file/d/1KhYNYXrsGpH4noM20tJAKtgqJpoJ3HBV/view?usp=sharing


### For insertion sort algorithm


```python
from vsort import sortVisualizer


x = sortVisualizer([70, 10, 7, 100, 96, 85, 83, 8, 87, 29])
x.insertion_sort()
```


#### Output


https://drive.google.com/file/d/1KHgl5-F4yepKj8H-VB2X-I1D3dReum1A/view?usp=drive_link


### For shell sort algorithm


```python
from vsort import sortVisualizer


x = sortVisualizer([70, 10, 7, 100, 96, 85, 83, 8, 87, 29])
x.shell_sort()
```


#### Output


https://drive.google.com/file/d/1uTvzLAZi453u3Q8ywXl6vx7Zcjwxz7Cr/view?usp=drive_link


### For heap sort algorithm


```python
from vsort import sortVisualizer


x = sortVisualizer([70, 10, 7, 100, 96, 85, 83, 8, 87, 29])
x.heap_sort()
```


#### Output


https://drive.google.com/file/d/1Gwv_zdUUHWG894W3NV_LSaN3xod638BY/view?usp=drive_link


#### You can sort in descending order 


```python
from vsort import sortVisualizer


x = sortVisualizer([70, 10, 7, 100, 96, 85, 83, 8, 87, 29], reverse=True)
```


#### You can reduce the sorting speed


```python
from vsort import sortVisualizer


x = sortVisualizer([70, 10, 7, 100, 96, 85, 83, 8, 87, 29], speed=7)
```


#### You can control the sorting steps by pressing Enter


```python
from vsort import sortVisualizer


x = sortVisualizer([70, 10, 7, 100, 96, 85, 83, 8, 87, 29], control=True)
```


## License


This project is licensed under the MIT LICENSE - see the [LICENSE](https://opensource.org/licenses/MIT) for more details.