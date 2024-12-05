from main import *
from datetime import datetime

# Initialize the chart with a title
chart = Chart("Example Chart")

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
    resource="Resource 3",
    start=None,
    end=date(2024,10,4), 
    duration=3,
    dependencies="T1,T2",
    percent_complete=0,
    )

chart.add_task("T2","Label for Task 2", duration = 1.5, dependencies="T1",resource = "Epic1")



# Customize the background color!
chart.set_background_color("B4B4B4")

# Enable Critical Path Highlighting
chart.enable_critical_path(True)

# Set the chart dimensions!
chart.set_dimensions(1500,1000)

# Show the chart in your browser!
chart.show()

# Save the html code for the chart!
chart.save('gantt_chart_critical_path.html')
