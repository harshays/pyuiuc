PyUIUC
<hr>
Python wrapper for UIUC CISAPI; Intended for use with Python 2.X

#### Overview
The ```pyuiuc/``` package contains modules to interact with UIUC's course schedule and catalog, using Python. The wrapper generalizes all calls using ```Schedule``` and ```Catalog``` classes. These classes can be used to retrieve the catalog or schedule of any year, semester, subject, course and/or section. For example, this code demonstrates the basic usage of ```Schedule```:

```python
cs_schedule = Schedule(year=2015, semester='fall', subject='CS')
courses     = cs_schedule.find('course') # list of all CS courses 
```
#### Setup
To use ```pyuiuc``` in your projects, do the standard:
```python
$ git clone https://github.com/harshays/pyuiuc.git
$ cd pyuiuc
$ python setup.py install # preferably in a virtual env
```
#### Examples
Have a look at the ```examples/``` directory. Most of it should be self-explanatory. If not, browse the docstrings in the ```tag.py``` module. To preview all docstrings, use Python's built-in ```help```:
```python
from pyuiuc.schedule import Schedule
help(Schedule)
```
#### Tests
```tests/``` have 100% coverageUIUC CISAPI Python API Wrapper
