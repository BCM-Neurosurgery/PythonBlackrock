# BLACKROCK UTILITIES FOR PYTHON TASKS
# DEVELOPED BY GEORGIOS KOKALAS

from os import path, listdir
from pandas import read_csv
from subprocess import run
from cerebus import cbpy

PORT_NAMES = ['NSP1', 'NSP2']
IP_ADDRESSES = []
for port in PORT_NAMES:
    process = run(f'netsh interface ip show address "{port}" | findstr "IP Address"',\
                  shell = True, capture_output = True, text=True)
    IP_ADDRESSES.append(process.stdout.strip().split()[2])


ONLINE_NSPS = [-1] * len(IP_ADDRESSES)
SUFFIXES = []
for inst, address in enumerate(IP_ADDRESSES):
    try:
        cbpy.open(instance=inst, parameter={'central-addr':address})
        ONLINE_NSPS[inst] = inst
        SUFFIXES.append(f'_NSP-{inst+1}')
    except:
        print(f"Issue opening NSP{inst+1}")
pass

EMU_NUM = -1
EMU_STR = ''
LOG_TABLE = ...
LOG_FILE = ''

def get_next_log_entry():
    global EMU_NUM, LOG_TABLE, LOG_FILE
    tablePath = path.join(path.expanduser('~'), 'Documents', 'MATLAB', 'PatientData', '+CurrentPatientLog')
    tableDir = listdir(tablePath)
    if len(tableDir) < 1:
        raise Exception("No file detected in +CurrentPatientLog")
    elif len(tableDir) > 1:
        raise Exception("More than 1 file detected in +CurrentPatientLog")
    else:
        fileName = tableDir[0]
        fileParts = fileName.split('_')
        subjID = fileParts[0]
        LOG_FILE = path.join(tablePath, fileName)
        LOG_TABLE = read_csv(LOG_FILE)
        EMU_NUM = LOG_TABLE['emu_id'][LOG_TABLE.shape[0]-1] + 1
        return EMU_NUM, subjID, LOG_TABLE
    
    
def make_EmuSaveName(EmuRunNum, SubjName, ExpName):
    global EMU_STR, LOG_TABLE, LOG_FILE
    EMU_STR = f'EMU-{EmuRunNum:04}'

    allString = f'EMU-{EmuRunNum:04}_subj-{SubjName}_{ExpName}'
    LOG_TABLE.loc[len(LOG_TABLE)] = [EMU_NUM, allString]
    LOG_TABLE.to_csv(LOG_FILE, index=False)

    return allString


def task_comment(Event:str, FileName:str):
    global POOL
    if len(Event)+len(SUFFIXES[0])+7 > 92:
        raise Exception("Event/comment provided is too long")
    
    eventCode = ''
    eventColor = (0,255,255,255)#16777215
    closeAfter = False
    match Event:
        #tbgr
        case 'start':
            eventCode = f'$TASKSTART {FileName}'
            eventColor = (0,0,255,0)#65280
        case 'stop':
            eventCode = f'$TASKSTOP {FileName}'
            eventColor =  (0,255,0,255)#16711935
            closeAfter = True
        case 'kill':
            eventCode = f'$TASKKILL {FileName}'
            eventColor = (0,0,0,255)#255
            closeAfter = True
        case 'error':
            eventCode = f'$TASKERR {FileName}'
            eventColor = (0,0,0,255)#255
            closeAfter = True
        case 'annotate':
            eventCode = f'@EVENT {FileName}'
            eventColor = (0,255,0,0)#16711680
        case _:
            eventCode = f'{Event}-{EMU_STR}'


    for nsp in ONLINE_NSPS:
        if nsp == -1:
            continue
        
        comment = f'{eventCode}{SUFFIXES[nsp]}'
        if Event == 'start': print(comment)      

        cbpy.set_comment(comment, rgba_tuple=eventColor, instance=nsp)

    if closeAfter:
        for idx in range(len(ONLINE_NSPS)-1, -1, -1):
            if ONLINE_NSPS[idx] != -1: 
                cbpy.close(ONLINE_NSPS[idx])

                

    