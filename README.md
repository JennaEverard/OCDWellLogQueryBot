# OCD Well Log Query Bot

>Command-line application to query the State of New Mexico Oil Conservation Database (OCD) to retrieve well info and well logs

## Installation Instructions

**Step 1: Install Code**

Clone this repository locally and then install the necessary python packages by running

```pip install -r requirements.txt```

**Step 2: Request OCD Account**

Go to [https://api.emnrd.nm.gov/](https://api.emnrd.nm.gov/) and register for a free account. Once you receive confirmation, add your username and password to ```config.py``` in the following section:

```
#### CREDENTIALS ####
USERNAME = #INPUT OCD USERNAME HERE#
PASSWORD = #INPUT OCD PASSWORD HERE#
```

**Step 3: Set up Inputs/Outputs**

- If you are doing batch runs, place your input files into the ```Inputs``` directory. All input files should be a one column csv with one API per row and no header. An example input file is provided
- All well logs will be saved in the ```Outputs - well log files``` directory, which will not exist until you run the application for the first time. Each set of well logs will be stored within a sub-directory titled with the well API. If a well has no logs, a directory for it will still be created (sorry - this is the behaviour I needed for my analyses...)
- When doing single well look-ups, the well information will be printed to the terminal (*not saved*)
- When doing batch runs, all well information will be compiled into a single summary csv that will be saved to the ```Outputs - csv summaries``` directory. An example of this output file is provided.

**Step 4: Run the Application!**

Navigate to the project directory in your terminal and run the application using

```python app.py```

and follow the on-screen instructions!


