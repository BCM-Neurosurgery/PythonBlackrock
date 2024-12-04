# PythonBlackrock
Contains script(s) meant to help behavioral tasks coded in Python send event comments to the Blackrock Neural Signal Processors, without the need for the MATLAB engine.
Meant to be used at the EMU used by BCM.


## Installations
The script(s) used in this repository require additional libraries on top of the standard ones that come with Python. This script needs **pandas**, and **cerebus**.

Pandas can be installed like any other Python module.

To install cerebus, download the wheel from the [Cerelink Repository](https://github.com/CerebusOSS/CereLink/releases).

### Installation Instructions
Assuming a Python virtual environment using a terminal in VSCode, the installation would look like this:

`python -m venv cerebusVenv`

`cerebusVenv\Scripts\Activate.ps1`

`pip install pandas`

`pip install cerebus-0.4-cp312-cp312-win_amd64.whl`

## Usage
As of version 1.0, to use the script, use `import Path_To_Script_Folder/BlackRockUtils as bru`. 

After that, run `emuNum, subjID, logTable=bru.get_next_log_entry()`

and `emuSaveName = bru.make_EmuSaveName(emuNum, subjID, ExpName)`, where `ExpName` is a string representing the name of your task.

After that, to send a comment simply use `task_comment(CommentString, emuSaveName)`.
