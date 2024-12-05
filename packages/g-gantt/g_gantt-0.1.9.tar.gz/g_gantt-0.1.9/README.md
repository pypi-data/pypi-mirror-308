# g_gantt

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Quick Start](#Quickstart)
- [License](#license)

## Description 
g_gantt is a python package that allows you to write Gantt Charts from Google's Javascript charting library in python!

The chart can either be automatically displayed in your browser or saved as html.

## Installation

```console
pip install g_gantt
```

## Quick Start

Import g_gantt and datetime for date()
```
import g_gantt
from datetime import datetime

chart = Chart("Example Chart Title")

chart.add_task(
    task_id="T1",
    task_label="Task 1", 
    resource="Resource 1",
    start=date(2024,10,1),
    end=None, 
    duration=1,
    dependencies=None,
    percent_complete=100,
    )

chart.add_task(
    task_id="T2",
    task_label="Task 2", 
    resource="Resource 2",
    start=date(2024,10,3),
    end=date(2024,10,5), 
    duration=None,
    dependencies="T1",
    percent_complete=30,
    )

chart.add_task(
    task_id="T3",
    task_label="Task 3", 
    resource="Resource 2",
    start=None,
    end=None, 
    duration=3,
    dependencies="T1,T2",
    percent_complete=0,
    )

chart.enable_critical_path(True)

chart.set_dimensions(1500,1000)

chart.show()

chart.save('gantt_chart.html')
```

## Guide
### Imports
To get started import g_gantt and import datetime for access to date()
```
import g_gantt
from datetime import datetime
```

First initalize a chart object with your gantt chart title

'''
chart = Chart("Example Chart Title")
'''

### Initatilzation
To initalize a chart object the only input you need is your title!
```
chart = Chart("Example Chart Title")
```

### Add Tasks
Tasks are added to a chart object with the add_task() function.
There are many different valid input combinations, below are a few 

```
#With all fields fully defined in long layout (recommended)
chart.add_task(
    task_id="T2",
    task_label="Task 2", 
    resource="Resource 1",
    start=None,
    end=None, 
    duration=1,
    dependencies="T1",
    percent_complete=100,
    )
```

```
#Default order fields in short layout (Not recommended)
chart.add_task("T2","Task 2","Resource 1",date(2024,10,1),None,1,"T1",100)
```

```
#with only duration
chart.add_task(
    task_id="T1",
    task_label="Task 1", 
    resource="Resource 1",
    start=None,
    end=None, 
    duration=1,
    dependencies=None,
    percent_complete=100,
    )
```

```
#with Start and End
chart.add_task(
    task_id="T1",
    task_label="Task 1", 
    resource="Resource 1",
    start=date(2024,10,1),
    end=date(2024,10,5), 
    duration=None,
    dependencies=None,
    percent_complete=100,
    )
```
```
#with Start and Duration
chart.add_task(
    task_id="T1",
    task_label="Task 1", 
    resource="Resource 1",
    start=date(2024,10,1),
    end=None, 
    duration=1,
    dependencies=None,
    percent_complete=100,
    )
```
```
#with End and Duration
chart.add_task(
    task_id="T1",
    task_label="Task 1", 
    resource="Resource 1",
    start=None,
    end=date(2024,10,5), 
    duration=1,
    dependencies=None,
    percent_complete=100,
    )
```

```
#with multiple dependencies
chart.add_task(
    task_id="T1",
    task_label="Task 1", 
    resource="Resource 1",
    start=date(2024,10,1),
    end=date(2024,10,5), 
    duration=None,
    dependencies="T1,T2,T3",
    percent_complete=100,
    )
```

```
#with half a day
chart.add_task(
    task_id="T1",
    task_label="Task 1", 
    resource="Resource 1",
    start=date(2024,10,1),
    end=None, 
    duration=.5,
    dependencies="T1,T2,T3",
    percent_complete=100,
    )
```

### Change Settings
```
chart.set_background_color("B4B4B4")
chart.set_dimensions(1500,1000)
chart.set_bar_corner_radius(2)
chart.set_arrows(
    angle = 45,
    color = "#000",
    length = 8,
    radius = 15,
    spaceAfter = 4,
    width = 1.4,
)
chart.enable_critical_path(False) #True by default
chart.enable_percent(False) #True by default
chart.enable_shadow(False) #True by default
chart.enable_sort_tasks(False) #True by default
```

### View and Save Chart
```
# Open in webbrowser
chart.show
```

```
# Save file
chart.save('Filename.html')
```






## License

`g_gantt` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
